#!/usr/bin/env python3
"""Verify the repository-level contract and integration of AI State Resolver v1.

This is intentionally a contract/integration verifier, not a semantic AI test.
It proves that the resolver specification exists, resume wiring is present, and
key safety/evidence rules remain synchronized with the roadmap.
"""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "AGENTS.md",
    "core/project-router.md",
    "core/ai-state-resolver.md",
    "core/ai-bootstrap-protocol.md",
    "workflows/resume.md",
    "docs/ROADMAP.md",
]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def check(condition, message):
    if condition:
        print(f"PASS: {message}")
        return True
    print(f"FAIL: {message}")
    return False


def contains(text, needle):
    return needle.lower() in text.lower()


def main():
    failures = 0

    for rel in REQUIRED_FILES:
        if not check((ROOT / rel).is_file(), f"required file exists: {rel}"):
            failures += 1

    if failures:
        print(f"\nState Resolver verification failed: {failures} missing required file(s).")
        return 1

    resolver = read("core/ai-state-resolver.md")
    resume = read("workflows/resume.md")
    router = read("core/project-router.md")
    roadmap = read("docs/ROADMAP.md")
    agents = read("AGENTS.md")

    resolver_checks = [
        (all(contains(resolver, x) for x in ("Observed", "Likely", "Unknown")),
         "resolver evidence model includes Observed / Likely / Unknown"),
        (contains(resolver, "recommended:"), "resolver output contract includes recommended action"),
        (contains(resolver, "authorization:"), "resolver output contract includes authorization"),
        (contains(resolver, "verification:"), "resolver output contract includes verification status/evidence"),
        (contains(resolver, "source inspection remains mandatory"), "resolver preserves mandatory source inspection"),
        (contains(resolver, "Priority"), "resolver defines unfinished-work prioritization"),
    ]

    resume_checks = [
        (contains(resume, "core/project-router.md"), "resume workflow invokes the Project Router"),
        (contains(resume, "AI State Resolver v1"), "resume workflow invokes AI State Resolver v1"),
        (contains(resume, "core/ai-state-resolver.md"), "resume workflow references resolver specification"),
        (contains(resume, "Observed / Likely / Unknown"), "resume workflow applies the evidence model"),
        (contains(resume, "Priority + risk + authorization"), "resume workflow applies priority/risk/authorization"),
        (contains(resume, "Inspect source → Implement → Verify → Persist"), "resume workflow preserves execution/verification loop"),
        (contains(resume, "Persist meaningful semantic progress"), "resume workflow persists semantic progress"),
    ]

    integration_checks = [
        (contains(router, "instead of guessing") and contains(router, "project-local `.ai/` context"),
         "project routing rejects guessing and keeps project-local context authoritative"),
        (contains(agents, "verification performed") and contains(agents, "tested facts"),
         "AGENTS completion standard requires evidence-backed verification"),
        (re.search(r"\[x\]\s+Integrate with resume workflow", roadmap, re.I) is not None,
         "roadmap marks resume integration complete"),
        (re.search(r"\[ \]\s+End-to-end verification", roadmap, re.I) is not None,
         "roadmap keeps end-to-end verification open until this verifier is actually executed"),
    ]

    for ok, message in resolver_checks + resume_checks + integration_checks:
        if not check(ok, message):
            failures += 1

    print("\nResult:")
    if failures:
        print(f"FAIL — {failures} verification check(s) failed.")
        return 1

    print("PASS — AI State Resolver v1 contract/integration checks passed.")
    print("NOTE — This does not prove semantic AI behavior, project correctness, or application tests.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
