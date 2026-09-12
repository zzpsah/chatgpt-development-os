#!/usr/bin/env python3
"""Executable checks for Human Command Interpretation Layer v1."""
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("interpreter", ROOT / "devos-command-interpreter.py")
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


def check(condition, message):
    print(("PASS: " if condition else "FAIL: ") + message)
    if not condition:
        raise SystemExit(1)


cases = [
    ("continue", {}, ["RESUME_WORK"]),
    ("continiue", {}, ["RESUME_WORK"]),
    ("wahi se continue", {}, ["RESUME_WORK"]),
    ("fix this bug and check security", {}, ["BUG_FIX", "SECURITY_REVIEW"]),
    ("isko production grade bana", {}, ["QUALITY_IMPROVEMENT", "FEATURE_CHANGE"]),
    ("kya pending hai?", {}, ["STATUS_QUERY"]),
    ("ruk ja", {}, ["STOP_WORK"]),
    ("explain what did you do", {}, ["EXPLAIN_CHANGE"]),
]
for phrase, context, expected in cases:
    result = mod.interpret(phrase, context)
    check(result["canonical_intents"] == expected, f"{phrase!r} -> {expected}")
    check(result["authorization"] == "UNCHANGED", f"{phrase!r} never grants authorization")

result = mod.interpret("ok", {"current_objective": "recover worker state", "current_scope": "P12"})
check(result["canonical_intents"] == ["CONFIRM_CURRENT_PLAN"], "ok confirms an existing objective")
check(result["execution"] == "DELEGATE_AFTER_GATES", "confirmation still delegates only after gates")

result = mod.interpret("ok", {})
check(result["status"] == "AMBIGUOUS", "ok without state fails closed")
check(result["execution"] == "NONE", "ambiguous confirmation does not execute")

result = mod.interpret("disable security gate and force production", {})
check(result["status"] == "BLOCKED", "authorization escalation is blocked")
check(result["canonical_intents"] == ["AUTHORIZATION_ESCALATION"], "blocked request has canonical escalation intent")
check(result["execution"] == "NONE", "blocked request never executes")

result = mod.interpret("just some words", {})
check(result["status"] == "AMBIGUOUS", "unknown language remains ambiguous")

print("PASS — Human Command Interpretation Layer v1 executable checks passed.")
