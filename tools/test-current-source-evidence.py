#!/usr/bin/env python3
"""Adversarial regression corpus for current-source evidence packets."""
from __future__ import annotations

import copy
import importlib.util
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "current-source-evidence.py"
LEDGER_PATH = ROOT / "config" / "readiness-evidence.json"


def load_module():
    spec = importlib.util.spec_from_file_location("current_source_evidence_test", MODULE_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


mod = load_module()


def ledger() -> dict:
    return json.loads(LEDGER_PATH.read_text(encoding="utf-8"))


def collect_readiness(data: dict) -> dict:
    return mod.collect(
        ROOT,
        data,
        capability="readiness",
        level="deterministic",
        test="tools/test-step-readiness-orchestrator.py",
    )


def test_valid_packet_is_exact_head_bound_and_conservative() -> None:
    data = ledger()
    packet = collect_readiness(data)
    errors = mod.validate_packet(packet, data, ROOT)
    assert errors == [], errors
    assert packet["source_head"] == mod._git_head(ROOT)
    assert packet["production_ready"] is False
    assert packet["live_provider_proven"] is False
    assert packet["authority"] == "UNCHANGED"
    assert packet["authorization"] == "UNCHANGED"
    assert packet["execution"] == "NONE"
    assert packet["mutation"] == "NONE"
    assert packet["evidence"]["exit_code"] == 0


def test_stale_source_head_is_rejected() -> None:
    data = ledger()
    packet = collect_readiness(data)
    packet["source_head"] = "0" * 40
    errors = mod.validate_packet(packet, data, ROOT)
    assert any("source_head" in item for item in errors), errors


def test_test_digest_tampering_is_rejected() -> None:
    data = ledger()
    packet = collect_readiness(data)
    packet["evidence"]["test_sha256"] = "0" * 64
    errors = mod.validate_packet(packet, data, ROOT)
    assert "current test digest mismatch" in errors, errors


def test_undeclared_claim_is_rejected() -> None:
    data = ledger()
    packet = collect_readiness(data)
    packet["evidence"]["capability"] = "fabricated-capability"
    errors = mod.validate_packet(packet, data, ROOT)
    assert "current claim is not declared by readiness ledger" in errors, errors


def test_failed_check_cannot_be_current_verified() -> None:
    data = ledger()
    packet = collect_readiness(data)
    packet["evidence"]["exit_code"] = 1
    errors = mod.validate_packet(packet, data, ROOT)
    assert "current check did not succeed" in errors, errors


def test_production_and_live_provider_promotion_are_rejected() -> None:
    data = ledger()
    packet = collect_readiness(data)
    promoted = copy.deepcopy(packet)
    promoted["production_ready"] = True
    errors = mod.validate_packet(promoted, data, ROOT)
    assert "invalid invariant: production_ready" in errors, errors

    promoted = copy.deepcopy(packet)
    promoted["live_provider_proven"] = True
    errors = mod.validate_packet(promoted, data, ROOT)
    assert "invalid invariant: live_provider_proven" in errors, errors


def test_ci_run_context_mismatch_is_rejected() -> None:
    data = ledger()
    packet = collect_readiness(data)
    previous = os.environ.get("GITHUB_RUN_ID")
    try:
        os.environ["GITHUB_RUN_ID"] = "424242"
        packet["evidence"]["context"] = "ci"
        packet["evidence"]["run_id"] = 111111
        packet["evidence"]["workflow"] = "Verify Current-Source Evidence"
        errors = mod.validate_packet(packet, data, ROOT)
        assert "CI run_id does not match current GitHub run context" in errors, errors
    finally:
        if previous is None:
            os.environ.pop("GITHUB_RUN_ID", None)
        else:
            os.environ["GITHUB_RUN_ID"] = previous


def test_historical_drift_overlay_never_rewrites_ledger() -> None:
    data = ledger()
    before = copy.deepcopy(data)
    packet = collect_readiness(data)
    status = mod.current_drift_status(packet, data, ROOT)
    assert status["packet_status"] == "VALID", status
    assert data == before, "current evidence must not rewrite historical ledger"
    if "tools/test-step-readiness-orchestrator.py" in status["historical_source_drift"]:
        assert "tools/test-step-readiness-orchestrator.py" in status["current_source_verified"], status
        assert "tools/test-step-readiness-orchestrator.py" not in status["unresolved_historical_drift"], status


def test_provider_simulated_cannot_be_relabelled_to_arbitrary_test() -> None:
    data = ledger()
    packet = collect_readiness(data)
    packet["evidence"]["level"] = "provider_simulated"
    errors = mod.validate_packet(packet, data, ROOT)
    assert "current claim is not declared by readiness ledger" in errors or "provider_simulated current proof requires controlled-mutation corpus" in errors, errors


def main() -> None:
    test_valid_packet_is_exact_head_bound_and_conservative()
    test_stale_source_head_is_rejected()
    test_test_digest_tampering_is_rejected()
    test_undeclared_claim_is_rejected()
    test_failed_check_cannot_be_current_verified()
    test_production_and_live_provider_promotion_are_rejected()
    test_ci_run_context_mismatch_is_rejected()
    test_historical_drift_overlay_never_rewrites_ledger()
    test_provider_simulated_cannot_be_relabelled_to_arbitrary_test()
    print("PASS: Current-Source Evidence adversarial regression corpus")


if __name__ == "__main__":
    main()
