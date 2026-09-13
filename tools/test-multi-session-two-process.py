#!/usr/bin/env python3
"""Two-process proof for DEVOS-MULTI-SESSION-v1.

Session A and Session B communicate only through persisted JSON files. Session B
is a fresh Python process and must revalidate repository identity/head rather than
reuse in-memory state or execution authority.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "multi-session-continuation.py"


def git_head() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()


def run(*args: str) -> dict:
    result = subprocess.run(
        [sys.executable, str(TOOL), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(result.stdout)


def main() -> None:
    head = git_head()
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        session_a_input = work / "session-a-input.json"
        packet_path = work / "continuation-packet.json"
        session_b_current = work / "session-b-current.json"
        drifted_current = work / "session-b-drifted.json"

        session_a_input.write_text(json.dumps({
            "project": "DEVOS",
            "objective": "continue repository-only maturity proof",
            "repository_head": head,
            "step_id": "S1",
            "last_safe_stage": "READINESS",
            "constraints": ["DO_NOT_DEPLOY"],
            "verification_requirements": ["fresh repository verification"],
            "evidence_refs": [".ai/CURRENT-STATE.md", ".ai/TASKS.md"],
        }), encoding="utf-8")

        # Session A persists continuity facts. No execution authority is emitted.
        subprocess.run(
            [sys.executable, str(TOOL), "build", "--input", str(session_a_input), "--output", str(packet_path)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
        assert packet["authority"] == "UNCHANGED"
        assert packet["authorization"] == "UNCHANGED"
        assert packet["execution"] == "NONE"
        assert packet["repository_head"] == head

        # Session B is a fresh process. Same-head continuity still requires revalidation.
        session_b_current.write_text(json.dumps({
            "project": "DEVOS",
            "repository_head": head,
        }), encoding="utf-8")
        same = run("resume", "--packet", str(packet_path), "--current", str(session_b_current))
        assert same["status"] == "REVALIDATE_REQUIRED", same
        assert same["reason"] == "SAVED_CANDIDATE_MUST_EARN_CURRENT_ELIGIBILITY"
        assert same["prior_authorization_reusable"] is False
        assert same["execution"] == "NONE"
        assert same["objective"] == "continue repository-only maturity proof"

        # Repository drift in Session B invalidates the saved candidate.
        drifted_current.write_text(json.dumps({
            "project": "DEVOS",
            "repository_head": "changed-head-for-test",
        }), encoding="utf-8")
        drifted = run("resume", "--packet", str(packet_path), "--current", str(drifted_current))
        assert drifted["status"] == "RECOMPILE_REQUIRED", drifted
        assert drifted["reason"] == "REPOSITORY_HEAD_CHANGED"
        assert drifted["prior_authorization_reusable"] is False
        assert drifted["execution"] == "NONE"

        # A fresh process may not turn a packet into execution authority by tampering.
        tampered = dict(packet)
        tampered["authorization"] = "ALREADY_GRANTED"
        packet_path.write_text(json.dumps(tampered), encoding="utf-8")
        hold = run("resume", "--packet", str(packet_path), "--current", str(session_b_current))
        assert hold["status"] == "HOLD"
        assert hold["reason"] == "PACKET_AUTHORITY_BOUNDARY_CHANGED"

    print("PASS: two-process repository-only continuation proof")


if __name__ == "__main__":
    main()
