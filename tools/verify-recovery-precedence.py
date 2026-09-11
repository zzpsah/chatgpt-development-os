#!/usr/bin/env python3
"""Verify repository-first recovery precedence contract."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "resolve-recovery-precedence.py"
SPEC = ROOT / "docs" / "P11-FEDERATION-SELF-HEALING.md"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    require(TOOL.is_file(), "recovery precedence resolver missing")
    require(SPEC.is_file(), "P11 specification missing")
    text = TOOL.read_text(encoding="utf-8")
    spec = SPEC.read_text(encoding="utf-8")
    for source in ("source+git", "requirements+decisions", "ai-state", "generated-index", "ai-memory"):
        require(source in text, f"precedence source missing: {source}")
        require(source in spec.lower(), f"P11 specification missing precedence source: {source}")
    require("never authoritative" in text, "AI memory must never be authoritative")
    require("ESCALATE_REVIEW" in text, "semantic/recovery conflicts must escalate")
    require("PROCEED_WITH_SOURCE_AND_GIT" in text, "healthy recovery path missing")
    print("PASS: repository-first recovery precedence contract is valid")
    print("PASS: AI memory is supplementary and non-authoritative")
    print("PASS: conflict escalation path is explicit")


if __name__ == "__main__":
    main()
