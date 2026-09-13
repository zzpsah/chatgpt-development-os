#!/usr/bin/env python3
"""Bounded controller -> execution-runtime handoff contract.

This module creates a runtime work-unit envelope only after independent
capability, authorization, and security checks. It does not execute actions.
P17 adds a stricter readiness-aware entry point without breaking the P12 path.
"""

from __future__ import annotations

import json
import sys
from typing import Any


ALLOWED_CONTROLLER_DECISION = "EXECUTION_CANDIDATE"
P17_CONTROLLER_PROTOCOL = "P16-CONTROLLER-v1"
P17_READINESS_PROTOCOL = "DEVOS-STEP-READINESS-v1"
P16_PLAN_PROTOCOL = "DEVOS-GOAL-PLAN-v1"


def build_handoff(controller: dict[str, Any]) -> dict[str, Any]:
    if controller.get("decision") != ALLOWED_CONTROLLER_DECISION:
        return {"status": "BLOCKED", "reason": "controller_decision_not_executable"}
    if controller.get("authority") != "UNCHANGED":
        return {"status": "BLOCKED", "reason": "authority_changed"}
    if controller.get("execution") != "NONE":
        return {"status": "BLOCKED", "reason": "execution_already_claimed"}
    if controller.get("authorization") != "UNCHANGED":
        return {"status": "BLOCKED", "reason": "authorization_boundary_changed"}

    gates = controller.get("gates", {})
    if not isinstance(gates, dict):
        return {"status": "BLOCKED", "reason": "controller_gates_invalid"}
    for gate in ("capability", "authorization", "security"):
        if gates.get(gate) is not True:
            return {"status": "BLOCKED", "reason": f"{gate}_gate_not_passed"}

    task_id = controller.get("task_id")
    objective = controller.get("objective")
    if not task_id or not objective:
        return {"status": "BLOCKED", "reason": "missing_work_unit_identity"}

    return {
        "status": "READY_FOR_RUNTIME",
        "authority": "UNCHANGED",
        "execution": "NOT_STARTED",
        "authorization": "UNCHANGED",
        "work_unit": {
            "id": task_id,
            "objective": objective,
            "scope": controller.get("scope", ""),
            "repository_head": controller.get("repository_head", "UNKNOWN"),
        },
        "evidence": [],
        "verification": "UNVERIFIED",
    }


def build_p17_handoff(controller: dict[str, Any], readiness: dict[str, Any]) -> dict[str, Any]:
    """Require an exact, fresh P17 READY envelope before runtime handoff."""
    if controller.get("protocol_version") != P17_CONTROLLER_PROTOCOL:
        return {"status": "BLOCKED", "reason": "p17_requires_compiled_plan_controller"}
    if controller.get("decision") != ALLOWED_CONTROLLER_DECISION:
        return {"status": "BLOCKED", "reason": "controller_decision_not_executable"}

    if readiness.get("protocol") != P17_READINESS_PROTOCOL:
        return {"status": "BLOCKED", "reason": "invalid_step_readiness_protocol"}
    if readiness.get("plan_protocol") != P16_PLAN_PROTOCOL:
        return {"status": "BLOCKED", "reason": "invalid_readiness_plan_protocol"}
    if readiness.get("status") != "READY":
        return {"status": "BLOCKED", "reason": "step_not_ready", "readiness_status": readiness.get("status")}
    if readiness.get("authority") != "UNCHANGED" or readiness.get("authorization") != "UNCHANGED":
        return {"status": "BLOCKED", "reason": "readiness_authority_boundary_changed"}
    if readiness.get("execution") != "NONE":
        return {"status": "BLOCKED", "reason": "readiness_claimed_execution"}

    readiness_gates = readiness.get("gates")
    if not isinstance(readiness_gates, dict) or not readiness_gates or not all(value is True for value in readiness_gates.values()):
        return {"status": "BLOCKED", "reason": "readiness_gates_not_satisfied"}

    controller_gates = controller.get("gates")
    required_controller_gates = {
        "scope", "repository_revalidated", "readiness", "capability",
        "authorization", "security", "verification_path",
    }
    if not isinstance(controller_gates, dict) or any(controller_gates.get(name) is not True for name in required_controller_gates):
        return {"status": "BLOCKED", "reason": "controller_gates_not_satisfied"}

    controller_step = controller.get("compiled_step")
    readiness_step = readiness.get("step")
    task_id = controller.get("task_id")
    step_id = readiness.get("step_id")
    if not isinstance(controller_step, dict) or not isinstance(readiness_step, dict):
        return {"status": "BLOCKED", "reason": "compiled_step_metadata_missing"}
    if not task_id or not step_id or task_id != step_id:
        return {"status": "BLOCKED", "reason": "readiness_controller_step_mismatch"}
    if controller_step.get("id") != task_id or readiness_step.get("id") != step_id:
        return {"status": "BLOCKED", "reason": "step_metadata_identity_mismatch"}
    if controller_step.get("objective") != readiness_step.get("objective"):
        return {"status": "BLOCKED", "reason": "step_objective_mismatch"}
    if controller_step.get("impact") != readiness_step.get("impact"):
        return {"status": "BLOCKED", "reason": "step_impact_mismatch"}
    if controller_step.get("verification") != readiness_step.get("verification"):
        return {"status": "BLOCKED", "reason": "step_verification_mismatch"}

    if readiness.get("repository_head") != controller.get("repository_head"):
        return {"status": "BLOCKED", "reason": "readiness_controller_repository_mismatch"}

    envelope = build_handoff(controller)
    if envelope.get("status") != "READY_FOR_RUNTIME":
        return envelope
    envelope["step_readiness"] = {
        "protocol": readiness.get("protocol"),
        "plan_protocol": readiness.get("plan_protocol"),
        "step_id": step_id,
        "status": readiness.get("status"),
        "repository_head": readiness.get("repository_head"),
        "execution_evidence": False,
    }
    return envelope


def main() -> int:
    payload = json.load(sys.stdin)
    print(json.dumps(build_handoff(payload), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
