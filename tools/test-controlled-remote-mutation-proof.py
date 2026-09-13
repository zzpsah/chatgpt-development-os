#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path

MODULE = Path(__file__).with_name("controlled-remote-mutation-proof.py")
spec = importlib.util.spec_from_file_location("controlled_remote_mutation", MODULE)
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class FakeClient:
    def __init__(self, *, mode="success"):
        self.mode = mode
        self.path = "docs/proof.txt"
        self.sha = "sha-old"
        self.content = "before\n"
        self.mutation_calls = 0
        self.read_calls = 0

    def get_file(self, repository, path):
        self.read_calls += 1
        if self.mode == "readback-fail" and self.mutation_calls:
            raise RuntimeError("temporary read failure")
        if self.mode == "readback-mismatch" and self.mutation_calls:
            return {"path": path, "sha": "sha-new", "content": "different\n"}
        return {"path": path, "sha": self.sha, "content": self.content}

    def update_file(self, repository, path, content, message, expected_sha):
        self.mutation_calls += 1
        if expected_sha != self.sha:
            raise RuntimeError("sha conflict")
        if self.mode == "conflict":
            raise RuntimeError("sha conflict")
        if self.mode == "uncertain":
            # Simulate a provider timeout after applying the change. The proof must
            # inspect state and never call update_file a second time.
            self.sha = "sha-new"
            self.content = content
            raise RuntimeError("provider timeout after request")
        self.sha = "sha-new"
        self.content = content
        return {"commit": {"sha": "commit-new"}, "content": {"path": path, "sha": self.sha}}


def payload(**overrides):
    base = {
        "repository": "zzpsah/test-repository",
        "path": "docs/proof.txt",
        "step_id": "S2",
        "expected_sha": "sha-old",
        "content": "after\n",
        "message": "test: controlled proof",
        "authorization": "ALREADY_GRANTED",
        "security_gate": "PASS",
    }
    base.update(overrides)
    return base


def main() -> None:
    success_client = FakeClient()
    success = mod.execute(payload(), success_client)
    assert success["status"] == "VERIFIED", success
    assert success["mutation_attempt_count"] == 1
    assert success_client.mutation_calls == 1
    assert success_client.read_calls == 2
    assert success["observed_sha"] == "sha-new"
    assert success["trace"]["readback"]["provider_result"]["response"]["content"] == "after\n"

    no_auth = FakeClient()
    blocked = mod.execute(payload(authorization="NOT_REQUIRED"), no_auth)
    assert blocked["status"] == "BLOCKED"
    assert no_auth.mutation_calls == 0 and no_auth.read_calls == 0

    no_security = FakeClient()
    blocked_security = mod.execute(payload(security_gate="UNKNOWN"), no_security)
    assert blocked_security["status"] == "BLOCKED"
    assert no_security.mutation_calls == 0

    stale = FakeClient()
    stale_result = mod.execute(payload(expected_sha="stale-sha"), stale)
    assert stale_result["status"] == "BLOCKED"
    assert stale_result["mutation_attempted"] is False
    assert stale.mutation_calls == 0
    assert stale.read_calls == 1

    conflict = FakeClient(mode="conflict")
    conflict_result = mod.execute(payload(), conflict)
    assert conflict_result["status"] == "HOLD", conflict_result
    assert conflict_result["replay"] == "FORBIDDEN"
    assert conflict.mutation_calls == 1

    uncertain = FakeClient(mode="uncertain")
    uncertain_result = mod.execute(payload(), uncertain)
    # An uncertain provider response may be reconciled by readback if the exact
    # intended state is observed, but it still must not retry the mutation.
    assert uncertain_result["status"] == "VERIFIED", uncertain_result
    assert uncertain.mutation_calls == 1
    assert uncertain.read_calls == 2

    mismatch = FakeClient(mode="readback-mismatch")
    mismatch_result = mod.execute(payload(), mismatch)
    assert mismatch_result["status"] == "HOLD", mismatch_result
    assert mismatch_result["replay"] == "FORBIDDEN"
    assert mismatch.mutation_calls == 1

    readback_fail = FakeClient(mode="readback-fail")
    readback_fail_result = mod.execute(payload(), readback_fail)
    assert readback_fail_result["status"] == "HOLD", readback_fail_result
    assert readback_fail.mutation_calls == 1

    bad_path = FakeClient()
    blocked_path = mod.execute(payload(path="../outside"), bad_path)
    assert blocked_path["status"] == "BLOCKED"
    assert bad_path.mutation_calls == 0

    print("PASS: controlled remote mutation proof regression corpus")


if __name__ == "__main__":
    main()
