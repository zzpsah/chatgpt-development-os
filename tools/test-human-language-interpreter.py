#!/usr/bin/env python3
from __future__ import annotations
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("hli", ROOT / "tools" / "human-language-interpreter.py")
assert spec and spec.loader
hli = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hli)


def check(phrase, context, *, decision="INTERPRETED", intents=(), constraints=()):
    out = hli.interpret({"phrase": phrase, "context": context})
    assert out["decision"] == decision, out
    for intent in intents:
        assert intent in out["intents"], out
    for constraint in constraints:
        assert constraint in out["constraints"], out
    assert out["authority"] == "UNCHANGED"
    assert out["authorization"] == "UNCHANGED"
    assert out["execution"] == "NONE"
    return out


ctx = {"project": "DEVOS", "previous_intent": "FEATURE_CHANGE", "active_objective": "Improve human language interpretation"}
check("Continue", ctx, intents=("RESUME_WORK", "FEATURE_CHANGE"))
check("kr do", ctx, intents=("RESUME_WORK", "FEATURE_CHANGE"))
check("wahi continue", ctx, intents=("RESUME_WORK", "FEATURE_CHANGE"))
check("jo error tha fix", ctx, intents=("BUG_FIX",))
check("isko aur better kro", ctx, intents=("QUALITY_IMPROVEMENT", "FEATURE_CHANGE"))
check("pehle wala hi but deploy mat karna", ctx, constraints=("DO_NOT_DEPLOY",))
check("check security", ctx, intents=("VALIDATION", "SECURITY_REVIEW"))
check("continue", {}, decision="CLARIFY")
high = check("deploy it", ctx)
assert "HIGH_IMPACT_REQUIRES_AUTHORIZATION_CHECK" in high["ambiguity"]
print("human-language-interpreter v2 tests: PASS")
