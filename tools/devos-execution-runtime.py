#!/usr/bin/env python3
"""Bounded executable runtime for an already-approved DevOS handoff.

The runtime executes verification-only Python scripts through the reference host
adapter, captures raw process evidence, derives verification from the exit status,
and optionally persists a checkpoint. It never grants authority and never commits.
"""
from __future__ import annotations

import importlib.util
import json
import sys
import time
import uuid
from pathlib import Path
from typing import Any

HANDOFF_VERSION = "P12-HANDOFF-v1"
RUNTIME_VERSION = "P12-RUNTIME-v1"
ALLOWED_CAPABILITY = "verification.run"


def _load_reference_verification() -> Any:
    path = Path(__file__).resolve().parents[1] / "adapters" / "reference-verification.py"
    spec = importlib.util.spec_from_file_location("devos_reference_verification", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("reference verification adapter unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _validate_verification(project_root: Path, verification: dict[str, Any]) -> tuple[bool, str]:
    command = verification.get("command")
    if not isinstance(command, list) or not command or not all(isinstance(x, str) for x in command):
        return False, "verification command must be an explicit argv list"
    if command[0] not in {sys.executable, "python", "python3"}:
        return False, "runtime only permits Python verification commands"
    if "-c" in command or "-m" in command:
        return False, "inline or module execution is outside runtime v1 bounds"
    if len(command) < 2:
        return False, "verification script is missing"
    script = (project_root / command[1]).resolve()
    if script.suffix != ".py" or not script.is_file():
        return False, "verification must target an existing Python script"
    if project_root.resolve() not in script.parents:
        return False, "verification script must remain inside project root"
    return True, ""


def _checkpoint(project_root: Path, handoff: dict[str, Any], status: str, evidence: list[dict[str, Any]], verification: str, blockers: list[str], next_action: str) -> dict[str, Any]:
    return {
        "id": f"runtime-{uuid.uuid4().hex}",
        "runtime_version": RUNTIME_VERSION,
        "objective": handoff["work_unit"]["objective"],
        "iteration": 1,
        "work_unit": handoff["work_unit"]["task_id"],
        "repository_head": "UNKNOWN",
        "status": status,
        "changes": [],
        "evidence": evidence,
        "verification": verification,
        "blockers": blockers,
        "next_action": next_action,
    }


def execute(handoff: dict[str, Any], project_root: Path, verification: dict[str, Any], checkpoint_path: Path | None = None) -> dict[str, Any]:
    """Execute one bounded verification work unit and return factual evidence."""
    if handoff.get("handoff_version") != HANDOFF_VERSION or handoff.get("status") != "APPROVED_FOR_RUNTIME":
        return {"status": "BLOCKED", "reason": "HANDOFF_NOT_APPROVED", "evidence": []}
    if handoff.get("authority") != "UNCHANGED":
        return {"status": "BLOCKED", "reason": "AUTHORITY_BOUNDARY_VIOLATION", "evidence": []}
    if handoff.get("execution") != "DELEGATE_TO_EXISTING_RUNTIME":
        return {"status": "BLOCKED", "reason": "RUNTIME_DELEGATION_REQUIRED", "evidence": []}
    if handoff.get("work_unit", {}).get("capability") != ALLOWED_CAPABILITY:
        return {"status": "BLOCKED", "reason": "UNSUPPORTED_RUNTIME_CAPABILITY", "evidence": []}

    project_root = project_root.resolve()
    valid, reason = _validate_verification(project_root, verification)
    if not valid:
        return {"status": "BLOCKED", "reason": reason, "evidence": []}

    adapter = _load_reference_verification()
    pre = _checkpoint(project_root, handoff, "IN_PROGRESS", [], "UNVERIFIED", [], "execute bounded verification")
    started = time.monotonic()
    result = adapter.run_verification(project_root, verification)
    duration = time.monotonic() - started

    raw_evidence = {
        "source": "reference-host-verification",
        "verification_id": verification.get("id", "unnamed"),
        "command": verification["command"],
        "status": result.get("status", "FAILED"),
        "exit_status": result.get("exit_status"),
        "stdout": result.get("stdout", ""),
        "stderr": result.get("stderr", ""),
        "duration_seconds": result.get("duration_seconds", duration),
    }
    evidence = [raw_evidence]
    verified = "VERIFIED" if result.get("status") == "VERIFIED" else "FAILED"
    final_status = "COMPLETE" if verified == "VERIFIED" else ("BLOCKED" if result.get("status") == "UNAVAILABLE" else "FAILED")
    next_action = "STOP/ESCALATE" if final_status != "COMPLETE" else "persist/continue with next bounded work unit"
    final = _checkpoint(project_root, handoff, final_status, evidence, verified, [] if final_status == "COMPLETE" else [result.get("reason", "verification failed")], next_action)

    if checkpoint_path is not None:
        checkpoint_path = checkpoint_path.resolve()
        checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
        checkpoint_path.write_text(json.dumps({"pre_action": pre, "post_action": final}, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    return {
        "runtime_version": RUNTIME_VERSION,
        "status": final_status,
        "evidence": evidence,
        "verification": verified,
        "security": "NOT_APPLICABLE",
        "checkpoint": final,
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="DevOS bounded execution runtime")
    parser.add_argument("project_root", type=Path)
    parser.add_argument("verification_script")
    parser.add_argument("--checkpoint", type=Path)
    args = parser.parse_args()
    handoff = {
        "handoff_version": HANDOFF_VERSION,
        "status": "APPROVED_FOR_RUNTIME",
        "authority": "UNCHANGED",
        "execution": "DELEGATE_TO_EXISTING_RUNTIME",
        "work_unit": {"task_id": "cli-verification", "objective": "run bounded verification", "capability": ALLOWED_CAPABILITY},
    }
    result = execute(handoff, args.project_root, {"id": "cli", "command": [sys.executable, args.verification_script], "timeout_seconds": 300}, args.checkpoint)
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["status"] == "COMPLETE" else 1)
