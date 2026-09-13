#!/usr/bin/env python3
"""Verify the Production E2E Harness against a real DevOS-managed project.

This proof is deliberately read-only with respect to the managed repository's
source and remote state. The only local mutation is an explicitly authorized
`.ai/EVIDENCE/` packet inside the ephemeral checkout; nothing is committed or
pushed by this verifier.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HARNESS_PATH = ROOT / "tools" / "production-e2e-harness.py"


def load_harness():
    spec = importlib.util.spec_from_file_location("production_e2e_managed", HARNESS_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def git(project: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=project, text=True, capture_output=True, check=True
    ).stdout.strip()


def normalize_remote(value: str) -> str:
    value = value.strip().removesuffix(".git")
    if value.startswith("git@github.com:"):
        return value.split("git@github.com:", 1)[1]
    marker = "github.com/"
    if marker in value:
        return value.split(marker, 1)[1]
    return value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True, type=Path)
    parser.add_argument("--expected-repository", required=True)
    args = parser.parse_args()

    project = args.project_root.resolve()
    assert project.is_dir(), f"managed project does not exist: {project}"
    assert (project / "README.md").is_file(), "managed project README.md is required"
    assert (project / "AGENTS.md").is_file(), "managed project AGENTS.md is required"
    assert (project / ".ai").is_dir(), "managed project .ai directory is required"

    origin = normalize_remote(git(project, "remote", "get-url", "origin"))
    assert origin == args.expected_repository, (origin, args.expected_repository)
    head = git(project, "rev-parse", "HEAD")
    status_before = git(project, "status", "--porcelain")

    harness = load_harness()
    evidence_rel = ".ai/EVIDENCE/production-e2e-managed-project.json"
    evidence = project / evidence_rel
    if evidence.exists():
        evidence.unlink()

    payload = {
        "project_root": str(project),
        "human_request": "check repository",
        "context": {"project": args.expected_repository},
        "repository_head": head,
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
            "id": "managed-project-identity",
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
            "path": evidence_rel,
            "authorization": "ALREADY_GRANTED",
        },
    }

    result = harness.run(payload)
    assert result["status"] == "COMPLETE", json.dumps(result, indent=2)
    assert result["stage"] == "RECOVERY"
    assert result["project"] == args.expected_repository
    assert result["repository_head"] == head
    assert result["trace"]["runtime"]["status"] == "SUCCESS"
    assert result["trace"]["verification"]["status"] == "VERIFIED"
    assert result["trace"]["persistence"]["status"] == "SUCCESS"
    assert result["trace"]["recovery"]["status"] == "SUCCESS"
    assert result["authority"] == "UNCHANGED"
    assert result["authorization"] == "UNCHANGED"

    packet = json.loads(evidence.read_text(encoding="utf-8"))
    assert packet["protocol"] == "DEVOS-PRODUCTION-E2E-v1"
    assert packet["status"] == "VERIFIED"
    assert packet["project"] == args.expected_repository
    assert packet["repository_head"] == head
    assert packet["execution_evidence"] is True

    # The proof must not alter source, commits, or remote state. The only allowed
    # local working-tree delta is the evidence packet produced above.
    status_after = git(project, "status", "--porcelain")
    new_lines = {
        line for line in status_after.splitlines()
        if line and line not in set(status_before.splitlines())
    }
    assert all(evidence_rel in line or ".ai/EVIDENCE/" in line for line in new_lines), new_lines
    assert git(project, "rev-parse", "HEAD") == head
    assert normalize_remote(git(project, "remote", "get-url", "origin")) == args.expected_repository

    print("PASS: Production E2E Harness real managed-project proof")
    print(f"EVIDENCE_PATH={evidence}")
    print(f"MANAGED_PROJECT_HEAD={head}")


if __name__ == "__main__":
    main()
