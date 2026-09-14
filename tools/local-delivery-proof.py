#!/usr/bin/env python3
"""Bounded automated delivery proof in a disposable local Git repository.

This is a deliberately small runtime proof.  It uses P15 -> P16 -> P17,
requires an exact scoped approval for one low-impact file update, verifies the
result, and persists a non-secret evidence packet in the disposable project.
It never contacts a provider, commits, pushes, deploys, or uses credentials.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = "DEVOS-LOCAL-DELIVERY-PROOF-v1"
APPROVAL_PROTOCOL = "DEVOS-LOCAL-DELIVERY-APPROVAL-v1"
TARGET = "delivery-marker.txt"
EVIDENCE_PATH = ".ai/local-delivery-evidence.json"


def load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools" / filename)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


P15 = load("local_delivery_p15", "human-language-interpreter.py")
P16 = load("local_delivery_p16", "semantic-goal-to-plan.py")
P17 = load("local_delivery_p17", "step-readiness-orchestrator.py")
CONTROLLER = load("local_delivery_controller", "development-task-controller.py")
HANDOFF = load("local_delivery_handoff", "devos-runtime-handoff.py")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(["git", *args], cwd=repo, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if result.returncode:
        raise RuntimeError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def initialize(repo: Path) -> str:
    repo.mkdir(parents=True, exist_ok=True)
    git(repo, "init", "-q")
    git(repo, "config", "user.email", "devos-proof@example.invalid")
    git(repo, "config", "user.name", "DevOS Local Proof")
    (repo / TARGET).write_text("before\n", encoding="utf-8")
    (repo / "verify_marker.py").write_text(
        "from pathlib import Path\nassert Path('delivery-marker.txt').read_text(encoding='utf-8') == 'after\\n'\n",
        encoding="utf-8",
    )
    git(repo, "add", TARGET, "verify_marker.py")
    git(repo, "commit", "-qm", "initial disposable delivery fixture")
    return git(repo, "rev-parse", "HEAD")


def approval_for(*, project: str, repository_head: str, step_id: str) -> dict[str, Any]:
    return {
        "protocol": APPROVAL_PROTOCOL,
        "approval_id": "LOCAL-DELIVERY-APPROVAL-1",
        "project": project,
        "repository_head": repository_head,
        "step_id": step_id,
        "capability": "local.file.update",
        "target": TARGET,
        "impact_ceiling": "LOW_IMPACT_MUTATION",
    }


def validate_approval(approval: Any, *, project: str, repository_head: str, step_id: str) -> str | None:
    if not isinstance(approval, dict) or approval.get("protocol") != APPROVAL_PROTOCOL:
        return "SCOPED_APPROVAL_INVALID"
    expected = {
        "project": project,
        "repository_head": repository_head,
        "step_id": step_id,
        "capability": "local.file.update",
        "target": TARGET,
        "impact_ceiling": "LOW_IMPACT_MUTATION",
    }
    for key, value in expected.items():
        if approval.get(key) != value:
            return f"SCOPED_APPROVAL_{key.upper()}_MISMATCH"
    if not isinstance(approval.get("approval_id"), str) or not approval["approval_id"].strip():
        return "SCOPED_APPROVAL_ID_INVALID"
    return None


def blocked(reason: str) -> dict[str, Any]:
    return {"protocol": PROTOCOL, "status": "HOLD", "reason": reason, "authority": "UNCHANGED", "authorization": "UNCHANGED", "execution": "NONE", "mutation": "NONE"}


def prepare(repo: Path) -> dict[str, Any]:
    if (repo / ".git").exists():
        return blocked("DISPOSABLE_REPOSITORY_MUST_BE_NEW")
    initial_head = initialize(repo)
    return {
        "protocol": PROTOCOL, "status": "PREPARED", "project": str(repo.resolve()),
        "repository_head": initial_head, "target": TARGET, "capability": "local.file.update",
        "required_approval": {"protocol": APPROVAL_PROTOCOL, "step_id": "S2", "impact_ceiling": "LOW_IMPACT_MUTATION"},
        "authority": "UNCHANGED", "authorization": "UNCHANGED", "execution": "NONE", "mutation": "NONE",
    }


def run(repo: Path, phrase: str, approval: dict[str, Any] | None) -> dict[str, Any]:
    if not (repo / ".git").exists():
        return blocked("DISPOSABLE_REPOSITORY_NOT_PREPARED")
    initial_head = git(repo, "rev-parse", "HEAD")
    project = str(repo.resolve())
    before = repo / TARGET
    before_digest = digest(before)

    p15 = P15.interpret({"phrase": phrase, "context": {"project": project}})
    if p15["decision"] != "INTERPRETED" or not p15["objective"]:
        return blocked("P15_DID_NOT_PRODUCE_A_CLEAR_OBJECTIVE") | {"p15": p15}
    plan = P16.compile_plan(p15["intents"][0], p15["objective"], project, p15["constraints"], p15["ambiguity"])
    if plan["decision"] != "PLANNED" or len(plan["steps"]) != 2:
        return blocked("P16_DID_NOT_PRODUCE_BOUNDED_READ_THEN_WRITE_PLAN") | {"p15": p15, "p16": plan}
    inspect_step, update_step = plan["steps"]
    if update_step["impact"] != "LOW_IMPACT_MUTATION" or update_step["authorization_required"] is not False:
        return blocked("P16_LOCAL_UPDATE_CLASSIFICATION_INVALID") | {"p15": p15, "p16": plan}

    inspect_readiness = P17.evaluate({
        "plan": plan, "step_id": inspect_step["id"], "compiled_repository_head": initial_head,
        "current_repository_head": git(repo, "rev-parse", "HEAD"), "completed_steps": [],
        "capabilities": {inspect_step["id"]: "AVAILABLE", update_step["id"]: "AVAILABLE"},
        "authorization_by_step": {}, "security_gate_by_step": {},
    })
    if inspect_readiness["status"] != "READY":
        return blocked("P17_INSPECTION_NOT_READY") | {"p15": p15, "p16": plan, "p17": inspect_readiness}
    inspected_digest = digest(before)
    if inspected_digest != before_digest:
        return blocked("LOCAL_TARGET_CHANGED_BEFORE_APPROVAL")

    approval_error = validate_approval(approval, project=project, repository_head=initial_head, step_id=update_step["id"])
    if approval_error:
        return blocked(approval_error) | {"p15": p15, "p16": plan, "before_digest": before_digest}

    update_readiness = P17.evaluate({
        "plan": plan, "step_id": update_step["id"], "compiled_repository_head": initial_head,
        "current_repository_head": git(repo, "rev-parse", "HEAD"), "completed_steps": [inspect_step["id"]],
        "capabilities": {inspect_step["id"]: "AVAILABLE", update_step["id"]: "AVAILABLE"},
        "authorization_by_step": {update_step["id"]: "ALREADY_GRANTED"}, "security_gate_by_step": {},
    })
    if update_readiness["status"] != "READY":
        return blocked("P17_UPDATE_NOT_READY") | {"p15": p15, "p16": plan, "p17": update_readiness}

    controller = CONTROLLER.decide({
        "compiled_plan": plan, "repository_head": initial_head, "scope": project,
        "completed_steps": [inspect_step["id"]], "authorization": "ALREADY_GRANTED", "security_gate": "NOT_APPLICABLE",
        "capabilities": {inspect_step["id"]: "AVAILABLE", update_step["id"]: "AVAILABLE"},
    })
    handoff = HANDOFF.build_p17_handoff(controller, update_readiness)
    if controller.get("decision") != "EXECUTION_CANDIDATE" or handoff.get("status") != "READY_FOR_RUNTIME":
        return blocked("CONTROLLER_OR_HANDOFF_NOT_READY") | {"controller": controller, "handoff": handoff}

    if digest(before) != before_digest:
        return blocked("LOCAL_TARGET_CHANGED_BEFORE_WRITE")
    before.write_text("after\n", encoding="utf-8")
    test = subprocess.run([sys.executable, "verify_marker.py"], cwd=repo, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    after_digest = digest(before)
    diff = git(repo, "diff", "--", TARGET)
    verified = test.returncode == 0 and before.read_text(encoding="utf-8") == "after\n" and before_digest != after_digest and diff
    evidence = {
        "protocol": PROTOCOL,
        "status": "VERIFIED" if verified else "HOLD",
        "repository": project,
        "initial_repository_head": initial_head,
        "target": TARGET,
        "before_sha256": before_digest,
        "after_sha256": after_digest,
        "test": {"command": [sys.executable, "verify_marker.py"], "exit_code": test.returncode},
        "observed_diff": diff,
        "p15": {"protocol": p15["protocol"], "intents": p15["intents"], "decision": p15["decision"]},
        "p16": {"protocol": plan["protocol"], "step_id": update_step["id"], "impact": update_step["impact"]},
        "p17": {"protocol": update_readiness["protocol"], "status": update_readiness["status"]},
        "scoped_approval_id": approval["approval_id"],
        "authority": "UNCHANGED",
        "authorization": "STEP_SCOPED_APPROVAL_VERIFIED",
        "execution": "LOCAL_FILE_UPDATE_COMPLETED" if verified else "NONE",
        "mutation": "LOCAL_DISPOSABLE_REPOSITORY_ONLY" if verified else "NONE",
        "limitations": ["No provider, deployment, credential, database, permission, or destructive operation was used.", "The disposable repository has an uncommitted verified diff; no commit or push is performed."],
    }
    packet = repo / EVIDENCE_PATH
    packet.parent.mkdir(exist_ok=True)
    packet.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return evidence | {"evidence_path": str(packet)}


def verify_evidence(path: Path) -> dict[str, Any]:
    evidence = json.loads(path.read_text(encoding="utf-8"))
    required = {"protocol", "status", "repository", "target", "before_sha256", "after_sha256", "test", "observed_diff", "authority", "authorization", "execution", "mutation", "limitations"}
    if not required.issubset(evidence) or evidence.get("protocol") != PROTOCOL:
        return blocked("EVIDENCE_PACKET_INVALID")
    repo = Path(evidence["repository"])
    target = repo / evidence["target"]
    if evidence.get("status") != "VERIFIED" or not target.is_file() or digest(target) != evidence["after_sha256"]:
        return blocked("EVIDENCE_READBACK_UNVERIFIED")
    return {"protocol": PROTOCOL, "status": "VERIFIED", "evidence_path": str(path), "authority": "UNCHANGED", "authorization": "UNCHANGED", "execution": "NONE", "mutation": "NONE"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", type=Path)
    parser.add_argument("--phrase", default="Update local delivery marker")
    parser.add_argument("--prepare", action="store_true")
    parser.add_argument("--approval", type=Path, help="JSON file containing exact step-scoped approval")
    parser.add_argument("--verify-evidence", type=Path)
    args = parser.parse_args()
    if args.verify_evidence:
        print(json.dumps(verify_evidence(args.verify_evidence), indent=2, sort_keys=True))
        return 0
    if not args.repository:
        parser.error("--repository is required unless --verify-evidence is supplied")
    if args.prepare:
        result = prepare(args.repository)
    else:
        if not args.approval:
            parser.error("--approval is required for execution; use --prepare first to obtain exact scope")
        result = run(args.repository, args.phrase, json.loads(args.approval.read_text(encoding="utf-8")))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0
