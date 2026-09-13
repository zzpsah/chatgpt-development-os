#!/usr/bin/env python3
"""Reference engine for actionable HOLD responses and scoped approval reuse.

This module is deterministic and side-effect free. It does not execute or
mutate repository/provider state. It evaluates whether a previously issued
approval may cover the next step and renders the information a human needs
when continuation must stop.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

STATUS_CHOICES = {"NEEDS_APPROVAL", "NEEDS_EVIDENCE", "BLOCKED", "HOLD", "STOP"}

@dataclass(frozen=True)
class Approval:
    project: str
    workflow: str
    capabilities: frozenset[str]
    targets: frozenset[str]
    impact_ceiling: str
    repository_head: str | None
    security_gate: str | None
    approval_id: str

@dataclass(frozen=True)
class NextStep:
    capability: str
    target: str
    impact: str
    repository_head: str | None
    security_gate: str | None
    description: str

IMPACT_ORDER = {
    "READ_ONLY": 0,
    "LOW": 1,
    "HIGH": 2,
    "DESTRUCTIVE": 3,
}


def can_reuse_approval(approval: Approval, step: NextStep, *, project: str, workflow: str) -> tuple[bool, list[str]]:
    """Return whether a scoped approval covers the next step without a new prompt."""
    reasons: list[str] = []
    if project != approval.project:
        reasons.append("PROJECT_SCOPE_CHANGED")
    if workflow != approval.workflow:
        reasons.append("WORKFLOW_SCOPE_CHANGED")
    if step.capability not in approval.capabilities:
        reasons.append("CAPABILITY_OUTSIDE_APPROVAL")
    if step.target not in approval.targets:
        reasons.append("TARGET_OUTSIDE_APPROVAL")
    if IMPACT_ORDER.get(step.impact, 99) > IMPACT_ORDER.get(approval.impact_ceiling, -1):
        reasons.append("IMPACT_EXCEEDS_APPROVAL_CEILING")
    if approval.repository_head is not None and step.repository_head != approval.repository_head:
        reasons.append("REPOSITORY_HEAD_CHANGED")
    if approval.security_gate is not None and step.security_gate != approval.security_gate:
        reasons.append("SECURITY_GATE_STATE_CHANGED")
    return (not reasons, reasons)


def continuation_decision(approval: Approval | None, step: NextStep, *, project: str, workflow: str) -> str:
    if approval is None:
        return "NEEDS_APPROVAL"
    reusable, _ = can_reuse_approval(approval, step, project=project, workflow=workflow)
    return "CONTINUE_WITH_EXISTING_APPROVAL" if reusable else "NEEDS_APPROVAL"


def actionable_hold(*, status: str, reason: str, next_step: NextStep | None,
                    required: Iterable[str], options: Iterable[str]) -> dict:
    if status not in STATUS_CHOICES:
        raise ValueError(f"unsupported actionable-hold status: {status}")
    if not reason.strip():
        raise ValueError("reason is required")
    payload = {
        "status": status,
        "reason": reason,
        "next": None,
        "impact": None,
        "approval_needed": list(required),
        "options": list(options),
        "authority": "UNCHANGED",
        "authorization": "UNCHANGED",
        "execution": "NONE",
        "mutation": "NONE",
    }
    if next_step is not None:
        payload["next"] = {
            "capability": next_step.capability,
            "target": next_step.target,
            "description": next_step.description,
        }
        payload["impact"] = next_step.impact
    return payload


def full_approval_summary(approval: Approval) -> dict:
    """Return an explicit human-readable approval scope without secrets."""
    return {
        "approval_id": approval.approval_id,
        "scope": {
            "project": approval.project,
            "workflow": approval.workflow,
            "capabilities": sorted(approval.capabilities),
            "targets": sorted(approval.targets),
            "impact_ceiling": approval.impact_ceiling,
            "repository_head": approval.repository_head,
            "security_gate": approval.security_gate,
        },
        "meaning": "FULL approval within the explicitly represented workflow scope; not blanket permission",
    }
