#!/usr/bin/env python3
"""Deterministic Human Language Execution Engine v2 pre-interpreter.

This layer resolves common short/elliptical Hinglish/English phrases from explicit
conversation/project context. It never grants authority or executes actions.
"""
from __future__ import annotations

import argparse
import json
import re
import unicodedata
from typing import Any

INTENT_PATTERNS = {
    "RESUME_WORK": [r"\bcontinue\b", r"\bresume\b", r"\bcarry on\b", r"\bproceed\b", r"\baage\b", r"\bchalu\b", r"जारी\s+रखो", r"आगे\s+बढ़ो"],
    "BUG_FIX": [r"\bfix\b", r"\bbug\b", r"\berror\b", r"\bbroken\b", r"\bthik\b", r"\bsahi\b", r"ठीक\s+करो", r"समस्या", r"गलती"],
    "FEATURE_CHANGE": [r"\badd\b", r"\bbuild\b", r"\bimplement\b", r"\bchange\b", r"\bupdate\b", r"\bbana\b", r"\bkro\b", r"\bkaro\b", r"बनाओ", r"जोड़ो", r"अपडेट", r"डिप्लॉय", r"तैनात"],
    "VALIDATION": [r"\bcheck\b", r"\btest\b", r"\bverify\b", r"\bvalidate\b", r"जांचो", r"जाँचो", r"परीक्षण"],
    "SECURITY_REVIEW": [r"\bsecurity\b", r"\bauth\b", r"\bpermission\b", r"सुरक्षा", r"अनुमति"],
    "INVESTIGATE": [r"\bwhy\b", r"\bkyu\b", r"\bproblem\b", r"\binvestigate\b", r"\bdiagnos"],
    "QUALITY_IMPROVEMENT": [r"\bbetter\b", r"\bimprove\b", r"\bprofessional\b", r"\bach[ha]+\b", r"\bacha\b"],
    "EXPLAIN_CHANGE": [r"\bexplain\b", r"\bkya kiya\b", r"\bwhat did\b"],
}

NEGATIVE = [r"\bdon'?t\b", r"\bdo not\b", r"\bmat\b", r"\bnahi\b", r"\bwithout\b", r"मत", r"नहीं", r"बिना"]
DEICTIC = [r"\bthis\b", r"\bthat\b", r"\bit\b", r"\bye\b", r"\bwo\b", r"\bwahi\b", r"\bsame\b", r"\bpehle wala\b", r"यह", r"ये", r"वो", r"वही", r"पहले\s+वाला", r"पिछला\s+काम"]
HIGH_IMPACT_TERMS = {
    "DELETE": ("delete", "डिलीट", "हटाओ", "मिटाओ"),
    "DEPLOY": ("deploy", "deployment", "डिप्लॉय", "तैनात"),
    "PRODUCTION": ("production", "प्रोडक्शन"),
    "MERGE": ("merge", "मर्ज"),
    "DATABASE": ("database", "डेटाबेस"),
    "MIGRATION": ("migration", "माइग्रेशन"),
    "SECRET": ("secret", "गुप्त"),
    "PERMISSION": ("permission", "अनुमति"),
    "SECURITY": ("security", "सुरक्षा"),
}


def norm(text: str) -> str:
    text = text.casefold().strip()
    text = "".join(
        char if (char.isalnum() or char.isspace() or char in "_-" or unicodedata.category(char).startswith("M")) else " "
        for char in text
    )
    return re.sub(r"\s+", " ", text)


def matches(text: str, patterns: list[str]) -> bool:
    return any(re.search(p, text) for p in patterns)


def interpret(payload: dict[str, Any]) -> dict[str, Any]:
    phrase = str(payload.get("phrase", "")).strip()
    text = norm(phrase)
    context = payload.get("context") or {}
    previous = context.get("previous_intent")
    active_objective = context.get("active_objective")
    project = context.get("project")

    intents = [name for name, pats in INTENT_PATTERNS.items() if matches(text, pats)]
    contextual = False
    ambiguity: list[str] = []

    short = len(text.split()) <= 4
    referential = matches(text, DEICTIC)
    generic_action = text in {"continue", "continue it", "do it", "kr do", "kar do", "kro", "karo", "wahi", "same", "proceed", "aage", "जारी रखो", "आगे बढ़ो", "कर दो", "करो", "वही"}

    if (generic_action or referential or (short and not intents)) and previous:
        if "RESUME_WORK" not in intents and generic_action:
            intents.insert(0, "RESUME_WORK")
        if previous not in intents:
            intents.append(previous)
        contextual = True
    elif generic_action and active_objective:
        intents = intents or ["RESUME_WORK"]
        contextual = True

    matched_high_impact = [
        canonical for canonical, terms in HIGH_IMPACT_TERMS.items()
        if any(term in text for term in terms)
    ]
    constraints = []
    if matches(text, NEGATIVE):
        constraints.extend(f"DO_NOT_{canonical}" for canonical in matched_high_impact)

    high_impact_requested = bool(matched_high_impact) and not constraints
    if not project:
        ambiguity.append("PROJECT_UNKNOWN")
    if not intents:
        ambiguity.append("INTENT_UNKNOWN")
    if (referential or generic_action) and not (previous or active_objective):
        ambiguity.append("REFERENT_UNKNOWN")
    if high_impact_requested:
        ambiguity.append("HIGH_IMPACT_REQUIRES_AUTHORIZATION_CHECK")

    material_ambiguity = any(x in ambiguity for x in {"PROJECT_UNKNOWN", "INTENT_UNKNOWN", "REFERENT_UNKNOWN"})
    confidence = "LOW" if material_ambiguity else ("MEDIUM" if contextual or high_impact_requested else "HIGH")
    decision = "CLARIFY" if material_ambiguity else "INTERPRETED"

    # A fresh, explicit, non-referential request carries its own objective.
    # Context remains authoritative for elliptical continuation/referential requests.
    objective = active_objective
    if decision == "INTERPRETED" and phrase and not generic_action and not referential:
        objective = phrase

    return {
        "protocol": "DEVOS-HUMAN-LANGUAGE-v2",
        "phrase": phrase,
        "normalized": text,
        "intents": intents,
        "project": project,
        "objective": objective,
        "constraints": constraints,
        "context_used": contextual,
        "confidence": confidence,
        "ambiguity": ambiguity,
        "decision": decision,
        "authorization": "UNCHANGED",
        "authority": "UNCHANGED",
        "execution": "NONE",
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--input", help="JSON payload; stdin when omitted")
    args = p.parse_args()
    raw = args.input if args.input is not None else __import__("sys").stdin.read()
    print(json.dumps(interpret(json.loads(raw)), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
