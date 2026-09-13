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

# Devanagari Hindi must remain structured input, not be erased during normalization.
hindi_check = check("रिपॉजिटरी जांचो", {"project": "DEVOS"}, intents=("VALIDATION",))
assert hindi_check["normalized"] == "रिपॉजिटरी जांचो", hindi_check
assert hindi_check["objective"] == "रिपॉजिटरी जांचो", hindi_check
check("पहले वाला ठीक करो", ctx, intents=("BUG_FIX", "FEATURE_CHANGE"))
check("पिछला काम जारी रखो", ctx, intents=("RESUME_WORK", "FEATURE_CHANGE"))
hindi_hold = check("प्रोडक्शन में तैनात करो", ctx, intents=("FEATURE_CHANGE",))
assert "HIGH_IMPACT_REQUIRES_AUTHORIZATION_CHECK" in hindi_hold["ambiguity"], hindi_hold
hindi_constraint = check("स्टेजिंग पर डिप्लॉय मत करना", ctx, intents=("FEATURE_CHANGE",), constraints=("DO_NOT_DEPLOY",))
assert "HIGH_IMPACT_REQUIRES_AUTHORIZATION_CHECK" not in hindi_constraint["ambiguity"], hindi_constraint
check("सुरक्षा जांचो", {"project": "DEVOS"}, intents=("SECURITY_REVIEW", "VALIDATION"))

fresh = check("check repository", {"project": "DEVOS"}, intents=("VALIDATION",))
assert fresh["objective"] == "check repository", fresh
assert fresh["context_used"] is False, fresh

continued = check("continue", ctx, intents=("RESUME_WORK", "FEATURE_CHANGE"))
assert continued["objective"] == ctx["active_objective"], continued

print("human-language-interpreter v2 multilingual regression corpus: PASS")
