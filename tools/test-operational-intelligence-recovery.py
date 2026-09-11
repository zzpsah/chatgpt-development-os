#!/usr/bin/env python3
"""Fresh-repository proof for deterministic P12 operational intelligence."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "tools/operational-intelligence.py"


def main() -> None:
    payload = {
        "tasks": [
            {"id": "source", "status": "COMPLETE", "priority": 2},
            {"id": "verify", "status": "PLANNED", "dependencies": ["source"], "priority": 10},
            {"id": "handoff", "status": "PLANNED", "dependencies": ["verify"], "priority": 5},
        ],
        "events": [{"type": "REPOSITORY_CHANGE"}, {"type": "HANDOFF_BOUNDARY"}],
        "failures": [{"class": "VERIFICATION_FAILED", "message": "test evidence", "run": "fixture"}],
        "evidence": [{"source": "test", "freshness": "current", "result": "failed"}],
    }
    with tempfile.TemporaryDirectory() as tmp:
        input_path = Path(tmp) / "input.json"
        input_path.write_text(json.dumps(payload), encoding="utf-8")
        runs = []
        for _ in range(2):
            completed = subprocess.run(
                [sys.executable, str(ENGINE), str(input_path)],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            runs.append(completed.stdout)
    assert runs[0] == runs[1], "operational analysis must be deterministic across fresh runs"
    result = json.loads(runs[0])
    assert result["protocol_version"] == "P12-OI-v3"
    assert result["failures"][0]["class"] == "VERIFICATION_FAILED"
    assert result["evidence"][0]["execution_evidence"] is True
    assert result["readiness"][0]["id"] == "verify"
    print("Operational Intelligence fresh-repository deterministic recovery proof: PASS")


if __name__ == "__main__":
    main()
