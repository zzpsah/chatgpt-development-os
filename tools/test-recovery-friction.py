#!/usr/bin/env python3
"""Adversarial regression corpus for repository-only cross-host recovery friction."""
from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import shutil
import tempfile

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "tools" / "recovery-friction.py"
spec = importlib.util.spec_from_file_location("recovery_friction", MODULE)
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def profile_all_available() -> dict:
    profile = json.loads((ROOT / "adapters/host-profile.example.json").read_text(encoding="utf-8"))
    for record in profile["capabilities"].values():
        record["status"] = "AVAILABLE"
    return profile


def copy_recovery_pack(target: Path) -> None:
    paths = list(mod.REQUIRED_REPOSITORY_INPUTS) + [
        "tools/verify-host-profile.py",
        "adapters/host-profile.example.json",
    ]
    for rel in paths:
        src = ROOT / rel
        dst = target / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def without_ci_sha(fn):
    old = os.environ.pop("GITHUB_SHA", None)
    old_expected = os.environ.pop("DEVOS_EXPECTED_HEAD", None)
    try:
        return fn()
    finally:
        if old is not None:
            os.environ["GITHUB_SHA"] = old
        if old_expected is not None:
            os.environ["DEVOS_EXPECTED_HEAD"] = old_expected


def test_clean_repository_inputs_recover() -> None:
    report = mod.analyze(ROOT, profile_all_available())
    assert report["recovery_status"] == "PASS", report
    assert report["host"]["status"] == "PASS", report
    assert report["friction"]["missing_repository_inputs"] == 0
    assert report["real_cross_vendor_account_proven"] is False
    assert report["authority"] == "UNCHANGED"
    assert report["execution"] == "NONE"
    assert report["mutation"] == "NONE"


def test_example_profile_exposes_delegation_friction() -> None:
    profile = json.loads((ROOT / "adapters/host-profile.example.json").read_text(encoding="utf-8"))
    report = mod.analyze(ROOT, profile)
    assert report["recovery_status"] == "PASS", report
    assert report["continuation_status"] == "WARN", report
    assert report["friction"]["delegatable_capabilities"] == 2, report
    assert report["real_cross_vendor_account_proven"] is False


def test_missing_durable_state_never_passes() -> None:
    with tempfile.TemporaryDirectory() as directory:
        pack = Path(directory)
        copy_recovery_pack(pack)
        (pack / ".ai/CURRENT-STATE.md").unlink()
        report = without_ci_sha(lambda: mod.analyze(pack, profile_all_available()))
        assert report["repository_state"]["status"] == "UNKNOWN", report
        assert report["recovery_status"] == "UNKNOWN", report
        assert ".ai/CURRENT-STATE.md" in report["repository_state"]["missing_inputs"]


def test_tampered_identity_blocks() -> None:
    with tempfile.TemporaryDirectory() as directory:
        pack = Path(directory)
        copy_recovery_pack(pack)
        manifest = pack / ".ai/manifest.yaml"
        manifest.write_text(
            manifest.read_text(encoding="utf-8").replace(
                "canonical_repository: zzpsah/chatgpt-development-os",
                "canonical_repository: attacker/not-devos",
            ),
            encoding="utf-8",
        )
        report = without_ci_sha(lambda: mod.analyze(pack, profile_all_available()))
        assert report["repository_state"]["status"] == "BLOCKED", report
        assert report["overall"] == "BLOCKED"


def test_missing_critical_host_capability_blocks() -> None:
    profile = profile_all_available()
    profile["capabilities"]["inspection"]["status"] = "MISSING"
    report = mod.analyze(ROOT, profile)
    assert report["host"]["status"] == "BLOCKED", report
    assert report["recovery_status"] == "BLOCKED", report
    assert report["friction"]["critical_capabilities_missing"] == 1


def test_missing_noncritical_capability_warns_without_authority() -> None:
    profile = profile_all_available()
    profile["capabilities"]["execution"]["status"] = "MISSING"
    report = mod.analyze(ROOT, profile)
    assert report["recovery_status"] == "PASS", report
    assert report["continuation_status"] == "WARN", report
    assert report["overall"] == "WARN", report
    assert report["authorization"] == "UNCHANGED"


def test_stale_expected_head_blocks() -> None:
    report = mod.analyze(ROOT, profile_all_available(), expected_head="0" * 40)
    assert report["repository_state"]["status"] == "BLOCKED", report
    assert report["overall"] == "BLOCKED"


def test_invalid_profile_fails_closed() -> None:
    profile = profile_all_available()
    profile["capabilities"]["verification"]["status"] = "ASSUMED"
    report = mod.analyze(ROOT, profile)
    assert report["host"]["status"] == "BLOCKED", report
    assert report["overall"] == "BLOCKED"
    assert report["host"]["profile_errors"], report


def main() -> None:
    test_clean_repository_inputs_recover()
    test_example_profile_exposes_delegation_friction()
    test_missing_durable_state_never_passes()
    test_tampered_identity_blocks()
    test_missing_critical_host_capability_blocks()
    test_missing_noncritical_capability_warns_without_authority()
    test_stale_expected_head_blocks()
    test_invalid_profile_fails_closed()
    print("PASS: Cross-Host Recovery Friction & Onboarding adversarial corpus")


if __name__ == "__main__":
    main()
