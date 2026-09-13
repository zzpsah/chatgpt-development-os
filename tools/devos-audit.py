#!/usr/bin/env python3
"""Read-only Trust-First audit for a DevOS checkout or supplied source pack.

The audit distinguishes repository absence from audit-pack incompleteness. It
never grants authorization, executes project work, or mutates the audited root.
It may execute explicitly declared deterministic verification scripts when
--run-checks is used (default), all of which are expected to be repository-read
only and/or use temporary test fixtures/provider fakes.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
from typing import Any

PROTOCOL = "DEVOS-TRUST-AUDIT-v1"
CANONICAL_REPOSITORY = "zzpsah/chatgpt-development-os"

CHECKS: dict[str, dict[str, Any]] = {
    "bootstrap": {
        "entrypoint": "tools/test-devos-bootstrap.py",
        "dependencies": [
            "tools/test-devos-bootstrap.py",
            "tools/devos-bootstrap.py",
            "AGENTS.md",
            ".ai/manifest.yaml",
            ".ai/CURRENT-STATE.md",
            "core/ai-bootstrap-protocol.md",
        ],
    },
    "planning": {
        "entrypoint": "tools/test-semantic-goal-to-plan.py",
        "dependencies": [
            "tools/test-semantic-goal-to-plan.py",
            "tools/semantic-goal-to-plan.py",
        ],
    },
    "readiness": {
        "entrypoint": "tools/test-step-readiness-orchestrator.py",
        "dependencies": [
            "tools/test-step-readiness-orchestrator.py",
            "tools/step-readiness-orchestrator.py",
            "tools/semantic-goal-to-plan.py",
        ],
    },
    "security_gate": {
        "entrypoint": "tools/verify-security-gate.py",
        "dependencies": [
            "tools/verify-security-gate.py",
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
        ],
    },
    "security_adversarial": {
        "entrypoint": "tools/test-security-boundary-adversarial.py",
        "dependencies": [
            "tools/test-security-boundary-adversarial.py",
            "tools/step-readiness-orchestrator.py",
            "tools/semantic-goal-to-plan.py",
            "tools/devos-runtime-handoff.py",
            "tools/devos-bootstrap.py",
            "AGENTS.md",
            ".ai/manifest.yaml",
            ".ai/CURRENT-STATE.md",
            "core/ai-bootstrap-protocol.md",
        ],
    },
    "controlled_mutation": {
        "entrypoint": "tools/test-controlled-remote-mutation-proof.py",
        "dependencies": [
            "tools/test-controlled-remote-mutation-proof.py",
            "tools/controlled-remote-mutation-proof.py",
            "tools/runtime-adapter-bridge.py",
            "adapters/reference-host.py",
            "adapters/github-reference.py",
        ],
    },
}

DOCUMENTATION = [
    "README.md",
    ".ai/CURRENT-STATE.md",
    ".ai/TASKS.md",
    ".ai/DECISIONS.md",
    "docs/DEVOS-MATURITY-ROADMAP.md",
    "core/step-readiness-authorization-orchestrator.md",
]


def manifest() -> list[str]:
    paths = set(DOCUMENTATION)
    for check in CHECKS.values():
        paths.update(check["dependencies"])
    return sorted(paths)


def _exists(root: Path, rel: str) -> bool:
    try:
        path = (root / rel).resolve()
        return path.is_relative_to(root.resolve()) and path.is_file()
    except (OSError, ValueError):
        return False


def inspect_identity(root: Path) -> dict[str, Any]:
    required = [".ai/manifest.yaml", "AGENTS.md"]
    missing = [rel for rel in required if not _exists(root, rel)]
    if missing:
        return {"result": "UNKNOWN", "evidence": "PACK_INCOMPLETE", "missing": missing}
    manifest_text = (root / ".ai/manifest.yaml").read_text(encoding="utf-8")
    agents_text = (root / "AGENTS.md").read_text(encoding="utf-8")
    manifest_ok = f"canonical_repository: {CANONICAL_REPOSITORY}" in manifest_text
    agents_ok = CANONICAL_REPOSITORY in agents_text and "core/ai-bootstrap-protocol.md" in agents_text
    ok = manifest_ok and agents_ok
    return {
        "result": "PASS" if ok else "FAIL",
        "evidence": "VERIFIED" if ok else "BLOCKED",
        "reason": "canonical repository identity fields match" if ok else "canonical repository identity mismatch",
    }


def inspect_check(root: Path, name: str, *, run_checks: bool) -> dict[str, Any]:
    spec = CHECKS[name]
    missing = [rel for rel in spec["dependencies"] if not _exists(root, rel)]
    row: dict[str, Any] = {
        "name": name,
        "entrypoint": spec["entrypoint"],
        "dependencies": list(spec["dependencies"]),
        "missing": missing,
    }
    if missing:
        row.update({
            "result": "UNKNOWN",
            "evidence": "PACK_INCOMPLETE",
            "reason": "advertised check cannot run because supplied source is missing declared dependencies",
        })
        return row
    if not run_checks:
        row.update({"result": "PASS", "evidence": "OBSERVED", "reason": "dependency closure present; execution not requested"})
        return row

    completed = subprocess.run(
        [sys.executable, str(root / spec["entrypoint"])],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    row["exit_code"] = completed.returncode
    row["stdout"] = completed.stdout.strip()
    row["stderr"] = completed.stderr.strip()
    if completed.returncode == 0:
        row.update({"result": "PASS", "evidence": "VERIFIED", "reason": "declared regression/check executed successfully"})
    else:
        row.update({"result": "FAIL", "evidence": "VERIFIED", "reason": "declared regression/check executed and failed"})
    return row


def inspect_docs(root: Path) -> dict[str, Any]:
    missing = [rel for rel in DOCUMENTATION if not _exists(root, rel)]
    return {
        "result": "UNKNOWN" if missing else "PASS",
        "evidence": "PACK_INCOMPLETE" if missing else "OBSERVED",
        "missing": missing,
        "note": "Presence is not semantic consistency proof; GitHub Issue #1 is external and not inferable from an offline pack.",
    }


def audit(root: Path, *, run_checks: bool = True) -> dict[str, Any]:
    root = root.resolve()
    checks = [inspect_check(root, name, run_checks=run_checks) for name in CHECKS]
    required = manifest()
    missing_manifest = [rel for rel in required if not _exists(root, rel)]
    identity = inspect_identity(root)

    if identity["result"] == "FAIL":
        overall = "BLOCKED"
    elif any(row["result"] == "FAIL" for row in checks):
        overall = "FAIL"
    elif missing_manifest or any(row["result"] == "UNKNOWN" for row in checks):
        overall = "UNKNOWN"
    else:
        overall = "PASS"

    return {
        "protocol": PROTOCOL,
        "repository": CANONICAL_REPOSITORY,
        "root": str(root),
        "mode": "READ_ONLY",
        "authority": "UNCHANGED",
        "authorization": "UNCHANGED",
        "execution": "NONE",
        "mutation": "NONE",
        "overall": overall,
        "identity": identity,
        "bundle": {
            "required_paths": required,
            "missing_paths": missing_manifest,
            "dependency_closed": not missing_manifest,
            "classification": "COMPLETE_FOR_ADVERTISED_CHECKS" if not missing_manifest else "PACK_INCOMPLETE",
            "rule": "NOT_INCLUDED_IN_AUDIT_PACK != NOT_PRESENT_IN_DEVOS",
        },
        "checks": checks,
        "documentation": inspect_docs(root),
        "external_unknowns": [
            "GitHub Issue #1 state/content is not proven by an offline source pack",
            "live-provider mutation is not proven by provider-simulated controlled-mutation tests",
            "production readiness is not implied by this audit",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="repository or unpacked audit-pack root")
    parser.add_argument("--no-run-checks", action="store_true", help="inspect dependency closure only")
    parser.add_argument("--manifest", action="store_true", help="print the dependency-closed audit-pack manifest only")
    args = parser.parse_args()

    if args.manifest:
        print("\n".join(manifest()))
        return 0

    report = audit(Path(args.root), run_checks=not args.no_run_checks)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["overall"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
