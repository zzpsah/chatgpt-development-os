#!/usr/bin/env python3
"""Run a read-only GitHub provider operation using the live-proven App auth path."""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
AUTH = ROOT / "tools" / "devos-github-actions-auth.py"
ADAPTER = ROOT / "tools" / "devos-github-provider-adapter.py"


def _load(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load {path.name}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def proven_token_provider(repository: str) -> str:
    auth = _load(AUTH, "devos_github_actions_auth_live")
    app_id = auth.os.environ.get("DEVOS_GITHUB_APP_ID", "").strip()
    private_key = auth.os.environ.get("DEVOS_GITHUB_APP_PRIVATE_KEY", "")
    if not app_id or not private_key:
        raise RuntimeError("DEVOS_GITHUB_APP_ID and DEVOS_GITHUB_APP_PRIVATE_KEY are required")
    owner, repo = auth.parse_repository(repository)
    app_jwt = auth.make_jwt(app_id, private_key)
    installation = auth.request_json(
        f"{auth.API_ROOT}/repos/{owner}/{repo}/installation",
        method="GET",
        bearer=app_jwt,
    )
    installation_id = installation.get("id")
    if not isinstance(installation_id, int):
        raise RuntimeError("GitHub App installation was not resolved for target repository")
    token_response = auth.mint_installation_token(app_jwt, installation_id)
    token = token_response.get("token")
    if not isinstance(token, str) or not token:
        raise RuntimeError("GitHub did not return an installation token")
    return token


def main() -> int:
    parser = argparse.ArgumentParser(description="Proven-auth read-only GitHub provider check")
    parser.add_argument("--repository", required=True)
    args = parser.parse_args()
    adapter = _load(ADAPTER, "devos_github_provider_adapter_live")
    owner, repo = _load(AUTH, "devos_github_actions_auth_identity").parse_repository(args.repository)
    operation = {
        "provider": "github",
        "owner": owner,
        "repository": repo,
        "resource": None,
        "capability": "read.repository",
        "workflow": "devos-controller-v1",
        "project": repo,
        "impact": "READ_ONLY",
        "freshness": "main",
        "action": "repository.get",
        "inputs": {},
    }
    result = adapter.execute(operation, token_provider=proven_token_provider)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result.get("status") == "COMPLETE" else 2


if __name__ == "__main__":
    raise SystemExit(main())
