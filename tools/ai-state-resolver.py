#!/usr/bin/env python3
"""Deterministically resolve evidence-backed DevOS state claims without writing or executing."""
from __future__ import annotations

import argparse
import fnmatch
import json
from collections import Counter
from pathlib import Path
from typing import Any

PROTOCOL = "DEVOS-AI-STATE-RESOLUTION-v2"
CONFIDENCE = {"observed": 2, "likely": 1, "unknown": 0}
BOUNDARY_EVENTS = {"RECOVERY_BOUNDARY", "HANDOFF_BOUNDARY"}
GROUNDING_TYPES = {"execution_evidence", "durable_state", "none"}


def _base() -> dict[str, Any]:
    return {"protocol": PROTOCOL, "authority": "UNCHANGED", "authorization": "UNCHANGED", "execution": "NONE", "mutation": "NONE"}


def _is_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _changed(patterns: list[str], paths: list[str]) -> bool:
    return any(fnmatch.fnmatch(path, pattern) for pattern in patterns for path in paths)


def resolve(payload: dict[str, Any]) -> dict[str, Any]:
    raw_claims = payload.get("claims", [])
    events = {str(event.get("type", "")) for event in payload.get("events", []) if isinstance(event, dict)}
    changed_paths = [str(path) for path in payload.get("changed_paths", []) if _is_text(path)]
    out = _base()
    if not isinstance(raw_claims, list):
        out.update({"status": "BLOCKED", "reason": "CLAIMS_INVALID", "claims": [], "weakest_state_confidence": "unknown", "unresolved_claim_ids": []})
        return out

    ids = [str(c.get("id", "")).strip() for c in raw_claims if isinstance(c, dict)]
    duplicate_ids = {claim_id for claim_id, count in Counter(ids).items() if claim_id and count > 1}
    resolved: list[dict[str, Any]] = []

    for raw in raw_claims:
        item = dict(raw) if isinstance(raw, dict) else {}
        claim_id = str(item.get("id", "")).strip()
        statement = item.get("statement")
        confidence = str(item.get("state_confidence", "unknown")).lower()
        grounding = item.get("grounding") if isinstance(item.get("grounding"), dict) else {}
        grounding_type = str(grounding.get("type", "none"))
        grounding_ref = grounding.get("ref")
        revalidate_on = item.get("revalidate_on", ["RECOVERY_BOUNDARY", "HANDOFF_BOUNDARY"])
        if not isinstance(revalidate_on, list):
            revalidate_on = []
        rules = [str(rule) for rule in revalidate_on]
        reasons: list[str] = []

        if not claim_id or not _is_text(statement):
            confidence = "unknown"; reasons.append("CLAIM_ID_OR_STATEMENT_INVALID")
        if confidence not in CONFIDENCE:
            confidence = "unknown"; reasons.append("STATE_CONFIDENCE_INVALID")
        if grounding_type not in GROUNDING_TYPES:
            confidence = "unknown"; reasons.append("GROUNDING_TYPE_INVALID")
        if confidence == "observed" and (grounding_type == "none" or not _is_text(grounding_ref)):
            confidence = "unknown"; reasons.append("OBSERVED_CLAIM_GROUNDING_MISSING")
        if claim_id in duplicate_ids:
            confidence = "unknown"; reasons.append("DUPLICATE_CLAIM_ID")
        if grounding_type == "execution_evidence" and item.get("p12_freshness") not in {"current", "fresh"}:
            if confidence == "observed": confidence = "likely"
            reasons.append("P12_EXECUTION_EVIDENCE_NOT_CURRENT")
        if grounding_type == "durable_state" and confidence == "observed":
            if BOUNDARY_EVENTS.intersection(rules).intersection(events):
                confidence = "likely"; reasons.append("REVALIDATION_BOUNDARY_REACHED")
            elif _changed([rule for rule in rules if rule not in BOUNDARY_EVENTS], changed_paths):
                confidence = "likely"; reasons.append("REVALIDATION_PATH_CHANGED")

        resolved.append({
            "id": claim_id or None, "statement": statement if _is_text(statement) else None,
            "state_confidence": confidence,
            "grounding": {"type": grounding_type, "ref": grounding_ref if _is_text(grounding_ref) else None},
            "revalidated_at": item.get("revalidated_at"), "revalidate_on": rules,
            "reasons": reasons,
        })

    unresolved = sorted(str(item["id"]) for item in resolved if item["id"] and item["state_confidence"] == "unknown")
    weakest = min((item["state_confidence"] for item in resolved), key=lambda value: CONFIDENCE[value], default="unknown")
    out.update({
        "status": "NEEDS_EVIDENCE" if unresolved else "RESOLVED",
        "claims": resolved,
        "weakest_state_confidence": weakest,
        "unresolved_claim_ids": unresolved,
        "state_confidence_summary": {level: sum(1 for item in resolved if item["state_confidence"] == level) for level in CONFIDENCE},
    })
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Read-only DevOS AI state resolver")
    parser.add_argument("input", help="JSON file containing claims, optional events, and changed_paths")
    args = parser.parse_args()
    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    print(json.dumps(resolve(payload), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
