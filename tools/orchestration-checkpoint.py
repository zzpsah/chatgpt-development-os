#!/usr/bin/env python3
"""Persist and safely resume a minimal P13 orchestration checkpoint."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


PROTOCOL = "P13-ORCHESTRATION-CHECKPOINT-v1"
CONTROL_DECISIONS = {"CONTINUE", "STOP", "ESCALATE"}


def build(orchestration: dict[str, Any]) -> dict[str, Any]:
    """Keep only recoverable orchestration facts, never raw runtime evidence."""
    decision = orchestration.get("decision")
    if decision not in CONTROL_DECISIONS:
        raise ValueError("invalid orchestration decision")
    if orchestration.get("authority") != "UNCHANGED" or orchestration.get("execution") != "NONE":
        raise ValueError("checkpoint requires an unexecuted orchestration decision")
    handoff = orchestration.get("runtime_handoff") or {}
    work_unit = handoff.get("work_unit") or {}
    return {
        "protocol_version": PROTOCOL,
        "goal": orchestration.get("goal"),
        "iteration": orchestration.get("iteration"),
        "decision": decision,
        "repository_head": work_unit.get("repository_head", "UNKNOWN"),
        "candidate_task_id": work_unit.get("id"),
        "authority": "UNCHANGED",
        "execution": "NONE",
        "reason": orchestration.get("reason", []),
    }


def resume(checkpoint: dict[str, Any], repository_head: str) -> dict[str, Any]:
    """Require fresh revalidation; never turn a saved candidate into execution."""
    if checkpoint.get("protocol_version") != PROTOCOL:
        return {"status": "ESCALATE", "reason": "UNSUPPORTED_CHECKPOINT"}
    if checkpoint.get("repository_head") != repository_head:
        return {"status": "ESCALATE", "reason": "REPOSITORY_HEAD_CHANGED"}
    return {
        "status": "REVALIDATE_REQUIRED",
        "reason": "SAVED_CANDIDATE_MUST_NOT_BE_REPLAYED",
        "candidate_task_id": checkpoint.get("candidate_task_id"),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    write = sub.add_parser("write")
    write.add_argument("orchestration", help="orchestrator JSON output")
    write.add_argument("--checkpoint", required=True, help="checkpoint file path")
    check = sub.add_parser("resume")
    check.add_argument("--checkpoint", required=True, help="checkpoint file path")
    check.add_argument("--repository-head", required=True, help="current Git HEAD")
    args = parser.parse_args()
    if args.command == "write":
        checkpoint = build(json.loads(Path(args.orchestration).read_text(encoding="utf-8")))
        path = Path(args.checkpoint)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(checkpoint, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(checkpoint, sort_keys=True))
        return 0
    checkpoint = json.loads(Path(args.checkpoint).read_text(encoding="utf-8"))
    print(json.dumps(resume(checkpoint, args.repository_head), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
