#!/usr/bin/env python3
"""Real DevOS continuation path: P15 -> P16 -> P17 -> controller.

This module is orchestration glue, not a new authorization system. Scoped approval
is validated before it is represented to P17 as step-bound authorization evidence.
No action is executed here.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def _load(name: str, filename: str):
    path = ROOT / "tools" / filename
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {filename}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


P15 = _load("devos_p15_interpreter", "human-language-interpreter.py")
P16 = _load("devos_p16_planner", "semantic-goal-to-plan.py")
P17 = _load("devos_p17_readiness", "step-readiness-orchestrator.py")
CONTROLLER = _load("devos_controller", "development-task-controller.py")
HOLD = _load("devos_actionable_hold", "devos-actionable-hold.py")

IMPACT_TO_APPROVAL = {
    "READ_ONLY": "READ_ONLY",
    "LOW_IMPACT_MUTATION": "LOW",
    "HIGH_IMPACT_MUTATION": "HIGH",
    "SECURITY_SENSITIVE": "HIGH",
    "PRODUCTION_OR_DESTRUCTIVE": "DESTRUCTIVE",
}


def _approval(raw: dict[str, Any] | None):
    if not isinstance(raw, dict):
        return None
    required = {"project", "workflow", "capabilities", "targets", "impact_ceiling", "approval_id"}
    if not required.issubset(raw):
        return None
    return HOLD.Approval(
        project=str(raw["project"]),
        workflow=str(raw["workflow"]),
        capabilities=frozenset(str(x) for x in raw.get("capabilities", [])),
        targets=frozenset(str(x) for x in raw.get("targets", [])),
        impact_ceiling=str(raw["impact_ceiling"]),
        repository_head=raw.get("repository_head"),
        security_gate=raw.get("security_gate"),
        approval_id=str(raw["approval_id"]),
    )


def _actionable(status: str, reason: str, *, capability: str, target: str,
                impact: str, repository_head: str | None, security_gate: str | None,
                description: str, required: list[str], reasons: list[str]) -> dict[str, Any]:
    step = HOLD.NextStep(capability, target, impact, repository_head, security_gate, description)
    examples = [
        f"approve {capability} on {target}",
        "show me the updated plan",
        "run the checks first",
        "hold",
    ]
    base = HOLD.actionable_hold(
        status=status,
        reason=reason,
        next_step=step,
        required=required,
        options=examples,
    )
    base.update({
        "next_action": description,
        "consequence": f"If approved and all P17 gates pass, {description}; this layer itself performs no execution.",
        "required_approval_or_evidence": required,
        "natural_language_examples": examples,
        "validation_reasons": reasons,
    })
    return base


def evaluate(payload: dict[str, Any]) -> dict[str, Any]:
    phrase = str(payload.get("phrase", "continue"))
    context = payload.get("context") or {}
    project = context.get("project")
    workflow = context.get("workflow")
    active_objective = context.get("active_objective")

    interpretation = P15.interpret({"phrase": phrase, "context": context})
    if interpretation.get("decision") != "INTERPRETED" or "RESUME_WORK" not in interpretation.get("intents", []):
        return {
            "protocol": "DEVOS-CONTINUATION-PATH-v1",
            "status": "BLOCKED",
            "reason": "P15 did not resolve a continuation request",
            "p15": interpretation,
            "authority": "UNCHANGED",
            "authorization": "UNCHANGED",
            "execution": "NONE",
            "mutation": "NONE",
        }
    if not isinstance(workflow, str) or not workflow.strip() or not isinstance(active_objective, str) or not active_objective.strip():
        return {
            "protocol": "DEVOS-CONTINUATION-PATH-v1",
            "status": "BLOCKED",
            "reason": "project/workflow continuation context is incomplete",
            "p15": interpretation,
            "authority": "UNCHANGED",
            "authorization": "UNCHANGED",
            "execution": "NONE",
            "mutation": "NONE",
        }

    intent = interpretation.get("intents", ["RESUME_WORK"])[0]
    plan = P16.compile_plan(intent, active_objective, project, interpretation.get("constraints", []), interpretation.get("ambiguity", []))
    if plan.get("decision") != "PLANNED":
        return {
            "protocol": "DEVOS-CONTINUATION-PATH-v1",
            "status": "BLOCKED",
            "reason": "P16 did not produce a planned continuation",
            "p15": interpretation,
            "p16": plan,
            "authority": "UNCHANGED",
            "authorization": "UNCHANGED",
            "execution": "NONE",
            "mutation": "NONE",
        }

    completed = [str(x) for x in payload.get("completed_steps", [])]
    step = next((s for s in plan["steps"] if str(s["id"]) not in set(completed)), None)
    if step is None:
        return {
            "protocol": "DEVOS-CONTINUATION-PATH-v1",
            "status": "NO_ACTION",
            "p15": interpretation,
            "p16": plan,
            "authority": "UNCHANGED",
            "authorization": "UNCHANGED",
            "execution": "NONE",
            "mutation": "NONE",
        }

    sid = str(step["id"])
    step_context = (payload.get("step_context_by_step") or {}).get(sid, {})
    capability = str(step_context.get("capability", ""))
    target = str(step_context.get("target", ""))
    current_head = payload.get("current_repository_head")
    security_gate = (payload.get("security_gate_by_step") or {}).get(sid)
    abstract_impact = IMPACT_TO_APPROVAL.get(str(step.get("impact")), "DESTRUCTIVE")
    description = str(step.get("objective", "continue planned step"))

    if not capability or not target:
        hold = _actionable(
            "NEEDS_EVIDENCE",
            "The continuation target/capability evidence is incomplete.",
            capability=capability or "UNKNOWN",
            target=target or "UNKNOWN",
            impact=abstract_impact,
            repository_head=current_head,
            security_gate=security_gate,
            description=description,
            required=["step capability and exact target evidence"],
            reasons=["STEP_SCOPE_EVIDENCE_MISSING"],
        )
        return {"protocol": "DEVOS-CONTINUATION-PATH-v1", "status": "HOLD", "hold": hold,
                "p15": interpretation, "p16": plan, "authority": "UNCHANGED",
                "authorization": "UNCHANGED", "execution": "NONE", "mutation": "NONE"}

    approval = _approval(payload.get("scoped_approval"))
    next_step = HOLD.NextStep(capability, target, abstract_impact, current_head, security_gate, description)
    if approval is None:
        reasons = ["SCOPED_APPROVAL_MISSING_OR_INVALID"]
        reusable = False
    else:
        reusable, reasons = HOLD.can_reuse_approval(approval, next_step, project=str(project), workflow=workflow)

    if not reusable:
        hold = _actionable(
            "NEEDS_APPROVAL",
            "The next continuation step is not covered by a current valid scoped approval.",
            capability=capability,
            target=target,
            impact=abstract_impact,
            repository_head=current_head,
            security_gate=security_gate,
            description=description,
            required=[f"fresh scoped approval for {capability} on {target} at the current repository/security state"],
            reasons=reasons,
        )
        return {"protocol": "DEVOS-CONTINUATION-PATH-v1", "status": "HOLD", "hold": hold,
                "p15": interpretation, "p16": plan, "approval_reuse": "REJECTED",
                "authority": "UNCHANGED", "authorization": "UNCHANGED",
                "execution": "NONE", "mutation": "NONE"}

    capabilities = dict(payload.get("capabilities") or {})
    capabilities.setdefault(sid, "AVAILABLE")
    p17_payload = {
        "plan": plan,
        "step_id": sid,
        "compiled_repository_head": current_head,
        "current_repository_head": current_head,
        "completed_steps": completed,
        "capabilities": capabilities,
        "authorization_by_step": {sid: "ALREADY_GRANTED"},
        "security_gate_by_step": dict(payload.get("security_gate_by_step") or {}),
    }
    readiness = P17.evaluate(p17_payload)
    if readiness.get("status") != "READY":
        required = ["fresh P17 readiness/security evidence"]
        hold = _actionable(
            "NEEDS_EVIDENCE" if readiness.get("status") == "NEEDS_EVIDENCE" else "BLOCKED",
            "P17 readiness did not permit continuation.",
            capability=capability,
            target=target,
            impact=abstract_impact,
            repository_head=current_head,
            security_gate=security_gate,
            description=description,
            required=required,
            reasons=[str(x) for x in readiness.get("reasons", [])],
        )
        return {"protocol": "DEVOS-CONTINUATION-PATH-v1", "status": "HOLD", "hold": hold,
                "p15": interpretation, "p16": plan, "p17": readiness,
                "approval_reuse": "SCOPED_APPROVAL_REUSED",
                "authority": "UNCHANGED", "authorization": "UNCHANGED",
                "execution": "NONE", "mutation": "NONE"}

    controller_payload = {
        "compiled_plan": plan,
        "completed_steps": completed,
        "scope": workflow,
        "repository_head": current_head,
        "capabilities": capabilities,
        "authorization": "ALREADY_GRANTED",
        "security_gate": "PASS" if security_gate == "PASS" else security_gate,
        "events": payload.get("events", []),
        "failures": payload.get("failures", []),
        "evidence": payload.get("evidence", []),
    }
    controller = CONTROLLER.decide(controller_payload)
    status = "CONTINUE" if controller.get("decision") == "EXECUTION_CANDIDATE" else "HOLD"
    result = {
        "protocol": "DEVOS-CONTINUATION-PATH-v1",
        "status": status,
        "approval_reuse": "SCOPED_APPROVAL_REUSED",
        "p15": interpretation,
        "p16": plan,
        "p17": readiness,
        "controller": controller,
        "authority": "UNCHANGED",
        "authorization": "UNCHANGED",
        "execution": "NONE",
        "mutation": "NONE",
    }
    if status == "HOLD":
        result["hold"] = _actionable(
            "BLOCKED",
            "The controller did not produce an execution candidate after P17 readiness.",
            capability=capability,
            target=target,
            impact=abstract_impact,
            repository_head=current_head,
            security_gate=security_gate,
            description=description,
            required=["resolve controller gates/evidence"],
            reasons=[str(x) for x in controller.get("reason", [])],
        )
    return result
