#!/usr/bin/env python3
"""Run the bounded multilingual P15 corpus through P16 and P17 without execution."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools" / filename)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


interpreter = load("p15_interpreter", "human-language-interpreter.py")
compiler = load("p16_compiler", "semantic-goal-to-plan.py")
readiness = load("p17_readiness", "step-readiness-orchestrator.py")
corpus = json.loads((ROOT / "config" / "p15-multilingual-corpus.json").read_text(encoding="utf-8"))

assert corpus["protocol"] == "DEVOS-P15-MULTILINGUAL-CORPUS-v1"
assert corpus["cases"]

for case in corpus["cases"]:
    interpreted = interpreter.interpret({"phrase": case["phrase"], "context": case["context"]})
    assert interpreted["decision"] == case["decision"], (case["id"], interpreted)
    assert interpreted["authority"] == "UNCHANGED"
    assert interpreted["authorization"] == "UNCHANGED"
    assert interpreted["execution"] == "NONE"
    for intent in case.get("intents", []):
        assert intent in interpreted["intents"], (case["id"], interpreted)
    if "ambiguity" in case:
        assert case["ambiguity"] in interpreted["ambiguity"], (case["id"], interpreted)

    plan = compiler.compile_plan(
        interpreted["intents"][0] if interpreted["intents"] else "INVESTIGATE",
        interpreted["objective"] or "",
        interpreted["project"],
        interpreted["constraints"],
        interpreted["ambiguity"],
    )
    if "p16_decision" in case:
        assert plan["decision"] == case["p16_decision"], (case["id"], plan)
        continue
    assert plan["decision"] == "PLANNED", (case["id"], plan)
    target = plan["steps"][-1]
    assert target["impact"] == case["p16_impact"], (case["id"], target)
    p17 = readiness.evaluate({
        "plan": plan,
        "step_id": target["id"],
        "compiled_repository_head": "p15-corpus-head",
        "current_repository_head": "p15-corpus-head",
        "completed_steps": [step["id"] for step in plan["steps"][:-1]],
        "capabilities": {step["id"]: "AVAILABLE" for step in plan["steps"]},
        "authorization_by_step": {},
        "security_gate_by_step": {},
    })
    assert p17["status"] == case["p17_status"], (case["id"], p17)
    assert p17["authority"] == "UNCHANGED"
    assert p17["authorization"] == "UNCHANGED"
    assert p17["execution"] == "NONE"

print("PASS: bounded P15 multilingual corpus preserves P16/P17 authorization and execution boundaries")
