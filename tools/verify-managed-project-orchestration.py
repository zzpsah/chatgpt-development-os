#!/usr/bin/env python3
"""P13 real managed-project orchestration proof.

The verifier must run against a separate checked-out DevOS-managed repository.
It proves that P13 can recover repository evidence, select one bounded work unit,
advance only on verified evidence, checkpoint safely, require revalidation on
resume, reject repository-head drift, and terminate when the bounded goal is
complete. It performs no mutation of the managed project.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def load(name: str, filename: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools" / filename)
    if spec is None or spec.loader is None:
        raise ImportError(f"could not load {filename}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def git_head(project_root: Path) -> str:
    result = subprocess.run(["git", "-C", str(project_root), "rev-parse", "HEAD"], check=True, text=True, capture_output=True)
    head = result.stdout.strip()
    if len(head) < 7:
        raise AssertionError("managed project did not expose a valid Git HEAD")
    return head


def verify_managed_context(project_root: Path, expected_repository: str) -> list[dict[str, Any]]:
    required = [".ai/manifest.yaml", ".ai/PROJECT.md", ".ai/CURRENT-STATE.md", ".ai/TASKS.md"]
    missing = [path for path in required if not (project_root / path).is_file()]
    if missing:
        raise AssertionError(f"managed project missing durable context: {missing}")
    manifest = (project_root / ".ai/manifest.yaml").read_text(encoding="utf-8")
    expected_lines = {
        "managed_by: development-os",
        f"canonical_repository: {expected_repository}",
        "context_directory: .ai",
        "secrets_policy: never-store-secrets",
    }
    absent = sorted(line for line in expected_lines if line not in manifest)
    if absent:
        raise AssertionError(f"managed-project manifest contract mismatch: {absent}")
    head = git_head(project_root)
    return [
        {"source": "managed-project", "kind": "git-head", "value": head},
        {"source": "managed-project", "kind": "manifest", "path": ".ai/manifest.yaml"},
        {"source": "managed-project", "kind": "current-state", "path": ".ai/CURRENT-STATE.md"},
        {"source": "managed-project", "kind": "tasks", "path": ".ai/TASKS.md"},
    ]


def base_payload(repository_head: str) -> dict[str, Any]:
    return {
        "goal": "Prove bounded autonomous orchestration against a real DevOS-managed project",
        "max_iterations": 4,
        "completed_iterations": 0,
        "repository_head": repository_head,
        "authorization": "NOT_REQUIRED",
        "security_gate": "NOT_APPLICABLE",
        "capabilities": {"verify_managed_context": "AVAILABLE", "checkpoint_resume": "AVAILABLE"},
        "tasks": [
            {"id": "recover_project", "status": "COMPLETE", "priority": 100, "objective": "Recover real managed-project identity and durable context", "scope": ".ai/"},
            {"id": "verify_managed_context", "status": "PLANNED", "priority": 90, "dependencies": ["recover_project"], "objective": "Verify managed-project repository evidence and context contract", "scope": ".ai/"},
            {"id": "checkpoint_resume", "status": "PLANNED", "priority": 80, "dependencies": ["verify_managed_context"], "objective": "Prove durable checkpoint and safe resume semantics", "scope": ".ai/ORCHESTRATION-CHECKPOINT.json"},
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True, help="checked-out external DevOS-managed project")
    parser.add_argument("--expected-repository", required=True, help="canonical owner/repository")
    args = parser.parse_args()
    project_root = Path(args.project_root).resolve()
    if not project_root.is_dir():
        raise SystemExit(f"managed project path does not exist: {project_root}")
    orchestrator = load("autonomous_orchestrator", "autonomous-orchestrator.py")
    checkpoint = load("orchestration_checkpoint", "orchestration-checkpoint.py")
    evidence = verify_managed_context(project_root, args.expected_repository)
    head = git_head(project_root)
    payload = base_payload(head)
    first = orchestrator.orchestrate(payload)
    assert first["decision"] == "CONTINUE", first
    assert first["runtime_handoff"]["status"] == "READY_FOR_RUNTIME", first
    assert first["runtime_handoff"]["work_unit"]["id"] == "verify_managed_context", first
    assert first["authority"] == "UNCHANGED" and first["execution"] == "NONE", first
    second = orchestrator.orchestrate(payload | {"completed_iterations": 1, "latest_runtime_outcome": {"task_id": "verify_managed_context", "status": "COMPLETE", "verification": "VERIFIED", "evidence": evidence}})
    assert second["decision"] == "CONTINUE", second
    assert second["runtime_handoff"]["work_unit"]["id"] == "checkpoint_resume", second
    saved = checkpoint.build(second)
    assert saved["repository_head"] == head, saved
    same_head = checkpoint.resume(saved, head)
    assert same_head["status"] == "REVALIDATE_REQUIRED", same_head
    changed_head = checkpoint.resume(saved, "0" * 40)
    assert changed_head == {"status": "ESCALATE", "reason": "REPOSITORY_HEAD_CHANGED"}, changed_head
    completed_tasks = [dict(task) for task in payload["tasks"]]
    for task in completed_tasks:
        if task["id"] == "verify_managed_context":
            task["status"] = "COMPLETE"
    final = orchestrator.orchestrate(payload | {"tasks": completed_tasks, "completed_iterations": 2, "latest_runtime_outcome": {"task_id": "checkpoint_resume", "status": "COMPLETE", "verification": "VERIFIED", "evidence": [{"source": "p13-checkpoint", "kind": "resume", "status": same_head["status"]}, {"source": "p13-checkpoint", "kind": "head-drift", "status": changed_head["status"]}]}})
    assert final["decision"] == "STOP", final
    assert final["controller"]["decision"] == "NO_ACTION", final
    assert final["authority"] == "UNCHANGED" and final["execution"] == "NONE", final
    print(json.dumps({"status": "PASS", "protocol": "P13-MANAGED-PROJECT-PROOF-v1", "managed_project": args.expected_repository, "repository_head": head, "sequence": [first["runtime_handoff"]["work_unit"]["id"], second["runtime_handoff"]["work_unit"]["id"], final["decision"]], "resume_same_head": same_head["status"], "resume_changed_head": changed_head["status"], "authority": final["authority"], "execution": final["execution"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
