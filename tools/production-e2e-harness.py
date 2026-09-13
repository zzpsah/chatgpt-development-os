#!/usr/bin/env python3
"""Production E2E Harness reference implementation.

Composes existing DevOS modules across the full governed path:
human request -> interpretation -> P16 plan -> P17 readiness -> controller ->
runtime handoff -> bounded adapter execution -> verification -> durable evidence.

The harness never creates authorization. Runtime requests, verification commands,
and evidence persistence are explicit caller-supplied inputs and remain bounded by
existing adapters.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def _load(name: str, relative: str):
    path = ROOT / relative
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {relative}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


interpreter = _load("e2e_hli", "tools/human-language-interpreter.py")
compiler = _load("e2e_plan", "tools/semantic-goal-to-plan.py")
readiness_mod = _load("e2e_readiness", "tools/step-readiness-orchestrator.py")
controller = _load("e2e_controller", "tools/development-task-controller.py")
handoff_mod = _load("e2e_handoff", "tools/devos-runtime-handoff.py")
bridge = _load("e2e_bridge", "tools/runtime-adapter-bridge.py")
verification_adapter = _load("e2e_verification", "adapters/reference-verification.py")
host_adapter = _load("e2e_host", "adapters/reference-host.py")

PROTOCOL = "DEVOS-PRODUCTION-E2E-v1"
TERMINAL_FAILURES = {"BLOCKED", "UNAVAILABLE", "FAILED"}
READ_OPERATIONS = {
    "filesystem.read",
    "git.inspect",
    "github.inspect.repository",
    "github.inspect.commit",
    "github.inspect.workflow_run",
}
MUTATION_OPERATIONS = {"filesystem.write_scoped", "github.mutate.file"}
GATED_IMPACTS = {"HIGH_IMPACT_MUTATION", "SECURITY_SENSITIVE", "PRODUCTION_OR_DESTRUCTIVE"}


def _blocked(stage: str, reason: Any, trace: dict[str, Any]) -> dict[str, Any]:
    return {
        "protocol": PROTOCOL,
        "status": "BLOCKED",
        "stage": stage,
        "reason": reason,
        "trace": trace,
        "authority": "UNCHANGED",
        "authorization": "UNCHANGED",
    }


def _persist_evidence(project_root: Path, payload: dict[str, Any], trace: dict[str, Any]) -> dict[str, Any]:
    persistence = payload.get("persistence") or {}
    path = persistence.get("path")
    authorization = persistence.get("authorization")
    if not isinstance(path, str) or not path.startswith(".ai/") or ".." in Path(path).parts:
        return {"status": "BLOCKED", "reason": "persistence path must be a bounded .ai/ path"}
    if authorization != "ALREADY_GRANTED":
        return {"status": "BLOCKED", "reason": "explicit persistence authorization required"}

    evidence_packet = {
        "protocol": PROTOCOL,
        "status": "VERIFIED",
        "project": trace["interpretation"].get("project"),
        "objective": trace["interpretation"].get("objective"),
        "repository_head": payload.get("repository_head"),
        "step_id": trace["readiness"].get("step_id"),
        "runtime_status": trace["runtime"].get("status"),
        "verification_status": trace["verification"].get("status"),
        "authority": "UNCHANGED",
        "authorization": "UNCHANGED",
        "execution_evidence": True,
    }
    content = json.dumps(evidence_packet, indent=2, sort_keys=True) + "\n"
    return host_adapter.write_text(project_root, path, content, authorization)


def _prepare_runtime_request(
    step: dict[str, Any],
    step_id: str,
    raw_request: Any,
    authorization_by_step: dict[str, Any],
    security_gate_by_step: dict[str, Any],
) -> tuple[dict[str, Any] | None, str | None]:
    if not isinstance(raw_request, dict):
        return None, "runtime_request must be an object"
    if raw_request.get("step_id") not in (None, step_id):
        return None, "runtime request step_id does not match selected step"

    request = dict(raw_request)
    request.pop("step_id", None)
    operation = request.get("operation")
    if operation not in READ_OPERATIONS | MUTATION_OPERATIONS:
        return None, "runtime operation is not in the bounded E2E allowlist"

    impact = step.get("impact")
    if impact == "READ_ONLY" and operation not in READ_OPERATIONS:
        return None, "read-only compiled step cannot execute a mutation operation"

    if operation in MUTATION_OPERATIONS:
        if impact == "READ_ONLY":
            return None, "mutation operation conflicts with read-only step impact"
        if authorization_by_step.get(step_id) != "ALREADY_GRANTED":
            return None, "mutation operation requires exact-step authorization"
        request["authorization"] = "ALREADY_GRANTED"
        if operation.startswith("github."):
            if security_gate_by_step.get(step_id) != "PASS":
                return None, "remote mutation requires exact-step Security Gate PASS"
            request["security_gate"] = "PASS"
    else:
        # Eligibility authorization and runtime-operation authorization are distinct.
        # A security-sensitive review may require approval to become READY while the
        # underlying read capability itself remains a NOT_REQUIRED operation.
        request["authorization"] = "NOT_REQUIRED"

    return request, None


def run(payload: dict[str, Any], github_client: Any = None) -> dict[str, Any]:
    trace: dict[str, Any] = {}
    project_root_raw = payload.get("project_root")
    if not isinstance(project_root_raw, str) or not project_root_raw:
        return _blocked("INPUT", "project_root is required", trace)
    project_root = Path(project_root_raw).resolve()
    if not project_root.is_dir():
        return _blocked("INPUT", "project_root must be an existing directory", trace)

    phrase = payload.get("human_request")
    context = payload.get("context") or {}
    if not isinstance(phrase, str) or not phrase.strip() or not isinstance(context, dict):
        return _blocked("INTERPRETATION", "human_request and object context are required", trace)

    interpreted = interpreter.interpret({"phrase": phrase, "context": context})
    trace["interpretation"] = interpreted
    if interpreted.get("decision") != "INTERPRETED":
        return _blocked("INTERPRETATION", interpreted.get("ambiguity", []), trace)
    intents = interpreted.get("intents") or []
    if not intents:
        return _blocked("INTERPRETATION", "no canonical intent produced", trace)

    plan = compiler.compile_plan(
        intents[0],
        interpreted.get("objective") or "",
        interpreted.get("project"),
        interpreted.get("constraints") or [],
        interpreted.get("ambiguity") or [],
    )
    trace["plan"] = plan
    if plan.get("decision") != "PLANNED" or not plan.get("steps"):
        return _blocked("PLANNING", plan.get("blockers") or plan.get("ambiguity") or plan.get("decision"), trace)

    step_id = payload.get("step_id") or plan["steps"][0]["id"]
    step = next((s for s in plan["steps"] if s.get("id") == step_id), None)
    if step is None:
        return _blocked("READINESS", "selected step is not in compiled plan", trace)

    repository_head = payload.get("repository_head")
    if not isinstance(repository_head, str) or not repository_head:
        return _blocked("READINESS", "repository_head evidence is required", trace)

    completed_steps = payload.get("completed_steps") or []
    capabilities = payload.get("capabilities") or {}
    authorization_by_step = payload.get("authorization_by_step") or {}
    security_gate_by_step = payload.get("security_gate_by_step") or {}
    if not all(isinstance(x, dict) for x in (capabilities, authorization_by_step, security_gate_by_step)):
        return _blocked("READINESS", "capability/auth/security evidence maps must be objects", trace)

    readiness = readiness_mod.evaluate({
        "plan": plan,
        "step_id": step_id,
        "compiled_repository_head": payload.get("compiled_repository_head", repository_head),
        "current_repository_head": repository_head,
        "completed_steps": completed_steps,
        "capabilities": capabilities,
        "authorization_by_step": authorization_by_step,
        "security_gate_by_step": security_gate_by_step,
    })
    trace["readiness"] = readiness
    if readiness.get("status") != "READY":
        return _blocked("READINESS", readiness.get("reasons", []), trace)

    auth_required = step.get("authorization_required") is True
    controller_authorization = "ALREADY_GRANTED" if auth_required else "NOT_REQUIRED"
    if auth_required and authorization_by_step.get(step_id) != "ALREADY_GRANTED":
        return _blocked("CONTROLLER", "exact-step authorization missing", trace)
    gated = step.get("impact") in GATED_IMPACTS
    controller_security = "PASS" if gated else "NOT_APPLICABLE"
    if gated and security_gate_by_step.get(step_id) != "PASS":
        return _blocked("CONTROLLER", "Security Gate PASS missing for gated impact", trace)

    decision = controller.decide({
        "compiled_plan": plan,
        "repository_head": repository_head,
        "scope": payload.get("scope", "repository"),
        "completed_steps": completed_steps,
        "capabilities": capabilities,
        "authorization": controller_authorization,
        "security_gate": controller_security,
    })
    trace["controller"] = decision
    if decision.get("decision") != "EXECUTION_CANDIDATE" or decision.get("task_id") != step_id:
        return _blocked("CONTROLLER", decision.get("reason", []), trace)

    handoff = handoff_mod.build_p17_handoff(decision, readiness)
    trace["handoff"] = handoff
    if handoff.get("status") != "READY_FOR_RUNTIME":
        return _blocked("HANDOFF", handoff.get("reason"), trace)

    runtime_request, runtime_error = _prepare_runtime_request(
        step,
        step_id,
        payload.get("runtime_request") or {},
        authorization_by_step,
        security_gate_by_step,
    )
    if runtime_error:
        return _blocked("RUNTIME", runtime_error, trace)
    assert runtime_request is not None

    runtime_result = bridge.execute(runtime_request, project_root, github_client=github_client)
    trace["runtime"] = runtime_result
    if runtime_result.get("status") in TERMINAL_FAILURES or runtime_result.get("status") != "SUCCESS":
        return _blocked("RUNTIME", runtime_result.get("reason") or runtime_result.get("status"), trace)

    verification = payload.get("verification") or {}
    if not isinstance(verification, dict):
        return _blocked("VERIFICATION", "verification must be an object", trace)
    verification_result = verification_adapter.run_verification(project_root, verification)
    trace["verification"] = verification_result
    if verification_result.get("status") != "VERIFIED":
        return _blocked("VERIFICATION", verification_result.get("reason") or verification_result.get("stderr"), trace)

    persistence_result = _persist_evidence(project_root, payload, trace)
    trace["persistence"] = persistence_result
    if persistence_result.get("status") != "SUCCESS":
        return _blocked("PERSISTENCE", persistence_result.get("reason"), trace)

    persisted_path = (payload.get("persistence") or {}).get("path")
    recovery_result = host_adapter.read_text(project_root, persisted_path)
    trace["recovery"] = recovery_result
    if recovery_result.get("status") != "SUCCESS" or PROTOCOL not in recovery_result.get("content", ""):
        return _blocked("RECOVERY", recovery_result.get("reason") or "persisted evidence could not be recovered", trace)

    return {
        "protocol": PROTOCOL,
        "status": "COMPLETE",
        "stage": "RECOVERY",
        "project": interpreted.get("project"),
        "objective": interpreted.get("objective"),
        "step_id": step_id,
        "repository_head": repository_head,
        "trace": trace,
        "authority": "UNCHANGED",
        "authorization": "UNCHANGED",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="JSON E2E scenario payload")
    parser.add_argument("--output", help="optional output JSON path")
    args = parser.parse_args()
    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    result = json.dumps(run(payload), indent=2, sort_keys=True) + "\n"
    if args.output:
        Path(args.output).write_text(result, encoding="utf-8")
    else:
        print(result, end="")


if __name__ == "__main__":
    main()
