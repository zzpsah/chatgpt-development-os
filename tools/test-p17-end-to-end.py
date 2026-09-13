#!/usr/bin/env python3
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools" / filename)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    interpreter = load("interpreter", "human-language-interpreter.py")
    compiler = load("compiler", "semantic-goal-to-plan.py")
    readiness_mod = load("readiness", "step-readiness-orchestrator.py")
    controller = load("controller", "development-task-controller.py")
    handoff = load("handoff", "devos-runtime-handoff.py")

    head = "repo-head-1"

    interpreted = interpreter.interpret({
        "phrase": "check repository",
        "context": {"project": "DEVOS"},
    })
    assert interpreted["decision"] == "INTERPRETED"
    assert interpreted["objective"] == "check repository"
    assert "VALIDATION" in interpreted["intents"]
    assert interpreted["execution"] == "NONE"

    plan = compiler.compile_plan(
        interpreted["intents"][0],
        interpreted["objective"],
        interpreted["project"],
        interpreted["constraints"],
        [],
    )
    assert plan["decision"] == "PLANNED"
    step = plan["steps"][0]

    readiness = readiness_mod.evaluate({
        "plan": plan,
        "step_id": step["id"],
        "compiled_repository_head": head,
        "current_repository_head": head,
        "completed_steps": [],
        "capabilities": {step["id"]: "AVAILABLE"},
        "authorization_by_step": {},
        "security_gate_by_step": {},
    })
    assert readiness["status"] == "READY"
    assert readiness["authority"] == "UNCHANGED"
    assert readiness["execution"] == "NONE"

    decision = controller.decide({
        "repository_head": head,
        "authorization": "NOT_REQUIRED",
        "security_gate": "NOT_APPLICABLE",
        "capabilities": {step["id"]: "AVAILABLE"},
        "tasks": [{
            "id": step["id"],
            "status": "PLANNED",
            "priority": 10,
            "objective": step["objective"],
            "scope": "repository",
        }],
    })
    assert decision["decision"] == "EXECUTION_CANDIDATE"
    assert decision["execution"] == "NONE"

    envelope = handoff.build_p17_handoff(decision, readiness)
    assert envelope["status"] == "READY_FOR_RUNTIME"
    assert envelope["execution"] == "NOT_STARTED"
    assert envelope["step_readiness"]["status"] == "READY"

    stale = readiness_mod.evaluate({
        "plan": plan,
        "step_id": step["id"],
        "compiled_repository_head": head,
        "current_repository_head": "repo-head-2",
        "completed_steps": [],
        "capabilities": {step["id"]: "AVAILABLE"},
        "authorization_by_step": {},
        "security_gate_by_step": {},
    })
    assert stale["status"] == "STOP"
    assert handoff.build_p17_handoff(decision, stale)["status"] == "BLOCKED"

    print("PASS: P15 -> P16 -> P17 -> controller -> runtime handoff reference path")


if __name__ == "__main__":
    main()
