#!/usr/bin/env python3
"""Bounded controller -> execution-runtime handoff contract.

This module creates a runtime work-unit envelope only after independent
capability, authorization, and security checks. It does not execute actions.
"""

from __future__ import annotations

import json
import sys
from typing import Any


ALLOWED_CONTROLLER_DECISION = "EXECUTION_CANDIDATE"


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


def main() -> int:
    payload = json.load(sys.stdin)
    print(json.dumps(build_handoff(payload), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
