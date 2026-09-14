#!/usr/bin/env python3
"""Deterministically resolve evidence-backed DevOS state claims without writing or executing."""
from __future__ import annotations

import argparse
import fnmatch
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

PROTOCOL = "DEVOS-AI-STATE-RESOLUTION-v2"
CONFIDENCE = {"observed": 2, "likely": 1, "unknown": 0}
BOUNDARY_EVENTS = {"RECOVERY_BOUNDARY", "HANDOFF_BOUNDARY"}
GROUNDING_TYPES = {"execution_evidence", "durable_state", "none"}
_MISSING = object()


def _base() -> dict[str, Any]:
    return {"protocol": PROTOCOL, "authority": "UNCHANGED", "authorization": "UNCHANGED", "execution": "NONE", "mutation": "NONE"}


def _is_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _changed(patterns: list[str], paths: list[str]) -> bool:
    return any(fnmatch.fnmatch(path, pattern) for pattern in patterns for path in paths)


def _canonical_fact_value(value: Any) -> str:
    """Return a stable JSON representation for contradiction comparison."""
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def resolve(payload: dict[str, Any]) -> dict[str, Any]:
    raw_claims = payload.get("claims", [])
    events = {str(event.get("type", "")) for event in payload.get("events", []) if isinstance(event, dict)}
    changed_paths = [str(path) for path in payload.get("changed_paths", []) if _is_text(path)]
    out = _base()
    if not isinstance(raw_claims, list):
        out.update({"status": "BLOCKED", "reason": "CLAIMS_INVALID", "claims": [], "weakest_state_confidence": "unknown", "unresolved_claim_ids": [], "contradictions": []})
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

        raw_fact_key = item.get("fact_key", _MISSING)
        raw_fact_value = item.get("fact_value", _MISSING)
        has_fact_key = raw_fact_key is not _MISSING
        has_fact_value = raw_fact_value is not _MISSING
        fact_key = raw_fact_key.strip() if _is_text(raw_fact_key) else None
        fact_value = None if raw_fact_value is _MISSING else raw_fact_value

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
        if has_fact_key != has_fact_value or (has_fact_key and fact_key is None):
            confidence = "unknown"; reasons.append("FACT_IDENTITY_INCOMPLETE")
        if grounding_type == "execution_evidence" and item.get("p12_freshness") not in {"current", "fresh"}:
            if confidence == "observed":
                confidence = "likely"
            reasons.append("P12_EXECUTION_EVIDENCE_NOT_CURRENT")
        if grounding_type == "durable_state":
            # A durable record proves that the assertion was recorded, not that
            # its underlying implementation/result was freshly established.
            # Only current P12 execution evidence may retain `observed`.
            if confidence == "observed":
                confidence = "likely"; reasons.append("DURABLE_STATE_CANNOT_SELF_UPGRADE_TO_OBSERVED")
            # Revalidation markers describe why durable-state support needs a
            # fresh check; they apply to already-likely durable claims as well.
            if BOUNDARY_EVENTS.intersection(rules).intersection(events):
                reasons.append("REVALIDATION_BOUNDARY_REACHED")
            elif _changed([rule for rule in rules if rule not in BOUNDARY_EVENTS], changed_paths):
                reasons.append("REVALIDATION_PATH_CHANGED")

        resolved.append({
            "id": claim_id or None, "statement": statement if _is_text(statement) else None,
            "fact_key": fact_key, "fact_value": fact_value,
            "state_confidence": confidence,
            "grounding": {"type": grounding_type, "ref": grounding_ref if _is_text(grounding_ref) else None},
            "revalidated_at": item.get("revalidated_at"), "revalidate_on": rules,
            "reasons": reasons,
        })

    # Cross-claim contradiction policy is deliberately structured, not NLP-based.
    # Only claims that explicitly identify the same fact_key participate. Different
    # canonical fact_value values for that key make every involved claim unknown.
    fact_groups: dict[str, list[tuple[int, str]]] = defaultdict(list)
    for index, item in enumerate(resolved):
        if item["fact_key"] is not None and "FACT_IDENTITY_INCOMPLETE" not in item["reasons"]:
            fact_groups[item["fact_key"]].append((index, _canonical_fact_value(item["fact_value"])))

    contradictions: list[dict[str, Any]] = []
    for fact_key in sorted(fact_groups):
        members = fact_groups[fact_key]
        values = sorted({canonical for _, canonical in members})
        if len(values) <= 1:
            continue
        claim_ids: list[str] = []
        for index, _ in members:
            item = resolved[index]
            item["state_confidence"] = "unknown"
            if "CROSS_CLAIM_CONTRADICTION" not in item["reasons"]:
                item["reasons"].append("CROSS_CLAIM_CONTRADICTION")
            if item["id"]:
                claim_ids.append(str(item["id"]))
        contradictions.append({
            "fact_key": fact_key,
            "claim_ids": sorted(claim_ids),
            "canonical_values": values,
        })

    unresolved = sorted(str(item["id"]) for item in resolved if item["id"] and item["state_confidence"] == "unknown")
    has_unknown = any(item["state_confidence"] == "unknown" for item in resolved)
    weakest = min((item["state_confidence"] for item in resolved), key=lambda value: CONFIDENCE[value], default="unknown")
    out.update({
        "status": "NEEDS_EVIDENCE" if has_unknown else "RESOLVED",
        "claims": resolved,
        "contradictions": contradictions,
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
