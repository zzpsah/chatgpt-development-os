#!/usr/bin/env python3
"""Integration regression for Current-Source Evidence -> Health -> Doctor."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKET_REL = ".ai/EVIDENCE/current-source-health-test.json"
PACKET_PATH = ROOT / PACKET_REL


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


current = load("current_source_health_test", ROOT / "tools/current-source-evidence.py")
health = load("devos_health_current_source_test", ROOT / "tools/devos-health.py")
doctor = load("devos_doctor_current_source_test", ROOT / "tools/devos-doctor.py")


def by_name(report: dict, name: str) -> dict:
    return next(row for row in report["checks"] if row["name"] == name)


def collect_packet() -> tuple[dict, dict]:
    ledger = json.loads((ROOT / "config/readiness-evidence.json").read_text(encoding="utf-8"))
    packet = current.collect(
        ROOT,
        ledger,
        capability="readiness",
        level="deterministic",
        test="tools/test-step-readiness-orchestrator.py",
    )
    assert current.validate_packet(packet, ledger, ROOT) == []
    return ledger, packet


def write_packet(packet: dict) -> None:
    PACKET_PATH.parent.mkdir(parents=True, exist_ok=True)
    PACKET_PATH.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def cleanup() -> None:
    try:
        PACKET_PATH.unlink()
    except FileNotFoundError:
        pass


def test_valid_packet_adds_current_proof_without_repointing_history() -> None:
    ledger, packet = collect_packet()
    before = json.loads(json.dumps(ledger))
    write_packet(packet)
    try:
        report = health.derive_health(ROOT, run_checks=False, current_source_packet=PACKET_REL)
        row = by_name(report, "current_source_evidence")
        assert row["status"] in {"PASS", "WARN"}, row
        status = report["current_source_evidence"]
        assert status["packet_status"] == "VALID", status
        assert status["rule"] == "CURRENT_EVIDENCE_ADDS_PROOF_BUT_NEVER_REWRITES_HISTORICAL_PROVENANCE"
        if "tools/test-step-readiness-orchestrator.py" in report["historical_source_drift"]:
            assert "tools/test-step-readiness-orchestrator.py" in status["current_source_verified"], status
            assert "tools/test-step-readiness-orchestrator.py" not in status["unresolved_historical_drift"], status
            assert by_name(report, "historical_source_freshness")["status"] == "WARN"
        after = json.loads((ROOT / "config/readiness-evidence.json").read_text(encoding="utf-8"))
        assert after == before, "Health must not rewrite readiness ledger"
        rendered = doctor.render(report)
        assert "Current-source evidence:" in rendered
        assert "packet_status: VALID" in rendered
        assert "production_ready: false" in rendered
        assert "live_mutation_proven: false" in rendered
    finally:
        cleanup()


def test_tampered_packet_blocks_health_instead_of_promoting() -> None:
    _, packet = collect_packet()
    packet["source_head"] = "0" * 40
    write_packet(packet)
    try:
        report = health.derive_health(ROOT, run_checks=False, current_source_packet=PACKET_REL)
        row = by_name(report, "current_source_evidence")
        assert row["status"] == "BLOCKED", row
        assert report["overall"] == "BLOCKED", report
    finally:
        cleanup()


def test_missing_packet_is_unknown_not_pass() -> None:
    cleanup()
    report = health.derive_health(ROOT, run_checks=False, current_source_packet=PACKET_REL)
    row = by_name(report, "current_source_evidence")
    assert row["status"] == "UNKNOWN", row
    assert report["overall"] != "PASS", report


def test_packet_path_escape_blocks() -> None:
    report = health.derive_health(ROOT, run_checks=False, current_source_packet="../outside.json")
    row = by_name(report, "current_source_evidence")
    assert row["status"] == "BLOCKED", row
    assert report["overall"] == "BLOCKED", report


def main() -> None:
    cleanup()
    test_valid_packet_adds_current_proof_without_repointing_history()
    test_tampered_packet_blocks_health_instead_of_promoting()
    test_missing_packet_is_unknown_not_pass()
    test_packet_path_escape_blocks()
    cleanup()
    print("PASS: Current-Source Evidence -> Foundation Health -> Doctor integration")


if __name__ == "__main__":
    main()
