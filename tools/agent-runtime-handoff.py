#!/usr/bin/env python3
"""Deterministic, side-effect-free agent runtime handoff and result validator.

This module bridges a P17 READY step plus an exact scoped approval into a
runtime-neutral local-agent handoff. It never executes a command, mutates a
repository, calls a provider, or upgrades authority.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

INPUT_PROTOCOL = "DEVOS-AGENT-RUNTIME-HANDOFF-INPUT-v1"
HANDOFF_PROTOCOL = "DEVOS-AGENT-RUNTIME-HANDOFF-v1"
PROFILE_PROTOCOL = "DEVOS-AGENT-RUNTIME-PROFILE-v1"
RESULT_PROTOCOL = "DEVOS-AGENT-RUNTIME-RESULT-v1"
VERDICT_PROTOCOL = "DEVOS-AGENT-RUNTIME-VERDICT-v1"
SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")

REQUIRED_RUNTIME_CAPABILITIES = {
    "filesystem.read",
    "filesystem.write_scoped",
    "git.inspect",
    "verification.run",
}
RUNTIME_CAPABILITY_STATES = {"AVAILABLE", "DELEGATABLE", "MISSING"}
SAFE_OPERATIONS = {"file.create", "file.update"}
PROHIBITED_OPERATIONS = [
    "file.delete",
    "git.push",
    "git.force_update",
    "deploy",
    "production_mutation",
    "credential_change",
    "secret_change",
    "database_mutation",
    "permission_change",
    "external_network_mutation",
    "unscoped_shell",
]
BOUNDARIES = {
    "authority": "UNCHANGED",
    "authorization": "UNCHANGED",
    "execution": "NONE",
    "mutation": "NONE",
    "production_ready": False,
}


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _safe_relative_path(value: Any) -> bool:
    if not _text(value):
        return False
    raw = value.replace("\\", "/")
    if raw.startswith("/") or re.match(r"^[A-Za-z]:/", raw):
        return False
    parts = [p for p in raw.split("/") if p not in ("", ".")]
    return bool(parts) and ".." not in parts


def _blocked(reasons: list[str]) -> dict[str, Any]:
    return {
        "protocol": HANDOFF_PROTOCOL,
        "status": "BLOCKED",
        "reasons": reasons,
        "handoff_id": None,
        "handoff": None,
        **BOUNDARIES,
    }


def _validate_runtime_profile(profile: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(profile, dict):
        return ["RUNTIME_PROFILE_NOT_OBJECT"]
    if profile.get("protocol") != PROFILE_PROTOCOL:
        errors.append("RUNTIME_PROFILE_PROTOCOL_INVALID")
    if not _text(profile.get("runtime_id")):
        errors.append("RUNTIME_ID_INVALID")
    if not _text(profile.get("adapter_version")):
        errors.append("RUNTIME_ADAPTER_VERSION_INVALID")
    caps = profile.get("capabilities")
    if not isinstance(caps, dict):
        return errors + ["RUNTIME_CAPABILITIES_INVALID"]
    unknown = sorted(set(caps) - REQUIRED_RUNTIME_CAPABILITIES)
    if unknown:
        errors.append("RUNTIME_CAPABILITIES_UNKNOWN=" + ",".join(unknown))
    for name in sorted(REQUIRED_RUNTIME_CAPABILITIES):
        state = caps.get(name)
        if state not in RUNTIME_CAPABILITY_STATES:
            errors.append("RUNTIME_CAPABILITY_INVALID=" + name)
        elif state != "AVAILABLE":
            errors.append("RUNTIME_CAPABILITY_NOT_AVAILABLE=" + name)
    return errors


def _validate_readiness(readiness: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(readiness, dict):
        return ["READINESS_NOT_OBJECT"]
    if readiness.get("protocol") != "DEVOS-STEP-READINESS-v1":
        errors.append("READINESS_PROTOCOL_INVALID")
    if readiness.get("status") != "READY":
        errors.append("READINESS_NOT_READY")
    if readiness.get("authority") != "UNCHANGED" or readiness.get("authorization") != "UNCHANGED":
        errors.append("READINESS_AUTHORITY_BOUNDARY_CHANGED")
    if readiness.get("execution") != "NONE":
        errors.append("READINESS_EXECUTION_ALREADY_CLAIMED")
    gates = readiness.get("gates")
    required_gates = {"plan", "freshness", "dependencies", "capability", "authorization", "security", "verification"}
    if not isinstance(gates, dict) or any(gates.get(name) is not True for name in required_gates):
        errors.append("READINESS_GATES_INCOMPLETE")
    step = readiness.get("step")
    if not isinstance(step, dict):
        return errors + ["READINESS_STEP_INVALID"]
    if not _text(step.get("id")) or not _text(step.get("objective")):
        errors.append("READINESS_STEP_ID_OR_OBJECTIVE_INVALID")
    if step.get("impact") != "LOW_IMPACT_MUTATION":
        errors.append("RUNTIME_V1_REQUIRES_LOW_IMPACT_MUTATION")
    if step.get("authorization_required") is not True:
        errors.append("RUNTIME_V1_REQUIRES_EXPLICIT_STEP_APPROVAL")
    if step.get("execution_evidence") is not False:
        errors.append("READINESS_EXECUTION_EVIDENCE_ALREADY_PRESENT")
    if not _text(step.get("verification")):
        errors.append("READINESS_VERIFICATION_INVALID")
    expected = step.get("expected_evidence")
    if not isinstance(expected, list) or not expected or any(not _text(item) for item in expected):
        errors.append("READINESS_EXPECTED_EVIDENCE_INVALID")
    if not _text(readiness.get("repository_head")) or not SHA40.fullmatch(readiness.get("repository_head", "")):
        errors.append("READINESS_REPOSITORY_HEAD_INVALID")
    if readiness.get("compiled_repository_head") != readiness.get("repository_head"):
        errors.append("READINESS_REPOSITORY_HEAD_MISMATCH")
    return errors


def _impact_rank(value: str) -> int:
    return {"READ_ONLY": 0, "LOW": 1, "HIGH": 2, "DESTRUCTIVE": 3}.get(value, 99)


def _validate_approval(payload: dict[str, Any]) -> list[str]:
    approval = payload.get("approval")
    readiness = payload.get("readiness") or {}
    work = payload.get("work_unit") or {}
    errors: list[str] = []
    if not isinstance(approval, dict):
        return ["APPROVAL_NOT_OBJECT"]
    required = {"approval_id", "project", "workflow", "capabilities", "targets", "impact_ceiling", "repository_head", "security_gate"}
    if set(approval) != required:
        errors.append("APPROVAL_FIELDS_INVALID")
    for field in ("approval_id", "project", "workflow"):
        if not _text(approval.get(field)):
            errors.append("APPROVAL_" + field.upper() + "_INVALID")
    if approval.get("project") != payload.get("project"):
        errors.append("APPROVAL_PROJECT_SCOPE_CHANGED")
    if approval.get("workflow") != payload.get("workflow"):
        errors.append("APPROVAL_WORKFLOW_SCOPE_CHANGED")
    caps = approval.get("capabilities")
    if not isinstance(caps, list) or any(not _text(item) for item in caps):
        errors.append("APPROVAL_CAPABILITIES_INVALID")
    else:
        required_caps = REQUIRED_RUNTIME_CAPABILITIES
        if not required_caps.issubset(set(caps)):
            errors.append("APPROVAL_CAPABILITIES_INCOMPLETE")
    targets = approval.get("targets")
    if not isinstance(targets, list) or not targets or any(not _safe_relative_path(item) for item in targets):
        errors.append("APPROVAL_TARGETS_INVALID")
    allowed_paths = work.get("allowed_paths") if isinstance(work, dict) else None
    if isinstance(targets, list) and isinstance(allowed_paths, list):
        outside = sorted(set(allowed_paths) - set(targets))
        if outside:
            errors.append("WORK_PATH_OUTSIDE_APPROVAL=" + ",".join(outside))
    if approval.get("impact_ceiling") not in {"READ_ONLY", "LOW", "HIGH", "DESTRUCTIVE"}:
        errors.append("APPROVAL_IMPACT_CEILING_INVALID")
    elif _impact_rank(approval["impact_ceiling"]) < _impact_rank("LOW"):
        errors.append("APPROVAL_IMPACT_CEILING_TOO_LOW")
    if approval.get("repository_head") != readiness.get("repository_head"):
        errors.append("APPROVAL_REPOSITORY_HEAD_CHANGED")
    if approval.get("security_gate") not in (None, "PASS"):
        errors.append("APPROVAL_SECURITY_GATE_INVALID")
    return errors


def _validate_work_unit(work: Any, readiness: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(work, dict):
        return ["WORK_UNIT_NOT_OBJECT"]
    allowed_fields = {"repository_root", "repository_head", "allowed_paths", "allowed_operations", "constraints"}
    if set(work) != allowed_fields:
        errors.append("WORK_UNIT_FIELDS_INVALID")
    if not _text(work.get("repository_root")):
        errors.append("WORK_REPOSITORY_ROOT_INVALID")
    if work.get("repository_head") != readiness.get("repository_head"):
        errors.append("WORK_REPOSITORY_HEAD_CHANGED")
    paths = work.get("allowed_paths")
    if not isinstance(paths, list) or not paths or any(not _safe_relative_path(path) for path in paths):
        errors.append("WORK_ALLOWED_PATHS_INVALID")
    elif len(set(paths)) != len(paths):
        errors.append("WORK_ALLOWED_PATHS_DUPLICATE")
    operations = work.get("allowed_operations")
    if not isinstance(operations, list) or not operations or any(op not in SAFE_OPERATIONS for op in operations):
        errors.append("WORK_ALLOWED_OPERATIONS_INVALID")
    constraints = work.get("constraints")
    if not isinstance(constraints, list) or any(not _text(item) for item in constraints):
        errors.append("WORK_CONSTRAINTS_INVALID")
    return errors


def compile_handoff(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return _blocked(["PAYLOAD_NOT_OBJECT"])
    allowed_fields = {"protocol", "project", "workflow", "readiness", "approval", "runtime", "work_unit"}
    reasons: list[str] = []
    if set(payload) != allowed_fields:
        reasons.append("HANDOFF_INPUT_FIELDS_INVALID")
    if payload.get("protocol") != INPUT_PROTOCOL:
        reasons.append("HANDOFF_INPUT_PROTOCOL_INVALID")
    if not _text(payload.get("project")):
        reasons.append("PROJECT_INVALID")
    if not _text(payload.get("workflow")):
        reasons.append("WORKFLOW_INVALID")
    reasons.extend(_validate_readiness(payload.get("readiness")))
    reasons.extend(_validate_runtime_profile(payload.get("runtime")))
    readiness = payload.get("readiness") if isinstance(payload.get("readiness"), dict) else {}
    reasons.extend(_validate_work_unit(payload.get("work_unit"), readiness))
    reasons.extend(_validate_approval(payload))
    if reasons:
        return _blocked(sorted(set(reasons)))

    readiness = payload["readiness"]
    step = readiness["step"]
    approval = payload["approval"]
    runtime = payload["runtime"]
    work = payload["work_unit"]
    handoff = {
        "protocol": HANDOFF_PROTOCOL,
        "runtime": {
            "runtime_id": runtime["runtime_id"].strip(),
            "adapter_version": runtime["adapter_version"].strip(),
        },
        "project": payload["project"].strip(),
        "workflow": payload["workflow"].strip(),
        "repository_root": work["repository_root"].strip(),
        "repository_head": readiness["repository_head"],
        "step": {
            "id": step["id"].strip(),
            "objective": step["objective"].strip(),
            "impact": step["impact"],
            "verification": step["verification"].strip(),
            "expected_evidence": list(step["expected_evidence"]),
            "stop_or_escalate_if": step.get("stop_or_escalate_if"),
        },
        "approval": {
            "approval_id": approval["approval_id"].strip(),
            "scope_verified": True,
            "capabilities": sorted(set(approval["capabilities"])),
            "targets": sorted(set(approval["targets"])),
            "impact_ceiling": approval["impact_ceiling"],
        },
        "operation_scope": {
            "allowed_paths": sorted(set(work["allowed_paths"])),
            "allowed_operations": sorted(set(work["allowed_operations"])),
            "constraints": list(work["constraints"]),
            "prohibited_operations": list(PROHIBITED_OPERATIONS),
        },
        "result_requirements": {
            "touched_files": "SUBSET_OF_ALLOWED_PATHS",
            "diff": "REQUIRED_FOR_COMPLETED_MUTATION",
            "tests": "AT_LEAST_ONE_PASSING_RESULT_REQUIRED",
            "readback": "EVERY_TOUCHED_FILE_MUST_BE_PRESENT_AND_HASHED",
            "repository_head_before": readiness["repository_head"],
        },
        **BOUNDARIES,
    }
    handoff_id = _digest(handoff)
    return {
        "protocol": HANDOFF_PROTOCOL,
        "status": "HANDOFF_READY",
        "reasons": ["P17_READY_AND_EXACT_APPROVAL_SCOPE_VERIFIED"],
        "handoff_id": handoff_id,
        "handoff": handoff,
        **BOUNDARIES,
    }


def _verdict(status: str, reasons: list[str], handoff_id: str | None, evidence: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "protocol": VERDICT_PROTOCOL,
        "status": status,
        "reasons": reasons,
        "handoff_id": handoff_id,
        "evidence": evidence,
        **BOUNDARIES,
    }


def verify_result(handoff_bundle: Any, result: Any) -> dict[str, Any]:
    if not isinstance(handoff_bundle, dict) or handoff_bundle.get("status") != "HANDOFF_READY":
        return _verdict("BLOCKED", ["HANDOFF_NOT_READY"], None)
    handoff = handoff_bundle.get("handoff")
    handoff_id = handoff_bundle.get("handoff_id")
    if not isinstance(handoff, dict) or not isinstance(handoff_id, str) or _digest(handoff) != handoff_id:
        return _verdict("BLOCKED", ["HANDOFF_INTEGRITY_INVALID"], handoff_id if isinstance(handoff_id, str) else None)
    if not isinstance(result, dict):
        return _verdict("BLOCKED", ["RESULT_NOT_OBJECT"], handoff_id)

    allowed_fields = {
        "protocol", "handoff_id", "runtime_id", "status", "repository_head_before",
        "touched_files", "diff", "tests", "readback", "prohibited_operations_used",
    }
    reasons: list[str] = []
    if set(result) != allowed_fields:
        reasons.append("RESULT_FIELDS_INVALID")
    if result.get("protocol") != RESULT_PROTOCOL:
        reasons.append("RESULT_PROTOCOL_INVALID")
    if result.get("handoff_id") != handoff_id:
        reasons.append("RESULT_HANDOFF_ID_MISMATCH")
    if result.get("runtime_id") != handoff["runtime"]["runtime_id"]:
        reasons.append("RESULT_RUNTIME_ID_MISMATCH")
    if result.get("repository_head_before") != handoff["repository_head"]:
        reasons.append("RESULT_REPOSITORY_HEAD_MISMATCH")
    claimed_status = result.get("status")
    if claimed_status not in {"COMPLETED", "FAILED", "BLOCKED"}:
        reasons.append("RESULT_STATUS_INVALID")

    touched = result.get("touched_files")
    allowed_paths = set(handoff["operation_scope"]["allowed_paths"])
    if not isinstance(touched, list) or any(not _safe_relative_path(path) for path in touched):
        reasons.append("RESULT_TOUCHED_FILES_INVALID")
        touched_set: set[str] = set()
    else:
        touched_set = set(touched)
        outside = sorted(touched_set - allowed_paths)
        if outside:
            reasons.append("RESULT_TOUCHED_FILE_OUTSIDE_SCOPE=" + ",".join(outside))

    prohibited_used = result.get("prohibited_operations_used")
    if not isinstance(prohibited_used, list) or any(not _text(item) for item in prohibited_used):
        reasons.append("RESULT_PROHIBITED_OPERATIONS_INVALID")
    elif prohibited_used:
        reasons.append("RESULT_PROHIBITED_OPERATION_USED=" + ",".join(sorted(set(prohibited_used))))

    diff = result.get("diff")
    if not isinstance(diff, dict) or set(diff) != {"status", "sha256", "changed_paths"}:
        reasons.append("RESULT_DIFF_INVALID")
    else:
        if diff.get("status") not in {"OBSERVED", "NONE"}:
            reasons.append("RESULT_DIFF_STATUS_INVALID")
        if diff.get("status") == "OBSERVED" and not SHA256.fullmatch(str(diff.get("sha256", ""))):
            reasons.append("RESULT_DIFF_DIGEST_INVALID")
        changed_paths = diff.get("changed_paths")
        if not isinstance(changed_paths, list) or any(not _safe_relative_path(path) for path in changed_paths):
            reasons.append("RESULT_DIFF_PATHS_INVALID")
        elif set(changed_paths) != touched_set:
            reasons.append("RESULT_DIFF_TOUCHED_FILES_MISMATCH")

    tests = result.get("tests")
    tests_ok = True
    if not isinstance(tests, list) or not tests:
        reasons.append("RESULT_TESTS_MISSING")
        tests_ok = False
    else:
        for index, test in enumerate(tests):
            if not isinstance(test, dict) or set(test) != {"name", "status", "exit_code", "output_sha256"}:
                reasons.append(f"RESULT_TEST_INVALID={index}")
                tests_ok = False
                continue
            if not _text(test.get("name")) or type(test.get("exit_code")) is not int:
                reasons.append(f"RESULT_TEST_SCHEMA_INVALID={index}")
                tests_ok = False
            if test.get("status") != "PASS" or test.get("exit_code") != 0:
                reasons.append(f"RESULT_TEST_NOT_PASS={index}")
                tests_ok = False
            if not SHA256.fullmatch(str(test.get("output_sha256", ""))):
                reasons.append(f"RESULT_TEST_OUTPUT_DIGEST_INVALID={index}")
                tests_ok = False

    readback = result.get("readback")
    readback_paths: set[str] = set()
    if not isinstance(readback, list):
        reasons.append("RESULT_READBACK_INVALID")
    else:
        for index, item in enumerate(readback):
            if not isinstance(item, dict) or set(item) != {"path", "status", "sha256"}:
                reasons.append(f"RESULT_READBACK_ITEM_INVALID={index}")
                continue
            path = item.get("path")
            if not _safe_relative_path(path):
                reasons.append(f"RESULT_READBACK_PATH_INVALID={index}")
                continue
            readback_paths.add(path)
            if item.get("status") != "PRESENT":
                reasons.append(f"RESULT_READBACK_NOT_PRESENT={path}")
            if not SHA256.fullmatch(str(item.get("sha256", ""))):
                reasons.append(f"RESULT_READBACK_DIGEST_INVALID={path}")
        missing = sorted(touched_set - readback_paths)
        if missing:
            reasons.append("RESULT_READBACK_MISSING=" + ",".join(missing))

    if claimed_status == "COMPLETED":
        if not touched_set:
            reasons.append("RESULT_COMPLETED_WITHOUT_TOUCHED_FILES")
        if isinstance(diff, dict) and diff.get("status") != "OBSERVED":
            reasons.append("RESULT_COMPLETED_WITHOUT_OBSERVED_DIFF")
        if not tests_ok:
            reasons.append("RESULT_COMPLETED_WITHOUT_PASSING_TESTS")

    if reasons:
        return _verdict("HOLD", sorted(set(reasons)), handoff_id)

    evidence = {
        "runtime_id": result["runtime_id"],
        "repository_head_before": result["repository_head_before"],
        "touched_files": sorted(touched_set),
        "diff_sha256": result["diff"]["sha256"] if result["diff"]["status"] == "OBSERVED" else None,
        "tests": sorted(result["tests"], key=lambda item: item["name"]),
        "readback": sorted(result["readback"], key=lambda item: item["path"]),
        "approval_id": handoff["approval"]["approval_id"],
        "step_id": handoff["step"]["id"],
        "rule": "RUNTIME_RESULT_IS_EVIDENCE_NOT_AUTHORITY",
    }
    if claimed_status == "COMPLETED":
        return _verdict("VERIFIED_RUNTIME_RESULT", ["DIFF_TESTS_AND_READBACK_MATCH_APPROVED_SCOPE"], handoff_id, evidence)
    return _verdict(claimed_status, ["RUNTIME_DID_NOT_CLAIM_COMPLETION"], handoff_id, evidence)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    build = sub.add_parser("build")
    build.add_argument("input")
    verify = sub.add_parser("verify-result")
    verify.add_argument("handoff")
    verify.add_argument("result")
    args = parser.parse_args()
    if args.command == "build":
        payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
        output = compile_handoff(payload)
        print(json.dumps(output, indent=2, sort_keys=True, ensure_ascii=False))
        return 0 if output["status"] == "HANDOFF_READY" else 2
    handoff = json.loads(Path(args.handoff).read_text(encoding="utf-8"))
    result = json.loads(Path(args.result).read_text(encoding="utf-8"))
    output = verify_result(handoff, result)
    print(json.dumps(output, indent=2, sort_keys=True, ensure_ascii=False))
    return 0 if output["status"] == "VERIFIED_RUNTIME_RESULT" else 2


if __name__ == "__main__":
    raise SystemExit(main())
