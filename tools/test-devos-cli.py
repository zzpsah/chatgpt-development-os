#!/usr/bin/env python3
"""Regression checks for the small cross-platform DevOS CLI dispatcher."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "tools" / "devos.py"
VERSION = ROOT / "VERSION"


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CLI), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def main() -> None:
    canonical_version = VERSION.read_text(encoding="utf-8").strip()

    direct = run("version")
    assert direct.returncode == 0, direct.stderr
    assert direct.stdout.strip() == canonical_version, direct.stdout

    flag = run("--version")
    assert flag.returncode == 0, flag.stderr
    assert flag.stdout.strip() == canonical_version, flag.stdout

    release = run("release-check", "--no-git", "--json")
    assert release.returncode == 0, release.stdout + release.stderr
    payload = json.loads(release.stdout)
    assert payload["status"] == "READY", payload
    assert payload["version"] == canonical_version, payload
    assert payload["production_ready"] is False
    assert payload["execution"] == "NONE"
    assert payload["mutation"] == "NONE"

    with tempfile.TemporaryDirectory() as temp_dir:
        unmanaged = Path(temp_dir) / "unmanaged"
        unmanaged.mkdir()
        lifecycle = run("project-lifecycle", "--path", str(unmanaged), "--require-managed", "--json")
        assert lifecycle.returncode == 2, lifecycle.stdout + lifecycle.stderr
        lifecycle_payload = json.loads(lifecycle.stdout)
        assert lifecycle_payload["status"] == "ONBOARDING_REQUIRED", lifecycle_payload
        assert lifecycle_payload["development_continuation_allowed"] is False

        managed = run(
            "project-lifecycle",
            "--path", str(unmanaged),
            "--apply",
            "--authorization", "EXPLICIT",
            "--require-managed",
            "--json",
        )
        assert managed.returncode == 0, managed.stdout + managed.stderr
        managed_payload = json.loads(managed.stdout)
        assert managed_payload["status"] == "MANAGED", managed_payload
        assert managed_payload["development_continuation_allowed"] is True

    fleet_packet = {
        "protocol": "DEVOS-PROJECT-FLEET-SNAPSHOT-v1",
        "provider": "cli-test",
        "observed_at": "2026-09-17T00:00:00+05:30",
        "repositories": [
            {
                "repository": "zzpsah/unmanaged-cli-test",
                "default_branch": "main",
                "observed_head": "a" * 40,
                "archived": False,
                "files": ["README.md"],
                "manifest": None,
            }
        ],
    }
    with tempfile.TemporaryDirectory() as temp_dir:
        fleet_path = Path(temp_dir) / "fleet.json"
        fleet_path.write_text(json.dumps(fleet_packet), encoding="utf-8")
        fleet = run("project-fleet", "--snapshot", str(fleet_path), "--json")
        assert fleet.returncode == 0, fleet.stdout + fleet.stderr
        fleet_payload = json.loads(fleet.stdout)
        assert fleet_payload["fleet_status"] == "ATTENTION", fleet_payload
        assert fleet_payload["summary"]["onboarding_required"] == 1
        assert fleet_payload["external_mutation"] == "NONE"

        fleet_clean = run("project-fleet", "--snapshot", str(fleet_path), "--require-clean", "--json")
        assert fleet_clean.returncode == 2, fleet_clean.stdout + fleet_clean.stderr

    readiness = run("production-readiness", "--json")
    assert readiness.returncode == 0, readiness.stdout + readiness.stderr
    readiness_payload = json.loads(readiness.stdout)
    assert readiness_payload["assessment_valid"] is True, readiness_payload
    assert readiness_payload["verdict"] == "HOLD", readiness_payload
    assert readiness_payload["production_ready"] is False, readiness_payload
    assert readiness_payload["publication_authorized"] is False, readiness_payload
    assert readiness_payload["deployment_authorized"] is False, readiness_payload
    assert readiness_payload["evidence_can_authorize"] is False, readiness_payload

    require_production = run("production-readiness", "--require-production", "--json")
    assert require_production.returncode == 2, require_production.stdout + require_production.stderr
    require_payload = json.loads(require_production.stdout)
    assert require_payload["assessment_valid"] is True, require_payload
    assert require_payload["verdict"] == "HOLD", require_payload

    target_packet = {
        "protocol": "DEVOS-PRODUCTION-TARGET-EVIDENCE-v1",
        "repository": "zzpsah/chatgpt-development-os",
        "source_sha": "0" * 40,
        "target": {"id": "prod-cli-test", "environment": "production", "kind": "service", "ref": "target://cli-test"},
        "observed_at": "2026-09-14T23:00:00+05:30",
        "observer": {"kind": "test", "ref": "observer://cli-test"},
        "criteria": [
            {"id": item, "status": "UNOBSERVED", "evidence": [], "limitations": ["CLI dispatch test only."]}
            for item in [
                "deployment_target",
                "high_impact_governance",
                "operational_observability",
                "recovery_disaster",
                "runtime_direct_conformance",
            ]
        ],
        "limitations": ["CLI dispatch test only."],
        "authority": "UNCHANGED",
        "authorization": "UNCHANGED",
        "execution": "NONE",
        "mutation": "NONE",
        "publication_authorized": False,
        "deployment_authorized": False,
        "production_ready": False,
    }
    with tempfile.TemporaryDirectory() as temp_dir:
        packet_path = Path(temp_dir) / "packet.json"
        packet_path.write_text(json.dumps(target_packet), encoding="utf-8")
        target_result = run(
            "production-target-evidence",
            str(packet_path),
            "--expected-source-sha",
            "0" * 40,
            "--expected-target-id",
            "prod-cli-test",
            "--json",
        )
    assert target_result.returncode == 0, target_result.stdout + target_result.stderr
    target_payload = json.loads(target_result.stdout)
    assert target_payload["status"] == "HOLD", target_payload
    assert target_payload["production_ready"] is False, target_payload
    assert target_payload["readiness_promotion_allowed"] is False, target_payload
    assert target_payload["semantic_review_required"] is True, target_payload

    source = CLI.read_text(encoding="utf-8")
    assert "shell=True" not in source
    assert "subprocess.run([sys.executable" in source

    print(
        f"PASS: DevOS CLI version={canonical_version}, project-lifecycle, project-fleet, release-check, production-readiness, and production-target-evidence dispatch are deterministic and shell-free"
    )


if __name__ == "__main__":
    main()
