#!/usr/bin/env python3
"""Regression corpus for the Universal Agent Runtime Adapter v1."""
from __future__ import annotations

import copy
import hashlib
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "tools" / "agent-runtime-handoff.py"
spec = importlib.util.spec_from_file_location("agent_runtime_handoff", MODULE)
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

HEAD = "a" * 40
HASH_A = hashlib.sha256(b"a").hexdigest()
HASH_B = hashlib.sha256(b"b").hexdigest()
HASH_C = hashlib.sha256(b"c").hexdigest()


def readiness():
    return {
        "protocol": "DEVOS-STEP-READINESS-v1",
        "plan_protocol": "DEVOS-GOAL-PLAN-v1",
        "status": "READY",
        "step_id": "S1",
        "repository_head": HEAD,
        "compiled_repository_head": HEAD,
        "gates": {
            "plan": True,
            "freshness": True,
            "dependencies": True,
            "capability": True,
            "authorization": True,
            "security": True,
            "verification": True,
        },
        "reasons": ["ALL_P17_GATES_SATISFIED"],
        "authority": "UNCHANGED",
        "authorization": "UNCHANGED",
        "execution": "NONE",
        "step": {
            "id": "S1",
            "objective": "Update src/app.py and its bounded test",
            "depends_on": [],
            "expected_evidence": ["diff", "tests", "readback"],
            "impact": "LOW_IMPACT_MUTATION",
            "authorization_required": True,
            "verification": "run configured local tests and read back changed files",
            "stop_or_escalate_if": "scope changes or verification fails",
            "execution_evidence": False,
        },
    }


def payload():
    return {
        "protocol": "DEVOS-AGENT-RUNTIME-HANDOFF-INPUT-v1",
        "project": "temporary-local-project",
        "workflow": "automated-software-delivery-v1",
        "readiness": readiness(),
        "approval": {
            "approval_id": "approval-S1-001",
            "project": "temporary-local-project",
            "workflow": "automated-software-delivery-v1",
            "capabilities": [
                "filesystem.read",
                "filesystem.write_scoped",
                "git.inspect",
                "verification.run",
            ],
            "targets": ["src/app.py", "tests/test_app.py"],
            "impact_ceiling": "LOW",
            "repository_head": HEAD,
            "security_gate": None,
        },
        "runtime": {
            "protocol": "DEVOS-AGENT-RUNTIME-PROFILE-v1",
            "runtime_id": "generic-local-agent",
            "adapter_version": "1.0",
            "capabilities": {
                "filesystem.read": "AVAILABLE",
                "filesystem.write_scoped": "AVAILABLE",
                "git.inspect": "AVAILABLE",
                "verification.run": "AVAILABLE",
            },
        },
        "work_unit": {
            "repository_root": "/tmp/devos-disposable/example",
            "repository_head": HEAD,
            "allowed_paths": ["src/app.py", "tests/test_app.py"],
            "allowed_operations": ["file.create", "file.update"],
            "constraints": [
                "local disposable repository only",
                "no delete deploy production credentials database permissions or remote mutation",
            ],
        },
    }


def good_result(bundle):
    return {
        "protocol": "DEVOS-AGENT-RUNTIME-RESULT-v1",
        "handoff_id": bundle["handoff_id"],
        "runtime_id": "generic-local-agent",
        "status": "COMPLETED",
        "repository_head_before": HEAD,
        "touched_files": ["src/app.py", "tests/test_app.py"],
        "diff": {
            "status": "OBSERVED",
            "sha256": HASH_A,
            "changed_paths": ["src/app.py", "tests/test_app.py"],
        },
        "tests": [
            {"name": "configured-local-tests", "status": "PASS", "exit_code": 0, "output_sha256": HASH_B}
        ],
        "readback": [
            {"path": "src/app.py", "status": "PRESENT", "sha256": HASH_B},
            {"path": "tests/test_app.py", "status": "PRESENT", "sha256": HASH_C},
        ],
        "prohibited_operations_used": [],
    }


def expect_block(mutator, reason):
    case = payload()
    mutator(case)
    out = mod.compile_handoff(case)
    assert out["status"] == "BLOCKED", out
    assert reason in out["reasons"], out


