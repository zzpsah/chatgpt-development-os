#!/usr/bin/env python3
"""Deterministic P12 controller decision envelope.

Operational Intelligence supplies an advisory candidate.  This controller
independently checks that candidate against the supplied scope, capability,
authorization, security, and repository-revalidation inputs.  It never runs a
work unit or changes authority.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def load_operational_intelligence() -> Any:
    """Load the hyphenated OI module without requiring package installation."""
    path = ROOT / "tools" / "operational-intelligence.py"
    spec = importlib.util.spec_from_file_location("operational_intelligence", path)
    if spec is None or spec.loader is None:
        raise ImportError("could not load Operational Intelligence")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _gate(value: Any, accepted: set[str]) -> bool:
    """Return whether a declared controller input satisfies one gate."""
    return str(value) in accepted


def decide(payload: dict[str, Any]) -> dict[str, Any]:
    """Return a non-executing controller decision envelope for one inventory."""
    tasks = payload.get("tasks", [])
    oi = load_operational_intelligence()
    analysis = oi.analyze(
        tasks,
        payload.get("events", []),
        payload.get("failures", []),
        payload.get("evidence", []),
    )
    recommendation = analysis["advisory_next_action"]
    base = {
        "protocol_version": "P12-CONTROLLER-v1",
        "authority": "UNCHANGED",
        "execution": "NONE",
        "authorization": "UNCHANGED",
        "operational_intelligence": {
            "authority": recommendation["authority"],
            "advisory_next_action": recommendation,
            "readiness": analysis["readiness"],
        },
    }

    if recommendation["action"] == "no_action":
        return base | {"decision": "NO_ACTION", "task_id": None, "gates": {},
                       "reason": recommendation["reason"]}

    task_id = recommendation["task_id"]
    if recommendation["action"].startswith("resolve:"):
        return base | {"decision": "BLOCKED", "task_id": task_id, "gates": {},
                       "reason": recommendation["reason"] + ["CONTROLLER_ROUTING_REQUIRED"]}

    task_by_id = {str(task.get("id")): task for task in tasks}
    task = task_by_id.get(str(task_id))
    readiness_by_id = {row["id"]: row["readiness"] for row in analysis["readiness"]}
    scope = task.get("scope") if task else None
    objective = task.get("objective") if task else None
    capabilities = payload.get("capabilities", {})
    gates = {
        "scope": isinstance(scope, str) and bool(scope.strip()),
        "repository_revalidated": isinstance(payload.get("repository_head"), str)
        and bool(payload["repository_head"].strip()),
        "readiness": readiness_by_id.get(task_id) == "READY",
        "capability": _gate(capabilities.get(task_id), {"AVAILABLE"}),
        "authorization": _gate(payload.get("authorization"), {"NOT_REQUIRED", "ALREADY_GRANTED"}),
        "security": _gate(payload.get("security_gate"), {"PASS", "NOT_APPLICABLE"}),
    }
    if all(gates.values()) and isinstance(objective, str) and bool(objective.strip()):
        return base | {"decision": "EXECUTION_CANDIDATE", "task_id": task_id,
                       "objective": objective, "scope": scope,
                       "repository_head": payload["repository_head"], "gates": gates,
                       "reason": recommendation["reason"]}

    failed = sorted(name for name, passed in gates.items() if not passed)
    if not isinstance(objective, str) or not objective.strip():
        failed.append("objective")
    return base | {"decision": "BLOCKED", "task_id": task_id, "gates": gates,
                   "reason": recommendation["reason"] + ["FAILED_GATES=" + ",".join(failed)]}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="JSON task inventory plus independent controller inputs")
    parser.add_argument("--output", help="optional JSON output path")
    args = parser.parse_args()
    result = json.dumps(decide(json.loads(Path(args.input).read_text(encoding="utf-8"))), indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(result, encoding="utf-8")
    else:
        print(result, end="")


if __name__ == "__main__":
    main()
