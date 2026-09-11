#!/usr/bin/env python3
"""Verify the repository contract for Teaching Engine v1."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def check(ok, message):
    print(("PASS: " if ok else "FAIL: ") + message)
    return ok


def main():
    failures = 0
    required = ["core/teaching-engine.md", "core/human-language-routing.md", "core/human-language-execution-engine.md", "core/verification-engine.md", "rules/security.md"]
    for path in required:
        if not check((ROOT / path).is_file(), f"required file exists: {path}"):
            failures += 1
    if failures:
        return 1

    teaching = read("core/teaching-engine.md")
    routing = read("core/human-language-routing.md")
    engine = read("core/human-language-execution-engine.md")

    checks = [
        (all(x in teaching for x in ("DO", "TEACH", "EXPLAIN")), "Teaching Engine defines all learning modes"),
        (all(x in teaching for x in ("Mental model", "Technical name", "Concrete example", "Internal/X-ray view", "Verification")), "Teaching Engine defines progressive teaching sequence"),
        (all(x in teaching for x in ("Level 1", "Level 2", "Level 3", "Level 4")), "Teaching Engine defines progressive depth levels"),
        (all(x in teaching for x in ("Observed", "Likely", "Unknown")), "Teaching Engine preserves evidence model"),
        (all(x in teaching for x in ("VERIFIED", "PARTIAL", "UNVERIFIED", "FAILED")), "Teaching Engine preserves verification states"),
        ("Teaching Engine" in routing and "teach me" in routing, "Human-language routing recognizes teaching intent"),
        ("authorization" in teaching.lower() and "does not grant authorization" in teaching.lower(), "Teaching mode does not bypass authorization"),
        ("Never expose secrets" in teaching and "private keys" in teaching, "Teaching Engine protects sensitive credentials"),
        ("core/teaching-engine.md" in routing, "Routing delegates teaching presentation to Teaching Engine"),
        ("Human Language Execution Engine" in teaching and "Verification" in teaching, "Teaching Engine remains integrated with execution and verification"),
    ]
    for ok, message in checks:
        if not check(ok, message):
            failures += 1

    print("\nResult:")
    if failures:
        print(f"FAIL — {failures} verification check(s) failed.")
        return 1
    print("PASS — Teaching Engine v1 contract checks passed.")
    print("NOTE — This verifies repository contracts, not user mastery.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
