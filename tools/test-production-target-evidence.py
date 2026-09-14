#!/usr/bin/env python3
"""Adversarial regression corpus for Production Target Evidence Intake v1."""
from __future__ import annotations

import copy
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "production-target-evidence.py"
SOURCE_SHA = "69b06853d5f360659ce42d5cf2c5ec7c8dccc04d"
TARGET_ID = "prod-example"
DIGEST = "a" * 64

spec = importlib.util.spec_from_file_location("production_target_evidence", MODULE_PATH)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def evidence(ref: str) -> dict:
    return {"ref": ref, "digest": DIGEST, "observed_scope": "bounded production target observation"}


def packet(status: str = "PASS") -> dict:
    criteria = []
    for criterion_id in sorted(module.REQUIRED_CRITERIA):
        criteria.append({
            "id": criterion_id,
            "status": status,
            "evidence": [] if status == "UNOBSERVED" else [evidence("evidence://" + criterion_id)],
            "limitations": ["Evidence is scoped to this exact target and observation only."],
        })
    return {
        "protocol": module.PROTOCOL,
        "repository": "zzpsah/chatgpt-development-os",
        "source_sha": SOURCE_SHA,
        "target": {"id": TARGET_ID, "environment": "production", "kind": "service", "ref": "target://prod-example"},
        "observed_at": "2026-09-14T23:00:00+05:30",
        "observer": {"kind": "external-verifier", "ref": "observer://bounded-test"},
        "criteria": criteria,
        "limitations": ["Candidate evidence cannot self-promote production readiness."],
        "authority": "UNCHANGED",
        "authorization": "UNCHANGED",
        "execution": "NONE",
        "mutation": "NONE",
        "publication_authorized": False,
        "deployment_authorized": False,
        "production_ready": False,
    }


def evaluate(payload: dict, *, source: str = SOURCE_SHA, target: str = TARGET_ID) -> dict:
    return module.evaluate(payload, expected_source_sha=source, expected_target_id=target)


def assert_blocked(payload: dict, prefix: str) -> None:
    result = evaluate(payload)
    assert result["status"] == "BLOCKED", result
    assert result["production_ready"] is False, result
    assert result["readiness_promotion_allowed"] is False, result
    assert result["semantic_review_required"] is True, result
    assert any(reason.startswith(prefix) for reason in result["reasons"]), result


def main() -> None:
    base = packet()
    complete = evaluate(base)
    assert complete["status"] == "CANDIDATE_COMPLETE", complete
    assert complete["candidate_criteria"] == sorted(module.REQUIRED_CRITERIA), complete
    assert complete["production_blockers"] == [], complete
    assert complete["production_ready"] is False
    assert complete["readiness_promotion_allowed"] is False
    assert complete["semantic_review_required"] is True
    assert complete["execution"] == "NONE"
    assert complete["mutation"] == "NONE"
    assert complete["publication_authorized"] is False
    assert complete["deployment_authorized"] is False

    hold = packet()
    hold["criteria"][0]["status"] = "UNOBSERVED"
    hold["criteria"][0]["evidence"] = []
    held = evaluate(hold)
    assert held["status"] == "HOLD", held
    assert held["production_blockers"] == [hold["criteria"][0]["id"]], held
    assert held["production_ready"] is False

    wrong_source = packet()
    assert_blocked(wrong_source, "SOURCE_SHA_MISMATCH") if False else None
    result = module.evaluate(wrong_source, expected_source_sha="b" * 40, expected_target_id=TARGET_ID)
    assert result["status"] == "BLOCKED" and "SOURCE_SHA_MISMATCH" in result["reasons"], result

    wrong_target = packet()
    result = module.evaluate(wrong_target, expected_source_sha=SOURCE_SHA, expected_target_id="other-prod")
    assert result["status"] == "BLOCKED" and "TARGET_ID_MISMATCH" in result["reasons"], result

    nonprod = packet()
    nonprod["target"]["environment"] = "staging"
    assert_blocked(nonprod, "TARGET_ENVIRONMENT_NOT_PRODUCTION")

    missing = packet()
    missing["criteria"] = missing["criteria"][:-1]
    assert_blocked(missing, "CRITERIA_MISSING")

    duplicate = packet()
    duplicate["criteria"].append(copy.deepcopy(duplicate["criteria"][0]))
    assert_blocked(duplicate, "CRITERION_DUPLICATE")

    unknown = packet()
    unknown["criteria"][0]["id"] = "invented_ready"
    assert_blocked(unknown, "CRITERION_UNKNOWN")

    pass_without_evidence = packet()
    pass_without_evidence["criteria"][0]["evidence"] = []
    assert_blocked(pass_without_evidence, "OBSERVED_WITHOUT_EVIDENCE")

    unobserved_with_evidence = packet()
    unobserved_with_evidence["criteria"][0]["status"] = "UNOBSERVED"
    assert_blocked(unobserved_with_evidence, "UNOBSERVED_WITH_EVIDENCE")

    bad_digest = packet()
    bad_digest["criteria"][0]["evidence"][0]["digest"] = "not-a-digest"
    assert_blocked(bad_digest, "EVIDENCE_DIGEST_INVALID")

    no_tz = packet()
    no_tz["observed_at"] = "2026-09-14T23:00:00"
    assert_blocked(no_tz, "OBSERVED_AT_INVALID")

    extra = packet()
    extra["magic_authority"] = True
    assert_blocked(extra, "PACKET_FIELDS_INVALID")

    for boundary, unsafe in (
        ("authority", "GRANTED"),
        ("authorization", "GRANTED"),
        ("execution", "ALLOWED"),
        ("mutation", "ALLOWED"),
        ("publication_authorized", True),
        ("deployment_authorized", True),
        ("production_ready", True),
    ):
        changed = packet()
        changed[boundary] = unsafe
        assert_blocked(changed, "BOUNDARY_CHANGED=" + boundary)

    print("PASS: production target evidence is target-bound, exact-scope, fail-closed, and cannot self-promote readiness")


if __name__ == "__main__":
    main()
