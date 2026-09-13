#!/usr/bin/env python3
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "tools" / "step-readiness-orchestrator.py"
spec = importlib.util.spec_from_file_location("step_readiness", MODULE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def base_plan():
    return {
        "protocol": "DEVOS-GOAL-PLAN-v1",
        "decision": "PLANNED",
        "steps": [
            {"id": "S1", "objective": "inspect repository", "depends_on": [], "impact": "READ_ONLY", "authorization_required": False, "verification": "fresh repository evidence"},
            {"id": "S2", "objective": "update code", "depends_on": ["S1"], "impact": "LOW_IMPACT_MUTATION", "authorization_required": False, "verification": "run tests"},
            {"id": "S3", "objective": "check security", "depends_on": ["S2"], "impact": "SECURITY_SENSITIVE", "authorization_required": True, "verification": "security checks"},
        ],
    }


def payload(step_id="S1"):
    return {
        "plan": base_plan(),
        "step_id": step_id,
        "compiled_repository_head": "abc",
        "current_repository_head": "abc",
        "completed_steps": [],
        "capabilities": {"S1": "AVAILABLE", "S2": "AVAILABLE", "S3": "AVAILABLE"},
        "authorization_by_step": {},
        "security_gate_by_step": {},
    }


def main():
    r = mod.evaluate(payload("S1"))
    assert r["status"] == "READY"
    assert r["execution"] == "NONE" and r["authority"] == "UNCHANGED"

    stale = payload("S1") | {"current_repository_head": "def"}
    assert mod.evaluate(stale)["status"] == "STOP"

    dep = payload("S2")
    assert mod.evaluate(dep)["status"] == "BLOCKED"
    dep["completed_steps"] = ["S1"]
    assert mod.evaluate(dep)["status"] == "READY"

    missing_cap = payload("S1")
    missing_cap["capabilities"] = {"S1": "MISSING"}
    assert mod.evaluate(missing_cap)["status"] == "BLOCKED"

    sec = payload("S3")
    sec["completed_steps"] = ["S1", "S2"]
    assert mod.evaluate(sec)["status"] == "NEEDS_APPROVAL"

    sec["authorization_by_step"] = {"S2": "ALREADY_GRANTED"}
    assert mod.evaluate(sec)["status"] == "NEEDS_APPROVAL", "approval for another step must not leak"

    sec["authorization_by_step"] = {"S3": "ALREADY_GRANTED"}
    assert mod.evaluate(sec)["status"] == "NEEDS_EVIDENCE"
    sec["security_gate_by_step"] = {"S3": "FAIL"}
    assert mod.evaluate(sec)["status"] == "BLOCKED"
    sec["security_gate_by_step"] = {"S3": "PASS"}
    assert mod.evaluate(sec)["status"] == "READY"

    no_verify = payload("S1")
    no_verify["plan"]["steps"][0]["verification"] = ""
    assert mod.evaluate(no_verify)["status"] == "NEEDS_EVIDENCE"

    bad = payload("S1")
    bad["plan"]["decision"] = "CLARIFY"
    assert mod.evaluate(bad)["status"] == "BLOCKED"

    missing_head = payload("S1") | {"compiled_repository_head": None}
    assert mod.evaluate(missing_head)["status"] == "NEEDS_EVIDENCE"

    print("PASS: P17 Step Readiness & Authorization Orchestrator regression corpus")


if __name__ == "__main__":
    main()
