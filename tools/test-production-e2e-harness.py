#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "tools" / "production-e2e-harness.py"
spec = importlib.util.spec_from_file_location("production_e2e_harness", MODULE)
assert spec and spec.loader
harness = importlib.util.module_from_spec(spec)
spec.loader.exec_module(harness)


def scenario(project_root: Path) -> dict:
    return {
        "project_root": str(project_root),
        "human_request": "check repository",
        "context": {"project": "E2E-FIXTURE"},
        "repository_head": "fixture-head-1",
        "capabilities": {"S1": "AVAILABLE"},
        "authorization_by_step": {},
        "security_gate_by_step": {},
        "runtime_request": {
            "step_id": "S1",
            "operation": "filesystem.read",
            "target": "README.md",
            "scope": "repository-read",
        },
        "verification": {
            "id": "readme-content",
            "command": [
                sys.executable,
                "-c",
                "from pathlib import Path; assert Path('README.md').read_text(encoding='utf-8') == 'hello\\n'",
            ],
            "expected_exit_codes": [0],
            "timeout_seconds": 30,
        },
        "persistence": {
            "path": ".ai/EVIDENCE/production-e2e.json",
            "authorization": "ALREADY_GRANTED",
        },
    }


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project = Path(tmp)
        (project / "README.md").write_text("hello\n", encoding="utf-8")

        success = harness.run(scenario(project))
        assert success["status"] == "COMPLETE", success
        assert success["stage"] == "RECOVERY", success
        assert success["authority"] == "UNCHANGED"
        assert success["authorization"] == "UNCHANGED"
        assert success["trace"]["readiness"]["status"] == "READY"
        assert success["trace"]["controller"]["decision"] == "EXECUTION_CANDIDATE"
        assert success["trace"]["handoff"]["status"] == "READY_FOR_RUNTIME"
        assert success["trace"]["runtime"]["status"] == "SUCCESS"
        assert success["trace"]["verification"]["status"] == "VERIFIED"
        assert success["trace"]["persistence"]["status"] == "SUCCESS"
        assert success["trace"]["recovery"]["status"] == "SUCCESS"

        packet_path = project / ".ai" / "EVIDENCE" / "production-e2e.json"
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
        assert packet["protocol"] == "DEVOS-PRODUCTION-E2E-v1"
        assert packet["execution_evidence"] is True
        assert packet["runtime_status"] == "SUCCESS"
        assert packet["verification_status"] == "VERIFIED"

        stale_payload = scenario(project)
        stale_payload["compiled_repository_head"] = "older-head"
        stale = harness.run(stale_payload)
        assert stale["status"] == "BLOCKED"
        assert stale["stage"] == "READINESS"
        assert stale["trace"]["readiness"]["status"] == "STOP"

        mutation_payload = scenario(project)
        mutation_payload["runtime_request"] = {
            "step_id": "S1",
            "operation": "filesystem.write_scoped",
            "target": "README.md",
            "scope": "repository-write",
            "content": "changed\n",
            "authorization": "ALREADY_GRANTED",
        }
        mutation = harness.run(mutation_payload)
        assert mutation["status"] == "BLOCKED"
        assert mutation["stage"] == "RUNTIME"
        assert "read-only" in str(mutation["reason"]).lower()
        assert (project / "README.md").read_text(encoding="utf-8") == "hello\n"

        verification_payload = scenario(project)
        verification_payload["verification"] = {
            "id": "forced-failure",
            "command": [sys.executable, "-c", "raise SystemExit(3)"],
            "expected_exit_codes": [0],
            "timeout_seconds": 30,
        }
        failed_verify = harness.run(verification_payload)
        assert failed_verify["status"] == "BLOCKED"
        assert failed_verify["stage"] == "VERIFICATION"
        assert failed_verify["trace"]["verification"]["status"] == "FAILED"

        persistence_payload = scenario(project)
        persistence_payload["persistence"] = {
            "path": ".ai/EVIDENCE/not-authorized.json",
            "authorization": "NOT_REQUIRED",
        }
        failed_persistence = harness.run(persistence_payload)
        assert failed_persistence["status"] == "BLOCKED"
        assert failed_persistence["stage"] == "PERSISTENCE"
        assert not (project / ".ai" / "EVIDENCE" / "not-authorized.json").exists()

        missing_capability = scenario(project)
        missing_capability["capabilities"] = {"S1": "MISSING"}
        blocked_capability = harness.run(missing_capability)
        assert blocked_capability["status"] == "BLOCKED"
        assert blocked_capability["stage"] == "READINESS"

    print("PASS: Production E2E Harness regression corpus")


if __name__ == "__main__":
    main()
