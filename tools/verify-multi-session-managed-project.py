#!/usr/bin/env python3
"""Real managed-project proof for DEVOS-MULTI-SESSION-v1.

Session A persists a continuation packet into an ephemeral managed-project
checkout. Session B is a fresh Python process that receives only repository-local
packet/current-state JSON and must revalidate project identity and Git HEAD.
No commit or push occurs.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "multi-session-continuation.py"


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


def run_tool(project: Path, *args: str) -> dict:
    result = subprocess.run(
        [sys.executable, str(TOOL), *args],
        cwd=project,
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(result.stdout)


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

    evidence_dir = project / ".ai" / "EVIDENCE"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    input_path = evidence_dir / "multi-session-a-input.json"
    packet_path = evidence_dir / "multi-session-continuation.json"
    current_path = evidence_dir / "multi-session-b-current.json"
    drift_path = evidence_dir / "multi-session-b-drift.json"
    proof_path = evidence_dir / "multi-session-managed-proof.json"

    # Session A: persist continuity facts only.
    input_path.write_text(json.dumps({
        "project": args.expected_repository,
        "objective": "continue managed-project verification from repository evidence",
        "repository_head": head,
        "step_id": "S1",
        "last_safe_stage": "READINESS",
        "constraints": ["DO_NOT_DEPLOY"],
        "verification_requirements": ["fresh repository verification"],
        "evidence_refs": ["README.md", "AGENTS.md", ".ai/"],
    }, indent=2) + "\n", encoding="utf-8")

    subprocess.run(
        [
            sys.executable,
            str(TOOL),
            "build",
            "--input",
            str(input_path),
            "--output",
            str(packet_path),
        ],
        cwd=project,
        text=True,
        capture_output=True,
        check=True,
    )
    packet = json.loads(packet_path.read_text(encoding="utf-8"))
    assert packet["authority"] == "UNCHANGED"
    assert packet["authorization"] == "UNCHANGED"
    assert packet["execution"] == "NONE"
    assert packet["repository_head"] == head

    # Session B: fresh process derives project identity/head from current repository.
    current_path.write_text(json.dumps({
        "project": origin,
        "repository_head": git(project, "rev-parse", "HEAD"),
    }, indent=2) + "\n", encoding="utf-8")
    resumed = run_tool(
        project,
        "resume",
        "--packet",
        str(packet_path),
        "--current",
        str(current_path),
    )
    assert resumed["status"] == "REVALIDATE_REQUIRED", resumed
    assert resumed["prior_authorization_reusable"] is False
    assert resumed["execution"] == "NONE"
    assert resumed["project"] == origin

    # Simulated later-session repository drift must invalidate the saved candidate.
    drift_path.write_text(json.dumps({
        "project": origin,
        "repository_head": "simulated-later-head",
    }, indent=2) + "\n", encoding="utf-8")
    drifted = run_tool(
        project,
        "resume",
        "--packet",
        str(packet_path),
        "--current",
        str(drift_path),
    )
    assert drifted["status"] == "RECOMPILE_REQUIRED", drifted
    assert drifted["reason"] == "REPOSITORY_HEAD_CHANGED"
    assert drifted["prior_authorization_reusable"] is False

    proof = {
        "protocol": "DEVOS-MULTI-SESSION-v1",
        "status": "PASS",
        "repository": origin,
        "repository_head": head,
        "session_a_packet_authority": packet["authority"],
        "session_a_packet_execution": packet["execution"],
        "session_b_same_head": resumed["status"],
        "session_b_changed_head": drifted["status"],
        "prior_authorization_reusable": resumed["prior_authorization_reusable"],
        "source_mutation": False,
        "remote_mutation": False,
    }
    proof_path.write_text(json.dumps(proof, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    # Proof must not alter tracked source/history or remote identity.
    assert git(project, "rev-parse", "HEAD") == head
    assert normalize_remote(git(project, "remote", "get-url", "origin")) == origin
    assert git(project, "diff", "--name-only", "HEAD") == ""
    status = set(git(project, "status", "--porcelain").splitlines())
    assert status, "expected bounded local evidence files"
    assert all(".ai/EVIDENCE" in line for line in status), status

    expected = [input_path, packet_path, current_path, drift_path, proof_path]
    for path in expected:
        assert path.is_file() and path.read_text(encoding="utf-8").strip(), path

    print("PASS: multi-session fresh-AI real managed-project proof")
    print(f"PACKET_PATH={packet_path}")
    print(f"PROOF_PATH={proof_path}")
    print(f"MANAGED_PROJECT_HEAD={head}")


if __name__ == "__main__":
    main()
