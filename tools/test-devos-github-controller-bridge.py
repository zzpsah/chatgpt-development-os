#!/usr/bin/env python3
"""Deterministic checks for controller -> P17 -> GitHub bridge boundaries."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "tools" / "devos-github-controller-bridge.py"
spec = importlib.util.spec_from_file_location("devos_github_controller_bridge", MODULE)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


def base_controller() -> dict:
    return {
        "protocol_version": "P16-CONTROLLER-v1",
        "decision": "EXECUTION_CANDIDATE",
        "authority": "UNCHANGED",
        "execution": "NONE",
        "authorization": "UNCHANGED",
        "task_id": "TASK-1",
        "objective": "Inspect repository",
        "project": "chatgpt-development-os",
        "workflow": "devos-controller-v1",
        "repository_head": "HEAD-1",
        "gates": {
            "scope": True,
            "repository_revalidated": True,
            "readiness": True,
            "capability": True,
            "authorization": True,
            "security": True,
            "verification_path": True,
        },
        "compiled_step": {
            "id": "TASK-1",
            "objective": "Inspect repository",
            "impact": "READ_ONLY",
            "verification": "UNVERIFIED",
            "provider_operation": {
                "provider": "github",
                "owner": "zzpsah",
                "repository": "chatgpt-development-os",
                "resource": None,
                "capability": "read.repository",
                "impact": "READ_ONLY",
                "action": "repository.get",
                "inputs": {},
            },
        },
    }


def base_readiness() -> dict:
    return {
        "protocol": "DEVOS-STEP-READINESS-v1",
        "plan_protocol": "DEVOS-GOAL-PLAN-v1",
        "status": "READY",
        "authority": "UNCHANGED",
        "authorization": "UNCHANGED",
        "execution": "NONE",
        "gates": {"scope": True, "authorization": True, "security": True, "capability": True, "verification": True},
        "step_id": "TASK-1",
        "repository_head": "HEAD-1",
        "step": {"id": "TASK-1", "objective": "Inspect repository", "impact": "READ_ONLY", "verification": "UNVERIFIED"},
    }


def main() -> None:
    blocked = module.execute(base_controller(), {**base_readiness(), "status": "NEEDS_APPROVAL"})
    assert blocked["status"] == "BLOCKED", blocked
    assert blocked["mutation"] == "NONE", blocked

    mismatched = base_controller()
    mismatched["compiled_step"]["provider_operation"] = None
    result = module.execute(mismatched, base_readiness())
    assert result["status"] == "BLOCKED", result
    assert "PROVIDER_OPERATION_MISSING" in result["reason_codes"], result

    changed_head = base_controller()
    readiness = base_readiness()
    readiness["repository_head"] = "HEAD-2"
    result = module.execute(changed_head, readiness)
    assert result["status"] == "BLOCKED", result
    assert result["reason_codes"] == ["readiness_controller_repository_mismatch"], result

    print("DevOS GitHub controller bridge checks: PASS (3 scenarios)")


if __name__ == "__main__":
    main()
