#!/usr/bin/env python3
"""Regression checks for the small cross-platform DevOS CLI dispatcher."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

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

    source = CLI.read_text(encoding="utf-8")
    assert "shell=True" not in source
    assert "subprocess.run([sys.executable" in source

    print(
        f"PASS: DevOS CLI version={canonical_version}, release-check, and production-readiness dispatch are deterministic and shell-free"
    )


if __name__ == "__main__":
    main()
