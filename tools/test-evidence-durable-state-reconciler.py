#!/usr/bin/env python3
"""Regression corpus for evidence -> durable-state reconciliation v1."""
from __future__ import annotations

import copy
import importlib.util
from pathlib import Path

MODULE = Path(__file__).with_name("evidence-durable-state-reconciler.py")
spec = importlib.util.spec_from_file_location("evidence_reconciler", MODULE)
mod = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(mod)

HEAD = "a" * 40
MERGE = "b" * 40


def base():
    return {
        "repository": "zzpsah/chatgpt-development-os",
        "objective": {"id": "evidence-durable-reconciliation-v1", "label": "Automated Evidence to Durable State Reconciliation v1"},
        "feature": {
            "pr_number": 99,
            "title": "Example bounded feature",
            "head_sha": HEAD,
            "merge_commit_sha": MERGE,
            "merged": True,
        },
        "workflows": [
            {"id": 1001, "name": "Verify Development OS", "head_sha": HEAD, "status": "completed", "conclusion": "success"},
            {"id": 1002, "name": "Verify Development OS Contracts", "head_sha": HEAD, "status": "completed", "conclusion": "success"},
        ],
        "required_workflows": ["Verify Development OS", "Verify Development OS Contracts"],
        "changed_files": ["tools/example.py", "docs/EXAMPLE.md", ".ai/SESSIONS/example.md"],
        "required_documentation_paths": ["docs/EXAMPLE.md", ".ai/SESSIONS/example.md"],
        "semantic_review": {
            "status": "APPROVED",
            "review_ref": ".ai/SESSIONS/example.md#semantic-review",
            "reviewed_targets": [".ai/CURRENT-STATE.md", ".ai/TASKS.md"],
        },
        "authority": "UNCHANGED",
        "authorization": "UNCHANGED",
        "execution": "NONE",
        "mutation": "NONE",
        "production_ready": False,
    }


def main():
    good = mod.reconcile(base())
    assert good["status"] == "READY_FOR_DURABLE_RECONCILIATION", good
    assert good["completion_evidence"] == {
        "implemented": True, "verified": True, "documented": True, "durable_state": False
    }, good
    assert good["authority"] == "UNCHANGED" and good["execution"] == "NONE", good
    assert good["production_ready"] is False, good
    assert good["ledger_record"], good
    assert len(good["ledger_record_sha256"]) == 64, good
    assert mod.validate_ledger_record(good["ledger_record"], good["ledger_record_sha256"]) == [], good

    reordered = base()
    reordered["workflows"] = list(reversed(reordered["workflows"]))
    reordered["changed_files"] = list(reversed(reordered["changed_files"]))
    deterministic = mod.reconcile(reordered)
    assert deterministic["ledger_record_sha256"] == good["ledger_record_sha256"], deterministic

    not_merged = base()
    not_merged["feature"]["merged"] = False
    result = mod.reconcile(not_merged)
    assert result["status"] == "NEEDS_EVIDENCE" and "FEATURE_NOT_MERGED" in result["reasons"], result

    failed_ci = base()
    failed_ci["workflows"][0]["conclusion"] = "failure"
    result = mod.reconcile(failed_ci)
    assert result["status"] == "NEEDS_EVIDENCE", result
    assert any(reason.startswith("WORKFLOW_NOT_SUCCESS=") for reason in result["reasons"]), result

    stale_ci = base()
    stale_ci["workflows"][0]["head_sha"] = "c" * 40
    result = mod.reconcile(stale_ci)
    assert result["status"] == "NEEDS_EVIDENCE", result
    assert any(reason.startswith("WORKFLOW_HEAD_MISMATCH=") for reason in result["reasons"]), result

    missing_workflow = base()
    missing_workflow["required_workflows"].append("Security Gate")
    result = mod.reconcile(missing_workflow)
    assert result["status"] == "NEEDS_EVIDENCE", result
    assert any(reason.startswith("REQUIRED_WORKFLOWS_MISSING=") for reason in result["reasons"]), result

    missing_doc = base()
    missing_doc["required_documentation_paths"].append("docs/MISSING.md")
    result = mod.reconcile(missing_doc)
    assert result["status"] == "NEEDS_EVIDENCE", result
    assert any(reason.startswith("REQUIRED_DOCUMENTATION_MISSING=") for reason in result["reasons"]), result

    review_required = base()
    review_required["semantic_review"] = {"status": "REQUIRED", "review_ref": None, "reviewed_targets": []}
    result = mod.reconcile(review_required)
    assert result["status"] == "SEMANTIC_REVIEW_REQUIRED", result
    assert result["ledger_record"] is None, result

    missing_target = base()
    missing_target["semantic_review"]["reviewed_targets"] = [".ai/CURRENT-STATE.md"]
    result = mod.reconcile(missing_target)
    assert result["status"] == "SEMANTIC_REVIEW_REQUIRED", result
    assert "SEMANTIC_REVIEW_TARGETS_MISSING=.ai/TASKS.md" in result["reasons"], result

    for field, bad in (
        ("authority", "GRANTED"),
        ("authorization", "GRANTED"),
        ("execution", "COMPLETE"),
        ("mutation", "WRITE"),
        ("production_ready", True),
    ):
        forged = base()
        forged[field] = bad
        result = mod.reconcile(forged)
        assert result["status"] == "BLOCKED", (field, result)
        assert "BOUNDARY_INVARIANT_CHANGED=" + field in result["reasons"], (field, result)

    unknown_field = base()
    unknown_field["auto_authorize"] = True
    result = mod.reconcile(unknown_field)
    assert result["status"] == "BLOCKED", result
    assert any(reason.startswith("UNKNOWN_INPUT_FIELDS=") for reason in result["reasons"]), result

    tampered_record = copy.deepcopy(good["ledger_record"])
    tampered_record["production_ready"] = True
    errors = mod.validate_ledger_record(tampered_record, good["ledger_record_sha256"])
    assert "RECORD_BOUNDARY_CHANGED=production_ready" in errors, errors
    assert "RECORD_DIGEST_MISMATCH" in errors, errors

    changed_record = copy.deepcopy(good["ledger_record"])
    changed_record["feature"]["title"] = "silently altered"
    errors = mod.validate_ledger_record(changed_record, good["ledger_record_sha256"])
    assert "RECORD_DIGEST_MISMATCH" in errors, errors

    assert ".ai/CURRENT-STATE.md" in {item["target"] for item in good["write_plan"]}, good
    assert "docs/DEVOS-ENGINEERING-STAGE-HISTORY.md" in {item["target"] for item in good["write_plan"]}, good
    assert "production_ready" in good["semantic_fields_never_inferred"], good
    assert "next_objective" in good["semantic_fields_never_inferred"], good

    print("PASS: exact-head merge/CI/documentation evidence gates durable reconciliation")
    print("PASS: semantic review is mandatory before a durable ledger record can be emitted")
    print("PASS: authority/authorization/execution/mutation/production readiness fail closed")
    print("PASS: reconciliation records are deterministic and tamper-evident")


if __name__ == "__main__":
    main()
