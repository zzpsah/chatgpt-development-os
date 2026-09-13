#!/usr/bin/env python3
"""Regression corpus for the MCP/App remote-permission control plane."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "tools" / "devos-mcp-governed-gateway.py"
spec = importlib.util.spec_from_file_location("devos_mcp_governed_gateway", MODULE)
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


def auth(**overrides):
    data = {
        "provider": "github", "owner": "zzpsah", "repository": "demo-a",
        "resource": "feature/a", "capability": "branch.create", "workflow": "W1",
        "project": "demo-a", "impact_ceiling": "HIGH", "freshness": "HEAD-A",
        "authorization_id": "APR-1",
    }
    data.update(overrides)
    return data


def op(**overrides):
    data = {
        "provider": "github", "owner": "zzpsah", "repository": "demo-a",
        "resource": "feature/a", "capability": "branch.create", "workflow": "W1",
        "project": "demo-a", "impact": "LOW", "freshness": "HEAD-A",
    }
    data.update(overrides)
    return data


def main() -> None:
    allowed = mod.evaluate_remote_operation(auth(), op())
    assert allowed["decision"] == "ALLOW_TO_PROVIDER_GATE"
    assert allowed["status"] == "READY"
    assert allowed["execution"] == "NONE"
    assert allowed["mutation"] == "NONE"

    delete = mod.evaluate_remote_operation(auth(), op(capability="repository.delete", repository="demo-a", resource=None, impact="DESTRUCTIVE"))
    assert delete["decision"] == "ACTIONABLE_HOLD"
    assert "CAPABILITY_SCOPE_CHANGED" in delete["reason_codes"]
    assert "IMPACT_EXCEEDS_APPROVAL_CEILING" in delete["reason_codes"]
    assert delete["what_will_happen"]
    assert delete["options"]

    other_repo = mod.evaluate_remote_operation(auth(), op(repository="demo-b", project="demo-b"))
    assert "REPOSITORY_SCOPE_CHANGED" in other_repo["reason_codes"]
    assert "PROJECT_SCOPE_CHANGED" in other_repo["reason_codes"]

    stale = mod.evaluate_remote_operation(auth(), op(freshness="HEAD-B"))
    assert "FRESHNESS_CHANGED" in stale["reason_codes"]
    assert stale["status"] == "NEEDS_APPROVAL"

    force = mod.evaluate_remote_operation(auth(capability="branch.update", impact_ceiling="HIGH"), op(capability="branch.force_update", resource="main", impact="DESTRUCTIVE"))
    assert force["decision"] == "ACTIONABLE_HOLD"
    assert "CAPABILITY_SCOPE_CHANGED" in force["reason_codes"]
    assert "IMPACT_EXCEEDS_APPROVAL_CEILING" in force["reason_codes"]

    missing = mod.evaluate_remote_operation(None, op(capability="repository.create", repository="new-project", resource=None, impact="HIGH"))
    assert missing["decision"] == "ACTIONABLE_HOLD"
    assert missing["status"] == "NEEDS_APPROVAL"
    assert missing["approval_required"]["explicit"] is True

    print("PASS: MCP governed remote-permission gateway regression corpus")


if __name__ == "__main__":
    main()
