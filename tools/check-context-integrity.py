#!/usr/bin/env python3
"""Check durable DevOS context freshness and integrity without mutating the project."""
from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path

ROOT = Path.cwd()
CONTEXT = ROOT / os.environ.get("DEVOS_CONTEXT_DIRECTORY", ".ai")
REQUIRED = [
    CONTEXT / "manifest.yaml",
    CONTEXT / "PROJECT.md",
    CONTEXT / "CURRENT-STATE.md",
    CONTEXT / "ARCHITECTURE.md",
    CONTEXT / "DECISIONS.md",
    CONTEXT / "TASKS.md",
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
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED if not path.is_file()]
    if missing:
        fail("required context files missing: " + ", ".join(missing))

    manifest = (CONTEXT / "manifest.yaml").read_text(encoding="utf-8")
    index = (CONTEXT / "STATE-INDEX.md").read_text(encoding="utf-8")
    state = (CONTEXT / "CURRENT-STATE.md").read_text(encoding="utf-8")

    version = extract(r"^context_version:\s*(\d+)\s*$", manifest, "context_version")
    if int(version) < 1:
        fail("context_version must be >= 1")
    if "specification: portable-project-context" not in manifest:
        fail("unsupported manifest specification")
    if "managed_by: development-os" not in manifest:
        fail("manifest does not identify Development OS")

    head = git("rev-parse", "HEAD")
    indexed_head = extract(r"^- HEAD:\s*([^\s]+)\s*$", index, "STATE-INDEX HEAD")
    if indexed_head != head:
        fail(f"STATE-INDEX HEAD {indexed_head} does not match repository HEAD {head}")

    status = git("status", "--short")
    if status:
        fail("working tree is dirty during integrity check: " + status.replace("\n", " | "))

    current_commit = re.search(r"^- Commit:\s*([0-9a-f]{40})\s*$", state, flags=re.MULTILINE)
    if current_commit:
        recorded = current_commit.group(1)
        if subprocess.run(["git", "cat-file", "-e", f"{recorded}^{{commit}}"], cwd=ROOT).returncode != 0:
            fail(f"CURRENT-STATE references missing commit {recorded}")

    print("PASS: required durable context files are present")
    print(f"PASS: manifest compatibility version is {version}")
    print(f"PASS: STATE-INDEX matches repository HEAD {head}")
    print("PASS: repository working tree is clean")
    print("PASS: CURRENT-STATE recorded commit is valid when present")
    print("RESULT: durable context integrity is healthy")


if __name__ == "__main__":
    main()
