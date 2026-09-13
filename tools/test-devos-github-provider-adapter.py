#!/usr/bin/env python3
"""Deterministic regression checks for the governed GitHub provider adapter."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "tools" / "devos-github-provider-adapter.py"
spec = importlib.util.spec_from_file_location("devos_github_provider_adapter", MODULE)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name] = module
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


def mutation_operation() -> dict:
    return {
        "provider": "github",
        "owner": "zzpsah",
        "repository": "chatgpt-development-os",
        "resource": "artifacts/live-test/reconciled.txt",
        "capability": "file.create",
        "workflow": "devos-controller-v1",
        "project": "chatgpt-development-os",
        "impact": "HIGH",
        "freshness": "head-1",
        "action": "file.create",
        "inputs": {"message": "test", "content": "hello", "branch": "feature/foo"},
    }


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

    original_gate = module._gate
    original_mutate = module._mutate
    module._gate = lambda operation, authorization: {"status": "CONTINUE_WITH_EXISTING_APPROVAL", "reasons": [], "capability": operation.capability}
    module._mutate = lambda token, operation: ({"commit": {"sha": "commit-1"}}, {"http_status": 201})
    reads = [
        RuntimeError("GitHub API request failed: HTTP 404: Not Found"),
        RuntimeError("GitHub API request failed: HTTP 404: Not Found"),
        {"sha": "blob-1"},
    ]
    sleep_calls: list[float] = []

    def eventual_read(token: str, operation: module.OperationRecord):
        value = reads.pop(0)
        if isinstance(value, Exception):
            raise value
        return value

    reconciled = module.execute(
        mutation_operation(),
        authorization_data={**AUTH, "resource": "artifacts/live-test/reconciled.txt", "capability": "file.create", "authorization_id": "AUTH-RECONCILE"},
        token_provider=fake_token_provider,
        client_read=eventual_read,
        sleep_fn=sleep_calls.append,
    )
    assert reconciled["status"] == "COMPLETE", reconciled
    assert reconciled["readback"]["status"] == "PRESENT", reconciled
    assert reconciled["readback"]["sha"] == "blob-1", reconciled
    assert reconciled["readback_attempts"] == 3, reconciled
    assert sleep_calls == [1.0, 2.0], sleep_calls

    reads.clear()
    reads.extend([RuntimeError("GitHub API request failed: HTTP 401: Bad credentials")])
    sleep_calls.clear()
    no_retry = module.execute(
        mutation_operation(),
        authorization_data={**AUTH, "resource": "artifacts/live-test/reconciled.txt", "capability": "file.create", "authorization_id": "AUTH-NO-RETRY"},
        token_provider=fake_token_provider,
        client_read=eventual_read,
        sleep_fn=sleep_calls.append,
    )
    assert no_retry["status"] == "HOLD", no_retry
    assert no_retry["reason_codes"] == ["READBACK_REQUIRED"], no_retry
    assert sleep_calls == [], sleep_calls

    module._gate = original_gate
    module._mutate = original_mutate

    print("DevOS GitHub provider adapter checks: PASS (6 scenarios)")


if __name__ == "__main__":
    main()
