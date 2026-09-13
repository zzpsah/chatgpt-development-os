#!/usr/bin/env python3
"""Repository-only multi-session continuation evaluator.

This module persists/reloads continuity facts only. It never turns a saved
candidate into execution authority and never manufactures authorization.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

PROTOCOL = "DEVOS-MULTI-SESSION-v1"


def build_packet(payload: dict[str, Any]) -> dict[str, Any]:
    project = payload.get("project")
    objective = payload.get("objective")
    repository_head = payload.get("repository_head")
    constraints = payload.get("constraints") or []
    verification = payload.get("verification_requirements") or []

    if not isinstance(project, str) or not project.strip():
        raise ValueError("project identity is required")
    if not isinstance(objective, str) or not objective.strip():
        raise ValueError("active objective is required")
    if not isinstance(repository_head, str) or not repository_head.strip():
        raise ValueError("repository head is required")
    if not isinstance(constraints, list) or not isinstance(verification, list):
        raise ValueError("constraints and verification_requirements must be lists")

    return {
        "protocol": PROTOCOL,
        "project": project,
        "objective": objective,
        "repository_head": repository_head,
        "step_id": payload.get("step_id"),
        "last_safe_stage": payload.get("last_safe_stage"),
        "constraints": constraints,
        "verification_requirements": verification,
        "evidence_refs": payload.get("evidence_refs") if isinstance(payload.get("evidence_refs"), list) else [],
        "authority": "UNCHANGED",
        "authorization": "UNCHANGED",
        "execution": "NONE",
    }


def resume(packet: dict[str, Any], current: dict[str, Any]) -> dict[str, Any]:
    base = {
        "protocol": PROTOCOL,
        "authority": "UNCHANGED",
        "authorization": "UNCHANGED",
        "execution": "NONE",
    }

    if packet.get("protocol") != PROTOCOL:
        return base | {"status": "HOLD", "reason": "UNSUPPORTED_CONTINUATION_PROTOCOL"}
    if packet.get("authority") != "UNCHANGED" or packet.get("authorization") != "UNCHANGED":
        return base | {"status": "HOLD", "reason": "PACKET_AUTHORITY_BOUNDARY_CHANGED"}
    if packet.get("execution") != "NONE":
        return base | {"status": "HOLD", "reason": "PACKET_MUST_NOT_CONTAIN_EXECUTION_AUTHORITY"}

    project = current.get("project")
    current_head = current.get("repository_head")
    if not isinstance(project, str) or not project:
        return base | {"status": "HOLD", "reason": "CURRENT_PROJECT_IDENTITY_REQUIRED"}
    if project != packet.get("project"):
        return base | {"status": "HOLD", "reason": "PROJECT_IDENTITY_MISMATCH"}
    if not isinstance(current_head, str) or not current_head:
        return base | {"status": "HOLD", "reason": "CURRENT_REPOSITORY_HEAD_REQUIRED"}

    objective = packet.get("objective")
    if not isinstance(objective, str) or not objective.strip():
        return base | {"status": "HOLD", "reason": "ACTIVE_OBJECTIVE_UNAVAILABLE"}

    if current.get("mutation_replay_forbidden") is True:
        return base | {
            "status": "HOLD",
            "reason": "MUTATION_REPLAY_FORBIDDEN",
            "project": project,
            "objective": objective,
            "candidate_step_id": packet.get("step_id"),
        }

    packet_head = packet.get("repository_head")
    if packet_head != current_head:
        return base | {
            "status": "RECOMPILE_REQUIRED",
            "reason": "REPOSITORY_HEAD_CHANGED",
            "project": project,
            "objective": objective,
            "packet_repository_head": packet_head,
            "current_repository_head": current_head,
            "candidate_step_id": packet.get("step_id"),
            "prior_authorization_reusable": False,
        }

    return base | {
        "status": "REVALIDATE_REQUIRED",
        "reason": "SAVED_CANDIDATE_MUST_EARN_CURRENT_ELIGIBILITY",
        "project": project,
        "objective": objective,
        "repository_head": current_head,
        "candidate_step_id": packet.get("step_id"),
        "constraints": packet.get("constraints") if isinstance(packet.get("constraints"), list) else [],
        "verification_requirements": packet.get("verification_requirements") if isinstance(packet.get("verification_requirements"), list) else [],
        "prior_authorization_reusable": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    build = sub.add_parser("build")
    build.add_argument("--input", required=True)
    build.add_argument("--output")
    check = sub.add_parser("resume")
    check.add_argument("--packet", required=True)
    check.add_argument("--current", required=True)
    args = parser.parse_args()

    if args.command == "build":
        packet = build_packet(json.loads(Path(args.input).read_text(encoding="utf-8")))
        rendered = json.dumps(packet, indent=2, sort_keys=True) + "\n"
        if args.output:
            Path(args.output).write_text(rendered, encoding="utf-8")
        else:
            print(rendered, end="")
        return 0

    packet = json.loads(Path(args.packet).read_text(encoding="utf-8"))
    current = json.loads(Path(args.current).read_text(encoding="utf-8"))
    print(json.dumps(resume(packet, current), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
