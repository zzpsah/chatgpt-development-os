#!/usr/bin/env python3
"""Executable P12 controller bridge: advisory OI -> independently gated decision.

This controller does not execute work. It converts Operational Intelligence output
into a deterministic candidate/hold/routing envelope while preserving existing
capability and authorization boundaries.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def load_oi():
    path = ROOT / "tools/operational-intelligence.py"
    name = "devos_operational_intelligence"
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def controller_decision(payload: dict[str, Any]) -> dict[str, Any]:
    oi = load_oi()
    tasks = list(payload.get("tasks", []))
    result = oi.analyze(tasks, payload.get("events", []), payload.get("failures", []), payload.get("evidence", []))
    recommendation = result["advisory_next_action"]
    by_id = {str(task["id"]): task for task in tasks}
    task_id = recommendation["task_id"]
    decision = "NO_ACTION"
    reasons: list[str] = []

    if recommendation["action"].startswith("work_on:") and task_id in by_id:
        task = by_id[task_id]
        state = next(x for x in result["readiness"] if x["id"] == task_id)
        if state["readiness"] != "READY":
            decision = "HOLD"
            reasons.append(f"readiness={state['readiness']}")
        if task.get("capability_required") and not task.get("capability_available", False):
            decision = "HOLD"
            reasons.append("CAPABILITY_MISSING")
        if task.get("authorization", "NOT_REQUIRED") == "REQUIRED":
            decision = "HOLD"
            reasons.append("AUTHORIZATION_REQUIRED")
        if not task.get("objective"):
            decision = "HOLD"
            reasons.append("OBJECTIVE_MISSING")
        if decision == "NO_ACTION":
            decision = "EXECUTION_CANDIDATE"
            reasons.append("OI_RECOMMENDATION_PASSED_INDEPENDENT_CONTROLLER_GATES")
    elif recommendation["action"].startswith("resolve:"):
        decision = "ROUTE_BLOCKER"
        reasons.append("OI_RECOMMENDS_RESOLUTION_NOT_EXECUTION")
    else:
        reasons.append("NO_EXECUTABLE_CANDIDATE")

    return {
        "controller_version": "P12-CTRL-v1",
        "decision": decision,
        "task_id": task_id,
        "advisory_next_action": recommendation,
        "reasons": reasons,
        "authority": "UNCHANGED",
        "execution": "NONE",
        "authorization": "UNCHANGED",
        "operational_intelligence": result,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="JSON task/controller input")
    parser.add_argument("--output", help="optional JSON output path")
    args = parser.parse_args()
    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    result = json.dumps(controller_decision(payload), indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(result, encoding="utf-8")
    else:
        print(result, end="")


if __name__ == "__main__":
    main()
