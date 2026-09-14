#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SECURITY_RELEVANT = {"HIGH_IMPACT_MUTATION", "SECURITY_SENSITIVE", "PRODUCTION_OR_DESTRUCTIVE"}
ALLOWED_IMPACTS = {"READ_ONLY", "LOW_IMPACT_MUTATION", "HIGH_IMPACT_MUTATION", "SECURITY_SENSITIVE", "PRODUCTION_OR_DESTRUCTIVE"}
STATE_CONFIDENCE = {"observed": 2, "likely": 1, "unknown": 0}
CONSTRAINT_TERMS = {
    "DO_NOT_DEPLOY": "deploy",
    "DO_NOT_PRODUCTION": "production",
    "DO_NOT_MERGE": "merge",
    "DO_NOT_DATABASE": "database",
    "DO_NOT_MIGRATION": "migration",
    "DO_NOT_DELETE": "delete",
    "DO_NOT_SECRET": "secret",
    "DO_NOT_CREDENTIAL": "credential",
    "DO_NOT_PERMISSION": "permission",
}


def _load_p16_classifier():
    path = ROOT / "tools" / "semantic-goal-to-plan.py"
    spec = importlib.util.spec_from_file_location("p16_semantic_classifier", path)
    if spec is None or spec.loader is None:
        raise ImportError("cannot load P16 semantic classifier")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.classify


classify_objective = _load_p16_classifier()


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


def _has_cycle(steps: dict[str, dict[str, Any]]) -> bool:
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(sid: str) -> bool:
        if sid in visiting:
            return True
        if sid in visited:
            return False
        visiting.add(sid)
        for dep in steps[sid].get("depends_on", []):
            if visit(str(dep)):
                return True
        visiting.remove(sid)
        visited.add(sid)
        return False

    return any(visit(sid) for sid in sorted(steps))


def _validate_state_resolution_summary(state_resolution: Any) -> str | None:
    if not isinstance(state_resolution, dict) or state_resolution.get("protocol") != "DEVOS-AI-STATE-RESOLUTION-v2":
        return "PLAN_STATE_RESOLUTION_INVALID"
    if state_resolution.get("authority") != "UNCHANGED" or state_resolution.get("authorization") != "UNCHANGED":
        return "PLAN_STATE_RESOLUTION_AUTHORITY_CHANGED"
    if state_resolution.get("execution") != "NONE" or state_resolution.get("mutation") != "NONE":
        return "PLAN_STATE_RESOLUTION_EXECUTION_CHANGED"
    if state_resolution.get("status") != "RESOLVED":
        return "PLAN_STATE_RESOLUTION_NOT_RESOLVED"

    unresolved = state_resolution.get("unresolved_claim_ids")
    if not isinstance(unresolved, list):
        return "PLAN_STATE_RESOLUTION_UNRESOLVED_INVALID"
    if unresolved:
        return "PLAN_STATE_CLAIMS_UNRESOLVED=" + ",".join(sorted(str(item) for item in unresolved))

    claims = state_resolution.get("claims")
    claim_count = state_resolution.get("claim_count")
    if not isinstance(claims, list) or not isinstance(claim_count, int) or claim_count < 0 or claim_count != len(claims):
        return "PLAN_STATE_RESOLUTION_CLAIMS_INVALID"

    counts = {level: 0 for level in STATE_CONFIDENCE}
    for claim in claims:
        if not isinstance(claim, dict):
            return "PLAN_STATE_RESOLUTION_CLAIM_INVALID"
        confidence = claim.get("state_confidence")
        if confidence not in STATE_CONFIDENCE:
            return "PLAN_STATE_RESOLUTION_CONFIDENCE_INVALID"
        claim_id = claim.get("id")
        if claim_id is not None and (not isinstance(claim_id, str) or not claim_id.strip()):
            return "PLAN_STATE_RESOLUTION_CLAIM_ID_INVALID"
        counts[confidence] += 1

    if counts["unknown"]:
        return "PLAN_STATE_RESOLUTION_HIDDEN_UNKNOWN_CLAIM"
    if state_resolution.get("state_confidence_summary") != counts:
        return "PLAN_STATE_RESOLUTION_SUMMARY_INCONSISTENT"
    weakest = state_resolution.get("weakest_state_confidence")
    expected_weakest = min((claim["state_confidence"] for claim in claims), key=lambda value: STATE_CONFIDENCE[value], default="unknown")
    if weakest != expected_weakest:
        return "PLAN_STATE_RESOLUTION_WEAKEST_INCONSISTENT"
    return None


