#!/usr/bin/env python3
"""Adversarial regression corpus for Production Readiness Evidence v2."""
from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "verify-production-readiness-v2.py"
CONFIG = ROOT / "config" / "production-readiness-v2.json"

spec = importlib.util.spec_from_file_location("production_readiness_v2", MODULE_PATH)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def canonical() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def report(payload: dict) -> dict:
    return module.assess(payload, ROOT)


def assert_invalid(payload: dict, reason_prefix: str) -> None:
    result = report(payload)
    assert result["assessment_valid"] is False, result
    assert result["production_ready"] is False, result
    assert result["verdict"] == "INVALID", result
    assert any(item.startswith(reason_prefix) for item in result["errors"]), result


def main() -> None:
    base = canonical()
    result = report(base)
    assert result["assessment_valid"] is True, result
    assert result["verdict"] == "HOLD", result
    assert result["production_ready"] is False, result
    assert result["proven_count"] == 5, result
    assert result["required_count"] == 10, result
    assert result["production_blockers"] == [
        "deployment_target",
        "high_impact_governance",
        "operational_observability",
        "recovery_disaster",
        "runtime_direct_conformance",
    ], result
    assert result["publication_authorized"] is False
    assert result["deployment_authorized"] is False
    assert result["evidence_can_authorize"] is False

    fake_ready = copy.deepcopy(base)
    fake_ready["production_ready"] = True
    assert_invalid(fake_ready, "PRODUCTION_READY_MISMATCH")

    fake_verdict = copy.deepcopy(base)
    fake_verdict["verdict"] = "READY"
    assert_invalid(fake_verdict, "VERDICT_MISMATCH")

    fake_blockers = copy.deepcopy(base)
    fake_blockers["production_blockers"] = []
    assert_invalid(fake_blockers, "PRODUCTION_BLOCKERS_MISMATCH")

    duplicate = copy.deepcopy(base)
    duplicate["criteria"].append(copy.deepcopy(duplicate["criteria"][0]))
    assert_invalid(duplicate, "CRITERION_DUPLICATE")

    missing_criterion = copy.deepcopy(base)
    missing_criterion["criteria"] = missing_criterion["criteria"][:-1]
    missing_criterion["production_blockers"].remove("high_impact_governance")
    assert_invalid(missing_criterion, "CRITERIA_MISSING")

    extra_top = copy.deepcopy(base)
    extra_top["invented_authority"] = True
    assert_invalid(extra_top, "TOP_FIELDS_UNKNOWN")

    extra_criterion_field = copy.deepcopy(base)
    extra_criterion_field["criteria"][0]["magic"] = "authority"
    assert_invalid(extra_criterion_field, "CRITERION_FIELDS_UNKNOWN")

    external_proven = copy.deepcopy(base)
    target = next(item for item in external_proven["criteria"] if item["id"] == "runtime_direct_conformance")
    target["status"] = "PROVEN"
    target["blocker"] = None
    external_proven["production_blockers"].remove("runtime_direct_conformance")
    assert_invalid(external_proven, "PROVEN_WITH_EXTERNAL_REQUIRED")

    hold_without_blocker = copy.deepcopy(base)
    target = next(item for item in hold_without_blocker["criteria"] if item["id"] == "deployment_target")
    target["blocker"] = ""
    assert_invalid(hold_without_blocker, "HOLD_BLOCKER_MISSING")

    missing_evidence = copy.deepcopy(base)
    missing_evidence["criteria"][0]["evidence_refs"] = ["tools/definitely-not-real.py"]
    assert_invalid(missing_evidence, "EVIDENCE_REF_MISSING")

    wrong_remote_class = copy.deepcopy(base)
    target = next(item for item in wrong_remote_class["criteria"] if item["id"] == "remote_mutation")
    target["evidence_class"] = "current_source"
    assert_invalid(wrong_remote_class, "ESTABLISHED_EVIDENCE_CLASS_CHANGED")

    publication = copy.deepcopy(base)
    publication["publication_authorized"] = True
    assert_invalid(publication, "BOUNDARY_CHANGED=publication_authorized")

    deployment = copy.deepcopy(base)
    deployment["deployment_authorized"] = True
    assert_invalid(deployment, "BOUNDARY_CHANGED=deployment_authorized")

    self_authorizing = copy.deepcopy(base)
    self_authorizing["evidence_can_authorize"] = True
    assert_invalid(self_authorizing, "BOUNDARY_CHANGED=evidence_can_authorize")

    wrong_version = copy.deepcopy(base)
    wrong_version["version"] = "999.0.0"
    assert_invalid(wrong_version, "VERSION_MISMATCH")

    # The protocol can represent READY only after every required criterion is backed
    # by non-external evidence.  Even then, readiness never becomes publication or
    # deployment authorization.
    all_proven = copy.deepcopy(base)
    for criterion in all_proven["criteria"]:
        if criterion["status"] == "HOLD":
            criterion["status"] = "PROVEN"
            criterion["evidence_class"] = "bounded_live_current"
            criterion["blocker"] = None
    all_proven["production_blockers"] = []
    all_proven["verdict"] = "READY"
    all_proven["production_ready"] = True
    ready = report(all_proven)
    assert ready["assessment_valid"] is True, ready
    assert ready["verdict"] == "READY", ready
    assert ready["production_ready"] is True, ready
    assert ready["production_blockers"] == [], ready
    assert ready["publication_authorized"] is False
    assert ready["deployment_authorized"] is False
    assert ready["evidence_can_authorize"] is False
    assert ready["execution"] == "NONE"
    assert ready["mutation"] == "NONE"

    print("PASS: Production Readiness Evidence v2 is fail-closed, blocker-exact, and authority-neutral")


if __name__ == "__main__":
    main()
