#!/usr/bin/env python3
"""Controlled remote mutation proof over the existing runtime adapter bridge.

This module does not create a new mutation capability. It governs one
`github.mutate.file` attempt with fresh pre-read/readback evidence and never
retries a mutation automatically.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = "DEVOS-CONTROLLED-MUTATION-v1"


def _load(name: str, relative: str):
    path = ROOT / relative
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {relative}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


bridge = _load("controlled_mutation_bridge", "tools/runtime-adapter-bridge.py")


def _base(status: str, reason: str | None = None) -> dict[str, Any]:
    result = {
        "protocol": PROTOCOL,
        "status": status,
        "authority": "UNCHANGED",
        "authorization": "UNCHANGED",
    }
    if reason:
        result["reason"] = reason
    return result


def _provider_file(response: Any) -> tuple[str | None, str | None, str | None]:
    """Normalize path, sha, content from a provider file response."""
    if not isinstance(response, dict):
        return None, None, None
    path = response.get("path") if isinstance(response.get("path"), str) else None
    sha = response.get("sha") if isinstance(response.get("sha"), str) else None
    content = response.get("content") if isinstance(response.get("content"), str) else None
    return path, sha, content


def execute(payload: dict[str, Any], github_client: Any) -> dict[str, Any]:
    repository = payload.get("repository")
    path = payload.get("path")
    step_id = payload.get("step_id")
    expected_sha = payload.get("expected_sha")
    desired_content = payload.get("content")
    message = payload.get("message")
    authorization = payload.get("authorization")
    security_gate = payload.get("security_gate")

    if not isinstance(repository, str) or repository.count("/") != 1:
        return _base("BLOCKED", "repository must be owner/name")
    if not isinstance(path, str) or not path or path.startswith("/") or ".." in path.split("/"):
        return _base("BLOCKED", "path must remain within repository")
    if not isinstance(step_id, str) or not step_id:
        return _base("BLOCKED", "exact step_id is required")
    if authorization != "ALREADY_GRANTED":
        return _base("BLOCKED", "exact-step authorization is required")
    if security_gate != "PASS":
        return _base("BLOCKED", "Security Gate PASS is required")
    if not isinstance(expected_sha, str) or not expected_sha:
        return _base("BLOCKED", "expected current file SHA is required")
    if not isinstance(desired_content, str):
        return _base("BLOCKED", "desired content is required")
    if not isinstance(message, str) or not message:
        return _base("BLOCKED", "commit message is required")
    if github_client is None:
        return _base("BLOCKED", "GitHub provider client is required")

    trace: dict[str, Any] = {}

    pre_read = bridge.execute(
        {
            "operation": "github.inspect.file",
            "target": repository,
            "scope": path,
            "authorization": "NOT_REQUIRED",
        },
        ROOT,
        github_client=github_client,
    )
    trace["pre_read"] = pre_read
    if pre_read.get("status") != "SUCCESS":
        return _base("BLOCKED", "fresh provider pre-read failed") | {"step_id": step_id, "trace": trace, "mutation_attempted": False}

    _, observed_sha, _ = _provider_file((pre_read.get("provider_result") or {}).get("response"))
    if not observed_sha:
        return _base("BLOCKED", "fresh provider pre-read did not expose file SHA") | {"step_id": step_id, "trace": trace, "mutation_attempted": False}
    if observed_sha != expected_sha:
        return _base("BLOCKED", "expected SHA does not match fresh provider state") | {
            "step_id": step_id,
            "trace": trace,
            "mutation_attempted": False,
            "expected_sha": expected_sha,
            "observed_sha": observed_sha,
        }

    mutation = bridge.execute(
        {
            "operation": "github.mutate.file",
            "target": repository,
            "scope": path,
            "content": desired_content,
            "message": message,
            "expected_sha": observed_sha,
            "authorization": "ALREADY_GRANTED",
            "security_gate": "PASS",
            "step_id": step_id,
        },
        ROOT,
        github_client=github_client,
    )
    trace["mutation"] = mutation

    # From this point onward the mutation adapter has been invoked exactly once.
    # Any non-verified outcome requires inspection/HOLD, never automatic replay.
    mutation_attempted = True
    if mutation.get("status") not in {"SUCCESS", "UNVERIFIED"}:
        return _base("HOLD", "mutation attempt did not produce verified completion; replay forbidden") | {
            "step_id": step_id,
            "trace": trace,
            "mutation_attempted": mutation_attempted,
            "replay": "FORBIDDEN",
        }

    readback = bridge.execute(
        {
            "operation": "github.inspect.file",
            "target": repository,
            "scope": path,
            "authorization": "NOT_REQUIRED",
        },
        ROOT,
        github_client=github_client,
    )
    trace["readback"] = readback
    if readback.get("status") != "SUCCESS":
        return _base("HOLD", "post-mutation readback failed; replay forbidden") | {
            "step_id": step_id,
            "trace": trace,
            "mutation_attempted": mutation_attempted,
            "replay": "FORBIDDEN",
        }

    observed_path, new_sha, observed_content = _provider_file((readback.get("provider_result") or {}).get("response"))
    if observed_path is not None and observed_path != path:
        return _base("HOLD", "post-mutation provider path mismatch; replay forbidden") | {
            "step_id": step_id,
            "trace": trace,
            "mutation_attempted": mutation_attempted,
            "replay": "FORBIDDEN",
        }
    if observed_content != desired_content:
        return _base("HOLD", "post-mutation content mismatch; replay forbidden") | {
            "step_id": step_id,
            "trace": trace,
            "mutation_attempted": mutation_attempted,
            "replay": "FORBIDDEN",
        }
    if not isinstance(new_sha, str) or not new_sha:
        return _base("HOLD", "post-mutation file SHA missing; replay forbidden") | {
            "step_id": step_id,
            "trace": trace,
            "mutation_attempted": mutation_attempted,
            "replay": "FORBIDDEN",
        }
    if new_sha == expected_sha:
        return _base("HOLD", "post-mutation file SHA did not change; replay forbidden") | {
            "step_id": step_id,
            "trace": trace,
            "mutation_attempted": mutation_attempted,
            "replay": "FORBIDDEN",
        }

    return _base("VERIFIED") | {
        "step_id": step_id,
        "repository": repository,
        "path": path,
        "precondition_sha": expected_sha,
        "observed_sha": new_sha,
        "trace": trace,
        "mutation_attempted": mutation_attempted,
        "mutation_attempt_count": 1,
        "replay": "NOT_NEEDED",
    }
