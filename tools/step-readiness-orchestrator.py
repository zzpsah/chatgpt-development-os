#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

SECURITY_RELEVANT = {"HIGH_IMPACT_MUTATION", "SECURITY_SENSITIVE", "PRODUCTION_OR_DESTRUCTIVE"}
ALLOWED_IMPACTS = {"READ_ONLY", "LOW_IMPACT_MUTATION", "HIGH_IMPACT_MUTATION", "SECURITY_SENSITIVE", "PRODUCTION_OR_DESTRUCTIVE"}


def _base(plan: dict[str, Any], step_id: str | None, compiled_head: str | None, current_head: str | None) -> dict[str, Any]:
    return {
        "protocol": "DEVOS-STEP-READINESS-v1",
        "plan_protocol": plan.get("protocol"),
        "step_id": step_id,
        "repository_head": current_head,
        "compiled_repository_head": compiled_head,
        "gates": {
            "plan": False,
            "freshness": False,
            "dependencies": False,
            "capability": False,
            "authorization": False,
            "security": False,
            "verification": False,
        },
        "reasons": [],
        "authority": "UNCHANGED",
        "authorization": "UNCHANGED",
        "execution": "NONE",
    }


def _validated_steps(plan: dict[str, Any]) -> tuple[dict[str, dict[str, Any]] | None, str | None]:
    raw_steps = plan.get("steps")
    if not isinstance(raw_steps, list) or not raw_steps:
        return None, "PLAN_STEPS_MISSING_OR_INVALID"

    steps: dict[str, dict[str, Any]] = {}
    for raw in raw_steps:
        if not isinstance(raw, dict):
            return None, "PLAN_STEP_NOT_OBJECT"
        sid = raw.get("id")
        if not isinstance(sid, str) or not sid.strip():
            return None, "PLAN_STEP_ID_INVALID"
        sid = sid.strip()
        if sid in steps:
            return None, "PLAN_STEP_ID_DUPLICATE=" + sid
        objective = raw.get("objective")
        if not isinstance(objective, str) or not objective.strip():
            return None, "PLAN_STEP_OBJECTIVE_MISSING=" + sid
        deps = raw.get("depends_on", [])
        if not isinstance(deps, list) or any(not isinstance(dep, str) or not dep.strip() for dep in deps):
            return None, "PLAN_STEP_DEPENDENCIES_INVALID=" + sid
        impact = raw.get("impact")
        if impact not in ALLOWED_IMPACTS:
            return None, "PLAN_STEP_IMPACT_INVALID=" + sid
        if raw.get("authorization_required") not in (True, False):
            return None, "PLAN_STEP_AUTHORIZATION_FLAG_INVALID=" + sid
        steps[sid] = raw

    known_ids = set(steps)
    for sid, step in steps.items():
        for dep in step.get("depends_on", []):
            if dep not in known_ids:
                return None, f"PLAN_DEPENDENCY_UNKNOWN={sid}:{dep}"
            if dep == sid:
                return None, "PLAN_SELF_DEPENDENCY=" + sid
    return steps, None


def evaluate(payload: dict[str, Any]) -> dict[str, Any]:
    plan = payload.get("plan") or {}
    step_id = payload.get("step_id")
    compiled_head = payload.get("compiled_repository_head")
    current_head = payload.get("current_repository_head")
    out = _base(plan, step_id, compiled_head, current_head)

    if plan.get("protocol") != "DEVOS-GOAL-PLAN-v1" or plan.get("decision") != "PLANNED":
        out["status"] = "BLOCKED"
        out["reasons"].append("PLAN_NOT_PLANNED_OR_PROTOCOL_INVALID")
        return out

    steps, structural_error = _validated_steps(plan)
    if structural_error:
        out["status"] = "BLOCKED"
        out["reasons"].append(structural_error)
        return out
    assert steps is not None
    out["gates"]["plan"] = True

    step = steps.get(str(step_id))
    if not step:
        out["status"] = "BLOCKED"
        out["reasons"].append("STEP_NOT_FOUND")
        return out

    if not compiled_head or not current_head:
        out["status"] = "NEEDS_EVIDENCE"
        out["reasons"].append("REPOSITORY_HEAD_EVIDENCE_MISSING")
        return out
    if compiled_head != current_head:
        out["status"] = "STOP"
        out["reasons"].append("STALE_PLAN_REPOSITORY_HEAD_CHANGED")
        return out
    out["gates"]["freshness"] = True

    completed = {str(x) for x in payload.get("completed_steps", [])}
    unknown_completed = sorted(x for x in completed if x not in steps)
    if unknown_completed:
        out["status"] = "BLOCKED"
        out["reasons"].append("COMPLETED_STEP_UNKNOWN=" + ",".join(unknown_completed))
        return out

    missing_deps = [str(dep) for dep in step.get("depends_on", []) if str(dep) not in completed]
    if missing_deps:
        out["status"] = "BLOCKED"
        out["reasons"].append("DEPENDENCIES_INCOMPLETE=" + ",".join(sorted(missing_deps)))
        return out
    out["gates"]["dependencies"] = True

    capability = payload.get("capabilities", {}).get(str(step_id))
    if capability != "AVAILABLE":
        out["status"] = "BLOCKED"
        out["reasons"].append("CAPABILITY_NOT_AVAILABLE")
        return out
    out["gates"]["capability"] = True

    if step.get("authorization_required") is True:
        step_auth = payload.get("authorization_by_step", {}).get(str(step_id))
        if step_auth != "ALREADY_GRANTED":
            out["status"] = "NEEDS_APPROVAL"
            out["reasons"].append("STEP_BOUND_AUTHORIZATION_REQUIRED")
            return out
    out["gates"]["authorization"] = True

    impact = step.get("impact")
    if impact in SECURITY_RELEVANT:
        security = payload.get("security_gate_by_step", {}).get(str(step_id))
        if security in (None, "UNKNOWN", "NOT_RUN"):
            out["status"] = "NEEDS_EVIDENCE"
            out["reasons"].append("SECURITY_GATE_EVIDENCE_REQUIRED")
            return out
        if security != "PASS":
            out["status"] = "BLOCKED"
            out["reasons"].append("SECURITY_GATE_NOT_PASS")
            return out
    out["gates"]["security"] = True

    verification = step.get("verification")
    if not isinstance(verification, str) or not verification.strip():
        out["status"] = "NEEDS_EVIDENCE"
        out["reasons"].append("VERIFICATION_PATH_MISSING")
        return out
    out["gates"]["verification"] = True

    out["status"] = "READY"
    out["step"] = {
        "id": step.get("id"),
        "objective": step.get("objective"),
        "impact": impact,
        "verification": verification,
    }
    out["reasons"].append("ALL_P17_GATES_SATISFIED")
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="JSON file containing plan plus fresh readiness evidence")
    args = parser.parse_args()
    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    print(json.dumps(evaluate(payload), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
