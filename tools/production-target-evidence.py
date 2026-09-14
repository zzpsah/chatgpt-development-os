#!/usr/bin/env python3
"""Validate target-bound external production evidence without creating authority.

This tool is deliberately read-only. It validates one evidence packet covering the
five external criteria currently blocking Production Readiness Evidence v2. Even a
fully valid PASS packet remains candidate evidence: semantic review and a separate
durable readiness reconciliation are required before any readiness criterion changes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

PROTOCOL = "DEVOS-PRODUCTION-TARGET-EVIDENCE-v1"
VERDICT_PROTOCOL = "DEVOS-PRODUCTION-TARGET-EVIDENCE-VERDICT-v1"
SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
REQUIRED_CRITERIA = {
    "runtime_direct_conformance",
    "recovery_disaster",
    "operational_observability",
    "deployment_target",
    "high_impact_governance",
}
BOUNDARIES = {
    "authority": "UNCHANGED",
    "authorization": "UNCHANGED",
    "execution": "NONE",
    "mutation": "NONE",
    "publication_authorized": False,
    "deployment_authorized": False,
    "production_ready": False,
}


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()


def _timestamp(value: Any) -> bool:
    if not _text(value):
        return False
    text = str(value).strip()
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None


def _base(status: str, reasons: list[str]) -> dict[str, Any]:
    return {
        "protocol": VERDICT_PROTOCOL,
        "status": status,
        "reasons": sorted(set(reasons)),
        "readiness_promotion_allowed": False,
        "semantic_review_required": True,
        **BOUNDARIES,
    }


def evaluate(
    payload: Any,
    *,
    expected_source_sha: str | None = None,
    expected_target_id: str | None = None,
) -> dict[str, Any]:
    reasons: list[str] = []
    if not isinstance(payload, dict):
        return _base("BLOCKED", ["PACKET_NOT_OBJECT"])

    expected_fields = {
        "protocol", "repository", "source_sha", "target", "observed_at", "observer",
        "criteria", "limitations", *BOUNDARIES,
    }
    if set(payload) != expected_fields:
        reasons.append("PACKET_FIELDS_INVALID")
    if payload.get("protocol") != PROTOCOL:
        reasons.append("PROTOCOL_INVALID")
    if not _text(payload.get("repository")):
        reasons.append("REPOSITORY_INVALID")

    source_sha = payload.get("source_sha")
    if not isinstance(source_sha, str) or not SHA40.fullmatch(source_sha):
        reasons.append("SOURCE_SHA_INVALID")
    if expected_source_sha is not None:
        if not SHA40.fullmatch(expected_source_sha):
            reasons.append("EXPECTED_SOURCE_SHA_INVALID")
        elif source_sha != expected_source_sha:
            reasons.append("SOURCE_SHA_MISMATCH")

    if not _timestamp(payload.get("observed_at")):
        reasons.append("OBSERVED_AT_INVALID")

    for key, expected in BOUNDARIES.items():
        if type(payload.get(key)) is not type(expected) or payload.get(key) != expected:
            reasons.append("BOUNDARY_CHANGED=" + key)

    target = payload.get("target")
    target_id: str | None = None
    if not isinstance(target, dict) or set(target) != {"id", "environment", "kind", "ref"}:
        reasons.append("TARGET_INVALID")
    else:
        if any(not _text(target.get(key)) for key in ("id", "environment", "kind", "ref")):
            reasons.append("TARGET_INVALID")
        else:
            target_id = str(target["id"]).strip()
            if target.get("environment") != "production":
                reasons.append("TARGET_ENVIRONMENT_NOT_PRODUCTION")
            if expected_target_id is not None and target_id != expected_target_id:
                reasons.append("TARGET_ID_MISMATCH")

    observer = payload.get("observer")
    if not isinstance(observer, dict) or set(observer) != {"kind", "ref"}:
        reasons.append("OBSERVER_INVALID")
    elif any(not _text(observer.get(key)) for key in ("kind", "ref")):
        reasons.append("OBSERVER_INVALID")

    limitations = payload.get("limitations")
    if not isinstance(limitations, list) or not limitations or any(not _text(item) for item in limitations):
        reasons.append("LIMITATIONS_INVALID")

    criteria = payload.get("criteria")
    normalized: list[dict[str, Any]] = []
    seen: set[str] = set()
    unresolved: list[str] = []
    if not isinstance(criteria, list):
        reasons.append("CRITERIA_INVALID")
    else:
        for index, item in enumerate(criteria):
            if not isinstance(item, dict) or set(item) != {"id", "status", "evidence", "limitations"}:
                reasons.append(f"CRITERION_INVALID={index}")
                continue
            criterion_id = item.get("id")
            if criterion_id not in REQUIRED_CRITERIA:
                reasons.append(f"CRITERION_UNKNOWN={criterion_id}")
                continue
            if criterion_id in seen:
                reasons.append(f"CRITERION_DUPLICATE={criterion_id}")
                continue
            seen.add(criterion_id)

            status = item.get("status")
            if status not in {"PASS", "FAIL", "UNOBSERVED"}:
                reasons.append(f"CRITERION_STATUS_INVALID={criterion_id}")
                continue

            item_limitations = item.get("limitations")
            if not isinstance(item_limitations, list) or not item_limitations or any(not _text(v) for v in item_limitations):
                reasons.append(f"CRITERION_LIMITATIONS_INVALID={criterion_id}")

            evidence = item.get("evidence")
            if not isinstance(evidence, list):
                reasons.append(f"CRITERION_EVIDENCE_INVALID={criterion_id}")
                evidence = []
            if status == "UNOBSERVED" and evidence:
                reasons.append(f"UNOBSERVED_WITH_EVIDENCE={criterion_id}")
            if status in {"PASS", "FAIL"} and not evidence:
                reasons.append(f"OBSERVED_WITHOUT_EVIDENCE={criterion_id}")

            normalized_evidence: list[dict[str, str]] = []
            for ev_index, ev in enumerate(evidence):
                if not isinstance(ev, dict) or set(ev) != {"ref", "digest", "observed_scope"}:
                    reasons.append(f"EVIDENCE_ITEM_INVALID={criterion_id}:{ev_index}")
                    continue
                if not _text(ev.get("ref")) or not _text(ev.get("observed_scope")):
                    reasons.append(f"EVIDENCE_REFERENCE_INVALID={criterion_id}:{ev_index}")
                digest = ev.get("digest")
                if not isinstance(digest, str) or not SHA256.fullmatch(digest):
                    reasons.append(f"EVIDENCE_DIGEST_INVALID={criterion_id}:{ev_index}")
                normalized_evidence.append({
                    "ref": str(ev.get("ref", "")).strip(),
                    "digest": str(ev.get("digest", "")),
                    "observed_scope": str(ev.get("observed_scope", "")).strip(),
                })

            if status != "PASS":
                unresolved.append(str(criterion_id))
            normalized.append({
                "id": str(criterion_id),
                "status": status,
                "evidence": sorted(normalized_evidence, key=lambda row: (row["ref"], row["digest"], row["observed_scope"])),
                "limitations": sorted(str(v).strip() for v in item_limitations) if isinstance(item_limitations, list) else [],
            })

        missing = sorted(REQUIRED_CRITERIA - seen)
        if missing:
            reasons.append("CRITERIA_MISSING=" + ",".join(missing))

    if reasons:
        return _base("BLOCKED", reasons) | {
            "target_id": target_id,
            "packet_digest": None,
            "candidate_criteria": [],
            "production_blockers": sorted(REQUIRED_CRITERIA),
        }

    normalized.sort(key=lambda row: row["id"])
    packet_digest = _digest(payload)
    passed = sorted(item["id"] for item in normalized if item["status"] == "PASS")
    blockers = sorted(unresolved)
    if blockers:
        return _base("HOLD", ["TARGET_EVIDENCE_INCOMPLETE"]) | {
            "target_id": target_id,
            "packet_digest": packet_digest,
            "candidate_criteria": passed,
            "production_blockers": blockers,
        }

    return _base("CANDIDATE_COMPLETE", [
        "ALL_EXTERNAL_CRITERIA_HAVE_TARGET_BOUND_PASS_EVIDENCE",
        "SEPARATE_SEMANTIC_REVIEW_AND_DURABLE_READINESS_RECONCILIATION_REQUIRED",
    ]) | {
        "target_id": target_id,
        "packet_digest": packet_digest,
        "candidate_criteria": sorted(REQUIRED_CRITERIA),
        "production_blockers": [],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", help="JSON production-target evidence packet")
    parser.add_argument("--expected-source-sha")
    parser.add_argument("--expected-target-id")
    parser.add_argument("--json", action="store_true", help="Retained for CLI symmetry; output is always JSON.")
    args = parser.parse_args()

    payload = json.loads(Path(args.packet).read_text(encoding="utf-8"))
    result = evaluate(
        payload,
        expected_source_sha=args.expected_source_sha,
        expected_target_id=args.expected_target_id,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] in {"HOLD", "CANDIDATE_COMPLETE"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
