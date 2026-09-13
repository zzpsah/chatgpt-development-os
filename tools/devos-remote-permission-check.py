#!/usr/bin/env python3
"""Side-effect-free evaluator for governed remote resource mutations.

This module decides whether an existing DevOS authorization envelope may be
reused for a requested remote operation. It never contacts a provider and
never treats provider credentials as authorization.
"""
from __future__ import annotations

from dataclasses import dataclass

IMPACT = {"READ_ONLY": 0, "LOW": 1, "HIGH": 2, "DESTRUCTIVE": 3}
CAPABILITIES = {
    "repository.create": "HIGH",
    "repository.delete": "DESTRUCTIVE",
    "branch.create": "LOW",
    "branch.update": "HIGH",
    "branch.delete": "DESTRUCTIVE",
    "branch.force_update": "DESTRUCTIVE",
    "file.create": "LOW",
    "file.update": "LOW",
    "file.delete": "HIGH",
    "pr.merge": "HIGH",
}


def capability_impact(capability: str) -> str | None:
    return CAPABILITIES.get(capability)


@dataclass(frozen=True)
class Authorization:
    provider: str
    owner: str
    repository: str | None
    resource: str | None
    capability: str
    workflow: str
    project: str
    impact_ceiling: str
    freshness: str | None
    authorization_id: str


@dataclass(frozen=True)
class Operation:
    provider: str
    owner: str
    repository: str | None
    resource: str | None
    capability: str
    workflow: str
    project: str
    impact: str
    freshness: str | None


def validate_operation(op: Operation) -> list[str]:
    reasons: list[str] = []
    if not op.provider.strip():
        reasons.append("INVALID_PROVIDER")
    if not op.owner.strip():
        reasons.append("INVALID_OWNER")
    if op.repository is not None and not op.repository.strip():
        reasons.append("INVALID_REPOSITORY")
    if op.resource is not None and not op.resource.strip():
        reasons.append("INVALID_RESOURCE")
    expected = capability_impact(op.capability)
    if expected is None:
        reasons.append("UNKNOWN_CAPABILITY")
    if op.impact not in IMPACT:
        reasons.append("INVALID_IMPACT")
    elif expected is not None and IMPACT[op.impact] < IMPACT[expected]:
        reasons.append("IMPACT_UNDERCLASSIFIED")
    return reasons


def validate_authorization(auth: Authorization) -> list[str]:
    reasons: list[str] = []
    if not auth.provider.strip():
        reasons.append("INVALID_AUTH_PROVIDER")
    if not auth.owner.strip():
        reasons.append("INVALID_AUTH_OWNER")
    if not auth.workflow.strip():
        reasons.append("INVALID_AUTH_WORKFLOW")
    if not auth.project.strip():
        reasons.append("INVALID_AUTH_PROJECT")
    if auth.impact_ceiling not in IMPACT:
        reasons.append("INVALID_AUTH_IMPACT_CEILING")
    if not auth.capability.strip() or auth.capability not in CAPABILITIES:
        reasons.append("INVALID_AUTH_CAPABILITY")
    if not auth.authorization_id.strip():
        reasons.append("MISSING_AUTHORIZATION_PROVENANCE")
    return reasons


def evaluate(auth: Authorization | None, op: Operation) -> tuple[str, list[str]]:
    op_reasons = validate_operation(op)
    if op_reasons:
        return "BLOCKED", op_reasons
    if auth is None:
        return "NEEDS_APPROVAL", ["NO_APPROVAL"]

    auth_reasons = validate_authorization(auth)
    if auth_reasons:
        return "BLOCKED", auth_reasons

    reasons: list[str] = []
    if auth.provider != op.provider:
        reasons.append("PROVIDER_SCOPE_CHANGED")
    if auth.owner != op.owner:
        reasons.append("OWNER_SCOPE_CHANGED")
    if auth.repository != op.repository:
        reasons.append("REPOSITORY_SCOPE_CHANGED")
    if auth.resource != op.resource:
        reasons.append("RESOURCE_SCOPE_CHANGED")
    if auth.capability != op.capability:
        reasons.append("CAPABILITY_SCOPE_CHANGED")
    if auth.workflow != op.workflow:
        reasons.append("WORKFLOW_SCOPE_CHANGED")
    if auth.project != op.project:
        reasons.append("PROJECT_SCOPE_CHANGED")
    if IMPACT.get(op.impact, 99) > IMPACT.get(auth.impact_ceiling, -1):
        reasons.append("IMPACT_EXCEEDS_APPROVAL_CEILING")
    if auth.freshness is not None and op.freshness != auth.freshness:
        reasons.append("FRESHNESS_CHANGED")
    return ("CONTINUE_WITH_EXISTING_APPROVAL", []) if not reasons else ("NEEDS_APPROVAL", reasons)


def actionable_hold(op: Operation, reasons: list[str]) -> dict:
    consequence = {
        "repository.create": "Creates a new remote repository with the selected owner/visibility policy.",
        "repository.delete": "Deletes the targeted remote repository and may make hosted data/history/settings unavailable.",
        "branch.create": "Creates a new remote branch at the selected target commit/ref.",
        "branch.update": "Moves the selected remote branch to a different commit and changes canonical remote state.",
        "branch.delete": "Deletes the selected remote branch; recovery depends on provider/history availability.",
        "branch.force_update": "Rewrites the selected remote ref and can discard reachable branch history; treat as destructive.",
        "file.create": "Creates a new remote repository file.",
        "file.update": "Replaces content in a remote repository file.",
        "file.delete": "Deletes a remote repository file.",
        "pr.merge": "Merges the selected pull request and changes the target branch's canonical history.",
    }.get(op.capability, "Changes remote repository state.")
    return {
        "status": "NEEDS_APPROVAL",
        "reason_codes": reasons,
        "next_action": op.capability,
        "target": {
            "provider": op.provider,
            "owner": op.owner,
            "repository": op.repository,
            "resource": op.resource,
        },
        "what_will_happen": consequence,
        "impact": op.impact,
        "approval_required": {
            "capability": op.capability,
            "target": op.resource or op.repository,
            "explicit": True,
        },
        "options": ["approve this exact action", "show the plan", "inspect target", "hold"],
        "authority": "UNCHANGED",
        "execution": "NONE",
        "mutation": "NONE",
    }
