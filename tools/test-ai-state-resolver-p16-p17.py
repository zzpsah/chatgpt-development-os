#!/usr/bin/env python3
"""Prove resolver v2 state confidence propagates through P16 and P17 without authority changes."""
from __future__ import annotations

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
assert plan["state_resolution"]["weakest_state_confidence"] == "observed", plan

ready = p17.evaluate({
    "plan": plan, "step_id": "S1", "compiled_repository_head": "head", "current_repository_head": "head",
    "completed_steps": [], "capabilities": {"S1": "AVAILABLE", "S2": "AVAILABLE"},
    "authorization_by_step": {}, "security_gate_by_step": {},
})
assert ready["status"] == "READY", ready
assert ready["authority"] == "UNCHANGED" and ready["execution"] == "NONE", ready

unknown = resolver.resolve({"claims": [{
    "id": "C2", "statement": "test result", "state_confidence": "observed",
    "grounding": {"type": "none", "ref": None},
}]})
clarify = p16.compile_plan("FEATURE_CHANGE", "update docs", "DEVOS", [], [], unknown)
assert clarify["decision"] == "CLARIFY", clarify
assert "C2" in " ".join(clarify["ambiguity"]), clarify
print("PASS: resolver claim confidence propagates P16 -> P17 without creating authority")
