#!/usr/bin/env python3
"""Governed GitHub provider adapter for the DevOS controller.

The adapter is the provider-side execution boundary after P17/controller approval.
It obtains a short-lived GitHub App installation token, evaluates the existing
remote-permission gate before any mutation, performs one bounded provider action,
then performs a fresh readback. It never prints or persists credentials.

Required environment variables:
  DEVOS_GITHUB_APP_ID
  DEVOS_GITHUB_APP_PRIVATE_KEY

The operation JSON is intentionally explicit. Mutation capabilities must match the
existing DevOS remote permission model. Read operations are provider reads only and
never create authorization.
"""
from __future__ import annotations

import argparse
import base64
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
PERMISSION_MODULE_PATH = ROOT / "tools" / "devos-remote-permission-check.py"
API_ROOT = "https://api.github.com"
API_VERSION = "2026-03-10"
USER_AGENT = "DevOS-GitHub-Provider-Adapter/1"
JWT_LIFETIME_SECONDS = 540
READ_ACTIONS = {"repository.get", "file.get", "branch.get", "pr.get"}
SUPPORTED_MUTATIONS = {"file.create", "file.update", "file.delete", "branch.create", "branch.update", "branch.force_update", "branch.delete", "pr.merge"}

@dataclass(frozen=True)
class AuthorizationRecord:
    provider: str
    owner: str
    repository: str | None
    resource: str | None
    capability: str
    workflow: str
    project: str
    impact_ceiling: str
    freshness: str | None
    authorization_id: str

@dataclass(frozen=True)
class OperationRecord:
    provider: str
    owner: str
    repository: str | None
    resource: str | None
    capability: str
    workflow: str
    project: str
    impact: str
    freshness: str | None
    action: str
    inputs: dict[str, Any]


