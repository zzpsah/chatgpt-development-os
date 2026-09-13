#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path

MODULE = Path(__file__).with_name("multi-session-continuation.py")
spec = importlib.util.spec_from_file_location("multi_session_continuation", MODULE)
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def packet():
    return mod.build_packet({
        "project": "DEVOS",
        "objective": "verify repository continuation",
        "repository_head": "abc123",
        "step_id": "S1",
        "last_safe_stage": "READINESS",
        "constraints": ["DO_NOT_DEPLOY"],
        "verification_requirements": ["fresh repository verification"],
        "evidence_refs": [".ai/SESSIONS/example.md"],
    })


def main() -> None:
    p = packet()
    assert p["authority"] == "UNCHANGED"
    assert p["authorization"] == "UNCHANGED"
    assert p["execution"] == "NONE"

    same = mod.resume(p, {"project": "DEVOS", "repository_head": "abc123"})
    assert same["status"] == "REVALIDATE_REQUIRED", same
    assert same["prior_authorization_reusable"] is False
    assert same["candidate_step_id"] == "S1"
    assert same["constraints"] == ["DO_NOT_DEPLOY"]

    changed = mod.resume(p, {"project": "DEVOS", "repository_head": "def456"})
    assert changed["status"] == "RECOMPILE_REQUIRED", changed
    assert changed["reason"] == "REPOSITORY_HEAD_CHANGED"
    assert changed["prior_authorization_reusable"] is False

    mismatch = mod.resume(p, {"project": "OTHER", "repository_head": "abc123"})
    assert mismatch["status"] == "HOLD"
    assert mismatch["reason"] == "PROJECT_IDENTITY_MISMATCH"

    mutation_hold = mod.resume(p, {
        "project": "DEVOS",
        "repository_head": "abc123",
        "mutation_replay_forbidden": True,
    })
    assert mutation_hold["status"] == "HOLD"
    assert mutation_hold["reason"] == "MUTATION_REPLAY_FORBIDDEN"

    tampered = dict(p)
    tampered["authorization"] = "ALREADY_GRANTED"
    bad_auth = mod.resume(tampered, {"project": "DEVOS", "repository_head": "abc123"})
    assert bad_auth["status"] == "HOLD"
    assert bad_auth["reason"] == "PACKET_AUTHORITY_BOUNDARY_CHANGED"

    executable = dict(p)
    executable["execution"] = "READY"
    bad_exec = mod.resume(executable, {"project": "DEVOS", "repository_head": "abc123"})
    assert bad_exec["status"] == "HOLD"
    assert bad_exec["reason"] == "PACKET_MUST_NOT_CONTAIN_EXECUTION_AUTHORITY"

    unsupported = dict(p)
    unsupported["protocol"] = "OLD"
    bad_protocol = mod.resume(unsupported, {"project": "DEVOS", "repository_head": "abc123"})
    assert bad_protocol["status"] == "HOLD"
    assert bad_protocol["reason"] == "UNSUPPORTED_CONTINUATION_PROTOCOL"

    print("PASS: multi-session / fresh-AI continuation regression corpus")


if __name__ == "__main__":
    main()
