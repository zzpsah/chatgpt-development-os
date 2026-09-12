#!/usr/bin/env python3
"""Executable contract checks for the P12 controller/OI advisory boundary."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_controller():
    path = ROOT / "tools/devos-task-controller.py"
    spec = importlib.util.spec_from_file_location("devos_task_controller", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    controller = load_controller()
    tasks = [
        {"id": "build", "status": "COMPLETE", "priority": 1, "objective": "build"},
        {"id": "test", "status": "PLANNED", "dependencies": ["build"], "priority": 10,
         "objective": "run tests", "capability_required": "python", "capability_available": True},
        {"id": "deploy", "status": "PLANNED", "dependencies": ["test"], "priority": 99,
         "objective": "deploy", "capability_required": "deploy", "capability_available": True,
         "authorization": "REQUIRED"},
    ]
    result = controller.controller_decision({"tasks": tasks})
    assert result["controller_version"] == "P12-CTRL-v1"
    assert result["decision"] == "EXECUTION_CANDIDATE"
    assert result["task_id"] == "test"
    assert result["advisory_next_action"]["authority"] == "ADVISORY_ONLY"
    assert result["authority"] == "UNCHANGED"
    assert result["execution"] == "NONE"
    assert result["authorization"] == "UNCHANGED"

    approval = controller.controller_decision({"tasks": [
        {"id": "deploy", "status": "NEEDS_APPROVAL", "priority": 99,
         "objective": "deploy", "authorization": "REQUIRED"}
    ]})
    assert approval["decision"] == "ROUTE_BLOCKER"
    assert approval["execution"] == "NONE"
    assert approval["authorization"] == "UNCHANGED"

    missing_cap = controller.controller_decision({"tasks": [
        {"id": "build", "status": "PLANNED", "priority": 10, "objective": "build",
         "capability_required": "compiler", "capability_available": False}
    ]})
    assert missing_cap["decision"] == "HOLD"
    assert "CAPABILITY_MISSING" in missing_cap["reasons"]

    complete = controller.controller_decision({"tasks": [
        {"id": "done", "status": "COMPLETE", "priority": 1, "objective": "done"}
    ]})
    assert complete["decision"] == "NO_ACTION"
    assert complete["task_id"] is None
    assert complete["execution"] == "NONE"
    print("P12 controller advisory integration v1 contract and executable checks: PASS")


if __name__ == "__main__":
    main()
