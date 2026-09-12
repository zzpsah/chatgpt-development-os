#!/usr/bin/env python3
"""Executable contract tests for P12 bounded runtime v1."""
from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def approved():
    return {
        "handoff_version": "P12-HANDOFF-v1",
        "status": "APPROVED_FOR_RUNTIME",
        "authority": "UNCHANGED",
        "execution": "DELEGATE_TO_EXISTING_RUNTIME",
        "work_unit": {"task_id": "runtime-test", "objective": "verify bounded runtime", "capability": "verification.run"},
    }


def main() -> None:
    runtime = load("devos_execution_runtime", ROOT / "tools" / "devos-execution-runtime.py")
    with tempfile.TemporaryDirectory() as tmp:
        project = Path(tmp)
        script = project / "verify.py"
        script.write_text("print('RUNTIME_RAW_EVIDENCE_OK')\n", encoding="utf-8")
        checkpoint = project / "checkpoint.json"
        result = runtime.execute(approved(), project, {"id": "runtime-smoke", "command": [sys.executable, "verify.py"], "timeout_seconds": 30}, checkpoint)
        assert result["status"] == "COMPLETE"
        assert result["verification"] == "VERIFIED"
        assert result["security"] == "NOT_APPLICABLE"
        assert result["evidence"][0]["exit_status"] == 0
        assert "RUNTIME_RAW_EVIDENCE_OK" in result["evidence"][0]["stdout"]
        saved = json.loads(checkpoint.read_text(encoding="utf-8"))
        assert saved["pre_action"]["status"] == "IN_PROGRESS"
        assert saved["post_action"]["status"] == "COMPLETE"
        assert saved["post_action"]["evidence"]

        blocked = runtime.execute(approved(), project, {"id": "unsafe", "command": ["sh", "-c", "echo unsafe"]})
        assert blocked["status"] == "BLOCKED"
        assert blocked["evidence"] == []

        failed_script = project / "fail.py"
        failed_script.write_text("raise SystemExit(3)\n", encoding="utf-8")
        failed = runtime.execute(approved(), project, {"id": "runtime-failure", "command": [sys.executable, "fail.py"], "timeout_seconds": 30})
        assert failed["status"] == "FAILED"
        assert failed["verification"] == "FAILED"
        assert failed["evidence"][0]["exit_status"] == 3

    print("P12 bounded execution runtime: PASS")


if __name__ == "__main__":
    main()
