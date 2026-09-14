#!/usr/bin/env python3
"""Read-only managed-repository delivery preflight.

Builds a P15 -> P16 -> P17 approval request for a local checkout without
editing it, running its tests, contacting a provider, committing, or pushing.
The only optional write is a JSON evidence packet outside the inspected repo.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = "DEVOS-MANAGED-REPOSITORY-PREFLIGHT-v1"
APPROVAL_PROTOCOL = "DEVOS-MANAGED-REPOSITORY-APPROVAL-REQUEST-v1"
SHA40 = re.compile(r"^[0-9a-f]{40}$")
BOUNDARIES = {"authority": "UNCHANGED", "authorization": "UNCHANGED", "execution": "NONE", "mutation": "NONE", "production_ready": False}


def load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools" / filename)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


P15 = load("managed_preflight_p15", "human-language-interpreter.py")
P16 = load("managed_preflight_p16", "semantic-goal-to-plan.py")
P17 = load("managed_preflight_p17", "step-readiness-orchestrator.py")


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def safe_path(path: str) -> bool:
    text = path.replace("\\", "/")
    return bool(text and not text.startswith("/") and not re.match(r"^[A-Za-z]:/", text) and ".." not in [x for x in text.split("/") if x])


def git(repo: Path, *args: str) -> tuple[int, str, str]:
    result = subprocess.run(["git", *args], cwd=repo, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def hold(reasons: list[str], **extra: Any) -> dict[str, Any]:
    return {"protocol": PROTOCOL, "status": "HOLD", "reasons": sorted(set(reasons)), **BOUNDARIES, **extra}


def preflight(repository: Path, phrase: str, allowed_paths: list[str], project: str | None = None) -> dict[str, Any]:
    repo = repository.resolve()
    if not repo.is_dir():
        return hold(["REPOSITORY_DIRECTORY_NOT_FOUND"])
    rc, top, _ = git(repo, "rev-parse", "--show-toplevel")
    if rc or Path(top).resolve() != repo:
        return hold(["REPOSITORY_ROOT_NOT_GIT_WORKTREE"])
    if not allowed_paths or any(not isinstance(path, str) or not safe_path(path) for path in allowed_paths):
        return hold(["ALLOWED_PATHS_INVALID"])
    if len(set(allowed_paths)) != len(allowed_paths):
        return hold(["ALLOWED_PATHS_DUPLICATE"])
    rc, head, _ = git(repo, "rev-parse", "HEAD")
    if rc or not SHA40.fullmatch(head):
        return hold(["REPOSITORY_HEAD_UNAVAILABLE"])
    rc, porcelain, _ = git(repo, "status", "--porcelain=v1")
    if rc:
        return hold(["WORKTREE_STATE_UNAVAILABLE"])
    if porcelain:
        return hold(["WORKTREE_NOT_CLEAN"], repository_head=head, observed_worktree=porcelain)

    project_id = project or repo.name
    p15 = P15.interpret({"phrase": phrase, "context": {"project": project_id}})
    if p15.get("decision") != "INTERPRETED" or not p15.get("objective") or not p15.get("intents"):
        return hold(["P15_OBJECTIVE_UNRESOLVED"], repository_head=head, p15=p15)
    plan = P16.compile_plan(p15["intents"][0], p15["objective"], project_id, p15.get("constraints", []), p15.get("ambiguity", []))
    if plan.get("decision") != "PLANNED" or len(plan.get("steps", [])) < 2:
        return hold(["P16_PLAN_NOT_BOUNDED_READ_THEN_CHANGE"], repository_head=head, p15=p15, p16=plan)
    read_step, change_step = plan["steps"][0], plan["steps"][-1]
    if read_step.get("impact") != "READ_ONLY" or change_step.get("impact") != "LOW_IMPACT_MUTATION":
        return hold(["P16_STEP_CLASSIFICATION_NOT_SUPPORTED"], repository_head=head, p15=p15, p16=plan)
    # Low impact is intentionally elevated to an explicit approval requirement in
    # this managed-repository preflight. This does not grant that approval.
    change_step["authorization_required"] = True
    change_step["expected_evidence"] = ["approved bounded diff", "passing configured tests", "fresh final readback"]
    change_step["verification"] = "run explicitly configured tests and read back every approved changed file"

    read_ready = P17.evaluate({"plan": plan, "step_id": read_step["id"], "compiled_repository_head": head, "current_repository_head": head, "completed_steps": [], "capabilities": {read_step["id"]: "AVAILABLE", change_step["id"]: "AVAILABLE"}, "authorization_by_step": {}, "security_gate_by_step": {}})
    if read_ready.get("status") != "READY":
        return hold(["P17_READ_PREFLIGHT_NOT_READY"], repository_head=head, p15=p15, p16=plan, p17=read_ready)
    change_ready = P17.evaluate({"plan": plan, "step_id": change_step["id"], "compiled_repository_head": head, "current_repository_head": head, "completed_steps": [read_step["id"]], "capabilities": {read_step["id"]: "AVAILABLE", change_step["id"]: "AVAILABLE"}, "authorization_by_step": {}, "security_gate_by_step": {}})
    if change_ready.get("status") != "NEEDS_APPROVAL" or "STEP_BOUND_AUTHORIZATION_REQUIRED" not in change_ready.get("reasons", []):
        return hold(["P17_CHANGE_APPROVAL_GATE_NOT_ENFORCED"], repository_head=head, p15=p15, p16=plan, p17=change_ready)

    request = {"protocol": APPROVAL_PROTOCOL, "approval_request_id": None, "project": project_id, "workflow": "managed-repository-delivery-v1", "repository_root": str(repo), "repository_head": head, "step_id": change_step["id"], "capability": "managed.repository.file.update", "targets": sorted(allowed_paths), "allowed_operations": ["file.create", "file.update"], "impact_ceiling": "LOW", "required_evidence": list(change_step["expected_evidence"]), "prohibited_operations": ["file.delete", "git.commit", "git.push", "deploy", "production_mutation", "credential_change", "secret_change", "database_mutation", "permission_change", "external_network_mutation"], "rule": "EXPLICIT_STEP_SCOPED_APPROVAL_REQUIRED"}
    request["approval_request_id"] = digest({k: v for k, v in request.items() if k != "approval_request_id"})
    result = hold(["EXPLICIT_STEP_SCOPED_APPROVAL_REQUIRED", "READ_ONLY_PREFLIGHT_COMPLETE"], repository=str(repo), repository_head=head, allowed_paths=sorted(allowed_paths), p15={"protocol": p15["protocol"], "decision": p15["decision"], "objective": p15["objective"]}, p16={"protocol": plan["protocol"], "decision": plan["decision"], "read_step": read_step["id"], "change_step": change_step["id"]}, p17={"read": read_ready, "change": change_ready}, approval_request=request)
    result["evidence_id"] = digest({k: v for k, v in result.items() if k != "evidence_id"})
    return result


def persist_external(packet: dict[str, Any], output: Path, repository: Path) -> None:
    target = output.resolve()
    repo = repository.resolve()
    if target == repo or repo in target.parents:
        raise ValueError("EVIDENCE_OUTPUT_MUST_BE_OUTSIDE_INSPECTED_REPOSITORY")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(packet, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", required=True, type=Path)
    parser.add_argument("--phrase", required=True)
    parser.add_argument("--allow-path", action="append", default=[])
    parser.add_argument("--project")
    parser.add_argument("--output", type=Path, help="optional evidence packet path outside inspected repository")
    args = parser.parse_args()
    result = preflight(args.repository, args.phrase, args.allow_path, args.project)
    if args.output:
        try:
            persist_external(result, args.output, args.repository)
            result["external_evidence_path"] = str(args.output.resolve())
        except ValueError as error:
            result = hold([str(error)], preflight=result)
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
    return 0 if result["status"] == "HOLD" and "READ_ONLY_PREFLIGHT_COMPLETE" in result.get("reasons", []) else 2


if __name__ == "__main__":
    raise SystemExit(main())