def _load_module(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load {path.name}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _make_jwt(app_id: str, private_key: str, now: int | None = None) -> str:
    try:
        app_number = int(app_id)
    except ValueError as exc:
        raise ValueError("DEVOS_GITHUB_APP_ID must be an integer") from exc
    issued_at = int(time.time()) if now is None else int(now)
    header = _b64url(json.dumps({"alg": "RS256", "typ": "JWT"}, separators=(",", ":")).encode())
    payload = _b64url(json.dumps({"iat": issued_at - 60, "exp": issued_at + JWT_LIFETIME_SECONDS, "iss": app_number}, separators=(",", ":")).encode())
    unsigned = f"{header}.{payload}".encode("ascii")
    key_path: Path | None = None
    result = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", prefix="devos-gh-key-", suffix=".pem", delete=False) as handle:
            handle.write(private_key)
            handle.flush()
            key_path = Path(handle.name)
        os.chmod(key_path, 0o600)
        result = subprocess.run(["openssl", "dgst", "-sha256", "-sign", str(key_path)], input=unsigned, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    except FileNotFoundError as exc:
        raise RuntimeError("openssl is required on the GitHub-hosted runner") from exc
    finally:
        if key_path is not None:
            try:
                key_path.unlink()
            except FileNotFoundError:
                pass
    if result is None or result.returncode != 0:
        raise RuntimeError("GitHub App private-key signing failed")
    return f"{unsigned.decode('ascii')}.{_b64url(result.stdout)}"


def _parse_repository(value: str) -> tuple[str, str]:
    parts = value.strip().split("/")
    if len(parts) != 2 or not all(parts) or any(part in {".", ".."} for part in parts):
        raise ValueError("repository must be in owner/name form")
    return parts[0], parts[1]


def _json_bytes(payload: dict[str, Any]) -> bytes:
    return json.dumps(payload, separators=(",", ":")).encode("utf-8")


def _request(url: str, *, token: str, method: str = "GET", body: dict[str, Any] | None = None) -> tuple[int, dict[str, Any]]:
    headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": API_VERSION, "User-Agent": USER_AGENT, "Authorization": f"Bearer {token}"}
    raw_body = _json_bytes(body) if body is not None else None
    if raw_body is not None:
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=raw_body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            raw = response.read().decode("utf-8")
            data = json.loads(raw) if raw else {}
            return response.status, data if isinstance(data, dict) else {"value": data}
    except urllib.error.HTTPError as exc:
        try:
            data = json.loads(exc.read().decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            data = {"message": "GitHub API request failed"}
        message = data.get("message", "GitHub API request failed") if isinstance(data, dict) else "GitHub API request failed"
        raise RuntimeError(f"GitHub API request failed: HTTP {exc.code}: {message}") from exc
    except urllib.error.URLError as exc:
        raise ConnectionError("GitHub API network request failed after request dispatch may have occurred") from exc


def _installation_token(repository: str) -> str:
    app_id = os.environ.get("DEVOS_GITHUB_APP_ID", "").strip()
    private_key = os.environ.get("DEVOS_GITHUB_APP_PRIVATE_KEY", "")
    if not app_id or not private_key:
        raise RuntimeError("DEVOS_GITHUB_APP_ID and DEVOS_GITHUB_APP_PRIVATE_KEY are required")
    owner, repo = _parse_repository(repository)
    jwt = _make_jwt(app_id, private_key)
    _, installation = _request(f"{API_ROOT}/repos/{urllib.parse.quote(owner)}/{urllib.parse.quote(repo)}/installation", token=jwt)
    installation_id = installation.get("id")
    if not isinstance(installation_id, int):
        raise RuntimeError("GitHub App installation was not resolved for target repository")
    _, target = _request(f"{API_ROOT}/repos/{urllib.parse.quote(owner)}/{urllib.parse.quote(repo)}", token=jwt)
    target_id = target.get("id")
    if not isinstance(target_id, int):
        raise RuntimeError("target repository metadata did not include an integer id")
    _, token_response = _request(f"{API_ROOT}/app/installations/{installation_id}/access_tokens", token=jwt, method="POST", body={"repository_ids": [target_id]})
    token = token_response.get("token")
    if not isinstance(token, str) or not token:
        raise RuntimeError("GitHub did not return an installation token")
    return token


def _gate(operation: OperationRecord, authorization: AuthorizationRecord | None) -> dict[str, Any]:
    mod = _load_module(PERMISSION_MODULE_PATH, "devos_remote_permission_check")
    op = mod.Operation(provider=operation.provider, owner=operation.owner, repository=operation.repository, resource=operation.resource, capability=operation.capability, workflow=operation.workflow, project=operation.project, impact=operation.impact, freshness=operation.freshness)
    auth = mod.Authorization(**authorization.__dict__) if authorization is not None else None
    status, reasons = mod.evaluate(auth, op)
    return {"status": status, "reasons": reasons, "capability": operation.capability}


def _read(token: str, operation: OperationRecord) -> dict[str, Any]:
    owner = urllib.parse.quote(operation.owner)
    repo = urllib.parse.quote(operation.repository or "")
    resource = operation.resource or ""
    if operation.action == "repository.get":
        return _request(f"{API_ROOT}/repos/{owner}/{repo}", token=token)[1]
    if operation.action == "file.get":
        path = urllib.parse.quote(resource.lstrip("/"), safe="/")
        return _request(f"{API_ROOT}/repos/{owner}/{repo}/contents/{path}", token=token)[1]
    if operation.action == "branch.get":
        branch = urllib.parse.quote(resource, safe="")
        return _request(f"{API_ROOT}/repos/{owner}/{repo}/git/ref/heads/{branch}", token=token)[1]
    if operation.action == "pr.get":
        return _request(f"{API_ROOT}/repos/{owner}/{repo}/pulls/{int(resource)}", token=token)[1]
    raise ValueError(f"unsupported read action: {operation.action}")


def _mutate(token: str, operation: OperationRecord) -> tuple[dict[str, Any], dict[str, Any]]:
    owner = urllib.parse.quote(operation.owner)
    repo = urllib.parse.quote(operation.repository or "")
    inp = operation.inputs
    action = operation.action
    if action in {"file.create", "file.update", "file.delete"}:
        path = urllib.parse.quote((operation.resource or "").lstrip("/"), safe="/")
        message = inp.get("message")
        if not isinstance(message, str) or not message.strip():
            raise ValueError("file mutation requires inputs.message")
        if action == "file.delete":
            expected_sha = inp.get("expected_sha")
            if not isinstance(expected_sha, str) or not expected_sha:
                raise ValueError("file.delete requires inputs.expected_sha for exactly-once protection")
            status, data = _request(f"{API_ROOT}/repos/{owner}/{repo}/contents/{path}", token=token, method="DELETE", body={"message": message, "sha": expected_sha, **({"branch": inp["branch"]} if isinstance(inp.get("branch"), str) else {})})
        else:
            content = inp.get("content")
            if not isinstance(content, str):
                raise ValueError(f"{action} requires inputs.content")
            body: dict[str, Any] = {"message": message, "content": base64.b64encode(content.encode("utf-8")).decode("ascii")}
            if isinstance(inp.get("branch"), str):
                body["branch"] = inp["branch"]
            if action == "file.update":
                expected_sha = inp.get("expected_sha")
                if not isinstance(expected_sha, str) or not expected_sha:
                    raise ValueError("file.update requires inputs.expected_sha for exactly-once protection")
                body["sha"] = expected_sha
            status, data = _request(f"{API_ROOT}/repos/{owner}/{repo}/contents/{path}", token=token, method="PUT", body=body)
        return data, {"http_status": status}
    if action in {"branch.create", "branch.update", "branch.force_update", "branch.delete"}:
        branch = operation.resource or ""
        if not branch or branch in {"HEAD", "main~1"}:
            raise ValueError("invalid branch resource")
        if action == "branch.create":
            source_sha = inp.get("sha")
            if not isinstance(source_sha, str) or not source_sha:
                raise ValueError("branch.create requires inputs.sha")
            status, data = _request(f"{API_ROOT}/repos/{owner}/{repo}/git/refs", token=token, method="POST", body={"ref": f"refs/heads/{branch}", "sha": source_sha})
        elif action == "branch.delete":
            status, data = _request(f"{API_ROOT}/repos/{owner}/{repo}/git/refs/heads/{urllib.parse.quote(branch, safe='')}", token=token, method="DELETE")
        else:
            target_sha = inp.get("sha")
            if not isinstance(target_sha, str) or not target_sha:
                raise ValueError(f"{action} requires inputs.sha")
            status, data = _request(f"{API_ROOT}/repos/{owner}/{repo}/git/refs/heads/{urllib.parse.quote(branch, safe='')}", token=token, method="PATCH", body={"sha": target_sha, "force": action == "branch.force_update"})
        return data, {"http_status": status}
    if action == "pr.merge":
        number = int(operation.resource or "0")
        method = inp.get("merge_method", "merge")
        if method not in {"merge", "squash", "rebase"}:
            raise ValueError("pr.merge inputs.merge_method must be merge, squash, or rebase")
        body: dict[str, Any] = {"merge_method": method}
        expected_sha = inp.get("expected_sha")
        if isinstance(expected_sha, str) and expected_sha:
            body["sha"] = expected_sha
        status, data = _request(f"{API_ROOT}/repos/{owner}/{repo}/pulls/{number}/merge", token=token, method="PUT", body=body)
        return data, {"http_status": status}
    raise ValueError(f"unsupported mutation action: {action}")


def _readback(token: str, operation: OperationRecord, result: dict[str, Any]) -> dict[str, Any]:
    action = operation.action
    if action.startswith("file."):
        if action == "file.delete":
            try:
                current = _read(token, OperationRecord(**{**operation.__dict__, "action": "file.get"}))
            except RuntimeError as exc:
                if "HTTP 404" in str(exc):
                    return {"status": "ABSENT", "resource": operation.resource}
                raise
            return {"status": "STILL_PRESENT", "resource": operation.resource, "current_sha": current.get("sha")}
        current = _read(token, OperationRecord(**{**operation.__dict__, "action": "file.get"}))
        return {"status": "PRESENT", "resource": operation.resource, "sha": current.get("sha")}
    if action in {"branch.create", "branch.update", "branch.force_update", "branch.delete"}:
        try:
            current = _read(token, OperationRecord(**{**operation.__dict__, "action": "branch.get"}))
        except RuntimeError as exc:
            if action == "branch.delete" and "HTTP 404" in str(exc):
                return {"status": "ABSENT", "resource": operation.resource}
            raise
        return {"status": "PRESENT", "resource": operation.resource, "sha": current.get("object", {}).get("sha")}
    if action == "pr.merge":
        current = _read(token, OperationRecord(**{**operation.__dict__, "action": "pr.get"}))
        return {"status": current.get("state"), "merged": current.get("merged"), "merged_at": current.get("merged_at"), "sha": current.get("merge_commit_sha")}
    return {"status": "NOT_APPLICABLE"}


def execute(operation_data: dict[str, Any], authorization_data: dict[str, Any] | None = None, token_provider: Callable[[str], str] = _installation_token, client_read: Callable[[str, OperationRecord], dict[str, Any]] | None = None) -> dict[str, Any]:
    operation = OperationRecord(provider=operation_data.get("provider", ""), owner=operation_data.get("owner", ""), repository=operation_data.get("repository"), resource=operation_data.get("resource"), capability=operation_data.get("capability", ""), workflow=operation_data.get("workflow", ""), project=operation_data.get("project", ""), impact=operation_data.get("impact", ""), freshness=operation_data.get("freshness"), action=operation_data.get("action", ""), inputs=operation_data.get("inputs", {}))
    if not isinstance(operation.inputs, dict):
        return {"status": "BLOCKED", "reason_codes": ["INVALID_INPUTS"], "authority": "UNCHANGED", "execution": "NONE", "mutation": "NONE"}
    if operation.provider != "github":
        return {"status": "BLOCKED", "reason_codes": ["UNSUPPORTED_PROVIDER"], "authority": "UNCHANGED", "execution": "NONE", "mutation": "NONE"}
    repository_identity = f"{operation.owner}/{operation.repository}" if operation.repository else None
    if operation.action in READ_ACTIONS:
        if not repository_identity:
            return {"status": "BLOCKED", "reason_codes": ["MISSING_REPOSITORY"], "authority": "UNCHANGED", "execution": "NONE", "mutation": "NONE"}
        try:
            token = token_provider(repository_identity)
            reader = client_read or _read
            data = reader(token, operation)
            return {"status": "COMPLETE", "action": operation.action, "target": operation.repository, "result": data, "credential_material": "NOT_INCLUDED", "authority": "UNCHANGED", "execution": "PROVIDER_READ", "mutation": "NONE", "evidence": "FRESH_PROVIDER_READ"}
        except Exception as exc:
            return {"status": "FAILED", "reason_codes": ["PROVIDER_READ_FAILED"], "reason": repr(exc), "authority": "UNCHANGED", "execution": "NONE", "mutation": "NONE"}
    if operation.action not in SUPPORTED_MUTATIONS:
        return {"status": "BLOCKED", "reason_codes": ["UNSUPPORTED_MUTATION_ACTION"], "authority": "UNCHANGED", "execution": "NONE", "mutation": "NONE"}
    authorization = AuthorizationRecord(**authorization_data) if authorization_data else None
    gate = _gate(operation, authorization)
    if gate["status"] != "CONTINUE_WITH_EXISTING_APPROVAL":
        return {"status": gate["status"], "reason_codes": gate["reasons"], "authority": "UNCHANGED", "execution": "NONE", "mutation": "NONE", "decision": "ACTIONABLE_HOLD"}
    if operation.capability != operation.action:
        return {"status": "BLOCKED", "reason_codes": ["CAPABILITY_ACTION_MISMATCH"], "authority": "UNCHANGED", "execution": "NONE", "mutation": "NONE"}
    if not repository_identity:
        return {"status": "BLOCKED", "reason_codes": ["MISSING_REPOSITORY"], "authority": "UNCHANGED", "execution": "NONE", "mutation": "NONE"}
    try:
        token = token_provider(repository_identity)
        result, transport = _mutate(token, operation)
    except ConnectionError as exc:
        return {"status": "HOLD", "reason_codes": ["UNCERTAIN_PROVIDER_RESULT"], "reason": str(exc), "next_action": "READBACK_BEFORE_RETRY", "authority": "UNCHANGED", "execution": "UNKNOWN", "mutation": "UNKNOWN"}
    except Exception as exc:
        return {"status": "FAILED", "reason_codes": ["PROVIDER_MUTATION_FAILED"], "reason": repr(exc), "authority": "UNCHANGED", "execution": "ATTEMPTED", "mutation": "UNKNOWN"}
    try:
        readback = _readback(token, operation, result)
    except Exception as exc:
        return {"status": "HOLD", "reason_codes": ["READBACK_REQUIRED"], "reason": repr(exc), "provider_response": result, "authority": "UNCHANGED", "execution": "UNKNOWN", "mutation": "UNKNOWN"}
    return {"status": "COMPLETE", "action": operation.action, "target": {"repository": operation.repository, "resource": operation.resource}, "provider_response": result, "transport": transport, "readback": readback, "credential_material": "NOT_INCLUDED", "authority": "UNCHANGED", "execution": "PROVIDER_MUTATION", "mutation": "COMPLETE", "evidence": "FRESH_PROVIDER_READBACK"}


def main() -> int:
    parser = argparse.ArgumentParser(description="Governed DevOS GitHub provider adapter")
    parser.add_argument("--operation-json", required=True)
    parser.add_argument("--authorization-json")
    args = parser.parse_args()
    try:
        operation = json.loads(args.operation_json)
        authorization = json.loads(args.authorization_json) if args.authorization_json else None
        result = execute(operation, authorization)
    except (json.JSONDecodeError, TypeError, ValueError, RuntimeError) as exc:
        result = {"status": "BLOCKED", "reason_codes": ["MALFORMED_ADAPTER_INPUT"], "reason": str(exc), "authority": "UNCHANGED", "execution": "NONE", "mutation": "NONE"}
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "COMPLETE" else 2

if __name__ == "__main__":
    raise SystemExit(main())
