#!/usr/bin/env python3
"""Real managed-project proof for DEVOS-FAILURE-RECOVERY-v1.

Uses zzpsah/automation-suite (or another explicitly supplied repository) in an
ephemeral checkout. Injects a replay-safe missing-capability failure, persists a
bounded checkpoint, repairs only the capability evidence, then proves the full
read-only E2E path recovers with fresh verification. No commit or push occurs.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "tools" / "failure-recovery-proof.py"
spec = importlib.util.spec_from_file_location("managed_failure_recovery", MODULE)
assert spec and spec.loader
recovery = importlib.util.module_from_spec(spec)
spec.loader.exec_module(recovery)


def git(project: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=project, text=True, capture_output=True, check=True
    ).stdout.strip()


def normalize_remote(value: str) -> str:
    value = value.strip().removesuffix(".git")
    if value.startswith("git@github.com:"):
        return value.split("git@github.com:", 1)[1]
    marker = "github.com/"
    return value.split(marker, 1)[1] if marker in value else value


def payload(project: Path, repository: str, head: str, capability: str) -> dict:
    return {
        "project_root": str(project),
        "human_request": "check repository",
        "context": {"project": repository},
        "repository_head": head,
        "capabilities": {"S1": capability},
        "authorization_by_step": {},
        "security_gate_by_step": {},
        "runtime_request": {
            "step_id": "S1",
            "operation": "filesystem.read",
            "target": "README.md",
            "scope": "repository-read",
        },
        "verification": {
            "id": "managed-recovery-identity",
            "command": [
                sys.executable,
                "-c",
                (
                    "from pathlib import Path; "
                    "assert Path('README.md').is_file(); "
                    "assert Path('README.md').read_text(encoding='utf-8').strip(); "
                    "assert Path('AGENTS.md').is_file(); "
                    "assert Path('.ai').is_dir()"
                ),
            ],
            "expected_exit_codes": [0],
            "timeout_seconds": 30,
        },
        "persistence": {
            "path": ".ai/EVIDENCE/failure-recovery-managed-result.json",
            "authorization": "ALREADY_GRANTED",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True, type=Path)
    parser.add_argument("--expected-repository", required=True)
    args = parser.parse_args()

    project = args.project_root.resolve()
    assert project.is_dir(), project
    origin = normalize_remote(git(project, "remote", "get-url", "origin"))
    assert origin == args.expected_repository, (origin, args.expected_repository)
    head = git(project, "rev-parse", "HEAD")

    failed_payload = payload(project, args.expected_repository, head, "MISSING")
    failed = recovery.harness.run(failed_payload)
    assert failed["status"] == "BLOCKED", json.dumps(failed, indent=2)
    assert failed["stage"] == "READINESS"
    checkpoint = recovery.build_checkpoint(failed_payload, failed)
    assert checkpoint["failure_class"] == "CAPABILITY_MISSING"
    assert checkpoint["mutation_attempted"] is False
    assert checkpoint["replay_policy"] == "REVALIDATE_THEN_RETRY_REPLAY_SAFE_PATH"

    checkpoint_rel = ".ai/EVIDENCE/failure-recovery-managed-checkpoint.json"
    checkpoint_write = recovery.host_adapter.write_text(
        project,
        checkpoint_rel,
        json.dumps(checkpoint, indent=2, sort_keys=True) + "\n",
        "ALREADY_GRANTED",
    )
    assert checkpoint_write["status"] == "SUCCESS", checkpoint_write

    repaired_payload = payload(project, args.expected_repository, head, "AVAILABLE")
    resumed = recovery.resume(checkpoint, repaired_payload)
    assert resumed["status"] == "RECOVERED_VERIFIED", json.dumps(resumed, indent=2)
    assert resumed["result"]["status"] == "COMPLETE"
    assert resumed["result"]["trace"]["verification"]["status"] == "VERIFIED"
    assert resumed["authority"] == "UNCHANGED"
    assert resumed["authorization"] == "UNCHANGED"

    result_rel = repaired_payload["persistence"]["path"]
    evidence_check = recovery.inspect_persisted_evidence(project, result_rel)
    assert evidence_check["status"] == "RECOVERABLE", evidence_check

    proof = {
        "protocol": "DEVOS-FAILURE-RECOVERY-v1",
        "status": "RECOVERED_VERIFIED",
        "repository": args.expected_repository,
        "repository_head": head,
        "failure_class": checkpoint["failure_class"],
        "failed_stage": checkpoint["failed_stage"],
        "last_safe_stage": checkpoint["last_safe_stage"],
        "replay_policy": checkpoint["replay_policy"],
        "repair": "capability evidence MISSING -> AVAILABLE",
        "mutation_attempted": checkpoint["mutation_attempted"],
        "verification_status": resumed["result"]["trace"]["verification"]["status"],
        "authority": "UNCHANGED",
        "authorization": "UNCHANGED",
    }
    proof_rel = ".ai/EVIDENCE/failure-recovery-managed-proof.json"
    proof_write = recovery.host_adapter.write_text(
        project,
        proof_rel,
        json.dumps(proof, indent=2, sort_keys=True) + "\n",
        "ALREADY_GRANTED",
    )
    assert proof_write["status"] == "SUCCESS", proof_write

    # The recovery proof must not change repository identity/history or tracked source.
    assert git(project, "rev-parse", "HEAD") == head
    assert normalize_remote(git(project, "remote", "get-url", "origin")) == args.expected_repository

    expected_evidence = {
        checkpoint_rel,
        result_rel,
        proof_rel,
    }
    for relative in expected_evidence:
        path = project / relative
        assert path.is_file(), f"missing expected evidence file: {relative}"
        assert path.read_text(encoding="utf-8").strip(), f"empty evidence file: {relative}"

    # Git may collapse multiple untracked files under .ai/EVIDENCE into one
    # directory-level porcelain entry, especially because the Production E2E
    # proof runs earlier in the same checkout. Validate the actual files above,
    # then require every working-tree delta to remain inside the bounded evidence
    # directory instead of requiring a new status line for each file.
    status_after = set(git(project, "status", "--porcelain").splitlines())
    assert status_after, "expected bounded local evidence status"
    assert all(".ai/EVIDENCE" in line for line in status_after), status_after

    tracked_delta = git(project, "diff", "--name-only", "HEAD")
    assert tracked_delta == "", tracked_delta

    print("PASS: Failure + Recovery Proof real managed-project recovery")
    print(f"FAILURE_CLASS={checkpoint['failure_class']}")
    print(f"CHECKPOINT_PATH={project / checkpoint_rel}")
    print(f"PROOF_PATH={project / proof_rel}")
    print(f"MANAGED_PROJECT_HEAD={head}")


if __name__ == "__main__":
    main()
