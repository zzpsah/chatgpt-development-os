#!/usr/bin/env python3
"""P13 bounded goal-to-next-safe-unit orchestration.

This planner joins the P12 controller decision and runtime-handoff contracts.
It never executes a work unit: its only control results are CONTINUE, STOP,
and ESCALATE.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def load(name: str, filename: str) -> Any:
    """Load a local tool module while preserving its import identity."""
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools" / filename)
    if spec is None or spec.loader is None:
        raise ImportError(f"could not load {filename}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def orchestrate(payload: dict[str, Any]) -> dict[str, Any]:
    """Choose one bounded next unit, stop, or escalate without execution."""
    goal = payload.get("goal")
    if not isinstance(goal, str) or not goal.strip():
        raise ValueError("goal must be a non-empty string")
    budget = payload.get("max_iterations", 1)
    completed = payload.get("completed_iterations", 0)
    if not isinstance(budget, int) or budget < 1:
        raise ValueError("max_iterations must be a positive integer")
    if not isinstance(completed, int) or completed < 0:
        raise ValueError("completed_iterations must be a non-negative integer")

    base = {
        "protocol_version": "P13-ORCHESTRATOR-v1",
        "goal": goal,
        "iteration": completed + 1,
        "max_iterations": budget,
        "authority": "UNCHANGED",
        "execution": "NONE",
    }
    if completed >= budget:
        return base | {"decision": "STOP", "reason": ["EXECUTION_BUDGET_EXHAUSTED"],
                       "controller": None, "runtime_handoff": None}

    controller = load("development_task_controller", "development-task-controller.py")
    handoff = load("devos_runtime_handoff", "devos-runtime-handoff.py")
    decision = controller.decide(payload)
    if decision["decision"] == "NO_ACTION":
        return base | {"decision": "STOP", "reason": decision["reason"],
                       "controller": decision, "runtime_handoff": None}
    if decision["decision"] != "EXECUTION_CANDIDATE":
        return base | {"decision": "ESCALATE", "reason": decision["reason"],
                       "controller": decision, "runtime_handoff": None}

    envelope = handoff.build_handoff(decision)
    if envelope["status"] != "READY_FOR_RUNTIME":
        return base | {"decision": "ESCALATE", "reason": [envelope["reason"]],
                       "controller": decision, "runtime_handoff": envelope}
    return base | {"decision": "CONTINUE", "reason": decision["reason"],
                   "controller": decision, "runtime_handoff": envelope}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="JSON goal, budget, task inventory, and controller inputs")
    parser.add_argument("--output", help="optional JSON output path")
    args = parser.parse_args()
    result = json.dumps(orchestrate(json.loads(Path(args.input).read_text(encoding="utf-8"))), indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(result, encoding="utf-8")
    else:
        print(result, end="")


if __name__ == "__main__":
    main()
