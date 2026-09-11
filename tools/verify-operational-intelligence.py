#!/usr/bin/env python3
"""Contract and executable checks for P12 Operational Intelligence v1."""
from __future__ import annotations

import importlib.util
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_engine():
    path = ROOT / "tools/operational-intelligence.py"
    spec = importlib.util.spec_from_file_location("operational_intelligence", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    contract = (ROOT / "core/operational-intelligence.md").read_text(encoding="utf-8")
    for needle in (
        "Operational Intelligence v1",
        "Dependency intelligence",
        "Priority intelligence",
        "Checkpoint intelligence",
        "Failure classification",
        "Evidence intelligence",
        "CAPABILITY_MISSING",
        "UNKNOWN",
        "does not authorize",
        "deterministic task graph construction",
    ):
        assert needle in contract, f"missing contract marker: {needle}"

    oi = load_engine()
    tasks = [
        {"id": "build", "status": "COMPLETE", "priority": 1},
        {"id": "test", "status": "PLANNED", "dependencies": ["build"], "priority": 10},
        {"id": "docs", "status": "PLANNED", "dependencies": ["test"], "priority": 5},
    ]
    result = oi.analyze(tasks)
    states = {item["id"]: item["readiness"] for item in result["readiness"]}
    assert states == {"build": "COMPLETE", "test": "READY", "docs": "WAITING"}
    assert result["cycle_detected"] is False

    cycle = [
        {"id": "a", "status": "PLANNED", "dependencies": ["b"]},
        {"id": "b", "status": "PLANNED", "dependencies": ["a"]},
    ]
    assert oi.analyze(cycle)["cycle_detected"] is True

    try:
        oi.analyze([{"id": "a", "dependencies": ["missing"]}])
    except ValueError as exc:
        assert "missing dependency references" in str(exc)
    else:
        raise AssertionError("missing dependencies must fail explicitly")

    print("Operational Intelligence v1 contract and executable checks: PASS")


if __name__ == "__main__":
    main()
