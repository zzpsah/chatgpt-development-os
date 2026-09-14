#!/usr/bin/env python3
"""Validate the current-source DevOS production-readiness evidence model.

A valid assessment is not authorization.  The verifier may report READY only when every
required production criterion is PROVEN, while publication/deployment authority remains
separate and false in this evidence document.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

PROTOCOL = "DEVOS-PRODUCTION-READINESS-EVIDENCE-v2"
REPOSITORY = "zzpsah/chatgpt-development-os"
SCOPE = "CURRENT_SOURCE_PRODUCTION_READINESS"
REQUIRED_CRITERIA = {
    "source_integrity",
    "authorization_security",
    "deterministic_verification",
    "provider_read",
    "remote_mutation",
    "runtime_direct_conformance",
    "recovery_disaster",
    "operational_observability",
    "deployment_target",
    "high_impact_governance",
}
ESTABLISHED_CLASS = {
    "source_integrity": "current_source",
    "authorization_security": "current_source",
    "deterministic_verification": "current_source",
    "provider_read": "current_live_read",
    "remote_mutation": "bounded_live_historical",
}
ALLOWED_EVIDENCE_CLASSES = {
    "current_source",
    "current_live_read",
    "bounded_live_current",
    "bounded_live_historical",
    "external_required",
}
TOP_FIELDS = {
    "protocol",
    "repository",
    "version",
    "assessment_scope",
    "authority",
    "authorization",
    "execution",
    "mutation",
    "publication_authorized",
    "deployment_authorized",
    "evidence_can_authorize",
    "production_ready",
    "verdict",
    "criteria",
    "production_blockers",
}
CRITERION_FIELDS = {
    "id",
    "required_for_production",
    "status",
    "evidence_class",
    "evidence_refs",
    "limitations",
    "blocker",
}
BOUNDARIES = {
    "authority": "UNCHANGED",
    "authorization": "UNCHANGED",
    "execution": "NONE",
    "mutation": "NONE",
    "publication_authorized": False,
    "deployment_authorized": False,
    "evidence_can_authorize": False,
}
LIVE_MUTATION_MARKERS = {
    "e8235f7864678a27bbf036def806a1624fb66678",
    "27a3b3cf4f7c8c8511f3c5a8f3283d8a6a883232",
    "3f530da3ee1efd4e52baad10fe4e644d4db5d116",
}


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _inside(root: Path, path: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def assess(payload: Any, root: Path) -> dict[str, Any]:
    root = root.resolve()
    errors: list[str] = []

    if not isinstance(payload, dict):
        return {
            "protocol": PROTOCOL,
            "assessment_valid": False,
            "verdict": "INVALID",
            "production_ready": False,
            "production_blockers": [],
            "errors": ["PAYLOAD_NOT_OBJECT"],
            **BOUNDARIES,
        }

    if set(payload) != TOP_FIELDS:
        missing = sorted(TOP_FIELDS - set(payload))
        unknown = sorted(set(payload) - TOP_FIELDS)
        if missing:
            errors.append("TOP_FIELDS_MISSING=" + ",".join(missing))
        if unknown:
            errors.append("TOP_FIELDS_UNKNOWN=" + ",".join(unknown))

    if payload.get("protocol") != PROTOCOL:
        errors.append("PROTOCOL_INVALID")
    if payload.get("repository") != REPOSITORY:
        errors.append("REPOSITORY_INVALID")
    if payload.get("assessment_scope") != SCOPE:
        errors.append("ASSESSMENT_SCOPE_INVALID")

    version_path = root / "VERSION"
    if not version_path.is_file():
        errors.append("VERSION_FILE_MISSING")
        canonical_version = None
    else:
        canonical_version = version_path.read_text(encoding="utf-8").strip()
        if payload.get("version") != canonical_version:
            errors.append("VERSION_MISMATCH")

    for key, expected in BOUNDARIES.items():
        value = payload.get(key)
        if type(value) is not type(expected) or value != expected:
            errors.append("BOUNDARY_CHANGED=" + key)

    criteria = payload.get("criteria")
    normalized: dict[str, dict[str, Any]] = {}
    if not isinstance(criteria, list):
        errors.append("CRITERIA_NOT_LIST")
        criteria = []

    seen: set[str] = set()
    for index, criterion in enumerate(criteria):
        if not isinstance(criterion, dict):
            errors.append(f"CRITERION_NOT_OBJECT={index}")
            continue
        if set(criterion) != CRITERION_FIELDS:
            missing = sorted(CRITERION_FIELDS - set(criterion))
            unknown = sorted(set(criterion) - CRITERION_FIELDS)
            if missing:
                errors.append(f"CRITERION_FIELDS_MISSING={index}:" + ",".join(missing))
            if unknown:
                errors.append(f"CRITERION_FIELDS_UNKNOWN={index}:" + ",".join(unknown))

        cid = criterion.get("id")
        if not _text(cid):
            errors.append(f"CRITERION_ID_INVALID={index}")
            continue
        cid = cid.strip()
        if cid in seen:
            errors.append("CRITERION_DUPLICATE=" + cid)
            continue
        seen.add(cid)
        if cid not in REQUIRED_CRITERIA:
            errors.append("CRITERION_UNKNOWN=" + cid)

        if criterion.get("required_for_production") is not True:
            errors.append("CRITERION_NOT_REQUIRED=" + cid)

        status = criterion.get("status")
        if status not in {"PROVEN", "HOLD"}:
            errors.append("CRITERION_STATUS_INVALID=" + cid)

        evidence_class = criterion.get("evidence_class")
        if evidence_class not in ALLOWED_EVIDENCE_CLASSES:
            errors.append("EVIDENCE_CLASS_INVALID=" + cid)
        expected_class = ESTABLISHED_CLASS.get(cid)
        if expected_class is not None and evidence_class != expected_class:
            errors.append("ESTABLISHED_EVIDENCE_CLASS_CHANGED=" + cid)
        if status == "PROVEN" and evidence_class == "external_required":
            errors.append("PROVEN_WITH_EXTERNAL_REQUIRED=" + cid)
        if status == "HOLD" and evidence_class != "external_required":
            errors.append("HOLD_WITHOUT_EXTERNAL_REQUIRED=" + cid)

        refs = criterion.get("evidence_refs")
        if not isinstance(refs, list) or not refs or any(not _text(item) for item in refs):
            errors.append("EVIDENCE_REFS_INVALID=" + cid)
        else:
            for raw_ref in refs:
                rel = Path(raw_ref.strip())
                if rel.is_absolute():
                    errors.append("EVIDENCE_REF_ABSOLUTE=" + cid)
                    continue
                resolved = (root / rel).resolve()
                if not _inside(root, resolved):
                    errors.append("EVIDENCE_REF_ESCAPES_ROOT=" + cid)
                elif not resolved.is_file():
                    errors.append("EVIDENCE_REF_MISSING=" + cid + ":" + raw_ref.strip())

        limitations = criterion.get("limitations")
        if not isinstance(limitations, list) or not limitations or any(not _text(item) for item in limitations):
            errors.append("LIMITATIONS_INVALID=" + cid)

        blocker = criterion.get("blocker")
        if status == "PROVEN" and blocker is not None:
            errors.append("PROVEN_HAS_BLOCKER=" + cid)
        if status == "HOLD" and not _text(blocker):
            errors.append("HOLD_BLOCKER_MISSING=" + cid)

        normalized[cid] = criterion

    missing_criteria = sorted(REQUIRED_CRITERIA - seen)
    if missing_criteria:
        errors.append("CRITERIA_MISSING=" + ",".join(missing_criteria))

    hold_ids = sorted(
        cid for cid, criterion in normalized.items()
        if criterion.get("required_for_production") is True and criterion.get("status") == "HOLD"
    )
    declared_blockers = payload.get("production_blockers")
    if not isinstance(declared_blockers, list) or any(not _text(item) for item in declared_blockers):
        errors.append("PRODUCTION_BLOCKERS_INVALID")
        declared_blockers_list: list[str] = []
    else:
        declared_blockers_list = [str(item).strip() for item in declared_blockers]
        if len(declared_blockers_list) != len(set(declared_blockers_list)):
            errors.append("PRODUCTION_BLOCKERS_DUPLICATE")
        if sorted(declared_blockers_list) != hold_ids:
            errors.append("PRODUCTION_BLOCKERS_MISMATCH")

    expected_ready = not hold_ids and seen == REQUIRED_CRITERIA
    expected_verdict = "READY" if expected_ready else "HOLD"
    if payload.get("verdict") != expected_verdict:
        errors.append("VERDICT_MISMATCH")
    if type(payload.get("production_ready")) is not bool or payload.get("production_ready") != expected_ready:
        errors.append("PRODUCTION_READY_MISMATCH")

    remote = normalized.get("remote_mutation")
    if remote and remote.get("status") == "PROVEN":
        history = root / "docs" / "DEVOS-ENGINEERING-STAGE-HISTORY.md"
        if not history.is_file():
            errors.append("LIVE_MUTATION_HISTORY_MISSING")
        else:
            text = history.read_text(encoding="utf-8")
            missing_markers = sorted(marker for marker in LIVE_MUTATION_MARKERS if marker not in text)
            if missing_markers:
                errors.append("LIVE_MUTATION_MARKERS_MISSING=" + ",".join(missing_markers))

    provider = normalized.get("provider_read")
    if provider and provider.get("status") == "PROVEN" and provider.get("evidence_class") != "current_live_read":
        errors.append("PROVIDER_READ_NOT_CURRENT_LIVE")

    valid = not errors
    return {
        "protocol": PROTOCOL,
        "assessment_valid": valid,
        "verdict": expected_verdict if valid else "INVALID",
        "production_ready": expected_ready if valid else False,
        "production_blockers": hold_ids,
        "proven_count": sum(1 for item in normalized.values() if item.get("status") == "PROVEN"),
        "required_count": len(REQUIRED_CRITERIA),
        "errors": sorted(set(errors)),
        **BOUNDARIES,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument("--input", default="config/production-readiness-v2.json")
    parser.add_argument("--json", action="store_true")
    parser.add_argument(
        "--require-production",
        action="store_true",
        help="Return exit 2 for a structurally valid assessment whose production verdict is HOLD.",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    input_path = Path(args.input)
    if not input_path.is_absolute():
        input_path = root / input_path
    try:
        payload = json.loads(input_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        report = {
            "protocol": PROTOCOL,
            "assessment_valid": False,
            "verdict": "INVALID",
            "production_ready": False,
            "production_blockers": [],
            "errors": [f"INPUT_UNREADABLE={type(exc).__name__}"],
            **BOUNDARIES,
        }
    else:
        report = assess(payload, root)

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"DEVOS PRODUCTION READINESS v2: {report['verdict']}")
        print(f"Assessment valid: {str(report['assessment_valid']).lower()}")
        print(f"Production ready: {str(report['production_ready']).lower()}")
        for blocker in report.get("production_blockers", []):
            print(f"- blocker: {blocker}")
        for error in report.get("errors", []):
            print(f"- error: {error}")
        print("- readiness evidence never grants publication, deployment, or execution authority")

    if not report["assessment_valid"]:
        return 1
    if args.require_production and not report["production_ready"]:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