def _validated_steps(plan: dict[str, Any]) -> tuple[dict[str, dict[str, Any]] | None, str | None]:
    if plan.get("protocol") != "DEVOS-GOAL-PLAN-v1" or plan.get("decision") != "PLANNED":
        return None, "PLAN_NOT_PLANNED_OR_PROTOCOL_INVALID"
    if plan.get("authority") != "UNCHANGED" or plan.get("authorization") != "UNCHANGED":
        return None, "PLAN_AUTHORITY_BOUNDARY_CHANGED"
    if plan.get("execution") != "NONE":
        return None, "PLAN_EXECUTION_ALREADY_CLAIMED"
    if not isinstance(plan.get("project"), str) or not plan["project"].strip():
        return None, "PLAN_PROJECT_INVALID"
    if not isinstance(plan.get("objective"), str) or not plan["objective"].strip():
        return None, "PLAN_OBJECTIVE_INVALID"

    ambiguity = plan.get("ambiguity", [])
    if not isinstance(ambiguity, list):
        return None, "PLAN_AMBIGUITY_INVALID"
    if any(str(item).strip() for item in ambiguity):
        return None, "PLANNED_PLAN_HAS_AMBIGUITY"

    state_resolution = plan.get("state_resolution")
    if state_resolution is not None:
        state_error = _validate_state_resolution_summary(state_resolution)
        if state_error:
            return None, state_error

    constraints = plan.get("constraints", [])
    if not isinstance(constraints, list) or any(not isinstance(item, str) for item in constraints):
        return None, "PLAN_CONSTRAINTS_INVALID"

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
        # P17 must not trust a mutable impact label when the same repository
        # contains the deterministic P16 classifier that produced it. Recompute
        # the minimum semantic impact from the objective and fail closed if a
        # compiled envelope was downgraded after planning.
        expected_impact = classify_objective(objective)
        if impact != expected_impact:
            return None, f"PLAN_STEP_IMPACT_MISMATCH={sid}:{impact}:{expected_impact}"
        auth_required = raw.get("authorization_required")
        if auth_required not in (True, False):
            return None, "PLAN_STEP_AUTHORIZATION_FLAG_INVALID=" + sid
        if impact in SECURITY_RELEVANT and auth_required is not True:
            return None, "PLAN_HIGH_IMPACT_AUTHORIZATION_INCONSISTENT=" + sid
        verification = raw.get("verification")
        if not isinstance(verification, str) or not verification.strip():
            return None, "PLAN_STEP_VERIFICATION_MISSING=" + sid
        expected = raw.get("expected_evidence")
        if not isinstance(expected, list) or not expected or any(not isinstance(item, str) or not item.strip() for item in expected):
            return None, "PLAN_STEP_EXPECTED_EVIDENCE_INVALID=" + sid
        stop = raw.get("stop_or_escalate_if")
        if not isinstance(stop, str) or not stop.strip():
            return None, "PLAN_STEP_STOP_CONDITION_MISSING=" + sid
        steps[sid] = raw

    known_ids = set(steps)
    for sid, step in steps.items():
        for dep in step.get("depends_on", []):
            if dep not in known_ids:
                return None, f"PLAN_DEPENDENCY_UNKNOWN={sid}:{dep}"
            if dep == sid:
                return None, "PLAN_SELF_DEPENDENCY=" + sid
    if _has_cycle(steps):
        return None, "PLAN_DEPENDENCY_CYCLE"

    for constraint in constraints:
        term = CONSTRAINT_TERMS.get(constraint)
        if not term:
            continue
        for sid, step in steps.items():
            if step.get("impact") == "READ_ONLY":
                continue
            if term in str(step.get("objective", "")).lower():
                return None, f"PLAN_CONSTRAINT_CONFLICT={constraint}:{sid}"

    return steps, None


