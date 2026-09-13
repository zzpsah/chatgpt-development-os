#!/usr/bin/env python3
"""Regression corpus for remote-permission continuation integration."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "tools" / "devos-governed-continuation.py"
spec = importlib.util.spec_from_file_location("devos_governed_continuation", MODULE)
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


def approval(**overrides):
    data = {
        "provider": "github",
        "owner": "zzpsah",
        "repository": "demo-a",
        "resource": "feature/a",
        "capability": "branch.create",
        "workflow": "W1",
        "project": "demo-a",
        "impact_ceiling": "HIGH",
        "freshness": "HEAD-A",
        "authorization_id": "APR-1",
    }
    data.update(overrides)
    return data


def operation(**overrides):
    data = {
        "provider": "github",
        "owner": "zzpsah",
        "repository": "demo-a",
        "resource": "feature/a",
        "capability": "branch.create",
        "workflow": "W1",
        "project": "demo-a",
        "impact": "LOW",
        "freshness": "HEAD-A",
    }
    data.update(overrides)
    return data


def main() -> None:
    result = mod.decide(approval(), operation())
    assert result["decision"] == "CONTINUE_WITH_EXISTING_APPROVAL"
    assert result["execution"] == "NONE"
    assert result["mutation"] == "NONE"
    assert result["authorization"] == "ALREADY_GRANTED"

    result = mod.decide(approval(), operation(capability="branch.delete", impact="DESTRUCTIVE"))
    assert result["decision"] == "ACTIONABLE_HOLD"
    assert "CAPABILITY_SCOPE_CHANGED" in result["reason_codes"]
    assert "IMPACT_EXCEEDS_APPROVAL_CEILING" in result["reason_codes"]
    assert result["what_will_happen"]
    assert result["options"]

    result = mod.decide(approval(), operation(repository="demo-b", project="demo-b"))
    assert result["decision"] == "ACTIONABLE_HOLD"
    assert "REPOSITORY_SCOPE_CHANGED" in result["reason_codes"]
    assert "PROJECT_SCOPE_CHANGED" in result["reason_codes"]

    result = mod.decide(approval(), operation(freshness="HEAD-B"))
    assert result["decision"] == "ACTIONABLE_HOLD"
    assert "FRESHNESS_CHANGED" in result["reason_codes"]

    result = mod.decide(approval(), operation(resource="main", capability="branch.force_update", impact="DESTRUCTIVE"))
    assert result["decision"] == "ACTIONABLE_HOLD"
    assert "CAPABILITY_SCOPE_CHANGED" in result["reason_codes"]
    assert "IMPACT_EXCEEDS_APPROVAL_CEILING" in result["reason_codes"]

    result = mod.decide(None, operation(capability="repository.delete", impact="DESTRUCTIVE", resource=None))
    assert result["decision"] == "ACTIONABLE_HOLD"
    assert result["status"] == "NEEDS_APPROVAL"
    assert result["impact"] == "DESTRUCTIVE"
    assert result["approval_required"]["explicit"] is True
    assert result["execution"] == "NONE"
    assert result["mutation"] == "NONE"

    # Approval for one repository must never bleed into another repository.
    result = mod.decide(approval(repository="repo-a", project="project-a"), operation(repository="repo-b", project="project-b"))
    assert "REPOSITORY_SCOPE_CHANGED" in result["reason_codes"]
    assert "PROJECT_SCOPE_CHANGED" in result["reason_codes"]

    print("PASS: governed continuation + remote permission integration corpus")


if __name__ == "__main__":
    main()
