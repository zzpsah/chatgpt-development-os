#!/usr/bin/env python3
"""Deterministic regression checks for the governed GitHub provider adapter."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "tools" / "devos-github-provider-adapter.py"
spec = importlib.util.spec_from_file_location("devos_github_provider_adapter", MODULE)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


AUTH = {
    "provider": "github",
    "owner": "zzpsah",
    "repository": "chatgpt-development-os",
    "resource": "feature/foo",
    "capability": "branch.update",
    "workflow": "devos-controller-v1",
    "project": "chatgpt-development-os",
    "impact_ceiling": "HIGH",
    "freshness": "head-1",
    "authorization_id": "AUTH-1",
}


def fake_token_provider(repository: str) -> str:
    assert repository == "zzpsah/chatgpt-development-os"
    return "FAKE-INSTALLATION-TOKEN"


def fake_read(token: str, operation: module.OperationRecord) -> dict:
    assert token == "FAKE-INSTALLATION-TOKEN"
    return {"full_name": operation.repository, "action": operation.action}


def main() -> None:
    read = module.execute(
        {
            "provider": "github",
            "owner": "zzpsah",
            "repository": "chatgpt-development-os",
            "resource": None,
            "capability": "read.repository",
            "workflow": "inspect",
            "project": "chatgpt-development-os",
            "impact": "READ_ONLY",
            "freshness": None,
            "action": "repository.get",
            "inputs": {},
        },
        token_provider=fake_token_provider,
        client_read=fake_read,
    )
    assert read["status"] == "COMPLETE", read
    assert read["credential_material"] == "NOT_INCLUDED", read
    assert read["execution"] == "PROVIDER_READ", read
    assert read["mutation"] == "NONE", read

    missing_auth = module.execute(
        {
            "provider": "github",
            "owner": "zzpsah",
            "repository": "chatgpt-development-os",
            "resource": "feature/foo",
            "capability": "branch.update",
            "workflow": "devos-controller-v1",
            "project": "chatgpt-development-os",
            "impact": "HIGH",
            "freshness": "head-1",
            "action": "branch.update",
            "inputs": {"sha": "abc"},
        },
        token_provider=fake_token_provider,
    )
    assert missing_auth["status"] == "NEEDS_APPROVAL", missing_auth
    assert "NO_APPROVAL" in missing_auth["reason_codes"], missing_auth
    assert missing_auth["mutation"] == "NONE", missing_auth

    wrong_scope = module.execute(
        {
            "provider": "github",
            "owner": "zzpsah",
            "repository": "other-repo",
            "resource": "feature/foo",
            "capability": "branch.update",
            "workflow": "devos-controller-v1",
            "project": "chatgpt-development-os",
            "impact": "HIGH",
            "freshness": "head-1",
            "action": "branch.update",
            "inputs": {"sha": "abc"},
        },
        authorization_data=AUTH,
        token_provider=fake_token_provider,
    )
    assert wrong_scope["status"] == "NEEDS_APPROVAL", wrong_scope
    assert "REPOSITORY_SCOPE_CHANGED" in wrong_scope["reason_codes"], wrong_scope
    assert wrong_scope["mutation"] == "NONE", wrong_scope

    mismatch = module.execute(
        {
            "provider": "github",
            "owner": "zzpsah",
            "repository": "chatgpt-development-os",
            "resource": "feature/foo",
            "capability": "branch.update",
            "workflow": "devos-controller-v1",
            "project": "chatgpt-development-os",
            "impact": "HIGH",
            "freshness": "head-1",
            "action": "branch.delete",
            "inputs": {},
        },
        authorization_data=AUTH,
        token_provider=fake_token_provider,
    )
    assert mismatch["status"] == "BLOCKED", mismatch
    assert "CAPABILITY_ACTION_MISMATCH" in mismatch["reason_codes"], mismatch
    assert mismatch["mutation"] == "NONE", mismatch

    print("DevOS GitHub provider adapter checks: PASS (4 scenarios)")


if __name__ == "__main__":
    main()
