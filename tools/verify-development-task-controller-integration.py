#!/usr/bin/env python3
"""Executable P12 controller/OI/runtime-handoff integration checks."""
from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools" / filename)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    controller = load("controller", "development-task-controller.py")
    handoff = load("handoff", "devos-runtime-handoff.py")
    payload = {
        "repository_head": "abc123",
        "authorization": "NOT_REQUIRED",
        "security_gate": "NOT_APPLICABLE",
        "capabilities": {"verify": "AVAILABLE"},
        "tasks": [
            {"id": "build", "status": "COMPLETE", "priority": 1,
             "objective": "Build source", "scope": "src/"},
            {"id": "verify", "status": "PLANNED", "priority": 10,
             "dependencies": ["build"], "objective": "Run verification", "scope": "tools/"},
        ],
    }
    decision = controller.decide(payload)
    assert decision["decision"] == "EXECUTION_CANDIDATE"
    assert decision["authority"] == "UNCHANGED"
    assert decision["execution"] == "NONE"
    assert decision["authorization"] == "UNCHANGED"
    assert decision["operational_intelligence"]["authority"] == "ADVISORY_ONLY"
    assert all(decision["gates"].values())

    envelope = handoff.build_handoff(decision)
    assert envelope["status"] == "READY_FOR_RUNTIME"
    assert envelope["execution"] == "NOT_STARTED"
    assert envelope["work_unit"]["id"] == "verify"

    blocked = controller.decide(payload | {"capabilities": {"verify": "MISSING"}})
    assert blocked["decision"] == "BLOCKED"
    assert blocked["gates"]["capability"] is False
    assert handoff.build_handoff(blocked)["status"] == "BLOCKED"

    approval = controller.decide(payload | {"authorization": "REQUIRED"})
    assert approval["decision"] == "BLOCKED"
    assert approval["gates"]["authorization"] is False
    print("P12 controller/OI/runtime-handoff integration: PASS")


if __name__ == "__main__":
    main()
