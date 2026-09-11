#!/usr/bin/env python3
"""Verify the durable DevOS context integrity checker contract."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "check-context-integrity.py"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    require(TOOL.is_file(), "context integrity checker is missing")
    text = TOOL.read_text(encoding="utf-8")
    for needle in (
        'STATE-INDEX HEAD',
        'git("rev-parse", "HEAD")',
        'git("status", "--short")',
        'manifest.yaml',
        'CURRENT-STATE.md',
        'cat-file',
        'DRIFT:',
        'RESULT: durable context integrity is healthy',
    ):
        require(needle in text, f"integrity checker contract missing {needle!r}")
    print("PASS: durable context freshness/integrity checker contract is valid")


if __name__ == "__main__":
    main()
