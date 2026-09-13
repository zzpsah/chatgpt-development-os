#!/usr/bin/env python3
"""Machine-derived, read-only DevOS foundation health and consistency status.

This module composes the existing Trust-First audit, readiness-evidence ledger,
and cross-host recovery-friction evidence. It does not create authority, execute
project work, mutate the repository, rewrite historical evidence, or promote
UNKNOWN/WARN to PASS.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = "DEVOS-FOUNDATION-HEALTH-v1"
CANONICAL_REPOSITORY = "zzpsah/chatgpt-development-os"
DEFAULT_HOST_PROFILE = "adapters/host-profile.example.json"
SEVERITY = {"PASS": 0, "WARN": 1, "UNKNOWN": 2, "FAIL": 3, "BLOCKED": 4}
INVARIANTS = [
    "PLAN != EXECUTION",
    "READY != EXECUTION",
    "INTERPRETATION != AUTHORIZATION",
    "OLD APPROVAL != NEW APPROVAL",
    "SIMULATED EVIDENCE != LIVE PROVIDER PROOF",
    "CHAT MEMORY != SOURCE OF TRUTH",
    "PROVIDER RESPONSE != COMPLETION PROOF",
    "RECOVERY != AUTOMATIC MUTATION REPLAY",
]


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if not spec or not spec.loader:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _row(name: str, status: str, reason: str, evidence: Any = None) -> dict[str, Any]:
    row = {"name": name, "status": status, "reason": reason}
    if evidence is not None:
        row["evidence"] = evidence
    return row


def _worst(rows: list[dict[str, Any]]) -> str:
    return max((row["status"] for row in rows), key=lambda value: SEVERITY[value], default="UNKNOWN")


def inspect_git(root: Path) -> dict[str, Any]:
    try:
        head = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=root, text=True, capture_output=True, check=False
        )
        if head.returncode != 0:
            return _row("git_source_state", "UNKNOWN", "Git metadata unavailable; remote/source freshness cannot be proven")
        head_sha = head.stdout.strip()
        status = subprocess.run(
            ["git", "status", "--porcelain"], cwd=root, text=True, capture_output=True, check=False
        )
        if status.returncode != 0:
            return _row("git_source_state", "UNKNOWN", "Git worktree state could not be inspected", {"head": head_sha})
        dirty = bool(status.stdout.strip())
        expected = os.environ.get("DEVOS_EXPECTED_HEAD") or os.environ.get("GITHUB_SHA")
        if expected and expected != head_sha:
            return _row(
                "git_source_state", "BLOCKED", "checked source HEAD does not match expected execution/source HEAD",
                {"head": head_sha, "expected_head": expected, "dirty": dirty},
            )
        if dirty:
            return _row("git_source_state", "WARN", "worktree has uncommitted source changes", {"head": head_sha, "dirty": True})
        return _row("git_source_state", "PASS", "Git worktree is clean and HEAD is internally consistent", {"head": head_sha, "dirty": False})
    except OSError as exc:
        return _row("git_source_state", "UNKNOWN", f"Git inspection unavailable: {exc}")


def inspect_ai_state(root: Path) -> dict[str, Any]:
    required = [".ai/manifest.yaml", ".ai/CURRENT-STATE.md", ".ai/TASKS.md", ".ai/DECISIONS.md"]
    missing = [rel for rel in required if not (root / rel).is_file()]
    if missing:
        return _row("ai_state_shape", "UNKNOWN", "required .ai durable-state files are missing", {"missing": missing})
    texts = {rel: (root / rel).read_text(encoding="utf-8") for rel in required}
    malformed = []
    if "canonical_repository: " + CANONICAL_REPOSITORY not in texts[".ai/manifest.yaml"]:
        malformed.append("manifest canonical_repository missing/mismatched")
    if "#" not in texts[".ai/CURRENT-STATE.md"]:
        malformed.append("CURRENT-STATE has no Markdown heading")
    if "## Active" not in texts[".ai/TASKS.md"]:
        malformed.append("TASKS is missing ## Active")
    if not texts[".ai/DECISIONS.md"].strip():
        malformed.append("DECISIONS is empty")
    if malformed:
        return _row("ai_state_shape", "FAIL", "durable .ai state is malformed", {"problems": malformed})
    return _row("ai_state_shape", "PASS", "required durable .ai state is structurally present")


def inspect_status_docs(root: Path, production_ready: bool, live_mutation_any: bool) -> dict[str, Any]:
    paths = [".ai/CURRENT-STATE.md", ".ai/TASKS.md", ".ai/DECISIONS.md", "docs/PRODUCTION-READINESS-EVIDENCE.md"]
    conflicts: list[str] = []
    merged_prs: set[str] = set()
    try:
        log = subprocess.run(
            ["git", "log", "-50", "--pretty=%B"], cwd=root, text=True, capture_output=True, check=False
        )
        if log.returncode == 0:
            merged_prs.update(re.findall(r"Merge PR #(\d+)", log.stdout))
    except OSError:
        pass
    for rel in paths:
        path = root / rel
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        lowered = text.lower()
        if not production_ready and re.search(r"production_ready\s*=\s*true", lowered):
            conflicts.append(f"{rel}: unsupported production_ready=true prose")
        if not live_mutation_any and re.search(r"live_mutation_proven\s*=\s*true", lowered):
            conflicts.append(f"{rel}: unsupported live_mutation_proven=true prose")
        for pr in merged_prs:
            for line in text.splitlines():
                low = line.lower()
                if f"pr #{pr}" in low and (" active" in low or "remains the active" in low or "until pr" in low):
                    conflicts.append(f"{rel}: merged PR #{pr} is still described as active")
                    break
    if conflicts:
        return _row("status_document_consistency", "WARN", "status prose conflicts with machine/Git-derived state", {"conflicts": sorted(set(conflicts))})
    return _row("status_document_consistency", "PASS", "no supported machine/prose contradiction detected")


def inspect_recovery_friction(root: Path, profile_rel: str = DEFAULT_HOST_PROFILE) -> tuple[dict[str, Any], dict[str, Any] | None]:
    """Compose the authoritative recovery-friction analyzer without reimplementing it."""
    try:
        profile_path = (root / profile_rel).resolve()
        if not profile_path.is_relative_to(root.resolve()):
            return _row("cross_host_recovery", "BLOCKED", "host profile path escapes repository"), None
        if not profile_path.is_file():
            return _row("cross_host_recovery", "UNKNOWN", "host profile is missing; recovery friction cannot be established", {"profile": profile_rel}), None
        profile = json.loads(profile_path.read_text(encoding="utf-8"))
        module = _load("recovery_friction_health", root / "tools" / "recovery-friction.py")
        report = module.analyze(root, profile)
    except json.JSONDecodeError as exc:
        return _row("cross_host_recovery", "BLOCKED", "host profile JSON is malformed", {"profile": profile_rel, "error": str(exc)}), None
    except (OSError, RuntimeError, ValueError, TypeError) as exc:
        return _row("cross_host_recovery", "UNKNOWN", "recovery-friction evidence could not be inspected", {"profile": profile_rel, "error": str(exc)}), None

    status = report.get("overall", "UNKNOWN")
    if status not in SEVERITY:
        status = "BLOCKED"
    evidence = {
        "protocol": report.get("protocol"),
        "evidence_class": report.get("evidence_class"),
        "real_cross_vendor_account_proven": report.get("real_cross_vendor_account_proven", False),
        "recovery_status": report.get("recovery_status", "UNKNOWN"),
        "continuation_status": report.get("continuation_status", "UNKNOWN"),
        "friction": report.get("friction", {}),
        "host": report.get("host", {}),
        "repository_state": report.get("repository_state", {}),
    }
    if report.get("real_cross_vendor_account_proven") is not False:
        return _row("cross_host_recovery", "BLOCKED", "deterministic recovery evidence attempted unsupported real cross-vendor/account promotion", evidence), report
    reason = (
        f"recovery={report.get('recovery_status', 'UNKNOWN')}; "
        f"continuation={report.get('continuation_status', 'UNKNOWN')}; "
        f"friction_units={report.get('friction', {}).get('friction_units', 'UNKNOWN')}"
    )
    return _row("cross_host_recovery", status, reason, evidence), report


def derive_health(root: Path = ROOT, *, run_checks: bool = True, host_profile: str = DEFAULT_HOST_PROFILE) -> dict[str, Any]:
    root = root.resolve()
    audit_mod = _load("devos_audit_health", root / "tools" / "devos-audit.py")
    evidence_mod = _load("readiness_evidence_health", root / "tools" / "verify-readiness-evidence.py")

    audit = audit_mod.audit(root, run_checks=run_checks)
    ledger_path = root / "config" / "readiness-evidence.json"
    ledger_errors: list[str]
    drift: list[str]
    ledger: dict[str, Any]
    try:
        ledger = evidence_mod.read_json(ledger_path)
        ledger_errors = evidence_mod.validate(ledger, root)
        drift = evidence_mod.historical_source_drift(ledger, root)
    except (OSError, ValueError, TypeError, KeyError) as exc:
        ledger = {}
        ledger_errors = [str(exc)]
        drift = []

    rows: list[dict[str, Any]] = []
    identity = audit.get("identity", {})
    if identity.get("result") == "FAIL":
        rows.append(_row("canonical_identity", "BLOCKED", identity.get("reason", "canonical repository identity mismatch"), identity))
    elif identity.get("result") == "PASS":
        rows.append(_row("canonical_identity", "PASS", "canonical repository identity verified", identity))
    else:
        rows.append(_row("canonical_identity", "UNKNOWN", "canonical repository identity is not proven", identity))

    bundle = audit.get("bundle", {})
    if bundle.get("dependency_closed") is True:
        rows.append(_row("dependency_closure", "PASS", "declared audit dependency closure is complete"))
    else:
        rows.append(_row("dependency_closure", "UNKNOWN", "declared audit dependency closure is incomplete", bundle.get("missing_paths", [])))

    checks = {row.get("name"): row for row in audit.get("checks", []) if isinstance(row, dict)}
    for label, source in [
        ("p15_interpretation", "interpretation"),
        ("p16_planning", "planning"),
        ("p17_readiness", "readiness"),
        ("security_gate_wiring", "security_gate"),
    ]:
        item = checks.get(source)
        if item is None:
            rows.append(_row(label, "UNKNOWN", f"authoritative audit does not expose {source} check"))
        elif item.get("result") == "PASS":
            rows.append(_row(label, "PASS", item.get("reason", "declared check passed")))
        elif item.get("result") == "FAIL":
            rows.append(_row(label, "FAIL", item.get("reason", "declared check failed"), item))
        else:
            rows.append(_row(label, "UNKNOWN", item.get("reason", "declared check is not proven"), item))

    rows.append(inspect_git(root))
    rows.append(inspect_ai_state(root))

    if ledger_errors:
        rows.append(_row("capability_evidence_consistency", "FAIL", "readiness evidence ledger is inconsistent", {"errors": ledger_errors}))
    else:
        rows.append(_row("capability_evidence_consistency", "PASS", "readiness evidence ledger validates conservatively"))

    if drift:
        rows.append(_row("historical_source_freshness", "WARN", "historical evidence source differs from current source; history remains pinned", {"historical_source_drift": drift}))
    else:
        rows.append(_row("historical_source_freshness", "PASS", "no current-source drift detected for pinned historical test evidence"))

    missing_evidence = []
    live_mutation_any = False
    for capability in ledger.get("capabilities", []) if isinstance(ledger.get("capabilities"), list) else []:
        if not isinstance(capability, dict):
            continue
        if capability.get("live_mutation_proven") is True:
            live_mutation_any = True
        if capability.get("implementation") in {"implemented", "partial"} and not capability.get("evidence"):
            missing_evidence.append(capability.get("id"))
    if missing_evidence:
        rows.append(_row("verification_evidence_presence", "UNKNOWN", "implemented/partial capabilities lack verification evidence", {"capabilities": missing_evidence}))
    else:
        rows.append(_row("verification_evidence_presence", "PASS", "implemented/partial capabilities have declared evidence records"))

    recovery_row, recovery_report = inspect_recovery_friction(root, host_profile)
    rows.append(recovery_row)

    production_ready = ledger.get("production_ready") is True
    rows.append(inspect_status_docs(root, production_ready, live_mutation_any))

    overall = _worst(rows)
    return {
        "protocol": PROTOCOL,
        "repository": CANONICAL_REPOSITORY,
        "mode": "READ_ONLY",
        "authority": "UNCHANGED",
        "authorization": "UNCHANGED",
        "execution": "NONE",
        "mutation": "NONE",
        "overall": overall,
        "checks": rows,
        "audit_protocol": audit.get("protocol"),
        "audit_overall": audit.get("overall"),
        "evidence_protocol": ledger.get("protocol"),
        "recovery_friction": recovery_report,
        "production_ready": bool(ledger.get("production_ready") is True),
        "live_mutation_proven": live_mutation_any,
        "historical_source_drift": drift,
        "invariants": INVARIANTS,
        "universal_product_goal": "AI A + Account A -> repository -> AI B + Account B -> correct state recovery -> safe continuation",
        "limitations": [
            "Offline health cannot prove remote Git freshness unless the caller supplies an expected HEAD.",
            "Historical evidence drift is WARN, never silently refreshed or promoted.",
            "Recovery-friction host-profile evidence is deterministic simulation, not an independent cross-vendor/account trial.",
            "Doctor/health status never creates execution authority or production readiness.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument("--no-run-checks", action="store_true")
    parser.add_argument("--host-profile", default=DEFAULT_HOST_PROFILE)
    args = parser.parse_args()
    try:
        report = derive_health(Path(args.root), run_checks=not args.no_run_checks, host_profile=args.host_profile)
    except Exception as exc:  # fail closed at the presentation boundary
        report = {
            "protocol": PROTOCOL,
            "mode": "READ_ONLY",
            "authority": "UNCHANGED",
            "authorization": "UNCHANGED",
            "execution": "NONE",
            "mutation": "NONE",
            "overall": "FAIL",
            "checks": [_row("health_engine", "FAIL", str(exc))],
        }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report.get("overall") == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
