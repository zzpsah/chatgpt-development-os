#!/usr/bin/env python3
"""Deterministic regression tests for GitHub capability discovery."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "devos-github-capability-discovery.py"
SPEC = importlib.util.spec_from_file_location("devos_github_capability_discovery", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("unable to load capability module")
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def main() -> None:
    results = MODULE.evaluate_capabilities(
        ["file.update", "branch.create", "repository.delete"],
        provider_permissions={"contents": "write", "administration": "write"},
        required_permissions={
            "file.update": {"contents": "write"},
            "branch.create": {"contents": "write"},
            "repository.delete": {"administration": "write"},
        },
        target_repository="example/repo",
        repository_scope=("example/repo",),
    )
    assert [r.status for r in results] == ["AVAILABLE", "AVAILABLE", "AVAILABLE"]

    hold = MODULE.evaluate_capability(
        "pr.merge",
        provider_permissions={"contents": "write"},
        required_permissions={},
        target_repository="example/repo",
        repository_scope=("example/repo",),
    )
    assert hold.status == "UNCONFIRMED"
    assert hold.reason == "PROVIDER_MAPPING_REQUIRED"

    insufficient = MODULE.evaluate_capability(
        "file.update",
        provider_permissions={"contents": "read"},
        required_permissions={"file.update": {"contents": "write"}},
        target_repository="example/repo",
        repository_scope=("example/repo",),
    )
    assert insufficient.status == "UNAVAILABLE"
    assert insufficient.reason.startswith("INSUFFICIENT_PROVIDER_PERMISSION_LEVEL:")

    outside_scope = MODULE.evaluate_capability(
        "branch.force_update",
        provider_permissions={"contents": "write"},
        required_permissions={"branch.force_update": {"contents": "write"}},
        target_repository="example/other",
        repository_scope=("example/repo",),
    )
    assert outside_scope.status == "UNAVAILABLE"
    assert outside_scope.reason == "TARGET_REPOSITORY_OUTSIDE_SCOPE"

    missing_target = MODULE.evaluate_capability(
        "pr.merge",
        provider_permissions={"pull_requests": "write"},
        required_permissions={"pr.merge": {"pull_requests": "write"}},
        repository_scope=("example/repo",),
    )
    assert missing_target.status == "UNCONFIRMED"
    assert missing_target.reason == "TARGET_REPOSITORY_REQUIRED"

    metadata = MODULE.safe_capability_metadata(
        provider="github",
        identity="example",
        permissions={"contents": "write"},
        results=(results[0],),
        target_repository="example/repo",
        repository_scope=("example/repo",),
    )
    assert metadata["credential_material"] == "NOT_INCLUDED"
    assert metadata["authorization"] == "UNCHANGED"
    assert metadata["execution"] == "NONE"
    assert metadata["mutation"] == "NONE"
    assert metadata["target_repository"] == "example/repo"
    assert metadata["repository_scope"] == ["example/repo"]
    assert "token" not in str(metadata).lower()

    try:
        MODULE.evaluate_capability(
            "unknown",
            provider_permissions={},
            required_permissions={},
        )
    except MODULE.CapabilityDiscoveryError as exc:
        assert str(exc).startswith("UNSUPPORTED_DEVOS_CAPABILITY:")
    else:
        raise AssertionError("unsupported capability must fail closed")

    print("DevOS GitHub capability discovery checks: PASS (8 scenarios)")


if __name__ == "__main__":
    main()