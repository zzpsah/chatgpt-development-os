#!/usr/bin/env python3
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "tools" / "step-readiness-orchestrator.py"
spec = importlib.util.spec_from_file_location("step_readiness", MODULE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def step(sid, objective, deps, impact, auth, verification):
    return {"id": sid, "objective": objective, "depends_on": deps,
            "expected_evidence": ["fresh repository/runtime evidence"],
            "impact": impact, "authorization_required": auth,
            "verification": verification,
            "stop_or_escalate_if": "ambiguity, missing capability/authorization, failed verification, or repository conflict"}


def base_plan():
    return {"protocol": "DEVOS-GOAL-PLAN-v1", "project": "DEVOS",
            "objective": "inspect repository then update code then check security",
            "decision": "PLANNED", "authority": "UNCHANGED",
            "authorization": "UNCHANGED", "execution": "NONE",
            "constraints": [], "ambiguity": [],
            "steps": [
                step("S1", "inspect repository", [], "READ_ONLY", False, "fresh repository evidence"),
                step("S2", "update code", ["S1"], "LOW_IMPACT_MUTATION", False, "run tests"),
                step("S3", "check security", ["S2"], "SECURITY_SENSITIVE", True, "security checks"),
            ]}


def payload(step_id="S1"):
    return {"plan": base_plan(), "step_id": step_id,
            "compiled_repository_head": "abc", "current_repository_head": "abc",
            "completed_steps": [],
            "capabilities": {"S1": "AVAILABLE", "S2": "AVAILABLE", "S3": "AVAILABLE"},
            "authorization_by_step": {}, "security_gate_by_step": {}}


def main():
    r = mod.evaluate(payload("S1"))
    assert r["status"] == "READY" and all(r["gates"].values())
    assert r["execution"] == "NONE" and r["authority"] == "UNCHANGED"
    assert r["step"]["execution_evidence"] is False

    assert mod.evaluate(payload("S1") | {"current_repository_head": "def"})["status"] == "STOP"

    dep = payload("S2")
    assert mod.evaluate(dep)["status"] == "BLOCKED"
    dep["completed_steps"] = ["S1"]
    assert mod.evaluate(dep)["status"] == "READY"

    done = payload("S1"); done["completed_steps"] = ["S1"]
    assert "STEP_ALREADY_COMPLETE" in mod.evaluate(done)["reasons"]

    fake = payload("S2"); fake["completed_steps"] = ["S1", "NOT_A_PLAN_STEP"]
    assert any(x.startswith("COMPLETED_STEP_UNKNOWN=") for x in mod.evaluate(fake)["reasons"])

    impossible = payload("S1"); impossible["completed_steps"] = ["S2"]
    assert any(x.startswith("COMPLETED_STEP_DEPENDENCY_INCOMPLETE=") for x in mod.evaluate(impossible)["reasons"])

    missing_cap = payload("S1"); missing_cap["capabilities"] = {"S1": "MISSING"}
    assert mod.evaluate(missing_cap)["status"] == "BLOCKED"

    invalid_maps = payload("S1"); invalid_maps["authorization_by_step"] = []
    assert mod.evaluate(invalid_maps)["status"] == "BLOCKED"

    sec = payload("S3"); sec["completed_steps"] = ["S1", "S2"]
    assert mod.evaluate(sec)["status"] == "NEEDS_APPROVAL"
    sec["authorization_by_step"] = {"S2": "ALREADY_GRANTED"}
    assert mod.evaluate(sec)["status"] == "NEEDS_APPROVAL"
    sec["authorization_by_step"] = {"S3": "ALREADY_GRANTED"}
    assert mod.evaluate(sec)["status"] == "NEEDS_EVIDENCE"
    sec["security_gate_by_step"] = {"S3": "FAIL"}
    assert mod.evaluate(sec)["status"] == "BLOCKED"
    sec["security_gate_by_step"] = {"S3": "PASS"}
    assert mod.evaluate(sec)["status"] == "READY"

    no_verify = payload("S1"); no_verify["plan"]["steps"][0]["verification"] = ""
    assert mod.evaluate(no_verify)["status"] == "BLOCKED"
    no_evidence = payload("S1"); no_evidence["plan"]["steps"][0]["expected_evidence"] = []
    assert mod.evaluate(no_evidence)["status"] == "BLOCKED"
    no_stop = payload("S1"); no_stop["plan"]["steps"][0]["stop_or_escalate_if"] = ""
    assert mod.evaluate(no_stop)["status"] == "BLOCKED"

    bad = payload("S1"); bad["plan"]["decision"] = "CLARIFY"
    assert mod.evaluate(bad)["status"] == "BLOCKED"
    auth_changed = payload("S1"); auth_changed["plan"]["authority"] = "GRANTED"
    assert mod.evaluate(auth_changed)["status"] == "BLOCKED"
    exec_claim = payload("S1"); exec_claim["plan"]["execution"] = "DONE"
    assert mod.evaluate(exec_claim)["status"] == "BLOCKED"
    ambiguous = payload("S1"); ambiguous["plan"]["ambiguity"] = ["which repository?"]
    assert mod.evaluate(ambiguous)["status"] == "BLOCKED"
    assert mod.evaluate(payload("S1") | {"compiled_repository_head": None})["status"] == "NEEDS_EVIDENCE"

    duplicate = payload("S1"); duplicate["plan"]["steps"].append(step("S1", "duplicate", [], "READ_ONLY", False, "evidence"))
    assert "PLAN_STEP_ID_DUPLICATE=S1" in mod.evaluate(duplicate)["reasons"]
    unknown = payload("S2"); unknown["plan"]["steps"][1]["depends_on"] = ["S404"]
    assert "PLAN_DEPENDENCY_UNKNOWN=S2:S404" in mod.evaluate(unknown)["reasons"]
    cycle = payload("S1"); cycle["plan"]["steps"][0]["depends_on"] = ["S3"]
    assert mod.evaluate(cycle)["status"] == "BLOCKED"
    no_obj = payload("S1"); no_obj["plan"]["steps"][0]["objective"] = ""
    assert "PLAN_STEP_OBJECTIVE_MISSING=S1" in mod.evaluate(no_obj)["reasons"]
    inconsistent = payload("S3"); inconsistent["plan"]["steps"][2]["authorization_required"] = False
    assert mod.evaluate(inconsistent)["status"] == "BLOCKED"

    # A compiled envelope cannot downgrade the P16 semantic impact after planning.
    # This closes the adversarial path where destructive/security-sensitive text is
    # relabelled LOW_IMPACT_MUTATION to avoid exact authorization/Security Gate.
    downgraded = payload("S1")
    downgraded["plan"]["steps"][0]["objective"] = "delete production database"
    downgraded["plan"]["steps"][0]["impact"] = "LOW_IMPACT_MUTATION"
    downgraded["plan"]["steps"][0]["authorization_required"] = False
    downgraded_result = mod.evaluate(downgraded)
    assert downgraded_result["status"] == "BLOCKED"
    assert any(x.startswith("PLAN_STEP_IMPACT_MISMATCH=S1:") for x in downgraded_result["reasons"])

    downgraded_security = payload("S1")
    downgraded_security["plan"]["steps"][0]["objective"] = "change authorization policy"
    downgraded_security["plan"]["steps"][0]["impact"] = "LOW_IMPACT_MUTATION"
    downgraded_security["plan"]["steps"][0]["authorization_required"] = False
    downgraded_security_result = mod.evaluate(downgraded_security)
    assert downgraded_security_result["status"] == "BLOCKED"
    assert any(x.startswith("PLAN_STEP_IMPACT_MISMATCH=S1:") for x in downgraded_security_result["reasons"])

    constraint = payload("S2"); constraint["plan"]["constraints"] = ["DO_NOT_DEPLOY"]
    constraint["plan"]["steps"][1]["objective"] = "deploy production"
    constraint["plan"]["steps"][1]["impact"] = "PRODUCTION_OR_DESTRUCTIVE"
    constraint["plan"]["steps"][1]["authorization_required"] = True
    assert mod.evaluate(constraint)["status"] == "BLOCKED"

    print("PASS: P17 Step Readiness & Authorization Orchestrator regression corpus")


if __name__ == "__main__":
    main()
