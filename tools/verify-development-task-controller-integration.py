#!/usr/bin/env python3
"""Executable P12/P16 controller, OI, and runtime-handoff integration checks."""
from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools" / filename)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    controller = load("controller", "development-task-controller.py")
    handoff = load("handoff", "devos-runtime-handoff.py")
    compiler = load("compiler", "semantic-goal-to-plan.py")

    # Legacy P12 inventory path remains compatible.
    payload = {
        "repository_head": "abc123",
        "authorization": "NOT_REQUIRED",
        "security_gate": "NOT_APPLICABLE",
        "capabilities": {"verify": "AVAILABLE"},
        "tasks": [
            {"id": "build", "status": "COMPLETE", "priority": 1,
             "objective": "Build source", "scope": "src/"},
            {"id": "verify", "status": "PLANNED", "priority": 10,
             "dependencies": ["build"], "objective": "Run verification", "scope": "tools/"},
        ],
    }
    decision = controller.decide(payload)
    assert decision["decision"] == "EXECUTION_CANDIDATE"
    assert decision["protocol_version"] == "P12-CONTROLLER-v1"
    assert decision["authority"] == "UNCHANGED"
    assert decision["execution"] == "NONE"
    assert decision["authorization"] == "UNCHANGED"
    assert decision["operational_intelligence"]["authority"] == "ADVISORY_ONLY"
    assert all(decision["gates"].values())

    envelope = handoff.build_handoff(decision)
    assert envelope["status"] == "READY_FOR_RUNTIME"
    assert envelope["execution"] == "NOT_STARTED"
    assert envelope["work_unit"]["id"] == "verify"

    blocked = controller.decide(payload | {"capabilities": {"verify": "MISSING"}})
    assert blocked["decision"] == "BLOCKED"
    assert blocked["gates"]["capability"] is False
    assert handoff.build_handoff(blocked)["status"] == "BLOCKED"

    approval = controller.decide(payload | {"authorization": "REQUIRED"})
    assert approval["decision"] == "BLOCKED"
    assert approval["gates"]["authorization"] is False

    # P16 compiled plans are consumed directly rather than reconstructed informally.
    plan = compiler.compile_plan("FEATURE_CHANGE", "update docs", "DEVOS", [], [])
    assert plan["decision"] == "PLANNED"
    assert plan["execution"] == "NONE" and plan["authority"] == "UNCHANGED"
    first = plan["steps"][0]
    compiled_payload = {
        "compiled_plan": plan,
        "repository_head": "p16-head",
        "scope": "repository",
        "completed_steps": [],
        "capabilities": {first["id"]: "AVAILABLE"},
        "authorization": "NOT_REQUIRED",
        "security_gate": "NOT_APPLICABLE",
    }
    compiled_decision = controller.decide(compiled_payload)
    assert compiled_decision["protocol_version"] == "P16-CONTROLLER-v1"
    assert compiled_decision["decision"] == "EXECUTION_CANDIDATE"
    assert compiled_decision["task_id"] == first["id"]
    assert compiled_decision["compiled_step"]["verification"] == first["verification"]
    assert compiled_decision["compiled_plan"]["execution"] == "NONE"
    assert compiled_decision["execution"] == "NONE"
    assert handoff.build_handoff(compiled_decision)["status"] == "READY_FOR_RUNTIME"

    # Completing the inspection unlocks the mutation while preserving dependency order.
    second = plan["steps"][1]
    second_decision = controller.decide(compiled_payload | {
        "completed_steps": [first["id"]],
        "capabilities": {second["id"]: "AVAILABLE"},
    })
    assert second_decision["decision"] == "EXECUTION_CANDIDATE"
    assert second_decision["task_id"] == second["id"]
    assert second_decision["compiled_step"]["impact"] == "LOW_IMPACT_MUTATION"

    # A non-PLANNED compiler envelope cannot become work.
    clarify = compiler.compile_plan("FEATURE_CHANGE", "update docs", None, [], [])
    clarify_decision = controller.decide({
        "compiled_plan": clarify,
        "repository_head": "p16-head",
        "capabilities": {},
        "authorization": "NOT_REQUIRED",
        "security_gate": "NOT_APPLICABLE",
    })
    assert clarify_decision["decision"] == "BLOCKED"
    assert "COMPILED_PLAN_NOT_PLANNED" in clarify_decision["reason"]
    assert clarify_decision["execution"] == "NONE"

    # High-impact compiler metadata strengthens gates; it never manufactures permission.
    high = compiler.compile_plan("FEATURE_CHANGE", "deploy production", "DEVOS", [], [])
    assert len(high["steps"]) == 2
    high_step = high["steps"][1]
    assert high_step["authorization_required"] is True
    high_payload = {
        "compiled_plan": high,
        "repository_head": "p16-head",
        "scope": "repository",
        "completed_steps": [high["steps"][0]["id"]],
        "capabilities": {high_step["id"]: "AVAILABLE"},
        "authorization": "NOT_REQUIRED",
        "security_gate": "PASS",
    }
    high_blocked = controller.decide(high_payload)
    assert high_blocked["decision"] == "BLOCKED"
    assert high_blocked["gates"]["authorization"] is False

    security_blocked = controller.decide(high_payload | {
        "authorization": "ALREADY_GRANTED",
        "security_gate": "NOT_APPLICABLE",
    })
    assert security_blocked["decision"] == "BLOCKED"
    assert security_blocked["gates"]["security"] is False

    high_ready = controller.decide(high_payload | {
        "authorization": "ALREADY_GRANTED",
        "security_gate": "PASS",
    })
    assert high_ready["decision"] == "EXECUTION_CANDIDATE"
    assert high_ready["execution"] == "NONE"

    print("P12/P16 controller/OI/runtime-handoff integration: PASS")


if __name__ == "__main__":
    main()
