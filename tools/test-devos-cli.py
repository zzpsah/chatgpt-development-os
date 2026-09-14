#!/usr/bin/env python3
"""Regression checks for the small cross-platform DevOS CLI dispatcher."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "tools" / "devos.py"


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CLI), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def main() -> None:
    direct = run("version")
    assert direct.returncode == 0, direct.stderr
    assert direct.stdout.strip() == "0.17.0", direct.stdout

    flag = run("--version")
    assert flag.returncode == 0, flag.stderr
    assert flag.stdout.strip() == "0.17.0", flag.stdout

    release = run("release-check", "--no-git", "--json")
    assert release.returncode == 0, release.stdout + release.stderr
    payload = json.loads(release.stdout)
    assert payload["status"] == "READY", payload
    assert payload["production_ready"] is False
    assert payload["execution"] == "NONE"
    assert payload["mutation"] == "NONE"

    source = CLI.read_text(encoding="utf-8")
    assert "shell=True" not in source
    assert "subprocess.run([sys.executable" in source

    print("PASS: DevOS CLI version and release-check dispatch are deterministic and shell-free")


if __name__ == "__main__":
    main()
