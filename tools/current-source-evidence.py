#!/usr/bin/env python3
"""Collect and validate bounded current-source evidence against the readiness ledger.

Current evidence is an ephemeral packet derived from an exact checkout. Historical
ledger rows remain untouched. This tool is read-only with respect to repository and
provider state; it may execute only a test already declared by the readiness ledger.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = "DEVOS-CURRENT-SOURCE-EVIDENCE-v1"
CANONICAL_REPOSITORY = "zzpsah/chatgpt-development-os"
ALLOWED_LEVELS = {"deterministic", "integrated", "provider_simulated"}


def _load_readiness(root: Path):
    path = root / "tools" / "verify-readiness-evidence.py"
    spec = importlib.util.spec_from_file_location("devos_readiness_for_current_evidence", path)
    if not spec or not spec.loader:
        raise RuntimeError("readiness evidence verifier unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _git_head(root: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=root, text=True,
            capture_output=True, check=False,
        )
    except OSError:
        return None
    value = result.stdout.strip()
    return value if result.returncode == 0 and re.fullmatch(r"[0-9a-f]{40}", value) else None


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def _declared_evidence(ledger: dict[str, Any]) -> set[tuple[str, str, str]]:
    result: set[tuple[str, str, str]] = set()
    for row in ledger.get("capabilities", []) if isinstance(ledger, dict) else []:
        if not isinstance(row, dict) or not isinstance(row.get("id"), str):
            continue
        capability = row["id"]
        for item in row.get("evidence", []) if isinstance(row.get("evidence"), list) else []:
            if isinstance(item, dict) and all(isinstance(item.get(key), str) for key in ("level", "test")):
                result.add((capability, item["level"], item["test"]))
    return result


def _packet_invariants(packet: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    expected = {
        "protocol": PROTOCOL,
        "repository": CANONICAL_REPOSITORY,
        "mode": "READ_ONLY",
        "authority": "UNCHANGED",
        "authorization": "UNCHANGED",
        "execution": "NONE",
        "mutation": "NONE",
        "production_ready": False,
        "live_provider_proven": False,
    }
    for key, value in expected.items():
        if type(packet.get(key)) is not type(value) or packet.get(key) != value:
            errors.append(f"invalid invariant: {key}")
    allowed = set(expected) | {"source_head", "evidence", "limitations"}
    if set(packet) - allowed:
        errors.append("unknown packet fields")
    return errors


def validate_packet(
    packet: dict[str, Any],
    ledger: dict[str, Any],
    root: Path = ROOT,
    *,
    expected_head: str | None = None,
) -> list[str]:
    """Validate a current packet against current source + authoritative ledger vocabulary."""
    root = root.resolve()
    errors = _packet_invariants(packet) if isinstance(packet, dict) else ["packet must be an object"]
    if errors and not isinstance(packet, dict):
        return errors

    verifier = _load_readiness(root)
    ledger_errors = verifier.validate(ledger, root)
    if ledger_errors:
        return errors + ["authoritative readiness ledger invalid: " + "; ".join(ledger_errors)]

    head = _git_head(root)
    source_head = packet.get("source_head")
    required_head = expected_head or os.environ.get("DEVOS_EXPECTED_HEAD") or os.environ.get("GITHUB_SHA") or head
    if not isinstance(source_head, str) or not re.fullmatch(r"[0-9a-f]{40}", source_head):
        errors.append("invalid source_head")
    if head is None:
        errors.append("Git HEAD unavailable")
    elif source_head != head:
        errors.append("packet source_head does not match current Git HEAD")
    if required_head and source_head != required_head:
        errors.append("packet source_head does not match expected source head")

    evidence = packet.get("evidence")
    if not isinstance(evidence, dict):
        return errors + ["evidence must be an object"]
    allowed_evidence = {
        "kind", "freshness", "capability", "level", "test", "test_sha256",
        "exit_code", "run_id", "workflow", "context",
    }
    if set(evidence) - allowed_evidence:
        errors.append("unknown evidence fields")
    if evidence.get("kind") != "current_check" or evidence.get("freshness") != "current":
        errors.append("current evidence kind/freshness mismatch")
    capability = evidence.get("capability")
    level = evidence.get("level")
    test = evidence.get("test")
    if not all(isinstance(value, str) and value for value in (capability, level, test)):
        errors.append("capability/level/test must be nonempty strings")
        return errors
    if level not in ALLOWED_LEVELS:
        errors.append("unsupported current-source evidence level")
    if (capability, level, test) not in _declared_evidence(ledger):
        errors.append("current claim is not declared by readiness ledger")

    try:
        test_path = verifier.file_in_root(root, test)
        if evidence.get("test_sha256") != _digest(test_path):
            errors.append("current test digest mismatch")
    except (OSError, ValueError, TypeError) as exc:
        errors.append(str(exc))

    if type(evidence.get("exit_code")) is not int or evidence.get("exit_code") != 0:
        errors.append("current check did not succeed")

    context = evidence.get("context")
    if context not in {"local", "ci"}:
        errors.append("invalid current evidence context")
    run_id = evidence.get("run_id")
    workflow = evidence.get("workflow")
    if context == "ci":
        if type(run_id) is not int or run_id <= 0:
            errors.append("CI evidence requires positive run_id")
        if not isinstance(workflow, str) or not workflow:
            errors.append("CI evidence requires workflow")
        env_run = os.environ.get("GITHUB_RUN_ID")
        if env_run and str(run_id) != env_run:
            errors.append("CI run_id does not match current GitHub run context")
    else:
        if run_id is not None or workflow is not None:
            errors.append("local evidence cannot claim CI run/workflow")

    if level == "provider_simulated" and test != "tools/test-controlled-remote-mutation-proof.py":
        errors.append("provider_simulated current proof requires controlled-mutation corpus")
    # Real external-provider and production proof are deliberately unavailable in v1.
    return errors


def current_drift_status(packet: dict[str, Any], ledger: dict[str, Any], root: Path = ROOT) -> dict[str, Any]:
    """Overlay valid current proof on historical drift without rewriting history."""
    verifier = _load_readiness(root.resolve())
    historical = verifier.historical_source_drift(ledger, root.resolve())
    errors = validate_packet(packet, ledger, root.resolve())
    test = packet.get("evidence", {}).get("test") if isinstance(packet, dict) else None
    resolved = [test] if not errors and test in historical else []
    return {
        "historical_source_drift": historical,
        "current_source_verified": resolved,
        "unresolved_historical_drift": [item for item in historical if item not in resolved],
        "packet_status": "VALID" if not errors else "HOLD",
        "errors": errors,
        "rule": "CURRENT_EVIDENCE_ADDS_PROOF_BUT_NEVER_REWRITES_HISTORICAL_PROVENANCE",
    }


def collect(
    root: Path,
    ledger: dict[str, Any],
    *,
    capability: str,
    level: str,
    test: str,
) -> dict[str, Any]:
    """Execute one ledger-declared repository test and return an ephemeral packet."""
    root = root.resolve()
    verifier = _load_readiness(root)
    if verifier.validate(ledger, root):
        raise ValueError("authoritative readiness ledger is invalid")
    if level not in ALLOWED_LEVELS:
        raise ValueError("unsupported current-source evidence level")
    if (capability, level, test) not in _declared_evidence(ledger):
        raise ValueError("requested current claim is not declared by readiness ledger")
    test_path = verifier.file_in_root(root, test)
    head = _git_head(root)
    if head is None:
        raise ValueError("Git HEAD unavailable")

    completed = subprocess.run(
        [sys.executable, str(test_path)], cwd=root, text=True,
        capture_output=True, check=False,
    )
    run_env = os.environ.get("GITHUB_RUN_ID")
    workflow = os.environ.get("GITHUB_WORKFLOW")
    context = "ci" if run_env else "local"
    return {
        "protocol": PROTOCOL,
        "repository": CANONICAL_REPOSITORY,
        "mode": "READ_ONLY",
        "authority": "UNCHANGED",
        "authorization": "UNCHANGED",
        "execution": "NONE",
        "mutation": "NONE",
        "production_ready": False,
        "live_provider_proven": False,
        "source_head": head,
        "evidence": {
            "kind": "current_check",
            "freshness": "current",
            "capability": capability,
            "level": level,
            "test": test,
            "test_sha256": _digest(test_path),
            "exit_code": completed.returncode,
            "run_id": int(run_env) if run_env and run_env.isdigit() else None,
            "workflow": workflow if run_env else None,
            "context": context,
        },
        "limitations": [
            "Packet proves only the declared test at this exact source head.",
            "CI run_id is execution-context metadata; this offline validator does not contact GitHub to authenticate the run.",
            "Current evidence does not grant authorization or imply production/live-provider proof.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument("--matrix", default="config/readiness-evidence.json")
    parser.add_argument("--capability", required=True)
    parser.add_argument("--level", required=True)
    parser.add_argument("--test", required=True)
    parser.add_argument("--output")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    verifier = _load_readiness(root)
    try:
        ledger = verifier.read_json(verifier.file_in_root(root, args.matrix))
        packet = collect(root, ledger, capability=args.capability, level=args.level, test=args.test)
        errors = validate_packet(packet, ledger, root)
        drift = current_drift_status(packet, ledger, root)
    except (OSError, ValueError, TypeError, RuntimeError, json.JSONDecodeError) as exc:
        print(json.dumps({"protocol": PROTOCOL, "status": "HOLD", "errors": [str(exc)]}, indent=2))
        return 2
    payload = {"packet": packet, "validation": {"status": "VALID" if not errors else "HOLD", "errors": errors}, "drift": drift}
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if not errors and packet["evidence"]["exit_code"] == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
