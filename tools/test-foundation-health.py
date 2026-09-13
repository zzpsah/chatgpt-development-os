#!/usr/bin/env python3
"""Adversarial regression corpus for Foundation Health & State Consistency."""
from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import shutil
import tempfile

ROOT = Path(__file__).resolve().parents[1]
HEALTH_PATH = ROOT / "tools" / "devos-health.py"
DOCTOR_PATH = ROOT / "tools" / "devos-doctor.py"


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


health = load("devos_health_test", HEALTH_PATH)
doctor = load("devos_doctor_test", DOCTOR_PATH)


def by_name(report: dict, name: str) -> dict:
    return next(row for row in report["checks"] if row["name"] == name)


def fixture() -> tuple[tempfile.TemporaryDirectory, Path]:
    tmp = tempfile.TemporaryDirectory()
    target = Path(tmp.name) / "repo"
    shutil.copytree(
        ROOT,
        target,
        ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"),
    )
    return tmp, target


def test_baseline_is_read_only_and_conservative() -> None:
    report = health.derive_health(ROOT, run_checks=False)
    assert report["overall"] in {"PASS", "WARN"}, report
    assert report["mode"] == "READ_ONLY"
    assert report["authority"] == "UNCHANGED"
    assert report["authorization"] == "UNCHANGED"
    assert report["execution"] == "NONE"
    assert report["mutation"] == "NONE"
    assert report["production_ready"] is False
    assert report["live_mutation_proven"] is False
    assert by_name(report, "canonical_identity")["status"] == "PASS"
    assert by_name(report, "dependency_closure")["status"] == "PASS"
    assert by_name(report, "p15_interpretation")["status"] == "PASS"
    assert by_name(report, "p16_planning")["status"] == "PASS"
    assert by_name(report, "p17_readiness")["status"] == "PASS"
    assert by_name(report, "security_gate_wiring")["status"] == "PASS"
    assert by_name(report, "capability_evidence_consistency")["status"] == "PASS"


def test_tampered_identity_blocks() -> None:
    tmp, root = fixture()
    try:
        path = root / ".ai/manifest.yaml"
        path.write_text(
            path.read_text(encoding="utf-8").replace(
                "canonical_repository: zzpsah/chatgpt-development-os",
                "canonical_repository: attacker/not-devos",
            ),
            encoding="utf-8",
        )
        report = health.derive_health(root, run_checks=False)
        assert by_name(report, "canonical_identity")["status"] == "BLOCKED", report
        assert report["overall"] == "BLOCKED", report
    finally:
        tmp.cleanup()


def test_missing_dependency_stays_unknown() -> None:
    tmp, root = fixture()
    try:
        (root / "rules/security.md").unlink()
        report = health.derive_health(root, run_checks=False)
        assert by_name(report, "dependency_closure")["status"] == "UNKNOWN", report
        assert by_name(report, "security_gate_wiring")["status"] == "UNKNOWN", report
        assert report["overall"] != "PASS", report
    finally:
        tmp.cleanup()


def test_unsupported_claim_promotion_fails() -> None:
    tmp, root = fixture()
    try:
        path = root / "config/readiness-evidence.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["production_ready"] = True
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        report = health.derive_health(root, run_checks=False)
        row = by_name(report, "capability_evidence_consistency")
        assert row["status"] == "FAIL", row
        assert report["overall"] in {"FAIL", "BLOCKED"}, report
    finally:
        tmp.cleanup()


def test_contradictory_status_document_warns() -> None:
    tmp, root = fixture()
    try:
        path = root / ".ai/CURRENT-STATE.md"
        path.write_text(path.read_text(encoding="utf-8") + "\nproduction_ready = true\n", encoding="utf-8")
        report = health.derive_health(root, run_checks=False)
        row = by_name(report, "status_document_consistency")
        assert row["status"] == "WARN", row
        assert report["overall"] != "PASS", report
    finally:
        tmp.cleanup()


def test_historical_source_drift_warns_without_repointing() -> None:
    tmp, root = fixture()
    try:
        target = root / "tools/test-step-readiness-orchestrator.py"
        target.write_text(target.read_text(encoding="utf-8") + "\n# adversarial drift\n", encoding="utf-8")
        ledger_before = json.loads((root / "config/readiness-evidence.json").read_text(encoding="utf-8"))
        snapshot_before = ledger_before["snapshot_head"]
        report = health.derive_health(root, run_checks=False)
        row = by_name(report, "historical_source_freshness")
        assert row["status"] == "WARN", row
        assert "tools/test-step-readiness-orchestrator.py" in report["historical_source_drift"], report
        ledger_after = json.loads((root / "config/readiness-evidence.json").read_text(encoding="utf-8"))
        assert ledger_after["snapshot_head"] == snapshot_before
    finally:
        tmp.cleanup()


def test_stale_expected_head_blocks() -> None:
    previous = os.environ.get("DEVOS_EXPECTED_HEAD")
    os.environ["DEVOS_EXPECTED_HEAD"] = "0" * 40
    try:
        row = health.inspect_git(ROOT)
        assert row["status"] == "BLOCKED", row
    finally:
        if previous is None:
            os.environ.pop("DEVOS_EXPECTED_HEAD", None)
        else:
            os.environ["DEVOS_EXPECTED_HEAD"] = previous


def test_malformed_ai_state_fails() -> None:
    tmp, root = fixture()
    try:
        path = root / ".ai/TASKS.md"
        path.write_text("# Tasks\nNo active heading.\n", encoding="utf-8")
        report = health.derive_health(root, run_checks=False)
        assert by_name(report, "ai_state_shape")["status"] == "FAIL", report
        assert report["overall"] in {"FAIL", "BLOCKED"}, report
    finally:
        tmp.cleanup()


def test_doctor_never_promotes_warn_or_unknown() -> None:
    report = {
        "overall": "WARN",
        "repository": "zzpsah/chatgpt-development-os",
        "checks": [{"name": "example", "status": "WARN", "reason": "historical drift"}],
        "production_ready": False,
        "live_mutation_proven": False,
        "historical_source_drift": ["tools/example.py"],
        "invariants": health.INVARIANTS,
        "universal_product_goal": "AI A + Account A -> repository -> AI B + Account B -> correct state recovery -> safe continuation",
        "limitations": [],
    }
    rendered = doctor.render(report)
    assert "DEVOS DOCTOR: WARN" in rendered
    assert "[WARN] example" in rendered
    assert "WARN and UNKNOWN are not PASS" in rendered
    assert "production_ready: false" in rendered


def main() -> None:
    test_baseline_is_read_only_and_conservative()
    test_tampered_identity_blocks()
    test_missing_dependency_stays_unknown()
    test_unsupported_claim_promotion_fails()
    test_contradictory_status_document_warns()
    test_historical_source_drift_warns_without_repointing()
    test_stale_expected_head_blocks()
    test_malformed_ai_state_fails()
    test_doctor_never_promotes_warn_or_unknown()
    print("PASS: Foundation Health & State Consistency adversarial regression corpus")


if __name__ == "__main__":
    main()
