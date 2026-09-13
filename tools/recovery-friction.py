#!/usr/bin/env python3
"""Measure repository-only DevOS recovery/onboarding friction for a host profile.

This is a read-only diagnostic. It does not authorize or execute project work,
mutate repository state, rewrite evidence, or claim a real cross-vendor/account
trial from a deterministic host-profile simulation.
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

PROTOCOL = "DEVOS-RECOVERY-FRICTION-v1"
CANONICAL_REPOSITORY = "zzpsah/chatgpt-development-os"
CANONICAL_URL = "https://github.com/zzpsah/chatgpt-development-os"

REQUIRED_REPOSITORY_INPUTS = (
    "AGENTS.md",
    ".ai/manifest.yaml",
    ".ai/CURRENT-STATE.md",
    ".ai/TASKS.md",
    ".ai/DECISIONS.md",
    "core/ai-bootstrap-protocol.md",
    "core/project-router.md",
    "docs/handoff/README.md",
)

CRITICAL_RECOVERY_CAPABILITIES = {
    "project_discovery", "bootstrap", "inspection", "state_resolution",
}
CONTINUATION_CAPABILITIES = {
    "intent_routing", "execution", "verification", "persistence",
}
SEVERITY = {"PASS": 0, "WARN": 1, "UNKNOWN": 2, "BLOCKED": 3}


def _load_host_validator(root: Path):
    path = root / "tools" / "verify-host-profile.py"
    spec = importlib.util.spec_from_file_location("devos_host_profile_for_recovery", path)
    if not spec or not spec.loader:
        raise RuntimeError("host-profile validator unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _read(root: Path, rel: str) -> str | None:
    path = root / rel
    try:
        resolved = path.resolve()
        if not resolved.is_relative_to(root.resolve()) or not resolved.is_file():
            return None
        return resolved.read_text(encoding="utf-8")
    except (OSError, UnicodeError, ValueError):
        return None


def _git_head(root: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=root, text=True,
            capture_output=True, check=False,
        )
    except OSError:
        return None
    return result.stdout.strip() if result.returncode == 0 else None


def _status(items: list[str], critical: bool = False) -> str:
    if not items:
        return "PASS"
    return "BLOCKED" if critical else "UNKNOWN"


def _worst(*statuses: str) -> str:
    return max(statuses, key=lambda value: SEVERITY[value])


def analyze(root: Path, profile: dict[str, Any], *, expected_head: str | None = None) -> dict[str, Any]:
    root = root.resolve()
    missing_inputs = [rel for rel in REQUIRED_REPOSITORY_INPUTS if _read(root, rel) is None]
    ambiguous: list[str] = []
    blocked: list[str] = []

    manifest = _read(root, ".ai/manifest.yaml") or ""
    current = _read(root, ".ai/CURRENT-STATE.md") or ""
    tasks = _read(root, ".ai/TASKS.md") or ""
    decisions = _read(root, ".ai/DECISIONS.md") or ""
    agents = _read(root, "AGENTS.md") or ""
    handoff = _read(root, "docs/handoff/README.md") or ""

    if manifest:
        if f"canonical_repository: {CANONICAL_REPOSITORY}" not in manifest:
            blocked.append("canonical repository identity is missing or mismatched in .ai/manifest.yaml")
        if f"canonical_url: {CANONICAL_URL}" not in manifest:
            ambiguous.append("canonical repository URL is not recoverable from .ai/manifest.yaml")
    if agents and CANONICAL_REPOSITORY not in agents:
        ambiguous.append("AGENTS.md does not expose the exact canonical repository")
    if current and not ("Source tree + Git" in current or "source tree + Git" in current):
        ambiguous.append("CURRENT-STATE does not clearly identify source/Git authority")
    if tasks and "## Active" not in tasks:
        ambiguous.append("TASKS does not expose an Active section")
    if decisions and not re.search(r"authorization|authority", decisions, flags=re.IGNORECASE):
        ambiguous.append("DECISIONS does not expose authorization/authority boundaries")
    if handoff and not re.search(r"bootstrap|handoff|recover", handoff, flags=re.IGNORECASE):
        ambiguous.append("stable handoff document does not expose a recovery/bootstrap entrypoint")

    head = _git_head(root)
    expected = expected_head or os.environ.get("DEVOS_EXPECTED_HEAD") or os.environ.get("GITHUB_SHA")
    if expected and head and expected != head:
        blocked.append("repository HEAD does not match expected source head")
    elif expected and not head:
        ambiguous.append("expected source head was supplied but Git HEAD is unavailable")

    validator = _load_host_validator(root)
    profile_errors = validator.validate(profile)
    capabilities = profile.get("capabilities", {}) if isinstance(profile, dict) else {}
    critical_missing: list[str] = []
    noncritical_missing: list[str] = []
    delegatable: list[str] = []
    available: list[str] = []
    if not profile_errors and isinstance(capabilities, dict):
        for name in validator.REQUIRED_CAPABILITIES:
            status = capabilities[name]["status"]
            if status == "AVAILABLE":
                available.append(name)
            elif status == "DELEGATABLE":
                delegatable.append(name)
            elif name in CRITICAL_RECOVERY_CAPABILITIES:
                critical_missing.append(name)
            else:
                noncritical_missing.append(name)

    repository_status = "BLOCKED" if blocked else _status(missing_inputs or ambiguous)
    profile_status = "BLOCKED" if profile_errors or critical_missing else (
        "WARN" if noncritical_missing or delegatable else "PASS"
    )
    recovery_status = _worst(repository_status, "BLOCKED" if critical_missing else "PASS")
    if recovery_status == "PASS" and delegatable & CRITICAL_RECOVERY_CAPABILITIES:
        recovery_status = "WARN"

    continuation_status = recovery_status
    if continuation_status == "PASS" and (noncritical_missing or delegatable):
        continuation_status = "WARN"
    elif continuation_status == "WARN":
        pass

    friction = {
        "missing_repository_inputs": len(missing_inputs),
        "ambiguous_repository_inputs": len(ambiguous),
        "blocked_repository_conditions": len(blocked),
        "critical_capabilities_missing": len(critical_missing),
        "noncritical_capabilities_missing": len(noncritical_missing),
        "delegatable_capabilities": len(delegatable),
    }
    friction["friction_units"] = sum(friction.values())

    overall = _worst(repository_status, profile_status, recovery_status, continuation_status)
    return {
        "protocol": PROTOCOL,
        "repository": CANONICAL_REPOSITORY,
        "mode": "READ_ONLY",
        "authority": "UNCHANGED",
        "authorization": "UNCHANGED",
        "execution": "NONE",
        "mutation": "NONE",
        "evidence_class": "DETERMINISTIC_HOST_PROFILE_SIMULATION",
        "real_cross_vendor_account_proven": False,
        "overall": overall,
        "recovery_status": recovery_status,
        "continuation_status": continuation_status,
        "repository": {
            "status": repository_status,
            "head": head,
            "expected_head": expected,
            "missing_inputs": missing_inputs,
            "ambiguous_inputs": ambiguous,
            "blocked_conditions": blocked,
        },
        "host": {
            "status": profile_status,
            "host_id": profile.get("host_id") if isinstance(profile, dict) else None,
            "profile_errors": profile_errors,
            "available": sorted(available),
            "delegatable": sorted(delegatable),
            "critical_missing": sorted(critical_missing),
            "noncritical_missing": sorted(noncritical_missing),
        },
        "friction": friction,
        "rules": [
            "CHAT MEMORY != SOURCE OF TRUTH",
            "INTERPRETATION != AUTHORIZATION",
            "READY != EXECUTION",
            "SIMULATED EVIDENCE != LIVE PROVIDER PROOF",
            "RECOVERY != AUTOMATIC MUTATION REPLAY",
        ],
        "limitations": [
            "This deterministic report does not prove an independent AI vendor/account trial.",
            "Host capability declarations are validated inputs, not observed provider behavior.",
            "Friction units are transparent issue counts, not a probabilistic readiness score.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument("--profile", default="adapters/host-profile.example.json")
    parser.add_argument("--expected-head")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    try:
        profile_path = (root / args.profile).resolve()
        if not profile_path.is_relative_to(root):
            raise ValueError("profile path escapes repository")
        profile = json.loads(profile_path.read_text(encoding="utf-8"))
        report = analyze(root, profile, expected_head=args.expected_head)
    except (OSError, ValueError, json.JSONDecodeError, RuntimeError) as exc:
        report = {
            "protocol": PROTOCOL,
            "mode": "READ_ONLY",
            "authority": "UNCHANGED",
            "authorization": "UNCHANGED",
            "execution": "NONE",
            "mutation": "NONE",
            "overall": "BLOCKED",
            "error": str(exc),
            "real_cross_vendor_account_proven": False,
        }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report.get("overall") == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
