#!/usr/bin/env python3
"""Verify the repository contract for Human Language Execution Engine v1."""
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "AGENTS.md",
    "core/human-language-routing.md",
    "core/human-language-execution-engine.md",
    "core/project-router.md",
    "core/human-command-interpreter.md",
    "tools/devos-command-interpreter.py",
    "tools/test-devos-command-interpreter.py",
    "workflows/resume.md",
    "workflows/bug-fix.md",
    "workflows/feature.md",
    "workflows/review.md",
    "rules/security.md",
]


def text(path):
    return (ROOT / path).read_text(encoding="utf-8")


def check(ok, message):
    print(("PASS: " if ok else "FAIL: ") + message)
    return ok


def main():
    failures = 0
    for path in REQUIRED_FILES:
        if not check((ROOT / path).is_file(), f"required file exists: {path}"):
            failures += 1
    if failures:
        return 1

    engine = text("core/human-language-execution-engine.md")
    routing = text("core/human-language-routing.md")
    router = text("core/project-router.md")
    security = text("rules/security.md")
    interpreter = text("tools/devos-command-interpreter.py")
    contract = text("core/human-command-interpreter.md")

    checks = [
        (all(x.lower() in engine.lower() for x in ("Human phrase", "Canonical intent", "Workflow", "Authorization", "Evidence", "Action", "Verification")),
         "engine defines the complete interpretation-to-verification pipeline"),
        (all(x.lower() in engine.lower() for x in ("RESUME_WORK", "BUG_FIX", "FEATURE_CHANGE", "VALIDATION", "SECURITY_REVIEW")),
         "engine defines core canonical intent families"),
        ("Multiple intents".lower() in engine.lower() and "compose" in engine.lower(),
         "engine defines safe multiple-intent composition"),
        ("Interpretation does not grant authority".lower() in engine.lower(),
         "engine preserves the authorization boundary"),
        (all(x.lower() in engine.lower() for x in ("Observed", "Likely", "Unknown")),
         "engine preserves the evidence model"),
        (all(x.lower() in engine.lower() for x in ("VERIFIED", "PARTIAL", "UNVERIFIED", "FAILED")),
         "engine defines verification outcome states"),
        ("semantic engineering intent".lower() in routing.lower(),
         "human-language routing remains semantic rather than keyword-only"),
        ("core/project-router.md" in engine and "selected repository and its project-local `.ai/` context remain authoritative".lower() in router.lower(),
         "engine delegates project selection to the authoritative Project Router"),
        ("Never infer success".lower() in engine.lower(),
         "engine prevents unsupported success claims"),
        ("authorization" in security.lower() and "least privilege" in security.lower(),
         "security baseline remains part of execution safety"),
        (re.search(r"No technical action is justified solely by emotional intensity", engine, re.I) is not None,
         "emotional language cannot independently authorize technical action"),
        ("P12-COMMAND-INTERPRETER-v1" in interpreter,
         "executable command interpreter declares a stable version"),
        (all(x in contract for x in ("continue", "continiue", "wahi se continue", "ok", "do it", "ruk ja")),
         "command interpreter contract documents casual command examples"),
        ("Interpretation never grants authorization" in contract,
         "command interpreter contract preserves authority separation"),
    ]

    for ok, message in checks:
        if not check(ok, message):
            failures += 1

    test = subprocess.run([sys.executable, str(ROOT / "tools/test-devos-command-interpreter.py")], cwd=ROOT, capture_output=True, text=True)
    if not check(test.returncode == 0, "executable Human Command Interpretation checks pass"):
        print(test.stdout)
        print(test.stderr)
        failures += 1

    print("\nResult:")
    if failures:
        print(f"FAIL — {failures} verification check(s) failed.")
        return 1
    print("PASS — Human Language Execution Engine v1 and Command Interpretation Layer v1 checks passed.")
    print("NOTE — This verifies repository contracts and deterministic examples, not general semantic AI behavior or application correctness.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
