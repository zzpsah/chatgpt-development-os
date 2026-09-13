#!/usr/bin/env python3
"""Deterministic Development Task Controller decision envelope.

The controller preserves the existing P12 task-inventory path and also consumes
P16 DEVOS-GOAL-PLAN-v1 envelopes. Compiled plans are planning evidence only:
they never execute work or manufacture authorization.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
COMPILED_PLAN_PROTOCOL = "DEVOS-GOAL-PLAN-v1"
SECURITY_RELEVANT = {"HIGH_IMPACT_MUTATION", "SECURITY_SENSITIVE", "PRODUCTION_OR_DESTRUCTIVE"}
ALLOWED_IMPACTS = {"READ_ONLY", "LOW_IMPACT_MUTATION", "HIGH_IMPACT_MUTATION", "SECURITY_SENSITIVE", "PRODUCTION_OR_DESTRUCTIVE"}
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


def load_operational_intelligence() -> Any:
    path = ROOT / "tools" / "operational-intelligence.py"
    spec = importlib.util.spec_from_file_location("operational_intelligence", path)
    if spec is None or spec.loader is None:
        raise ImportError("could not load Operational Intelligence")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _gate(value: Any, accepted: set[str]) -> bool:
    return str(value) in accepted


def _base(recommendation: dict[str, Any], analysis: dict[str, Any], protocol: str = "P12-CONTROLLER-v1") -> dict[str, Any]:
    return {
        "protocol_version": protocol,
        "authority": "UNCHANGED",
        "execution": "NONE",
        "authorization": "UNCHANGED",
        "operational_intelligence": {
            "authority": recommendation["authority"],
            "advisory_next_action": recommendation,
            "readiness": analysis["readiness"],
        },
    }


def _plan_summary(plan: dict[str, Any]) -> dict[str, Any]:
    """Preserve semantic plan metadata without presenting it as execution evidence."""
    return {
        "protocol": plan.get("protocol"),
        "decision": plan.get("decision"),
        "project": plan.get("project"),
        "objective": plan.get("objective"),
        "constraints": list(plan.get("constraints", [])) if isinstance(plan.get("constraints", []), list) else [],
        "assumptions": list(plan.get("assumptions", [])) if isinstance(plan.get("assumptions", []), list) else [],
        "ambiguity": list(plan.get("ambiguity", [])) if isinstance(plan.get("ambiguity", []), list) else [],
        "authority_requirements": list(plan.get("authority_requirements", [])) if isinstance(plan.get("authority_requirements", []), list) else [],
        "verification_requirements": list(plan.get("verification_requirements", [])) if isinstance(plan.get("verification_requirements", []), list) else [],
        "authority": plan.get("authority"),
        "authorization": plan.get("authorization"),
        "execution": plan.get("execution"),
        "execution_evidence": False,
    }


def _validate_compiled_plan(plan: dict[str, Any]) -> tuple[dict[str, dict[str, Any]] | None, list[str]]:
    reasons: list[str] = []
    if plan.get("protocol") != COMPILED_PLAN_PROTOCOL:
        reasons.append("COMPILED_PLAN_PROTOCOL_INVALID")
    if plan.get("decision") != "PLANNED":
        reasons.append("COMPILED_PLAN_NOT_PLANNED")
    if plan.get("authority") != "UNCHANGED":
        reasons.append("COMPILED_PLAN_AUTHORITY_CHANGED")
    if plan.get("authorization") != "UNCHANGED":
        reasons.append("COMPILED_PLAN_AUTHORIZATION_CHANGED")
    if plan.get("execution") != "NONE":
        reasons.append("COMPILED_PLAN_EXECUTION_CLAIMED")
    if not isinstance(plan.get("project"), str) or not plan["project"].strip():
        reasons.append("COMPILED_PLAN_PROJECT_INVALID")
    if not isinstance(plan.get("objective"), str) or not plan["objective"].strip():
        reasons.append("COMPILED_PLAN_OBJECTIVE_INVALID")

    ambiguity = plan.get("ambiguity", [])
    if not isinstance(ambiguity, list):
        reasons.append("COMPILED_PLAN_AMBIGUITY_INVALID")
    elif any(str(item).strip() for item in ambiguity):
        reasons.append("COMPILED_PLAN_PLANNED_WITH_AMBIGUITY")

    constraints = plan.get("constraints", [])
    if not isinstance(constraints, list) or any(not isinstance(item, str) for item in constraints):
        reasons.append("COMPILED_PLAN_CONSTRAINTS_INVALID")
        constraints = []

    raw_steps = plan.get("steps")
    if not isinstance(raw_steps, list) or not raw_steps:
        reasons.append("COMPILED_PLAN_STEPS_MISSING")
        return None, reasons

    steps: dict[str, dict[str, Any]] = {}
    for raw in raw_steps:
        if not isinstance(raw, dict):
            reasons.append("COMPILED_PLAN_STEP_INVALID")
            continue
        sid = raw.get("id")
        if not isinstance(sid, str) or not sid.strip():
            reasons.append("COMPILED_PLAN_STEP_ID_INVALID")
            continue
        sid = sid.strip()
        if sid in steps:
            reasons.append("COMPILED_PLAN_STEP_ID_DUPLICATE=" + sid)
            continue
        objective = raw.get("objective")
        if not isinstance(objective, str) or not objective.strip():
            reasons.append("COMPILED_PLAN_STEP_OBJECTIVE_MISSING=" + sid)
        deps = raw.get("depends_on", [])
        if not isinstance(deps, list) or any(not isinstance(dep, str) or not dep.strip() for dep in deps):
            reasons.append("COMPILED_PLAN_STEP_DEPENDENCIES_INVALID=" + sid)
        impact = raw.get("impact")
        if impact not in ALLOWED_IMPACTS:
            reasons.append("COMPILED_PLAN_STEP_IMPACT_INVALID=" + sid)
        auth_required = raw.get("authorization_required")
        if auth_required not in (True, False):
            reasons.append("COMPILED_PLAN_STEP_AUTHORIZATION_FLAG_INVALID=" + sid)
        elif impact in SECURITY_RELEVANT and auth_required is not True:
            reasons.append("COMPILED_PLAN_HIGH_IMPACT_AUTHORIZATION_INCONSISTENT=" + sid)
        verification = raw.get("verification")
        if not isinstance(verification, str) or not verification.strip():
            reasons.append("COMPILED_PLAN_STEP_VERIFICATION_MISSING=" + sid)
        expected = raw.get("expected_evidence")
        if not isinstance(expected, list) or not expected or any(not isinstance(item, str) or not item.strip() for item in expected):
            reasons.append("COMPILED_PLAN_STEP_EXPECTED_EVIDENCE_INVALID=" + sid)
        stop = raw.get("stop_or_escalate_if")
        if not isinstance(stop, str) or not stop.strip():
            reasons.append("COMPILED_PLAN_STEP_STOP_CONDITION_MISSING=" + sid)
        steps[sid] = raw

    known = set(steps)
    for sid, step in steps.items():
        deps = step.get("depends_on", [])
        if not isinstance(deps, list):
            continue
        for dep in deps:
            if dep not in known:
                reasons.append(f"COMPILED_PLAN_DEPENDENCY_UNKNOWN={sid}:{dep}")
            elif dep == sid:
                reasons.append("COMPILED_PLAN_SELF_DEPENDENCY=" + sid)

    for constraint in constraints:
        term = CONSTRAINT_TERMS.get(constraint)
        if not term:
            continue
        for sid, step in steps.items():
            if step.get("impact") == "READ_ONLY":
                continue
            objective = str(step.get("objective", "")).lower()
            if term in objective:
                reasons.append(f"COMPILED_PLAN_CONSTRAINT_CONFLICT={constraint}:{sid}")

    return (steps if not reasons else None), reasons


def _tasks_from_compiled_plan(plan: dict[str, Any], steps: dict[str, dict[str, Any]], payload: dict[str, Any]) -> tuple[list[dict[str, Any]] | None, list[str]]:
    completed = {str(x) for x in payload.get("completed_steps", [])}
    unknown_completed = sorted(x for x in completed if x not in steps)
    if unknown_completed:
        return None, ["COMPLETED_STEP_UNKNOWN=" + ",".join(unknown_completed)]

    impossible: list[str] = []
    for sid in sorted(completed):
        deps = [str(dep) for dep in steps[sid].get("depends_on", [])]
        missing = [dep for dep in deps if dep not in completed]
        if missing:
            impossible.append(f"COMPLETED_STEP_DEPENDENCY_INCOMPLETE={sid}:{','.join(sorted(missing))}")
    if impossible:
        return None, impossible

    scope_by_step = payload.get("scope_by_step", {})
    default_scope = payload.get("scope", "compiled-plan")
    ordered = list(plan.get("steps", []))
    total = len(ordered)
    tasks: list[dict[str, Any]] = []
    for index, step in enumerate(ordered):
        sid = str(step["id"])
        scope = scope_by_step.get(sid, default_scope) if isinstance(scope_by_step, dict) else default_scope
        tasks.append({
            "id": sid,
            "status": "COMPLETE" if sid in completed else "PLANNED",
            "priority": total - index,
            "dependencies": list(step.get("depends_on", [])),
            "objective": step["objective"],
            "scope": scope,
        })
    return tasks, []


def _compiled_step_summary(step: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": step.get("id"),
        "objective": step.get("objective"),
        "depends_on": list(step.get("depends_on", [])),
        "expected_evidence": list(step.get("expected_evidence", [])),
        "impact": step.get("impact"),
        "authorization_required": step.get("authorization_required"),
        "verification": step.get("verification"),
        "stop_or_escalate_if": step.get("stop_or_escalate_if"),
        "execution_evidence": False,
    }


def _decide_tasks(payload: dict[str, Any], tasks: list[dict[str, Any]], compiled_steps: dict[str, dict[str, Any]] | None = None, compiled_plan: dict[str, Any] | None = None) -> dict[str, Any]:
    oi = load_operational_intelligence()
    analysis = oi.analyze(
        tasks,
        payload.get("events", []),
        payload.get("failures", []),
        payload.get("evidence", []),
    )
    recommendation = analysis["advisory_next_action"]
    protocol = "P16-CONTROLLER-v1" if compiled_steps is not None else "P12-CONTROLLER-v1"
    base = _base(recommendation, analysis, protocol)

    if compiled_steps is not None and compiled_plan is not None:
        base["compiled_plan"] = _plan_summary(compiled_plan)

    if recommendation["action"] == "no_action":
        return base | {"decision": "NO_ACTION", "task_id": None, "gates": {},
                       "reason": recommendation["reason"]}

    task_id = str(recommendation["task_id"])
    if recommendation["action"].startswith("resolve:"):
        return base | {"decision": "BLOCKED", "task_id": task_id, "gates": {},
                       "reason": recommendation["reason"] + ["CONTROLLER_ROUTING_REQUIRED"]}

    task_by_id = {str(task.get("id")): task for task in tasks}
    task = task_by_id.get(task_id)
    readiness_by_id = {str(row["id"]): row["readiness"] for row in analysis["readiness"]}
    scope = task.get("scope") if task else None
    objective = task.get("objective") if task else None
    capabilities = payload.get("capabilities", {})

    authorization_ok = _gate(payload.get("authorization"), {"NOT_REQUIRED", "ALREADY_GRANTED"})
    security_ok = _gate(payload.get("security_gate"), {"PASS", "NOT_APPLICABLE"})
    verification_ok = True
    step: dict[str, Any] | None = None

    if compiled_steps is not None:
        step = compiled_steps[task_id]
        impact = step.get("impact")
        authorization_required = step.get("authorization_required") is True
        verification = step.get("verification")
        verification_ok = isinstance(verification, str) and bool(verification.strip())
        if authorization_required:
            authorization_ok = _gate(payload.get("authorization"), {"ALREADY_GRANTED"})
        if impact in SECURITY_RELEVANT:
            security_ok = _gate(payload.get("security_gate"), {"PASS"})

    gates = {
        "scope": isinstance(scope, str) and bool(scope.strip()),
        "repository_revalidated": isinstance(payload.get("repository_head"), str)
        and bool(payload["repository_head"].strip()),
        "readiness": readiness_by_id.get(task_id) == "READY",
        "capability": _gate(capabilities.get(task_id), {"AVAILABLE"}),
        "authorization": authorization_ok,
        "security": security_ok,
        "verification_path": verification_ok,
    }

    if all(gates.values()) and isinstance(objective, str) and bool(objective.strip()):
        result = base | {"decision": "EXECUTION_CANDIDATE", "task_id": task_id,
                         "objective": objective, "scope": scope,
                         "repository_head": payload["repository_head"], "gates": gates,
                         "reason": recommendation["reason"]}
        if step is not None:
            result["compiled_step"] = _compiled_step_summary(step)
        return result

    failed = sorted(name for name, passed in gates.items() if not passed)
    if not isinstance(objective, str) or not objective.strip():
        failed.append("objective")
    result = base | {"decision": "BLOCKED", "task_id": task_id, "gates": gates,
                     "reason": recommendation["reason"] + ["FAILED_GATES=" + ",".join(failed)]}
    if step is not None:
        result["compiled_step"] = _compiled_step_summary(step)
    return result


def _blocked_compiled(plan: dict[str, Any], reasons: list[str]) -> dict[str, Any]:
    return {
        "protocol_version": "P16-CONTROLLER-v1",
        "decision": "BLOCKED",
        "task_id": None,
        "gates": {"compiled_plan": False},
        "reason": reasons,
        "compiled_plan": _plan_summary(plan),
        "authority": "UNCHANGED",
        "authorization": "UNCHANGED",
        "execution": "NONE",
    }


def decide(payload: dict[str, Any]) -> dict[str, Any]:
    """Return a non-executing controller decision for legacy tasks or a P16 plan."""
    if "compiled_plan" not in payload:
        return _decide_tasks(payload, payload.get("tasks", []))

    plan = payload.get("compiled_plan") or {}
    if not isinstance(plan, dict):
        return {
            "protocol_version": "P16-CONTROLLER-v1",
            "decision": "BLOCKED",
            "task_id": None,
            "gates": {"compiled_plan": False},
            "reason": ["COMPILED_PLAN_INVALID"],
            "authority": "UNCHANGED",
            "authorization": "UNCHANGED",
            "execution": "NONE",
        }

    steps, reasons = _validate_compiled_plan(plan)
    if steps is None:
        return _blocked_compiled(plan, reasons)

    tasks, task_reasons = _tasks_from_compiled_plan(plan, steps, payload)
    if tasks is None:
        return _blocked_compiled(plan, task_reasons)

    return _decide_tasks(payload, tasks, steps, plan)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="JSON task inventory or compiled plan plus independent controller inputs")
    parser.add_argument("--output", help="optional JSON output path")
    args = parser.parse_args()
    result = json.dumps(decide(json.loads(Path(args.input).read_text(encoding="utf-8"))), indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(result, encoding="utf-8")
    else:
        print(result, end="")


if __name__ == "__main__":
    main()
