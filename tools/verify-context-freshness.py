#!/usr/bin/env python3
"""Detect freshness/integrity drift in a DevOS-managed project."""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path.cwd()
CONTEXT = ROOT / ".ai"
INDEX = CONTEXT / "STATE-INDEX.md"
REQUIRED = [
    CONTEXT / "manifest.yaml",
    CONTEXT / "PROJECT.md",
    CONTEXT / "CURRENT-STATE.md",
    CONTEXT / "DECISIONS.md",
    CONTEXT / "TASKS.md",
    CONTEXT / "CHANGELOG.md",
    INDEX,
]


def git(*args: str) -> str:
    result = subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True, check=False)
    return result.stdout.strip()


def fail(message: str) -> None:
    raise SystemExit(f"DRIFT: {message}")


def main() -> None:
    for path in REQUIRED:
        if not path.exists():
            fail(f"missing required context file: {path.relative_to(ROOT)}")

    head = git("rev-parse", "HEAD")
    index_text = INDEX.read_text(encoding="utf-8")
    match = re.search(r"^- HEAD: ([0-9a-f]{40})$", index_text, re.MULTILINE)
    if not match:
        fail("STATE-INDEX.md does not contain a valid HEAD")
    indexed_head = match.group(1)
    if indexed_head != head:
        fail(f"STATE-INDEX.md HEAD {indexed_head} differs from Git HEAD {head}")

    status = git("status", "--porcelain")
    unmanaged = [line for line in status.splitlines() if line and not line.endswith(".ai/STATE-INDEX.md")]
    if unmanaged:
        fail("working tree contains unpersisted changes outside derived index")

    for marker in ("Generated automatically by Development OS.", "Deterministic repository/context evidence"):
        if marker not in index_text:
            fail(f"STATE-INDEX.md missing integrity marker: {marker}")

    print("PASS: DevOS context freshness/integrity check is healthy")
    print(f"PASS: context index matches Git HEAD {head}")


if __name__ == "__main__":
    main()
