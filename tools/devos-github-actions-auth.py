#!/usr/bin/env python3
"""Read-only GitHub App installation authentication for GitHub-hosted DevOS.

This runner is designed for GitHub Actions. It deliberately avoids the web OAuth
callback flow because the DevOS runtime can live entirely inside GitHub Actions.

Required environment variables:
  DEVOS_GITHUB_APP_ID
  DEVOS_GITHUB_APP_PRIVATE_KEY

The private key is used only in memory plus a short-lived 0600 signing file for
OpenSSL. It is never printed, committed, uploaded as an artifact, or persisted as
DevOS evidence. The script only performs authentication/token-minting and read-only
verification of the target repository.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import subprocess
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API_ROOT = "https://api.github.com"
USER_AGENT = "DevOS-GitHub-App-Runtime/1"
JWT_LIFETIME_SECONDS = 540


def b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def parse_repository(value: str) -> tuple[str, str]:
    normalized = value.strip()
    segments = normalized.split("/")
    if len(segments) != 2 or not all(segments):
        raise ValueError("repository must be in owner/name form")
    if any(segment in {".", ".."} for segment in segments):
        raise ValueError("invalid repository path")
    owner, repo = segments
    return owner, repo


def make_jwt(app_id: str, private_key: str, now: int | None = None) -> str:
    try:
        app_number = int(app_id)
    except ValueError as exc:
        raise ValueError("DEVOS_GITHUB_APP_ID must be an integer") from exc

    issued_at = int(time.time()) if now is None else int(now)
    header = b64url(json.dumps({"alg": "RS256", "typ": "JWT"}, separators=(",", ":")).encode())
    payload = b64url(
        json.dumps(
            {"iat": issued_at - 60, "exp": issued_at + JWT_LIFETIME_SECONDS, "iss": app_number},
            separators=(",", ":"),
        ).encode()
    )
    unsigned = f"{header}.{payload}".encode("ascii")

    key_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", prefix="devos-gh-key-", suffix=".pem", delete=False) as handle:
            handle.write(private_key)
            handle.flush()
            key_path = Path(handle.name)
        os.chmod(key_path, 0o600)
        result = subprocess.run(
            ["openssl", "dgst", "-sha256", "-sign", str(key_path)],
            input=unsigned,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except FileNotFoundError as exc:
        raise RuntimeError("openssl is required on the GitHub-hosted runner") from exc
    finally:
        if key_path is not None:
            try:
                key_path.unlink()
            except FileNotFoundError:
                pass

    if result.returncode != 0:
        raise RuntimeError("GitHub App private-key signing failed")

    return f"{unsigned.decode('ascii')}.{b64url(result.stdout)}"


def request_json(url: str, *, method: str, bearer: str, body: bytes | None = None) -> dict:
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": USER_AGENT,
        "Authorization": f"Bearer {bearer}",
    }
    if body is not None:
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        try:
            provider = json.loads(exc.read().decode("utf-8"))
            message = provider.get("message", "GitHub API request failed")
        except (UnicodeDecodeError, json.JSONDecodeError):
            message = "GitHub API request failed"
        raise RuntimeError(f"GitHub API request failed: HTTP {exc.code}: {message}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError("GitHub API network request failed") from exc
    if not isinstance(data, dict):
        raise RuntimeError("GitHub API returned an unexpected response shape")
    return data


def mint_installation_token(app_jwt: str, installation_id: int) -> dict:
    url = f"{API_ROOT}/app/installations/{installation_id}/access_tokens"
    return request_json(url, method="POST", bearer=app_jwt, body=b"{}")


def verify(repository: str) -> dict:
    app_id = os.environ.get("DEVOS_GITHUB_APP_ID", "").strip()
    private_key = os.environ.get("DEVOS_GITHUB_APP_PRIVATE_KEY", "")
    if not app_id or not private_key:
        raise RuntimeError("DEVOS_GITHUB_APP_ID and DEVOS_GITHUB_APP_PRIVATE_KEY are required")

    owner, repo = parse_repository(repository)
    app_jwt = make_jwt(app_id, private_key)

    installation = request_json(
        f"{API_ROOT}/repos/{urllib.parse.quote(owner)}/{urllib.parse.quote(repo)}/installation",
        method="GET",
        bearer=app_jwt,
    )
    installation_id = installation.get("id")
    if not isinstance(installation_id, int):
        raise RuntimeError("GitHub App installation was not resolved for the target repository")

    token_response = mint_installation_token(app_jwt, installation_id)
    installation_token = token_response.get("token")
    if not isinstance(installation_token, str) or not installation_token:
        raise RuntimeError("GitHub did not return an installation token")

    target = request_json(
        f"{API_ROOT}/repos/{urllib.parse.quote(owner)}/{urllib.parse.quote(repo)}",
        method="GET",
        bearer=installation_token,
    )

    permissions = token_response.get("permissions", {})
    if not isinstance(permissions, dict):
        permissions = {}

    return {
        "status": "PASS",
        "authentication": "github_app_installation_token",
        "repository": target.get("full_name", repository),
        "installation_id": installation_id,
        "installation_account": installation.get("account", {}).get("login"),
        "repository_id": target.get("id"),
        "private_repository": target.get("private"),
        "default_branch": target.get("default_branch"),
        "granted_permissions": permissions,
        "credential_material": "NOT_INCLUDED",
        "execution": "NONE",
        "mutation": "NONE",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only DevOS GitHub App authentication smoke check")
    parser.add_argument("--repository", required=True, help="Target repository in owner/name form")
    args = parser.parse_args()

    result = verify(args.repository)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
