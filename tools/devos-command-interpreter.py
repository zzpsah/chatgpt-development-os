#!/usr/bin/env python3
"""Deterministic Human Command Interpretation Layer v1 for DevOS.

Maps short/casual human messages to bounded canonical intents. This module
interprets language only; it never grants authorization or executes work.
"""
from __future__ import annotations

import argparse
import json
import re
from typing import Any

VERSION = "P12-COMMAND-INTERPRETER-v1"

_INTENT_RULES = [
    ("STOP_WORK", (r"\b(?:ruk|ruko|stop|pause|hold)\b", r"\bstop\s+(?:work|this)\b")),
    ("STATUS_QUERY", (r"\b(?:kya\s+pending|what(?:'s| is)\s+pending|pending\s+hai|status\s+(?:kya|check))\b",)),
    ("EXPLAIN_CHANGE", (r"\b(?:what\s+did\s+you\s+do|explain|samjha(?:o|de)|kya\s+kiya)\b",)),
    ("SECURITY_REVIEW", (r"\b(?:security|secure|safety)\b",)),
    ("BUG_FIX", (r"\b(?:fix|broken|bug|error|issue|problem)\b", r"\b(?:bakchodi|gand\s+faad)\s+(?:fix|khatm|solve)\b")),
    ("QUALITY_IMPROVEMENT", (r"\b(?:production\s+grade|production\s+ready|professional|make\s+it\s+better|better\s+bana|improve|harden)\b",)),
    ("FEATURE_CHANGE", (r"\b(?:add|build|implement|create|change|develop|bana(?:o|de)?)\b",)),
    ("RESUME_WORK", (r"\b(?:continue|continiue|resume|proceed|carry\s+on|pick\s+up|wahi\s+se\s+continue)\b",)),
]

_CONFIRM = re.compile(r"^(?:ok|okay|yes|haan|han|do\s+it|doit|kar\s+do|ye\s+bhi\s+kar\s+de|go\s+ahead|proceed)$", re.I)
_RESUME = re.compile(r"\b(?:continue|continiue|resume|proceed|wahi\s+se\s+continue|pick\s+up)\b", re.I)
_UNSAFE = re.compile(r"\b(?:bypass|disable|remove)\b.{0,30}\b(?:security|auth|authorization|gate|approval)\b|\bforce\s+(?:prod|production)\b", re.I)


def _clean(text: str) -> str:
    text = re.sub(r"\s+", " ", text.strip().lower())
    return text.strip(" .,!?:;\t\n")


def _intent_hits(text: str) -> list[str]:
    matches: list[tuple[int, int, str]] = []
    for priority, (intent, patterns) in enumerate(_INTENT_RULES):
        positions = [m.start() for pattern in patterns for m in re.finditer(pattern, text, re.I)]
        if positions:
            matches.append((min(positions), priority, intent))
    return [intent for _, _, intent in sorted(matches)]


def interpret(phrase: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
    if not isinstance(phrase, str) or not phrase.strip():
        raise ValueError("human phrase must be non-empty text")
    if context is not None and not isinstance(context, dict):
        raise ValueError("context must be an object")
    context = context or {}
    text = _clean(phrase)
    current_objective = context.get("current_objective")
    current_scope = context.get("current_scope")
    if _UNSAFE.search(text):
        return {
            "interpreter_version": VERSION,
            "status": "BLOCKED",
            "canonical_intents": ["AUTHORIZATION_ESCALATION"],
            "confidence": "HIGH",
            "user_phrase": phrase,
            "normalized_phrase": text,
            "scope": current_scope or "unknown",
            "authorization": "UNCHANGED",
            "action": "HOLD_FOR_AUTHORIZATION_REVIEW",
            "execution": "NONE",
        }

    if _CONFIRM.fullmatch(text):
        if current_objective:
            return {
                "interpreter_version": VERSION,
                "status": "INTERPRETED",
                "canonical_intents": ["CONFIRM_CURRENT_PLAN"],
                "confidence": "HIGH",
                "user_phrase": phrase,
                "normalized_phrase": text,
                "scope": current_scope or "current_objective",
                "authorization": "UNCHANGED",
                "action": "CONTINUE_CURRENT_BOUNDED_PLAN",
                "execution": "DELEGATE_AFTER_GATES",
            }
        return {
            "interpreter_version": VERSION,
            "status": "AMBIGUOUS",
            "canonical_intents": ["CONFIRM_CURRENT_PLAN"],
            "confidence": "LOW",
            "user_phrase": phrase,
            "normalized_phrase": text,
            "scope": "unknown",
            "authorization": "UNCHANGED",
            "action": "RECOVER_STATE_BEFORE_ACTION",
            "execution": "NONE",
        }

    hits = _intent_hits(text)
    if not hits and _RESUME.search(text):
        hits = ["RESUME_WORK"]
    if not hits:
        return {
            "interpreter_version": VERSION,
            "status": "AMBIGUOUS",
            "canonical_intents": [],
            "confidence": "LOW",
            "user_phrase": phrase,
            "normalized_phrase": text,
            "scope": current_scope or "unknown",
            "authorization": "UNCHANGED",
            "action": "HOLD_FOR_CLARIFICATION",
            "execution": "NONE",
        }

    ordered: list[str] = []
    for intent in hits:
        if intent not in ordered:
            ordered.append(intent)
    if "RESUME_WORK" in ordered and current_objective is None:
        confidence = "MEDIUM"
        action = "RECOVER_CURRENT_STATE_THEN_SELECT_NEXT_BOUNDED_WORK"
    elif ordered == ["STOP_WORK"]:
        confidence = "HIGH"
        action = "HOLD_AUTONOMOUS_CONTINUATION"
    elif "STATUS_QUERY" in ordered:
        confidence = "HIGH"
        action = "REPORT_REPOSITORY_AND_DURABLE_STATE"
    else:
        confidence = "HIGH"
        action = "ROUTE_TO_WORKFLOW_AFTER_GATES"

    return {
        "interpreter_version": VERSION,
        "status": "INTERPRETED",
        "canonical_intents": ordered,
        "confidence": confidence,
        "user_phrase": phrase,
        "normalized_phrase": text,
        "project_reference": context.get("project_reference", "current_repository"),
        "scope": (current_scope or "current_objective") if current_objective else (current_scope or "unknown"),
        "authorization": "UNCHANGED",
        "action": action,
        "execution": "NONE" if action.startswith(("HOLD", "REPORT", "RECOVER")) else "DELEGATE_AFTER_GATES",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Interpret casual DevOS commands without executing them")
    parser.add_argument("phrase")
    parser.add_argument("--context", default="{}")
    args = parser.parse_args()
    context = json.loads(args.context)
    print(json.dumps(interpret(args.phrase, context), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
