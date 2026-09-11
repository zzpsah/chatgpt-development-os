#!/usr/bin/env python3
"""Verify the repository contract for Security Gate v1."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "AGENTS.md",
    "rules/security.md",
    "core/security-gate.md",
    "core/human-language-execution-engine.md",
    "core/verification-engine.md",
    "workflows/security.md",
    "workflows/review.md",
    "workflows/feature.md",
    "workflows/bug-fix.md",
    "workflows/resume.md",
]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def check(ok, message):
    print(("PASS: " if ok else "FAIL: ") + message)
    return ok


def main():
    failures = 0
    for path in REQUIRED_FILES:
        if not check((ROOT / path).is_file(), f"required file exists: {path}"):
            failures += 1
    if failures:
        print(f"\nResult: FAIL — {failures} required file(s) missing.")
        return 1

    gate = read("core/security-gate.md")
    engine = read("core/human-language-execution-engine.md")
    review = read("workflows/review.md")
    security = read("rules/security.md")
    workflow = read("workflows/security.md")

    checks = [
        (all(x.lower() in gate.lower() for x in ("Scope", "Authentication and authorization", "Data access and privacy", "Secrets and credentials", "Inputs and uploads", "Dependencies and configuration", "Runtime and deployment boundaries", "Verification")),
         "Security Gate defines the required review stages"),
        (all(x in gate for x in ("PASS", "CONDITIONAL", "BLOCKED", "NOT_APPLICABLE", "UNVERIFIED")),
         "Security Gate defines explicit decision states"),
        (all(x in gate for x in ("CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO")),
         "Security Gate defines finding severity"),
        (all(x.lower() in gate.lower() for x in ("Observed", "Likely", "Unknown")),
         "Security Gate preserves the evidence model"),
        ("100% secure".lower() in gate.lower() and "never state" in gate.lower(),
         "Security Gate prevents absolute-security claims"),
        ("No technical action is justified solely by emotional intensity".lower() in engine.lower(),
         "Human-language execution preserves authorization boundary"),
        ("workflows/security.md" in engine and "Security Gate" in engine,
         "security intent routes to dedicated Security Gate workflow"),
        ("workflows/security.md" in review and "core/security-gate.md" in review,
         "Review workflow delegates material security reviews to Security Gate"),
        (all(x.lower() in workflow.lower() for x in ("Scope", "evidence", "residual risk", "authorization", "verification")),
         "Security Gate workflow includes scope, evidence, risk, authorization, and verification"),
        (all(x.lower() in security.lower() for x in ("Never commit secrets", "least privilege", "row-level security", "student", "authorization")),
         "Security baseline retains core security controls"),
        ("Verification / Test Engine".lower() in review.lower(),
         "Review workflow remains integrated with Verification/Test Engine"),
    ]

    for ok, message in checks:
        if not check(ok, message):
            failures += 1

    print("\nResult:")
    if failures:
        print(f"FAIL — {failures} verification check(s) failed.")
        return 1
    print("PASS — Security Gate v1 contract checks passed.")
    print("NOTE — This verifies repository contracts, not complete application security.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
