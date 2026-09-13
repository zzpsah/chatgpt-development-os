#!/usr/bin/env python3
"""Deterministic Human Language Execution Engine v2 reference interpreter.

This layer resolves short/elliptical human requests against explicit supplied context.
It never grants authorization and never executes technical actions.
"""
from __future__ import annotations

import argparse
import json
import re
from typing import Any

INTENT_PATTERNS = [
    ("SECURITY_REVIEW", ("security", "secure", "auth check", "security dekh")),
    ("BUG_FIX", ("fix", "bug", "broken", "error", "issue", "nahi chal", "not working", "thik kro", "theek karo")),
    ("VALIDATION", ("check", "test", "verify", "sahi hai", "correct")),
    ("INVESTIGATE", ("why", "kyu", "kyon", "kya problem", "investigate", "diagnose")),
    ("QUALITY_IMPROVEMENT", ("improve", "better", "acha kro", "accha karo", "professional", "enhance")),
    ("RESUME_WORK", ("continue", "resume", "carry on", "aage", "age badho", "wahi continue")),
    ("FEATURE_CHANGE", ("add", "build", "create", "implement", "change", "update", "bana", "kro", "kar do")),
]

NEGATIVE_PATTERNS = {
    "NO_DEPLOY": ("deploy mat", "don't deploy", "do not deploy", "no deploy", "production mat"),
    "NO_DELETE": ("delete mat", "don't delete", "do not delete"),
    "NO_MERGE": ("merge mat", "don't merge", "do not merge"),
}

REFERENTIAL = ("ye", "yahi", "wo", "woh", "wahi", "same", "usko", "isko", "pehle wala", "pichla")
SHORT_CONTINUATIONS = {"continue", "continue kro", "continue karo", "kr do", "kar do", "kro", "do it", "yes do it", "ok do it", "aage"}


def norm(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s_-]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def detect_intents(text: str) -> list[str]:
    found: list[str] = []
    for intent, patterns in INTENT_PATTERNS:
        if any(pattern in text for pattern in patterns):
            found.append(intent)
    # A generic action word should not dilute a more specific intent.
    if len(found) > 1 and "FEATURE_CHANGE" in found:
        found.remove("FEATURE_CHANGE")
    return found


def interpret(payload: dict[str, Any]) -> dict[str, Any]:
    raw = str(payload.get("utterance") or "").strip()
    text = norm(raw)
    context = payload.get("context") if isinstance(payload.get("context"), dict) else {}
    prior_intent = str(context.get("last_intent") or "").upper() or None
    prior_objective = str(context.get("last_objective") or "").strip() or None
    project = str(context.get("project") or "").strip() or None

    constraints = [name for name, pats in NEGATIVE_PATTERNS.items() if any(p in text for p in pats)]
    intents = detect_intents(text)
    referential = any(re.search(rf"\b{re.escape(token)}\b", text) for token in REFERENTIAL)
    continuation = text in SHORT_CONTINUATIONS or text.startswith("continue") or text.startswith("resume")
    inherited = False

    if (continuation or referential) and prior_intent:
        if not intents or intents == ["RESUME_WORK"] or (len(text.split()) <= 4 and "FEATURE_CHANGE" in intents):
            intents = [prior_intent]
            inherited = True

    if not intents and prior_intent and len(text.split()) <= 4:
        # Very short command: inherit only when an explicit prior objective exists.
        if prior_objective:
            intents = [prior_intent]
            inherited = True

    ambiguity: list[str] = []
    if not raw:
        ambiguity.append("EMPTY_UTTERANCE")
    if (referential or continuation) and not prior_objective:
        ambiguity.append("MISSING_REFERENT")
    if not intents:
        ambiguity.append("INTENT_UNRESOLVED")
    if len(intents) > 1:
        ambiguity.append("MULTIPLE_INTENTS")

    if not ambiguity:
        confidence = "HIGH" if (not inherited or (prior_objective and prior_intent)) else "MEDIUM"
    elif intents and ambiguity == ["MULTIPLE_INTENTS"]:
        confidence = "MEDIUM"
    else:
        confidence = "LOW"

    # Clarify only when ambiguity can materially alter what would be done.
    action = "CLARIFY" if confidence == "LOW" else "ROUTE"
    objective = prior_objective if inherited else (raw or None)

    return {
        "protocol": "DEVOS-HUMAN-LANGUAGE-v2",
        "utterance": raw,
        "normalized": text,
        "intents": intents,
        "primary_intent": intents[0] if intents else None,
        "objective": objective,
        "project": project,
        "context_inherited": inherited,
        "constraints": constraints,
        "confidence": confidence,
        "ambiguity": ambiguity,
        "decision": action,
        "authorization": "UNCHANGED",
        "execution": "NONE",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--payload", required=True, help="JSON with utterance and optional context")
    args = parser.parse_args()
    print(json.dumps(interpret(json.loads(args.payload)), ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
