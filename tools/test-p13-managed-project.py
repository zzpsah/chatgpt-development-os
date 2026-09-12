#!/usr/bin/env python3
"""End-to-end P13 proof in an isolated DevOS-managed Git project."""
from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools" / filename)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def git(project: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=project, check=True, text=True,
                          capture_output=True).stdout.strip()


def main() -> None:
    orchestrator = load("p13_orchestrator", "autonomous-orchestrator.py")
    checkpoint_tool = load("p13_checkpoint", "orchestration-checkpoint.py")
    with tempfile.TemporaryDirectory() as tmp:
        project = Path(tmp) / "managed-project"
        shutil.copytree(ROOT / "templates" / "project", project)
        (project / "app.txt").write_text("managed project fixture\n", encoding="utf-8")
        git(project, "init")
        git(project, "config", "user.name", "DevOS P13 Test")
        git(project, "config", "user.email", "devos-p13@example.invalid")
        git(project, "add", ".")
        git(project, "commit", "-m", "test: initialize managed project")
        head = git(project, "rev-parse", "HEAD")

        base = {
            "goal": "Verify and record the managed-project fixture",
            "max_iterations": 3,
            "completed_iterations": 0,
            "repository_head": head,
            "authorization": "NOT_REQUIRED",
            "security_gate": "NOT_APPLICABLE",
            "capabilities": {"verify": "AVAILABLE", "record": "AVAILABLE"},
            "tasks": [
                {"id": "inspect", "status": "COMPLETE", "priority": 1,
                 "objective": "Inspect managed project", "scope": "app.txt"},
                {"id": "verify", "status": "PLANNED", "priority": 10,
                 "dependencies": ["inspect"], "objective": "Verify fixture", "scope": "app.txt"},
                {"id": "record", "status": "PLANNED", "priority": 5,
                 "dependencies": ["verify"], "objective": "Record verified result", "scope": ".ai/"},
            ],
        }
        first = orchestrator.orchestrate(base)
        assert first["decision"] == "CONTINUE"
        assert first["runtime_handoff"]["work_unit"]["id"] == "verify"

        checkpoint_path = project / ".ai" / "ORCHESTRATION-CHECKPOINT.json"
        checkpoint = checkpoint_tool.build(first)
        checkpoint_path.write_text(json.dumps(checkpoint, indent=2) + "\n", encoding="utf-8")
        assert checkpoint_tool.resume(json.loads(checkpoint_path.read_text(encoding="utf-8")), head)["status"] == "REVALIDATE_REQUIRED"

        next_unit = orchestrator.orchestrate(base | {"latest_runtime_outcome": {
            "task_id": "verify", "status": "COMPLETE", "verification": "VERIFIED",
            "evidence": [{"source": "runtime", "exit_status": 0, "command": "fixture-check"}],
        }})
        assert next_unit["decision"] == "CONTINUE"
        assert next_unit["runtime_handoff"]["work_unit"]["id"] == "record"

        git(project, "commit", "--allow-empty", "-m", "test: simulate repository change")
        changed_head = git(project, "rev-parse", "HEAD")
        assert checkpoint_tool.resume(checkpoint, changed_head)["status"] == "ESCALATE"
        assert checkpoint_tool.resume(checkpoint, changed_head)["reason"] == "REPOSITORY_HEAD_CHANGED"

    print("P13 isolated managed-project end-to-end proof: PASS")


if __name__ == "__main__":
    main()
