#!/usr/bin/env python3
"""Contract and executable checks for P12 Operational Intelligence."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_engine():
    path = ROOT / "tools/operational-intelligence.py"
    spec = importlib.util.spec_from_file_location("operational_intelligence", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


def main() -> None:
    contract = (ROOT / "core/operational-intelligence.md").read_text(encoding="utf-8")
    for needle in (
        "Operational Intelligence v1", "Dependency intelligence", "Priority intelligence",
        "Checkpoint intelligence", "Failure classification", "Evidence intelligence",
        "CAPABILITY_MISSING", "UNKNOWN", "does not authorize",
        "deterministic task graph construction", "dependency-aware prioritization",
        "checkpoint signals", "raw evidence", "freshness",
    ):
        assert needle in contract, f"missing contract marker: {needle}"

    oi = load_engine()
    tasks = [
        {"id": "build", "status": "COMPLETE", "priority": 1},
        {"id": "test", "status": "PLANNED", "dependencies": ["build"], "priority": 10},
        {"id": "docs", "status": "PLANNED", "dependencies": ["test"], "priority": 5},
        {"id": "approval", "status": "NEEDS_APPROVAL", "priority": 99},
    ]
    result = oi.analyze(
        tasks,
        [{"type": "REPOSITORY_CHANGE"}, {"type": "SESSION_BOUNDARY"}],
        [{"status": "verification", "message": "failed", "run": "ci-1"}],
        [{"source": "test", "freshness": "current", "result": "failed"},
         {"source": "ai_assertion", "freshness": "current", "result": "pass"}],
    )
    states = {item["id"]: item["readiness"] for item in result["readiness"]}
    assert states == {"build": "COMPLETE", "test": "READY", "docs": "WAITING", "approval": "UNAUTHORIZED"}
    assert result["cycle_detected"] is False
    assert [x["event"] for x in result["checkpoints"]] == ["REPOSITORY_CHANGE", "SESSION_BOUNDARY"]
    ranked = [x["id"] for x in result["priority"]]
    assert ranked.index("test") < ranked.index("docs")
    reasons = next(x["reasons"] for x in result["priority"] if x["id"] == "test")
    assert "explicit_priority=10" in reasons and "dependent_count=1" in reasons

    assert result["failures"][0]["class"] == "VERIFICATION_FAILED"
    assert result["failures"][0]["confidence"] == "status"
    assert result["failures"][0]["raw_evidence"]["run"] == "ci-1"
    assert result["evidence"][0]["execution_evidence"] is True
    assert result["evidence"][1]["execution_evidence"] is False

    cycle = [{"id": "a", "status": "PLANNED", "dependencies": ["b"]},
             {"id": "b", "status": "PLANNED", "dependencies": ["a"]}]
    assert oi.analyze(cycle)["cycle_detected"] is True
    try:
        oi.analyze([{"id": "a", "dependencies": ["missing"]}])
    except ValueError as exc:
        assert "missing dependency references" in str(exc)
    else:
        raise AssertionError("missing dependencies must fail explicitly")
    assert oi.checkpoint_signals([{"type": "UNKNOWN_EVENT"}])[0]["checkpoint"] is False
    assert oi.classify_failure({"class": "made_up", "evidence": "x"})["class"] == "UNKNOWN"
    print("Operational Intelligence v3 contract and executable checks: PASS")


if __name__ == "__main__":
    main()
