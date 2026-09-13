#!/usr/bin/env python3
"""Adversarial cross-layer tests for DevOS authorization/security boundaries.

This corpus is deterministic and provider-free. It does not execute project work
or perform mutations. It verifies that tampered/stale evidence cannot cross the
P16/P17/controller/runtime boundary.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def load(name: str, relative: str):
    path = ROOT / relative
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


readiness = load("security_boundary_readiness", "tools/step-readiness-orchestrator.py")
handoff = load("security_boundary_handoff", "tools/devos-runtime-handoff.py")
bootstrap = load("security_boundary_bootstrap", "tools/devos-bootstrap.py")


def step(objective: str, impact: str, auth: bool) -> dict:
    return {
        "id": "S1",
        "objective": objective,
        "depends_on": [],
        "expected_evidence": ["fresh repository/runtime evidence"],
        "impact": impact,
        "authorization_required": auth,
        "verification": "fresh applicable verification",
        "stop_or_escalate_if": "missing authorization, failed Security Gate, or repository drift",
    }


def plan(objective: str = "delete production database", impact: str = "PRODUCTION_OR_DESTRUCTIVE", auth: bool = True) -> dict:
    return {
        "protocol": "DEVOS-GOAL-PLAN-v1",
        "project": "DEVOS",
        "objective": objective,
        "decision": "PLANNED",
        "authority": "UNCHANGED",
        "authorization": "UNCHANGED",
        "execution": "NONE",
        "constraints": [],
        "ambiguity": [],
        "steps": [step(objective, impact, auth)],
    }


def readiness_payload(p: dict, *, current_head: str = "abc", auth: bool = True, security: str | None = "PASS") -> dict:
    return {
        "plan": p,
        "step_id": "S1",
        "compiled_repository_head": "abc",
        "current_repository_head": current_head,
        "completed_steps": [],
        "capabilities": {"S1": "AVAILABLE"},
        "authorization_by_step": {"S1": "ALREADY_GRANTED"} if auth else {},
        "security_gate_by_step": {"S1": security} if security is not None else {},
    }


def test_destructive_action_disguised_as_low_impact() -> None:
    tampered = plan(impact="LOW_IMPACT_MUTATION", auth=False)
    result = readiness.evaluate(readiness_payload(tampered, auth=False, security=None))
    assert result["status"] == "BLOCKED", result
    assert any(reason.startswith("PLAN_STEP_IMPACT_MISMATCH=S1:") for reason in result["reasons"]), result


def test_old_authorization_cannot_survive_repository_drift() -> None:
    result = readiness.evaluate(readiness_payload(plan(), current_head="def", auth=True, security="PASS"))
    assert result["status"] == "STOP", result
    assert "STALE_PLAN_REPOSITORY_HEAD_CHANGED" in result["reasons"]


def test_wrong_repository_identity_holds_bootstrap() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        for rel in bootstrap.REQUIRED_FILES:
            target = root / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text((ROOT / rel).read_text(encoding="utf-8"), encoding="utf-8")
        manifest = root / ".ai/manifest.yaml"
        manifest.write_text(
            manifest.read_text(encoding="utf-8").replace(
                "canonical_repository: zzpsah/chatgpt-development-os",
                "canonical_repository: attacker/not-devos",
            ),
            encoding="utf-8",
        )
        ok, evidence = bootstrap.check(root)
        assert not ok, evidence
        assert ("canonical-identity", "HOLD") in evidence


def test_missing_authorization_and_security_gate_block() -> None:
    missing_auth = readiness.evaluate(readiness_payload(plan(), auth=False, security="PASS"))
    assert missing_auth["status"] == "NEEDS_APPROVAL", missing_auth

    missing_security = readiness.evaluate(readiness_payload(plan(), auth=True, security=None))
    assert missing_security["status"] == "NEEDS_EVIDENCE", missing_security

    failed_security = readiness.evaluate(readiness_payload(plan(), auth=True, security="FAIL"))
    assert failed_security["status"] == "BLOCKED", failed_security


def controller_envelope() -> dict:
    return {
        "protocol_version": "P16-CONTROLLER-v1",
        "decision": "EXECUTION_CANDIDATE",
        "authority": "UNCHANGED",
        "authorization": "UNCHANGED",
        "execution": "NONE",
        "task_id": "S1",
        "objective": "inspect repository",
        "scope": "compiled-plan",
        "repository_head": "abc",
        "compiled_step": {
            "id": "S1",
            "objective": "inspect repository",
            "impact": "READ_ONLY",
            "verification": "fresh repository evidence",
        },
        "gates": {
            "scope": True,
            "repository_revalidated": True,
            "readiness": True,
            "capability": True,
            "authorization": True,
            "security": True,
            "verification_path": True,
        },
    }


def ready_envelope() -> dict:
    return {
        "protocol": "DEVOS-STEP-READINESS-v1",
        "plan_protocol": "DEVOS-GOAL-PLAN-v1",
        "step_id": "S1",
        "status": "READY",
        "repository_head": "abc",
        "compiled_repository_head": "abc",
        "authority": "UNCHANGED",
        "authorization": "UNCHANGED",
        "execution": "NONE",
        "gates": {
            "plan": True,
            "freshness": True,
            "dependencies": True,
            "capability": True,
            "authorization": True,
            "security": True,
            "verification": True,
        },
        "step": {
            "id": "S1",
            "objective": "inspect repository",
            "impact": "READ_ONLY",
            "verification": "fresh repository evidence",
        },
    }


def test_wrong_step_and_readiness_bypass_block_runtime_handoff() -> None:
    controller = controller_envelope()
    wrong_step = ready_envelope()
    wrong_step["step_id"] = "S2"
    wrong_step["step"] = dict(wrong_step["step"], id="S2")
    result = handoff.build_p17_handoff(controller, wrong_step)
    assert result["status"] == "BLOCKED", result
    assert result["reason"] == "readiness_controller_step_mismatch"

    not_ready = ready_envelope()
    not_ready["status"] = "NEEDS_APPROVAL"
    result = handoff.build_p17_handoff(controller, not_ready)
    assert result["status"] == "BLOCKED", result
    assert result["reason"] == "step_not_ready"

    wrong_head = ready_envelope()
    wrong_head["repository_head"] = "def"
    result = handoff.build_p17_handoff(controller, wrong_head)
    assert result["status"] == "BLOCKED", result
    assert result["reason"] == "readiness_controller_repository_mismatch"


def test_plan_cannot_execute_directly() -> None:
    raw_plan = plan(objective="inspect repository", impact="READ_ONLY", auth=False)
    result = handoff.build_handoff(raw_plan)
    assert result["status"] == "BLOCKED", result
    assert result["reason"] == "controller_decision_not_executable"


def main() -> None:
    test_destructive_action_disguised_as_low_impact()
    test_old_authorization_cannot_survive_repository_drift()
    test_wrong_repository_identity_holds_bootstrap()
    test_missing_authorization_and_security_gate_block()
    test_wrong_step_and_readiness_bypass_block_runtime_handoff()
    test_plan_cannot_execute_directly()
    print("PASS: adversarial Security Gate / authorization boundary corpus")


if __name__ == "__main__":
    main()
