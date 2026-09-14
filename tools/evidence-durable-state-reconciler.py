#!/usr/bin/env python3
"""Deterministic evidence -> durable-state reconciliation gate for DevOS.

This tool validates machine-verifiable completion evidence and produces an audit-only
reconciliation record. It never grants authority, executes provider mutations, chooses
semantic truth, or upgrades production readiness.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

PROTOCOL = "DEVOS-EVIDENCE-DURABLE-RECONCILIATION-v1"
RECORD_PROTOCOL = "DEVOS-DURABLE-RECONCILIATION-RECORD-v1"
SHA40 = re.compile(r"^[0-9a-f]{40}$")
BOUNDARY_FIELDS = {
    "authority": "UNCHANGED",
    "authorization": "UNCHANGED",
    "execution": "NONE",
    "mutation": "NONE",
    "production_ready": False,
}
ALLOWED_INPUT_FIELDS = {
    "repository",
    "objective",
    "feature",
    "workflows",
    "required_workflows",
    "changed_files",
    "required_documentation_paths",
    "semantic_review",
    *BOUNDARY_FIELDS,
}
SEMANTIC_FIELDS_NEVER_INFERRED = [
    "authority",
    "authorization",
    "production_ready",
    "architecture_stage",
    "next_objective",
    "contradiction_truth_winner",
    "permission_scope",
]


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _sha(value: Any) -> bool:
    return isinstance(value, str) and bool(SHA40.fullmatch(value))


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()


def _base(status: str, reasons: list[str]) -> dict[str, Any]:
    return {
        "protocol": PROTOCOL,
        "status": status,
        "reasons": reasons,
        **BOUNDARY_FIELDS,
        "semantic_fields_never_inferred": list(SEMANTIC_FIELDS_NEVER_INFERRED),
    }


def _invalid(payload: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(payload, dict):
        return ["PAYLOAD_NOT_OBJECT"]
    unknown = sorted(set(payload) - ALLOWED_INPUT_FIELDS)
    if unknown:
        errors.append("UNKNOWN_INPUT_FIELDS=" + ",".join(unknown))
    for key, expected in BOUNDARY_FIELDS.items():
        if key not in payload or type(payload.get(key)) is not type(expected) or payload.get(key) != expected:
            errors.append("BOUNDARY_INVARIANT_CHANGED=" + key)
    if not _text(payload.get("repository")):
        errors.append("REPOSITORY_INVALID")
    objective = payload.get("objective")
    if not isinstance(objective, dict) or set(objective) - {"id", "label"}:
        errors.append("OBJECTIVE_INVALID")
    elif not _text(objective.get("id")) or not _text(objective.get("label")):
        errors.append("OBJECTIVE_INVALID")
    feature = payload.get("feature")
    if not isinstance(feature, dict) or set(feature) - {"pr_number", "title", "head_sha", "merge_commit_sha", "merged"}:
        errors.append("FEATURE_INVALID")
    else:
        if type(feature.get("pr_number")) is not int or feature.get("pr_number", 0) <= 0:
            errors.append("FEATURE_PR_INVALID")
        if not _text(feature.get("title")):
            errors.append("FEATURE_TITLE_INVALID")
        if not _sha(feature.get("head_sha")):
            errors.append("FEATURE_HEAD_INVALID")
        if not _sha(feature.get("merge_commit_sha")):
            errors.append("FEATURE_MERGE_COMMIT_INVALID")
        if type(feature.get("merged")) is not bool:
            errors.append("FEATURE_MERGED_FLAG_INVALID")
    for field in ("workflows", "required_workflows", "changed_files", "required_documentation_paths"):
        if not isinstance(payload.get(field), list):
            errors.append(field.upper() + "_INVALID")
    review = payload.get("semantic_review")
    if not isinstance(review, dict) or set(review) - {"status", "review_ref", "reviewed_targets"}:
        errors.append("SEMANTIC_REVIEW_INVALID")
    else:
        if review.get("status") not in {"REQUIRED", "APPROVED"}:
            errors.append("SEMANTIC_REVIEW_STATUS_INVALID")
        if review.get("review_ref") is not None and not _text(review.get("review_ref")):
            errors.append("SEMANTIC_REVIEW_REF_INVALID")
        targets = review.get("reviewed_targets", [])
        if not isinstance(targets, list) or any(not _text(item) for item in targets):
            errors.append("SEMANTIC_REVIEW_TARGETS_INVALID")
    return errors


def _workflow_evidence(payload: dict[str, Any]) -> tuple[bool, list[str], list[dict[str, Any]]]:
    feature = payload["feature"]
    feature_head = feature["head_sha"]
    reasons: list[str] = []
    normalized: list[dict[str, Any]] = []
    names: set[str] = set()
    workflows = payload["workflows"]
    if not workflows:
        reasons.append("NO_WORKFLOW_EVIDENCE")
    for index, item in enumerate(workflows):
        if not isinstance(item, dict):
            reasons.append(f"WORKFLOW_INVALID={index}")
            continue
        allowed = {"id", "name", "head_sha", "status", "conclusion"}
        if set(item) - allowed:
            reasons.append(f"WORKFLOW_UNKNOWN_FIELDS={index}")
            continue
        run_id = item.get("id")
        name = item.get("name")
        head_sha = item.get("head_sha")
        status = item.get("status")
        conclusion = item.get("conclusion")
        if type(run_id) is not int or run_id <= 0 or not _text(name) or not _sha(head_sha):
            reasons.append(f"WORKFLOW_SCHEMA_INVALID={index}")
            continue
        if status != "completed" or conclusion != "success":
            reasons.append(f"WORKFLOW_NOT_SUCCESS={name}")
        if head_sha != feature_head:
            reasons.append(f"WORKFLOW_HEAD_MISMATCH={name}")
        names.add(name.strip())
        normalized.append({
            "id": run_id,
            "name": name.strip(),
            "head_sha": head_sha,
            "status": status,
            "conclusion": conclusion,
        })
    required = payload["required_workflows"]
    if any(not _text(name) for name in required):
        reasons.append("REQUIRED_WORKFLOW_NAME_INVALID")
    else:
        missing = sorted(set(name.strip() for name in required) - names)
        if missing:
            reasons.append("REQUIRED_WORKFLOWS_MISSING=" + ",".join(missing))
    normalized.sort(key=lambda row: (row["name"], row["id"]))
    return not reasons, reasons, normalized


def _documentation_evidence(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    changed = payload["changed_files"]
    required = payload["required_documentation_paths"]
    if any(not _text(path) for path in changed):
        reasons.append("CHANGED_FILE_INVALID")
        return False, reasons
    if any(not _text(path) for path in required):
        reasons.append("REQUIRED_DOCUMENTATION_PATH_INVALID")
        return False, reasons
    changed_set = {path.strip() for path in changed}
    missing = sorted(path.strip() for path in required if path.strip() not in changed_set)
    if missing:
        reasons.append("REQUIRED_DOCUMENTATION_MISSING=" + ",".join(missing))
    return not reasons, reasons


def _write_plan() -> list[dict[str, str]]:
    return [
        {"target": ".ai/RECONCILIATION-LEDGER.jsonl", "mode": "APPEND_MACHINE_RECORD"},
        {"target": ".ai/SESSIONS/", "mode": "CREATE_RECONCILIATION_SESSION"},
        {"target": ".ai/CURRENT-STATE.md", "mode": "SEMANTIC_REVIEWED_UPDATE"},
        {"target": ".ai/TASKS.md", "mode": "SEMANTIC_REVIEWED_UPDATE"},
        {"target": "docs/DEVOS-ENGINEERING-STAGE-HISTORY.md", "mode": "MATERIALITY_REVIEW_REQUIRED"},
    ]


def reconcile(payload: Any) -> dict[str, Any]:
    errors = _invalid(payload)
    if errors:
        return _base("BLOCKED", errors) | {
            "completion_evidence": {"implemented": False, "verified": False, "documented": False, "durable_state": False},
            "write_plan": [],
            "ledger_record": None,
            "ledger_record_sha256": None,
        }
    assert isinstance(payload, dict)
    feature = payload["feature"]
    workflow_ok, workflow_reasons, workflows = _workflow_evidence(payload)
    docs_ok, docs_reasons = _documentation_evidence(payload)
    implemented = feature["merged"] is True
    evidence_reasons: list[str] = []
    if not implemented:
        evidence_reasons.append("FEATURE_NOT_MERGED")
    evidence_reasons.extend(workflow_reasons)
    evidence_reasons.extend(docs_reasons)

    completion = {
        "implemented": implemented,
        "verified": workflow_ok,
        "documented": docs_ok,
        "durable_state": False,
    }
    machine_facts = {
        "repository": payload["repository"].strip(),
        "objective": {"id": payload["objective"]["id"].strip(), "label": payload["objective"]["label"].strip()},
        "feature": dict(feature),
        "workflows": workflows,
        "changed_files": sorted({path.strip() for path in payload["changed_files"]}),
        "required_documentation_paths": sorted({path.strip() for path in payload["required_documentation_paths"]}),
    }
    if evidence_reasons:
        return _base("NEEDS_EVIDENCE", evidence_reasons) | {
            "machine_facts": machine_facts,
            "completion_evidence": completion,
            "write_plan": [],
            "ledger_record": None,
            "ledger_record_sha256": None,
        }

    review = payload["semantic_review"]
    if review["status"] != "APPROVED" or not _text(review.get("review_ref")):
        return _base("SEMANTIC_REVIEW_REQUIRED", ["SEMANTIC_REVIEW_NOT_APPROVED"]) | {
            "machine_facts": machine_facts,
            "completion_evidence": completion,
            "write_plan": _write_plan(),
            "ledger_record": None,
            "ledger_record_sha256": None,
        }

    required_targets = {".ai/CURRENT-STATE.md", ".ai/TASKS.md"}
    reviewed_targets = {str(item).strip() for item in review.get("reviewed_targets", [])}
    if not required_targets.issubset(reviewed_targets):
        missing = sorted(required_targets - reviewed_targets)
        return _base("SEMANTIC_REVIEW_REQUIRED", ["SEMANTIC_REVIEW_TARGETS_MISSING=" + ",".join(missing)]) | {
            "machine_facts": machine_facts,
            "completion_evidence": completion,
            "write_plan": _write_plan(),
            "ledger_record": None,
            "ledger_record_sha256": None,
        }

    record = {
        "protocol": RECORD_PROTOCOL,
        "repository": machine_facts["repository"],
        "objective": machine_facts["objective"],
        "feature": machine_facts["feature"],
        "workflow_evidence": workflows,
        "changed_files": machine_facts["changed_files"],
        "required_documentation_paths": machine_facts["required_documentation_paths"],
        "semantic_review": {
            "status": "APPROVED",
            "review_ref": review["review_ref"].strip(),
            "reviewed_targets": sorted(reviewed_targets),
        },
        "completion_evidence": completion,
        **BOUNDARY_FIELDS,
        "rule": "MACHINE_FACTS_MAY_BE_AUTOMATED_SEMANTIC_STATE_REQUIRES_REVIEW",
    }
    return _base("READY_FOR_DURABLE_RECONCILIATION", []) | {
        "machine_facts": machine_facts,
        "completion_evidence": completion,
        "write_plan": _write_plan(),
        "ledger_record": record,
        "ledger_record_sha256": _digest(record),
    }


def validate_ledger_record(record: Any, expected_digest: str | None = None) -> list[str]:
    errors: list[str] = []
    if not isinstance(record, dict):
        return ["RECORD_NOT_OBJECT"]
    expected_fields = {
        "protocol", "repository", "objective", "feature", "workflow_evidence", "changed_files",
        "required_documentation_paths", "semantic_review", "completion_evidence", "rule", *BOUNDARY_FIELDS,
    }
    if set(record) != expected_fields:
        errors.append("RECORD_FIELDS_INVALID")
    if record.get("protocol") != RECORD_PROTOCOL:
        errors.append("RECORD_PROTOCOL_INVALID")
    for key, expected in BOUNDARY_FIELDS.items():
        if type(record.get(key)) is not type(expected) or record.get(key) != expected:
            errors.append("RECORD_BOUNDARY_CHANGED=" + key)
    review = record.get("semantic_review")
    if not isinstance(review, dict) or review.get("status") != "APPROVED" or not _text(review.get("review_ref")):
        errors.append("RECORD_SEMANTIC_REVIEW_INVALID")
    completion = record.get("completion_evidence")
    if not isinstance(completion, dict) or completion != {
        "implemented": True, "verified": True, "documented": True, "durable_state": False
    }:
        errors.append("RECORD_COMPLETION_EVIDENCE_INVALID")
    if record.get("rule") != "MACHINE_FACTS_MAY_BE_AUTOMATED_SEMANTIC_STATE_REQUIRES_REVIEW":
        errors.append("RECORD_RULE_INVALID")
    if expected_digest is not None:
        if not isinstance(expected_digest, str) or not re.fullmatch(r"[0-9a-f]{64}", expected_digest):
            errors.append("EXPECTED_DIGEST_INVALID")
        elif _digest(record) != expected_digest:
            errors.append("RECORD_DIGEST_MISMATCH")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="JSON evidence bundle or reconciliation record")
    parser.add_argument("--verify-record", action="store_true")
    parser.add_argument("--expected-digest")
    args = parser.parse_args()
    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    if args.verify_record:
        errors = validate_ledger_record(payload, args.expected_digest)
        print(json.dumps({"status": "VALID" if not errors else "HOLD", "errors": errors}, indent=2, sort_keys=True))
        return 0 if not errors else 1
    result = reconcile(payload)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "READY_FOR_DURABLE_RECONCILIATION" else 2


if __name__ == "__main__":
    raise SystemExit(main())
