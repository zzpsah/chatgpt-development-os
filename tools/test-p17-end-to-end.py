#!/usr/bin/env python3
import copy
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
    assert plan["execution"] == "NONE"
    step = plan["steps"][0]

    readiness_payload = {
        "plan": plan,
        "step_id": step["id"],
        "compiled_repository_head": head,
        "current_repository_head": head,
        "completed_steps": [],
        "capabilities": {step["id"]: "AVAILABLE"},
        "authorization_by_step": {},
        "security_gate_by_step": {},
    }
    readiness = readiness_mod.evaluate(readiness_payload)
    assert readiness["status"] == "READY"
    assert readiness["authority"] == "UNCHANGED"
    assert readiness["execution"] == "NONE"
    assert all(readiness["gates"].values())

    decision = controller.decide({
        "compiled_plan": plan,
        "repository_head": head,
        "scope": "repository",
        "completed_steps": [],
        "authorization": "NOT_REQUIRED",
        "security_gate": "NOT_APPLICABLE",
        "capabilities": {step["id"]: "AVAILABLE"},
    })
    assert decision["protocol_version"] == "P16-CONTROLLER-v1"
    assert decision["decision"] == "EXECUTION_CANDIDATE"
    assert decision["task_id"] == step["id"]
    assert decision["compiled_step"]["id"] == step["id"]
    assert decision["compiled_step"]["execution_evidence"] is False
    assert decision["execution"] == "NONE"

    envelope = handoff.build_p17_handoff(decision, readiness)
    assert envelope["status"] == "READY_FOR_RUNTIME"
    assert envelope["execution"] == "NOT_STARTED"
    assert envelope["step_readiness"]["status"] == "READY"
    assert envelope["step_readiness"]["step_id"] == step["id"]
    assert envelope["step_readiness"]["execution_evidence"] is False

    # A forged READY envelope for another step cannot ride a valid controller decision.
    forged_step = copy.deepcopy(readiness)
    forged_step["step_id"] = "S999"
    forged_step["step"]["id"] = "S999"
    forged = handoff.build_p17_handoff(decision, forged_step)
    assert forged["status"] == "BLOCKED"
    assert forged["reason"] == "readiness_controller_step_mismatch"

    # A READY envelope with a failed/forged gate cannot be handed to runtime.
    forged_gate = copy.deepcopy(readiness)
    forged_gate["gates"]["verification"] = False
    assert handoff.build_p17_handoff(decision, forged_gate)["status"] == "BLOCKED"

    # Legacy P12 controller decisions are intentionally insufficient for P17 handoff.
    legacy = controller.decide({
        "repository_head": head,
        "authorization": "NOT_REQUIRED",
        "security_gate": "NOT_APPLICABLE",
        "capabilities": {"legacy": "AVAILABLE"},
        "tasks": [{"id": "legacy", "status": "PLANNED", "priority": 1,
                   "objective": "inspect repository", "scope": "repository"}],
    })
    assert legacy["decision"] == "EXECUTION_CANDIDATE"
    assert legacy["protocol_version"] == "P12-CONTROLLER-v1"
    assert handoff.build_p17_handoff(legacy, readiness)["status"] == "BLOCKED"

    stale = readiness_mod.evaluate(readiness_payload | {
        "current_repository_head": "repo-head-2",
    })
    assert stale["status"] == "STOP"
    assert handoff.build_p17_handoff(decision, stale)["status"] == "BLOCKED"

    print("PASS: P15 -> P16 compiled plan -> P17 readiness -> controller -> runtime handoff")


if __name__ == "__main__":
    main()
