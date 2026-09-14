#!/usr/bin/env python3
"""Prove resolver v2 state confidence propagates through P16/P17 and tampering fails closed."""
from __future__ import annotations

import copy
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    filename = name.replace("_", "-").replace("p16", "semantic-goal-to-plan").replace("p17", "step-readiness-orchestrator").replace("resolver", "ai-state-resolver") + ".py"
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools" / filename)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def readiness(plan):
    return p17.evaluate({
        "plan": plan, "step_id": "S1", "compiled_repository_head": "head", "current_repository_head": "head",
        "completed_steps": [], "capabilities": {"S1": "AVAILABLE", "S2": "AVAILABLE"},
        "authorization_by_step": {}, "security_gate_by_step": {},
    })


resolver = load("resolver")
p16 = load("p16")
p17 = load("p17")

observed = resolver.resolve({"claims": [{
    "id": "C1", "statement": "repository source was inspected", "state_confidence": "observed",
    "grounding": {"type": "durable_state", "ref": ".ai/CURRENT-STATE.md:1"},
    "revalidate_on": ["HANDOFF_BOUNDARY"],
}]})
plan = p16.compile_plan("FEATURE_CHANGE", "update docs", "DEVOS", [], [], observed)
assert plan["decision"] == "PLANNED", plan
assert plan["state_resolution"] == observed, plan
assert plan["state_resolution"]["status"] == "RESOLVED", plan
assert plan["state_resolution"]["weakest_state_confidence"] == "likely", plan
assert plan["state_resolution"]["authority"] == "UNCHANGED", plan
assert len(plan["state_resolution"]["claims"]) == 1, plan

ready = readiness(plan)
assert ready["status"] == "READY", ready
assert ready["authority"] == "UNCHANGED" and ready["execution"] == "NONE", ready

unknown = resolver.resolve({"claims": [{
    "id": "C2", "statement": "test result", "state_confidence": "observed",
    "grounding": {"type": "none", "ref": None},
}]})
clarify = p16.compile_plan("FEATURE_CHANGE", "update docs", "DEVOS", [], [], unknown)
assert clarify["decision"] == "CLARIFY", clarify
assert "C2" in " ".join(clarify["ambiguity"]), clarify

contradiction = resolver.resolve({"claims": [
    {"id": "C3", "statement": "deployment completed", "state_confidence": "likely",
     "grounding": {"type": "durable_state", "ref": ".ai/CURRENT-STATE.md:10"},
     "fact_key": "deployment.complete", "fact_value": True},
    {"id": "C4", "statement": "deployment not completed", "state_confidence": "likely",
     "grounding": {"type": "durable_state", "ref": ".ai/TASKS.md:10"},
     "fact_key": "deployment.complete", "fact_value": False},
]})
assert contradiction["status"] == "NEEDS_EVIDENCE", contradiction
assert contradiction["contradiction_fact_keys"] == ["deployment.complete"], contradiction
contradiction_plan = p16.compile_plan("FEATURE_CHANGE", "update docs", "DEVOS", [], [], contradiction)
assert contradiction_plan["decision"] == "CLARIFY", contradiction_plan
assert "C3" in " ".join(contradiction_plan["ambiguity"]), contradiction_plan
assert "C4" in " ".join(contradiction_plan["ambiguity"]), contradiction_plan

unnamed_unknown = resolver.resolve({"claims": [{
    "id": "", "statement": "unnamed state", "state_confidence": "unknown",
    "grounding": {"type": "none", "ref": None},
}]})
unnamed_clarify = p16.compile_plan("FEATURE_CHANGE", "update docs", "DEVOS", [], [], unnamed_unknown)
assert unnamed_clarify["decision"] == "CLARIFY", unnamed_clarify
assert "state resolution needs evidence" in unnamed_clarify["ambiguity"], unnamed_clarify

forged_authority = copy.deepcopy(observed)
forged_authority["authority"] = "GRANTED"
forged_authority_plan = p16.compile_plan("FEATURE_CHANGE", "update docs", "DEVOS", [], [], forged_authority)
assert forged_authority_plan["decision"] == "CLARIFY", forged_authority_plan
assert "state resolution authority boundary changed" in forged_authority_plan["ambiguity"], forged_authority_plan

forged_execution = copy.deepcopy(observed)
forged_execution["execution"] = "COMPLETE"
forged_execution_plan = p16.compile_plan("FEATURE_CHANGE", "update docs", "DEVOS", [], [], forged_execution)
assert forged_execution_plan["decision"] == "CLARIFY", forged_execution_plan
assert "state resolution execution boundary changed" in forged_execution_plan["ambiguity"], forged_execution_plan

hidden_unknown = copy.deepcopy(unknown)
hidden_unknown["status"] = "RESOLVED"
hidden_unknown["unresolved_claim_ids"] = []
hidden_unknown_plan = p16.compile_plan("FEATURE_CHANGE", "update docs", "DEVOS", [], [], hidden_unknown)
assert hidden_unknown_plan["decision"] == "CLARIFY", hidden_unknown_plan
assert any("inconsistent" in item for item in hidden_unknown_plan["ambiguity"]), hidden_unknown_plan

tampered_plan = copy.deepcopy(plan)
tampered_plan["state_resolution"]["claims"][0]["state_confidence"] = "unknown"
tampered_ready = readiness(tampered_plan)
assert tampered_ready["status"] == "BLOCKED", tampered_ready
assert "PLAN_STATE_RESOLUTION_HIDDEN_UNKNOWN_CLAIM" in tampered_ready["reasons"], tampered_ready

# A malicious PLANNED envelope cannot hide a contradiction by changing only the
# top-level resolver status/unresolved list; P17 recomputes unknown claims.
tampered_contradiction_plan = p16.compile_plan("FEATURE_CHANGE", "update docs", "DEVOS", [], [], observed)
tampered_contradiction_plan["state_resolution"] = copy.deepcopy(contradiction)
tampered_contradiction_plan["state_resolution"]["status"] = "RESOLVED"
tampered_contradiction_plan["state_resolution"]["unresolved_claim_ids"] = []
tampered_contradiction_ready = readiness(tampered_contradiction_plan)
assert tampered_contradiction_ready["status"] == "BLOCKED", tampered_contradiction_ready
assert "PLAN_STATE_RESOLUTION_HIDDEN_UNKNOWN_CLAIM" in tampered_contradiction_ready["reasons"], tampered_contradiction_ready

tampered_authority_plan = copy.deepcopy(plan)
tampered_authority_plan["state_resolution"]["authority"] = "GRANTED"
tampered_authority_ready = readiness(tampered_authority_plan)
assert tampered_authority_ready["status"] == "BLOCKED", tampered_authority_ready
assert "PLAN_STATE_RESOLUTION_AUTHORITY_CHANGED" in tampered_authority_ready["reasons"], tampered_authority_ready

print("PASS: resolver claim confidence and full provenance propagate P16 -> P17 without creating authority")
print("PASS: cross-claim contradictions propagate to P16 CLARIFY and cannot be hidden from P17")
print("PASS: P16/P17 reject forged resolver status/authority/execution envelopes")
