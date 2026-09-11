#!/usr/bin/env python3
"""Verify safe deterministic context reconciliation boundaries."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "reconcile-derived-context.py"
SYNC = ROOT / "tools" / "context-sync.py"
FORBIDDEN = ("PROJECT.md", "DECISIONS.md", "TASKS.md", "CURRENT-STATE.md", "ARCHITECTURE.md")
DERIVED = ("STATE-INDEX.md", "CHANGELOG.md", "PROJECT-IDENTITY.json")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    require(TOOL.is_file(), "reconciliation tool missing")
    require(SYNC.is_file(), "canonical sync tool missing")
    text = TOOL.read_text(encoding="utf-8")
    for name in DERIVED:
        require(name in text, f"derived file not represented: {name}")
    for name in FORBIDDEN:
        require(name in text, f"forbidden semantic file not represented in safety boundary: {name}")
    require("unsafe" in text and "BLOCKED:" in text, "semantic reconciliation must be blocked")
    require("does not modify semantic project state" in text, "tool must declare semantic no-write boundary")
    require("context-sync.py" in text, "repair must delegate to canonical sync implementation")
    print("PASS: safe reconciliation boundaries are structurally valid")


if __name__ == "__main__":
    main()
