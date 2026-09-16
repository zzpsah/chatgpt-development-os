#!/usr/bin/env python3
"""Deterministic, read-only remediation planner for DevOS project fleets."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

INPUT_PROTOCOL = "DEVOS-PROJECT-FLEET-WATCH-v1"
PROTOCOL = "DEVOS-PROJECT-REMEDIATION-PLAN-v1"
ALLOWED_STATES = {"MANAGED", "ONBOARDING_REQUIRED", "HOLD", "BLOCKED", "ARCHIVED"}

BOUNDARIES = {
    "authority": "UNCHANGED",
    "authorization": "UNCHANGED",
    "execution": "NONE",
    "mutation": "NONE",
    "provider_mutation": "NONE",
    "onboarding_authorized": False,
    "production_ready": False,
    "publication_authorized": False,
    "deployment_authorized": False,
}


def blocked(reason: str) -> dict[str, Any]:
    return {
        "protocol": PROTOCOL,
        "status": "BLOCKED",
        "reason": reason,
        "remediation_required": False,
        "actions": [],
        "summary": {},
        **BOUNDARIES,
    }


def _action_for(item: dict[str, Any], regression: bool) -> dict[str, Any] | None:
    repository = item["repository"]
    state = item["fleet_state"]
    management_state = item.get("management_state")
    if state in {"MANAGED", "ARCHIVED"}:
        return None

    if regression:
        kind, priority = "RESTORE_MANAGED_STATE", 100
    elif state == "HOLD":
        kind, priority = "RESOLVE_MANAGEMENT_CONFLICT", 95
    elif state == "BLOCKED":
        kind, priority = "INVESTIGATE_BLOCKER", 90
    elif management_state == "PARTIAL":
        kind, priority = "COMPLETE_ONBOARDING", 80
    else:
        kind, priority = "ONBOARD_PROJECT", 70

    return {
        "repository": repository,
        "priority": priority,
        "action": kind,
        "source_state": state,
        "management_state": management_state,
        "reason": item.get("reason"),
        "missing_files": sorted(item.get("missing_files") or []),
        "requires_explicit_authorization": True,
        "safe_apply": False,
        "next_gate": "P17_READINESS_AND_SCOPED_APPROVAL",
    }


def plan(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return blocked("fleet assessment must be an object")
    if payload.get("protocol") != INPUT_PROTOCOL:
        return blocked("fleet assessment protocol is invalid")
    repositories = payload.get("repositories")
    if not isinstance(repositories, list):
        return blocked("fleet repositories must be a list")

    regressions: set[str] = set()
    drift = payload.get("drift")
    if drift is not None:
        if not isinstance(drift, dict):
            return blocked("fleet drift must be an object or null")
        raw = drift.get("management_regressions", [])
        if not isinstance(raw, list) or any(not isinstance(x, str) for x in raw):
            return blocked("management_regressions must be a list of repository identities")
        regressions = set(raw)

    seen: set[str] = set()
    actions: list[dict[str, Any]] = []
    state_counts: dict[str, int] = {}
    for item in repositories:
        if not isinstance(item, dict):
            return blocked("each fleet repository entry must be an object")
        repository = item.get("repository")
        state = item.get("fleet_state")
        if not isinstance(repository, str) or not repository.strip():
            return blocked("each fleet repository entry requires a repository identity")
        if repository in seen:
            return blocked(f"duplicate fleet repository: {repository}")
        seen.add(repository)
        if state not in ALLOWED_STATES:
            return blocked(f"unsupported fleet state for {repository}: {state}")
        state_counts[state] = state_counts.get(state, 0) + 1
        action = _action_for(item, repository in regressions)
        if action:
            actions.append(action)

    unknown_regressions = sorted(regressions - seen)
    if unknown_regressions:
        return blocked("management_regressions references unknown repositories: " + ", ".join(unknown_regressions))

    actions.sort(key=lambda item: (-item["priority"], item["repository"].lower(), item["action"]))
    return {
        "protocol": PROTOCOL,
        "status": "READY",
        "remediation_required": bool(actions),
        "action_count": len(actions),
        "actions": actions,
        "summary": {
            "repositories": len(repositories),
            "states": dict(sorted(state_counts.items())),
            "highest_priority": actions[0]["priority"] if actions else None,
        },
        "next_action": "REVIEW_AND_AUTHORIZE_SCOPED_REMEDIATION" if actions else "NONE",
        **BOUNDARIES,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="DevOS Project Remediation Planner v1")
    parser.add_argument("fleet", help="Project Fleet Watch JSON output")
    parser.add_argument("--require-clean", action="store_true", help="exit non-zero when remediation is required")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        payload = json.loads(Path(args.fleet).read_text(encoding="utf-8"))
        report = plan(payload)
    except (OSError, json.JSONDecodeError) as exc:
        report = blocked(f"fleet load failed: {exc}")

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print("DEVOS PROJECT REMEDIATION PLANNER v1")
        print(f"Status: {report.get('status')}")
        print(f"Actions: {report.get('action_count', 0)}")
        for item in report.get("actions", []):
            print(f"P{item['priority']:03d} {item['action']:28} {item['repository']}")
        print("Mutation: NONE")
        print("Authorization: UNCHANGED")

    if report.get("status") == "BLOCKED":
        return 2
    if args.require_clean and report.get("remediation_required"):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