def main():
    ready = mod.compile_handoff(payload())
    assert ready["status"] == "HANDOFF_READY", ready
    assert len(ready["handoff_id"]) == 64, ready
    assert ready["execution"] == "NONE" and ready["mutation"] == "NONE", ready
    assert ready["production_ready"] is False, ready
    assert ready["handoff"]["approval"]["scope_verified"] is True, ready
    assert set(ready["handoff"]["operation_scope"]["allowed_operations"]) == {"file.create", "file.update"}, ready
    assert "file.delete" in ready["handoff"]["operation_scope"]["prohibited_operations"], ready
    assert "deploy" in ready["handoff"]["operation_scope"]["prohibited_operations"], ready

    # Deterministic scope normalization.
    reordered = payload()
    reordered["approval"]["capabilities"].reverse()
    reordered["approval"]["targets"].reverse()
    reordered["work_unit"]["allowed_paths"].reverse()
    reordered["work_unit"]["allowed_operations"].reverse()
    normalized = mod.compile_handoff(reordered)
    assert normalized["status"] == "HANDOFF_READY", normalized
    assert normalized["handoff_id"] == ready["handoff_id"], (normalized, ready)

    expect_block(lambda x: x["readiness"].update(status="NEEDS_APPROVAL"), "READINESS_NOT_READY")
    expect_block(lambda x: x["readiness"]["step"].update(impact="HIGH_IMPACT_MUTATION"), "RUNTIME_V1_REQUIRES_LOW_IMPACT_MUTATION")
    expect_block(lambda x: x["readiness"]["step"].update(authorization_required=False), "RUNTIME_V1_REQUIRES_EXPLICIT_STEP_APPROVAL")
    expect_block(lambda x: x["approval"].update(repository_head="b" * 40), "APPROVAL_REPOSITORY_HEAD_CHANGED")
    expect_block(lambda x: x["work_unit"].update(repository_head="b" * 40), "WORK_REPOSITORY_HEAD_CHANGED")
    expect_block(lambda x: x["work_unit"]["allowed_paths"].append("../escape.txt"), "WORK_ALLOWED_PATHS_INVALID")
    expect_block(lambda x: x["work_unit"]["allowed_operations"].append("file.delete"), "WORK_ALLOWED_OPERATIONS_INVALID")

    def outside_approval(x):
        x["work_unit"]["allowed_paths"].append("src/extra.py")
    expect_block(outside_approval, "WORK_PATH_OUTSIDE_APPROVAL=src/extra.py")

    def missing_runtime_cap(x):
        x["runtime"]["capabilities"]["verification.run"] = "MISSING"
    expect_block(missing_runtime_cap, "RUNTIME_CAPABILITY_NOT_AVAILABLE=verification.run")

    verified = mod.verify_result(ready, good_result(ready))
    assert verified["status"] == "VERIFIED_RUNTIME_RESULT", verified
    assert verified["evidence"]["approval_id"] == "approval-S1-001", verified
    assert verified["evidence"]["rule"] == "RUNTIME_RESULT_IS_EVIDENCE_NOT_AUTHORITY", verified
    assert verified["authorization"] == "UNCHANGED" and verified["execution"] == "NONE", verified

    tampered = copy.deepcopy(ready)
    tampered["handoff"]["operation_scope"]["allowed_paths"].append("src/extra.py")
    out = mod.verify_result(tampered, good_result(ready))
    assert out["status"] == "BLOCKED" and "HANDOFF_INTEGRITY_INVALID" in out["reasons"], out

    outside = good_result(ready)
    outside["touched_files"].append("src/extra.py")
    outside["diff"]["changed_paths"].append("src/extra.py")
    out = mod.verify_result(ready, outside)
    assert out["status"] == "HOLD", out
    assert "RESULT_TOUCHED_FILE_OUTSIDE_SCOPE=src/extra.py" in out["reasons"], out

    failed_test = good_result(ready)
    failed_test["tests"][0].update(status="FAIL", exit_code=1)
    out = mod.verify_result(ready, failed_test)
    assert out["status"] == "HOLD", out
    assert "RESULT_TEST_NOT_PASS=0" in out["reasons"], out
    assert "RESULT_COMPLETED_WITHOUT_PASSING_TESTS" in out["reasons"], out

    missing_readback = good_result(ready)
    missing_readback["readback"] = missing_readback["readback"][:1]
    out = mod.verify_result(ready, missing_readback)
    assert out["status"] == "HOLD", out
    assert "RESULT_READBACK_MISSING=tests/test_app.py" in out["reasons"], out

    prohibited = good_result(ready)
    prohibited["prohibited_operations_used"] = ["git.push"]
    out = mod.verify_result(ready, prohibited)
    assert out["status"] == "HOLD", out
    assert "RESULT_PROHIBITED_OPERATION_USED=git.push" in out["reasons"], out

    mismatch = good_result(ready)
    mismatch["diff"]["changed_paths"] = ["src/app.py"]
    out = mod.verify_result(ready, mismatch)
    assert out["status"] == "HOLD" and "RESULT_DIFF_TOUCHED_FILES_MISMATCH" in out["reasons"], out

    wrong_head = good_result(ready)
    wrong_head["repository_head_before"] = "b" * 40
    out = mod.verify_result(ready, wrong_head)
    assert out["status"] == "HOLD" and "RESULT_REPOSITORY_HEAD_MISMATCH" in out["reasons"], out

    print("PASS: P17 READY plus exact approval compiles to a tamper-evident runtime-neutral handoff")
    print("PASS: v1 permits only scoped local create/update and preserves authority/execution boundaries")
    print("PASS: out-of-scope mutation, failed tests, missing readback, prohibited use, and tampering fail closed")
    print("PASS: runtime completion becomes evidence only after diff + tests + readback agree with approved scope")


if __name__ == "__main__":
    main()
