#!/usr/bin/env python3
"""Check durable DevOS context freshness and integrity without mutating the project."""
from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path

ROOT = Path.cwd()
CONTEXT = ROOT / os.environ.get("DEVOS_CONTEXT_DIRECTORY", ".ai")
CORE_REQUIRED = [
    CONTEXT / "manifest.yaml",
    CONTEXT / "PROJECT.md",
    CONTEXT / "CURRENT-STATE.md",
    CONTEXT / "ARCHITECTURE.md",
    CONTEXT / "DECISIONS.md",
    CONTEXT / "TASKS.md",
]
DERIVED = [
    CONTEXT / "STATE-INDEX.md",
    CONTEXT / "CHANGELOG.md",
]


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, text=True, capture_output=True, check=True
    ).stdout.strip()


def fail(message: str) -> None:
    raise SystemExit(f"DRIFT: {message}")


def extract(pattern: str, text: str, label: str) -> str:
    match = re.search(pattern, text, flags=re.MULTILINE)
    if not match:
        fail(f"{label} is missing")
    return match.group(1).strip()


def main() -> None:
    missing_core = [str(path.relative_to(ROOT)) for path in CORE_REQUIRED if not path.is_file()]
    if missing_core:
        fail("required semantic context files missing: " + ", ".join(missing_core))

    manifest = (CONTEXT / "manifest.yaml").read_text(encoding="utf-8")
    state = (CONTEXT / "CURRENT-STATE.md").read_text(encoding="utf-8")
    head = git("rev-parse", "HEAD")

    version = extract(r"^context_version:\s*(\d+)\s*$", manifest, "context_version")
    if int(version) < 1:
        fail("context_version must be >= 1")
    if "specification: portable-project-context" not in manifest:
        fail("unsupported manifest specification")
    if "managed_by: development-os" not in manifest:
        fail("manifest does not identify Development OS")

    status = git("status", "--short")
    if status:
        fail("working tree is dirty during integrity check: " + status.replace("\n", " | "))

    derived_missing = [str(path.relative_to(ROOT)) for path in DERIVED if not path.is_file()]
    if derived_missing and os.environ.get("DEVOS_ALLOW_MISSING_DERIVED", "false").lower() != "true":
        fail("derived context files missing: " + ", ".join(derived_missing))

    index_path = CONTEXT / "STATE-INDEX.md"
    if index_path.exists():
        index = index_path.read_text(encoding="utf-8")
        indexed_head = extract(r"^- HEAD:\s*([^\s]+)\s*$", index, "STATE-INDEX HEAD")
        if indexed_head != head:
            fail(f"STATE-INDEX HEAD {indexed_head} does not match repository HEAD {head}")
    elif os.environ.get("DEVOS_ALLOW_MISSING_DERIVED", "false").lower() == "true":
        print("WARN: STATE-INDEX.md is missing and is treated as repairable derived drift")

    current_commit = re.search(r"^- Commit:\s*([0-9a-f]{40})\s*$", state, flags=re.MULTILINE)
    if current_commit:
        recorded = current_commit.group(1)
        if subprocess.run(["git", "cat-file", "-e", f"{recorded}^{{commit}}"], cwd=ROOT).returncode != 0:
            fail(f"CURRENT-STATE references missing commit {recorded}")

    if not (CONTEXT / "CHANGELOG.md").exists() and os.environ.get("DEVOS_ALLOW_MISSING_DERIVED", "false").lower() == "true":
        print("WARN: CHANGELOG.md is missing and is treated as repairable derived drift")

    print("PASS: required semantic durable context files are present")
    print(f"PASS: manifest compatibility version is {version}")
    if index_path.exists():
        print(f"PASS: STATE-INDEX matches repository HEAD {head}")
    print("PASS: repository working tree is clean")
    print("PASS: CURRENT-STATE recorded commit is valid when present")
    print("RESULT: durable context integrity is healthy")


if __name__ == "__main__":
    main()
