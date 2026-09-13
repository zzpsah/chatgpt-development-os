#!/usr/bin/env python3
"""Failure + Recovery Proof supervisor for the merged Production E2E Harness.

This module never grants authority and never executes an action merely because a
checkpoint exists. It classifies observed E2E failures, records the last safe
stage, and permits full-path retry only when replay is safe (read-only) and the
repaired payload is freshly revalidated. Mutation replay is deliberately blocked
once a mutation runtime attempt has begun or succeeded.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = "DEVOS-FAILURE-RECOVERY-v1"
E2E_PROTOCOL = "DEVOS-PRODUCTION-E2E-v1"
STAGES = [
    "INPUT",
    "INTERPRETATION",
    "PLANNING",
    "READINESS",
    "CONTROLLER",
    "HANDOFF",
    "RUNTIME",
    "VERIFICATION",
    "PERSISTENCE",
    "RECOVERY",
]
MUTATION_OPERATIONS = {"filesystem.write_scoped", "github.mutate.file"}


def _load(name: str, relative: str):
    path = ROOT / relative
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {relative}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


harness = _load("recovery_e2e", "tools/production-e2e-harness.py")
host_adapter = _load("recovery_host", "adapters/reference-host.py")


def _reason_text(result: dict[str, Any]) -> str:
    reason = result.get("reason")
    if isinstance(reason, list):
        return " | ".join(str(x) for x in reason)
    return str(reason or "")


def classify_failure(result: dict[str, Any]) -> str:
    if result.get("protocol") != E2E_PROTOCOL or result.get("status") != "BLOCKED":
        return "INVALID_FAILURE_RESULT"
    stage = str(result.get("stage") or "UNKNOWN")
    text = _reason_text(result).upper()
    trace = result.get("trace") if isinstance(result.get("trace"), dict) else {}
    readiness = trace.get("readiness") if isinstance(trace.get("readiness"), dict) else {}
    readiness_status = str(readiness.get("status") or "")
    readiness_reasons = " | ".join(str(x) for x in readiness.get("reasons", []))
    all_text = f"{text} | {readiness_reasons}".upper()

    if stage in {"INPUT", "INTERPRETATION"}:
        return "INPUT_AMBIGUOUS"
    if stage == "PLANNING":
        return "PLAN_BLOCKED"
    if stage == "READINESS":
        if readiness_status == "STOP" or "STALE_PLAN" in all_text or "HEAD_CHANGED" in all_text:
            return "REPOSITORY_DRIFT"
        if "DEPENDENC" in all_text:
            return "DEPENDENCY_BLOCKED"
        if "CAPABILITY" in all_text:
            return "CAPABILITY_MISSING"
        if readiness_status == "NEEDS_APPROVAL" or "AUTHORIZATION" in all_text or "APPROVAL" in all_text:
            return "AUTHORIZATION_REQUIRED"
        if "SECURITY" in all_text:
            return "SECURITY_BLOCKED"
        return "READINESS_BLOCKED"
    if stage in {"CONTROLLER", "HANDOFF"}:
        if "AUTHORIZATION" in all_text:
            return "AUTHORIZATION_REQUIRED"
        if "SECURITY" in all_text:
            return "SECURITY_BLOCKED"
        if "CAPABILITY" in all_text:
            return "CAPABILITY_MISSING"
        return "CONTROL_BOUNDARY_BLOCKED"
    if stage == "RUNTIME":
        if "UNAVAILABLE" in all_text or "NOT CONFIGURED" in all_text or "FILE NOT FOUND" in all_text:
            return "PROVIDER_OR_RUNTIME_UNAVAILABLE"
        return "RUNTIME_FAILED"
    if stage == "VERIFICATION":
        return "VERIFICATION_FAILED"
    if stage == "PERSISTENCE":
        if "AUTHORIZATION" in all_text:
            return "PERSISTENCE_AUTHORIZATION_REQUIRED"
        return "PERSISTENCE_FAILED"
    if stage == "RECOVERY":
        return "RECOVERY_FAILED"
    return "UNKNOWN_FAILURE"


def _last_safe_stage(result: dict[str, Any]) -> str | None:
    failed_stage = str(result.get("stage") or "")
    if failed_stage not in STAGES:
        return None
    index = STAGES.index(failed_stage)
    if index == 0:
        return None
    trace = result.get("trace") if isinstance(result.get("trace"), dict) else {}
    # Walk backwards to the last stage represented by successful evidence.
    mapping = {
        "INTERPRETATION": "interpretation",
        "PLANNING": "plan",
        "READINESS": "readiness",
        "CONTROLLER": "controller",
        "HANDOFF": "handoff",
        "RUNTIME": "runtime",
        "VERIFICATION": "verification",
        "PERSISTENCE": "persistence",
        "RECOVERY": "recovery",
    }
    for candidate in reversed(STAGES[:index]):
        key = mapping.get(candidate)
        if key and key in trace:
            return candidate
    return "INPUT" if index > 0 else None


def build_checkpoint(payload: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    failure_class = classify_failure(result)
    runtime_request = payload.get("runtime_request") if isinstance(payload.get("runtime_request"), dict) else {}
    operation = runtime_request.get("operation")
    mutation = operation in MUTATION_OPERATIONS
    trace = result.get("trace") if isinstance(result.get("trace"), dict) else {}
    runtime = trace.get("runtime") if isinstance(trace.get("runtime"), dict) else {}
    runtime_status = runtime.get("status")
    failed_stage = str(result.get("stage") or "UNKNOWN")

    mutation_attempted = mutation and failed_stage in {"RUNTIME", "VERIFICATION", "PERSISTENCE", "RECOVERY"}
    if mutation_attempted:
        replay_policy = "NO_REPLAY_HOLD"
    elif failure_class == "REPOSITORY_DRIFT":
        replay_policy = "RECOMPILE_AND_REVALIDATE_REQUIRED"
    elif failure_class in {"INPUT_AMBIGUOUS", "PLAN_BLOCKED"}:
        replay_policy = "CORRECT_INPUT_THEN_REVALIDATE"
    else:
        replay_policy = "REVALIDATE_THEN_RETRY_REPLAY_SAFE_PATH"

    return {
        "protocol": PROTOCOL,
        "status": "FAILED_CHECKPOINT",
        "failure_class": failure_class,
        "failed_stage": failed_stage,
        "last_safe_stage": _last_safe_stage(result),
        "repository_head": payload.get("repository_head"),
        "compiled_repository_head": payload.get("compiled_repository_head", payload.get("repository_head")),
        "step_id": payload.get("step_id") or (trace.get("readiness") or {}).get("step_id"),
        "runtime_operation": operation,
        "mutation_operation": mutation,
        "mutation_attempted": mutation_attempted,
        "runtime_status": runtime_status,
        "raw_reason": result.get("reason"),
        "replay_policy": replay_policy,
        "authority": "UNCHANGED",
        "authorization": "UNCHANGED",
        "execution": "NONE",
    }


def inspect_persisted_evidence(project_root: Path, relative_path: str) -> dict[str, Any]:
    observed = host_adapter.read_text(project_root, relative_path)
    if observed.get("status") != "SUCCESS":
        return {
            "protocol": PROTOCOL,
            "status": "HOLD",
            "reason": "PERSISTED_EVIDENCE_UNAVAILABLE",
            "authority": "UNCHANGED",
            "execution": "NONE",
        }
    try:
        packet = json.loads(observed.get("content", ""))
    except json.JSONDecodeError:
        return {
            "protocol": PROTOCOL,
            "status": "HOLD",
            "reason": "PERSISTED_EVIDENCE_CORRUPT",
            "authority": "UNCHANGED",
            "execution": "NONE",
        }
    required = (
        packet.get("protocol") == E2E_PROTOCOL
        and packet.get("status") == "VERIFIED"
        and packet.get("execution_evidence") is True
        and packet.get("runtime_status") == "SUCCESS"
        and packet.get("verification_status") == "VERIFIED"
    )
    return {
        "protocol": PROTOCOL,
        "status": "RECOVERABLE" if required else "HOLD",
        "reason": "PERSISTED_EVIDENCE_VALID" if required else "PERSISTED_EVIDENCE_INVALID",
        "packet": packet if required else None,
        "authority": "UNCHANGED",
        "execution": "NONE",
    }


def resume(
    checkpoint: dict[str, Any],
    repaired_payload: dict[str, Any],
    github_client: Any = None,
) -> dict[str, Any]:
    if checkpoint.get("protocol") != PROTOCOL or checkpoint.get("status") != "FAILED_CHECKPOINT":
        return {
            "protocol": PROTOCOL,
            "status": "HOLD",
            "reason": "INVALID_RECOVERY_CHECKPOINT",
            "authority": "UNCHANGED",
            "execution": "NONE",
        }
    if checkpoint.get("authority") != "UNCHANGED" or checkpoint.get("authorization") != "UNCHANGED":
        return {
            "protocol": PROTOCOL,
            "status": "HOLD",
            "reason": "CHECKPOINT_AUTHORITY_BOUNDARY_CHANGED",
            "authority": "UNCHANGED",
            "execution": "NONE",
        }
    if checkpoint.get("mutation_attempted") is True:
        return {
            "protocol": PROTOCOL,
            "status": "HOLD",
            "reason": "MUTATION_REPLAY_FORBIDDEN",
            "checkpoint": checkpoint,
            "authority": "UNCHANGED",
            "execution": "NONE",
        }

    old_head = checkpoint.get("repository_head")
    new_head = repaired_payload.get("repository_head")
    if not isinstance(new_head, str) or not new_head:
        return {
            "protocol": PROTOCOL,
            "status": "HOLD",
            "reason": "CURRENT_REPOSITORY_HEAD_REQUIRED",
            "authority": "UNCHANGED",
            "execution": "NONE",
        }
    if old_head != new_head and repaired_payload.get("recompiled_after_repository_change") is not True:
        return {
            "protocol": PROTOCOL,
            "status": "HOLD",
            "reason": "RECOMPILE_REQUIRED_AFTER_REPOSITORY_CHANGE",
            "authority": "UNCHANGED",
            "execution": "NONE",
        }

    if checkpoint.get("failure_class") == "REPOSITORY_DRIFT":
        compiled = repaired_payload.get("compiled_repository_head", new_head)
        if compiled != new_head:
            return {
                "protocol": PROTOCOL,
                "status": "HOLD",
                "reason": "STALE_PLAN_NOT_REPAIRED",
                "authority": "UNCHANGED",
                "execution": "NONE",
            }

    retry_payload = dict(repaired_payload)
    retry_payload.pop("recompiled_after_repository_change", None)
    result = harness.run(retry_payload, github_client=github_client)
    if result.get("status") == "COMPLETE":
        return {
            "protocol": PROTOCOL,
            "status": "RECOVERED_VERIFIED",
            "reason": "REPLAY_SAFE_PATH_REVALIDATED_AND_VERIFIED",
            "previous_checkpoint": checkpoint,
            "result": result,
            "authority": "UNCHANGED",
            "authorization": "UNCHANGED",
            "execution": "COMPLETED",
        }

    next_checkpoint = build_checkpoint(retry_payload, result)
    return {
        "protocol": PROTOCOL,
        "status": "HOLD",
        "reason": "RECOVERY_ATTEMPT_STILL_BLOCKED",
        "previous_checkpoint": checkpoint,
        "next_checkpoint": next_checkpoint,
        "result": result,
        "authority": "UNCHANGED",
        "authorization": "UNCHANGED",
        "execution": "NONE",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    classify_cmd = sub.add_parser("checkpoint")
    classify_cmd.add_argument("--payload", required=True)
    classify_cmd.add_argument("--result", required=True)
    resume_cmd = sub.add_parser("resume")
    resume_cmd.add_argument("--checkpoint", required=True)
    resume_cmd.add_argument("--payload", required=True)
    inspect_cmd = sub.add_parser("inspect-evidence")
    inspect_cmd.add_argument("--project-root", required=True)
    inspect_cmd.add_argument("--path", required=True)
    args = parser.parse_args()

    if args.command == "checkpoint":
        output = build_checkpoint(
            json.loads(Path(args.payload).read_text(encoding="utf-8")),
            json.loads(Path(args.result).read_text(encoding="utf-8")),
        )
    elif args.command == "resume":
        output = resume(
            json.loads(Path(args.checkpoint).read_text(encoding="utf-8")),
            json.loads(Path(args.payload).read_text(encoding="utf-8")),
        )
    else:
        output = inspect_persisted_evidence(Path(args.project_root).resolve(), args.path)
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
