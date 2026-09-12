#!/usr/bin/env python3
"""Executable P13 orchestration regression checks."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load():
    spec = importlib.util.spec_from_file_location("autonomous_orchestrator", ROOT / "tools/autonomous-orchestrator.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def payload() -> dict:
    return {
        "goal": "Verify the project",
        "max_iterations": 2,
        "completed_iterations": 0,
        "repository_head": "abc123",
        "authorization": "NOT_REQUIRED",
        "security_gate": "NOT_APPLICABLE",
        "capabilities": {"verify": "AVAILABLE", "document": "AVAILABLE"},
        "tasks": [
            {"id": "source", "status": "COMPLETE", "priority": 1,
             "objective": "Inspect source", "scope": "src/"},
            {"id": "verify", "status": "PLANNED", "priority": 10,
             "dependencies": ["source"], "objective": "Run verification", "scope": "tools/"},
            {"id": "document", "status": "PLANNED", "priority": 5,
             "dependencies": ["verify"], "objective": "Record result", "scope": ".ai/"},
        ],
    }


def main() -> None:
    orchestrator = load()
    ready = orchestrator.orchestrate(payload())
    assert ready["decision"] == "CONTINUE"
    assert ready["execution"] == "NONE"
    assert ready["runtime_handoff"]["status"] == "READY_FOR_RUNTIME"
    assert ready["runtime_handoff"]["execution"] == "NOT_STARTED"

    next_unit = orchestrator.orchestrate(payload() | {"latest_runtime_outcome": {
        "task_id": "verify", "status": "COMPLETE", "verification": "VERIFIED",
        "evidence": [{"source": "runtime", "exit_status": 0}],
    }})
    assert next_unit["decision"] == "CONTINUE"
    assert next_unit["runtime_handoff"]["work_unit"]["id"] == "document"

    unevidenced = orchestrator.orchestrate(payload() | {"latest_runtime_outcome": {
        "task_id": "verify", "status": "COMPLETE", "verification": "VERIFIED", "evidence": []
    }})
    assert unevidenced["decision"] == "ESCALATE"
    assert unevidenced["reason"] == ["RUNTIME_OUTCOME_MISSING_EVIDENCE"]

    budget = orchestrator.orchestrate(payload() | {"completed_iterations": 2})
    assert budget["decision"] == "STOP"
    assert budget["reason"] == ["EXECUTION_BUDGET_EXHAUSTED"]

    blocked = orchestrator.orchestrate(payload() | {"authorization": "REQUIRED"})
    assert blocked["decision"] == "ESCALATE"
    assert blocked["controller"]["gates"]["authorization"] is False

    no_action = orchestrator.orchestrate(payload() | {"tasks": [
        {"id": "done", "status": "COMPLETE", "priority": 1,
         "objective": "Done", "scope": "src/"}
    ]})
    assert no_action["decision"] == "STOP"
    print("P13 autonomous goal-to-next-safe-unit orchestration: PASS")


if __name__ == "__main__":
    main()
