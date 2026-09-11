#!/usr/bin/env python3
"""Verify bounded deterministic derived-context self-healing."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "self-heal-derived-context.py"
DERIVED = ("STATE-INDEX.md", "CHANGELOG.md", "PROJECT-IDENTITY.json")
SEMANTIC = ("PROJECT.md", "DECISIONS.md", "TASKS.md", "CURRENT-STATE.md", "ARCHITECTURE.md")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    require(TOOL.is_file(), "self-healer is missing")
    text = TOOL.read_text(encoding="utf-8")
    require('DERIVED = {"STATE-INDEX.md", "CHANGELOG.md", "PROJECT-IDENTITY.json"}' in text, "derived allowlist missing")
    require("BLOCKED:" in text, "unsafe requests must be blocked")
    require("semantic project state" in text, "semantic-state safety boundary missing")
    require("BOUNDARY: semantic project state unchanged" in text, "self-heal must declare semantic no-write boundary")
    for name in DERIVED:
        require(name in text, f"derived target missing: {name}")
    allowlist = text.split("DERIVED =", 1)[1].split("SEMANTIC =", 1)[0]
    for name in SEMANTIC:
        require(name not in allowlist, f"semantic file leaked into derived allowlist: {name}")
    require("rev-parse" in text and "log" in text, "self-healer must derive artifacts from Git evidence")
    print("PASS: deterministic derived-context self-healing contract is valid")
    print("PASS: semantic project files remain outside the self-healing allowlist")


if __name__ == "__main__":
    main()
