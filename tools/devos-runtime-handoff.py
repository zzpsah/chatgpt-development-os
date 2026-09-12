#!/usr/bin/env python3
"""Bounded controller-to-runtime handoff; never executes work or grants authority."""
from __future__ import annotations

from typing import Any


def build_handoff(controller_result: dict[str, Any], task: dict[str, Any]) -> dict[str, Any]:
    """Convert an independently approved controller candidate into a runtime envelope.

    The caller must supply explicit capability, authorization, and Security Gate results.
    This function only validates the boundary and constructs data for the existing runtime.
    """
    reasons: list[str] = []
    if controller_result.get("decision") != "EXECUTION_CANDIDATE":
        reasons.append("CONTROLLER_CANDIDATE_REQUIRED")
    if controller_result.get("authority") != "UNCHANGED":
        reasons.append("AUTHORITY_BOUNDARY_VIOLATION")
    if controller_result.get("execution") != "NONE":
        reasons.append("EXECUTION_MUST_REMAIN_NONE")
    if task.get("capability_required") and task.get("capability_status") != "AVAILABLE":
        reasons.append("CAPABILITY_NOT_AVAILABLE")
    if task.get("authorization", "NOT_REQUIRED") == "REQUIRED" and task.get("authorization_status") != "APPROVED":
        reasons.append("AUTHORIZATION_NOT_APPROVED")
    security_required = task.get("security_relevant", False)
    if security_required and task.get("security_status") != "PASS":
        reasons.append("SECURITY_GATE_NOT_PASSED")
    if not task.get("objective"):
        reasons.append("OBJECTIVE_MISSING")

    if reasons:
        return {
            "handoff_version": "P12-HANDOFF-v1",
            "status": "HOLD",
            "reasons": reasons,
            "authority": "UNCHANGED",
            "execution": "NONE",
        }

    return {
        "handoff_version": "P12-HANDOFF-v1",
        "status": "APPROVED_FOR_RUNTIME",
        "authority": "UNCHANGED",
        "execution": "DELEGATE_TO_EXISTING_RUNTIME",
        "work_unit": {
            "task_id": task["id"],
            "objective": task["objective"],
            "capability": task.get("capability_required"),
        },
        "gates": {
            "capability": task.get("capability_status", "NOT_REQUIRED"),
            "authorization": task.get("authorization_status", "NOT_REQUIRED"),
            "security": task.get("security_status", "NOT_APPLICABLE"),
        },
        "evidence": [],
        "verification": "PENDING_RUNTIME",
    }


def accept_runtime_result(handoff: dict[str, Any], runtime_result: dict[str, Any]) -> dict[str, Any]:
    """Close the handoff only from raw runtime evidence; never fabricate evidence."""
    if handoff.get("status") != "APPROVED_FOR_RUNTIME":
        return {"status": "HOLD", "reason": "HANDOFF_NOT_APPROVED", "evidence": []}
    evidence = runtime_result.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        return {"status": "FAILED", "reason": "RAW_EXECUTION_EVIDENCE_REQUIRED", "evidence": []}
    return {
        "status": runtime_result.get("status", "FAILED"),
        "evidence": evidence,
        "verification": runtime_result.get("verification", "UNVERIFIED"),
        "security": runtime_result.get("security", "UNVERIFIED"),
    }