def evaluate(payload: dict[str, Any]) -> dict[str, Any]:
    plan = payload.get("plan") or {}
    if not isinstance(plan, dict):
        plan = {}
    step_id = payload.get("step_id")
    compiled_head = payload.get("compiled_repository_head")
    current_head = payload.get("current_repository_head")
    out = _base(plan, step_id, compiled_head, current_head)

    steps, structural_error = _validated_steps(plan)
    if structural_error:
        out["status"] = "BLOCKED"
        out["reasons"].append(structural_error)
        return out
    assert steps is not None
    out["gates"]["plan"] = True

    if not isinstance(step_id, str) or not step_id.strip():
        out["status"] = "BLOCKED"
        out["reasons"].append("STEP_ID_INVALID")
        return out
    step_id = step_id.strip()
    out["step_id"] = step_id
    step = steps.get(step_id)
    if not step:
        out["status"] = "BLOCKED"
        out["reasons"].append("STEP_NOT_FOUND")
        return out

    if not isinstance(compiled_head, str) or not compiled_head.strip() or not isinstance(current_head, str) or not current_head.strip():
        out["status"] = "NEEDS_EVIDENCE"
        out["reasons"].append("REPOSITORY_HEAD_EVIDENCE_MISSING")
        return out
    if compiled_head != current_head:
        out["status"] = "STOP"
        out["reasons"].append("STALE_PLAN_REPOSITORY_HEAD_CHANGED")
        return out
    out["gates"]["freshness"] = True

    completed_raw = payload.get("completed_steps", [])
    if not isinstance(completed_raw, list) or any(not isinstance(x, str) or not x.strip() for x in completed_raw):
        out["status"] = "BLOCKED"
        out["reasons"].append("COMPLETED_STEPS_INVALID")
        return out
    completed = {x.strip() for x in completed_raw}
    unknown_completed = sorted(x for x in completed if x not in steps)
    if unknown_completed:
        out["status"] = "BLOCKED"
        out["reasons"].append("COMPLETED_STEP_UNKNOWN=" + ",".join(unknown_completed))
        return out
    if step_id in completed:
        out["status"] = "BLOCKED"
        out["reasons"].append("STEP_ALREADY_COMPLETE")
        return out
    for completed_id in sorted(completed):
        missing = sorted(str(dep) for dep in steps[completed_id].get("depends_on", []) if str(dep) not in completed)
        if missing:
            out["status"] = "BLOCKED"
            out["reasons"].append(f"COMPLETED_STEP_DEPENDENCY_INCOMPLETE={completed_id}:{','.join(missing)}")
            return out

    missing_deps = [str(dep) for dep in step.get("depends_on", []) if str(dep) not in completed]
    if missing_deps:
        out["status"] = "BLOCKED"
        out["reasons"].append("DEPENDENCIES_INCOMPLETE=" + ",".join(sorted(missing_deps)))
        return out
    out["gates"]["dependencies"] = True

    capabilities = payload.get("capabilities", {})
    authorization_by_step = payload.get("authorization_by_step", {})
    security_by_step = payload.get("security_gate_by_step", {})
    if not isinstance(capabilities, dict) or not isinstance(authorization_by_step, dict) or not isinstance(security_by_step, dict):
        out["status"] = "BLOCKED"
        out["reasons"].append("READINESS_EVIDENCE_MAP_INVALID")
        return out

    capability = capabilities.get(step_id)
    if capability != "AVAILABLE":
        out["status"] = "BLOCKED"
        out["reasons"].append("CAPABILITY_NOT_AVAILABLE")
        return out
    out["gates"]["capability"] = True

    if step.get("authorization_required") is True:
        step_auth = authorization_by_step.get(step_id)
        if step_auth != "ALREADY_GRANTED":
            out["status"] = "NEEDS_APPROVAL"
            out["reasons"].append("STEP_BOUND_AUTHORIZATION_REQUIRED")
            return out
    out["gates"]["authorization"] = True

    impact = step.get("impact")
    if impact in SECURITY_RELEVANT:
        security = security_by_step.get(step_id)
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
    out["gates"]["verification"] = True

    out["status"] = "READY"
    out["step"] = {
        "id": step.get("id"),
        "objective": step.get("objective"),
        "depends_on": list(step.get("depends_on", [])),
        "expected_evidence": list(step.get("expected_evidence", [])),
        "impact": impact,
        "authorization_required": step.get("authorization_required"),
        "verification": verification,
        "stop_or_escalate_if": step.get("stop_or_escalate_if"),
        "execution_evidence": False,
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
