#!/usr/bin/env python3
"""Regression proof for P13 checkpoint persistence and safe resume."""
from __future__ import annotations

import importlib.util
import json
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


def main() -> None:
    orchestrator = load("orchestrator", "autonomous-orchestrator.py")
    checkpoint_tool = load("checkpoint", "orchestration-checkpoint.py")
    payload = {
        "goal": "Verify project", "max_iterations": 1, "completed_iterations": 0,
        "repository_head": "abc123", "authorization": "NOT_REQUIRED",
        "security_gate": "NOT_APPLICABLE", "capabilities": {"verify": "AVAILABLE"},
        "tasks": [{"id": "verify", "status": "PLANNED", "priority": 1,
                   "objective": "Run test", "scope": "tools/"}],
    }
    decision = orchestrator.orchestrate(payload)
    checkpoint = checkpoint_tool.build(decision)
    assert checkpoint["candidate_task_id"] == "verify"
    assert checkpoint["execution"] == "NONE"
    assert checkpoint_tool.resume(checkpoint, "abc123")["status"] == "REVALIDATE_REQUIRED"
    assert checkpoint_tool.resume(checkpoint, "changed")["reason"] == "REPOSITORY_HEAD_CHANGED"
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / ".ai" / "ORCHESTRATION-CHECKPOINT.json"
        path.parent.mkdir(parents=True)
        path.write_text(json.dumps(checkpoint), encoding="utf-8")
        assert json.loads(path.read_text(encoding="utf-8"))["protocol_version"] == checkpoint_tool.PROTOCOL
    print("P13 durable checkpoint and safe resume proof: PASS")


if __name__ == "__main__":
    main()
