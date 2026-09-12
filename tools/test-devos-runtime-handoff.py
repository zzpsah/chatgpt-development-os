#!/usr/bin/env python3
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
    handoff = load("devos_runtime_handoff", "devos-runtime-handoff.py")
    candidate = {"decision": "EXECUTION_CANDIDATE", "authority": "UNCHANGED", "execution": "NONE"}
    base = {"id": "test", "objective": "run tests", "capability_required": "python"}

    for task, expected in [
        ({**base, "capability_status": "MISSING"}, "CAPABILITY_NOT_AVAILABLE"),
        ({**base, "capability_status": "AVAILABLE", "authorization": "REQUIRED", "authorization_status": "PENDING"}, "AUTHORIZATION_NOT_APPROVED"),
        ({**base, "capability_status": "AVAILABLE", "security_relevant": True, "security_status": "BLOCKED"}, "SECURITY_GATE_NOT_PASSED"),
    ]:
        result = handoff.build_handoff(candidate, task)
        assert result["status"] == "HOLD"
        assert expected in result["reasons"]

    approved = handoff.build_handoff(candidate, {**base, "capability_status": "AVAILABLE"})
    assert approved["status"] == "APPROVED_FOR_RUNTIME"
    assert approved["execution"] == "DELEGATE_TO_EXISTING_RUNTIME"
    assert approved["authority"] == "UNCHANGED"
    assert approved["verification"] == "PENDING_RUNTIME"

    no_evidence = handoff.accept_runtime_result(approved, {"status": "COMPLETE"})
    assert no_evidence["status"] == "FAILED"
    assert no_evidence["reason"] == "RAW_EXECUTION_EVIDENCE_REQUIRED"

    observed = handoff.accept_runtime_result(approved, {
        "status": "COMPLETE",
        "evidence": [{"type": "exit_status", "value": 0}],
        "verification": "PASS",
        "security": "NOT_APPLICABLE",
    })
    assert observed["status"] == "COMPLETE"
    assert observed["evidence"]
    assert observed["verification"] == "PASS"
    print("P12 bounded controller-to-runtime handoff v1: PASS")


if __name__ == "__main__":
    main()
