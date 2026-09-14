#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = Path(__file__).with_name("agent-runtime-conformance-evidence.py")
REGISTRY_MODULE = Path(__file__).with_name("agent-runtime-profile-registry.py")
REGISTRY = ROOT / "config" / "agent-runtime-profile-registry.json"

spec = importlib.util.spec_from_file_location("runtime_conformance", MODULE)
mod = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(mod)

registry_spec = importlib.util.spec_from_file_location("runtime_registry", REGISTRY_MODULE)
registry_mod = importlib.util.module_from_spec(registry_spec)
assert registry_spec and registry_spec.loader
registry_spec.loader.exec_module(registry_mod)

HEAD = "1" * 40
DIGEST = hashlib.sha256(b"probe").hexdigest()


def evidence_for(bundle, *, runtime_id="codex"):
    challenge = bundle["challenge"]
    return {
        "protocol": mod.EVIDENCE_PROTOCOL,
        "challenge_id": bundle["challenge_id"],
        "runtime_id": runtime_id,
        "adapter_version": challenge["adapter_version"],
        "repository_head": challenge["repository_head"],
        "nonce": challenge["nonce"],
        "invocation_provenance": {
            "kind": "direct-runtime-session",
            "ref": "session/example-proof",
            "observed_by": "bounded-host-adapter",
        },
        "capabilities": {
            name: {
                "status": "PASS",
                "ref": f"probe/{name}",
                "scope": "disposable-conformance-fixture",
                "digest": DIGEST,
            }
            for name in sorted(mod.REQUIRED_CAPABILITIES)
        },
        "limitations": [
            "Packet validity alone does not verify runtime identity or authorize registry promotion."
        ],
    }


def main():
    challenge = mod.create_challenge("codex", "candidate-1", HEAD, "nonce-001")
    assert challenge["status"] == "CHALLENGE_READY", challenge
    assert challenge["authority"] == "UNCHANGED"
    assert challenge["authorization"] == "UNCHANGED"
    assert challenge["execution"] == "NONE"
    assert challenge["mutation"] == "NONE"
    assert challenge["production_ready"] is False

    valid_evidence = evidence_for(challenge)
    verdict = mod.evaluate_evidence(challenge, valid_evidence)
    assert verdict["status"] == "EVIDENCE_PACKET_VALID", verdict
    assert verdict["registry_promotion_allowed"] is False
    assert verdict["direct_runtime_verified"] is False
    assert "DIRECT_INVOCATION_ATTESTATION_AND_SEMANTIC_REVIEW_STILL_REQUIRED" in verdict["reasons"]

    # A valid candidate packet must not self-promote the durable runtime registry.
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    codex = next(item for item in registry["profiles"] if item["runtime_id"] == "codex")
    assert codex["status"] == "DECLARED"
    held = registry_mod.resolve_profile(registry, "codex")
    assert held["status"] == "HOLD"
    assert "RUNTIME_PROFILE_NOT_VERIFIED=DECLARED" in held["reasons"]

    tampered_challenge = copy.deepcopy(challenge)
    tampered_challenge["challenge"]["nonce"] = "changed"
    blocked = mod.evaluate_evidence(tampered_challenge, valid_evidence)
    assert blocked["status"] == "BLOCKED"
    assert "CHALLENGE_INTEGRITY_INVALID" in blocked["reasons"]

    mismatch = evidence_for(challenge, runtime_id="claude-code")
    blocked = mod.evaluate_evidence(challenge, mismatch)
    assert blocked["status"] == "BLOCKED"
    assert "EVIDENCE_RUNTIME_ID_MISMATCH" in blocked["reasons"]

    replay_challenge = mod.create_challenge("codex", "candidate-1", HEAD, "nonce-002")
    blocked = mod.evaluate_evidence(replay_challenge, valid_evidence)
    assert blocked["status"] == "BLOCKED"
    assert any(reason in blocked["reasons"] for reason in ("EVIDENCE_CHALLENGE_ID_MISMATCH", "EVIDENCE_NONCE_MISMATCH"))

    failed = evidence_for(challenge)
    failed["capabilities"]["verification.run"]["status"] = "FAIL"
    held = mod.evaluate_evidence(challenge, failed)
    assert held["status"] == "HOLD"
    assert "CAPABILITY_PROBE_FAILED=verification.run" in held["reasons"]
    assert held["registry_promotion_allowed"] is False

    forged_extra = evidence_for(challenge)
    forged_extra["capabilities"]["unscoped.shell"] = {
        "status": "PASS",
        "ref": "probe/unscoped-shell",
        "scope": "invalid",
        "digest": DIGEST,
    }
    blocked = mod.evaluate_evidence(challenge, forged_extra)
    assert blocked["status"] == "BLOCKED"
    assert "CAPABILITY_SET_INVALID" in blocked["reasons"]

    no_provenance = evidence_for(challenge)
    no_provenance["invocation_provenance"] = {}
    blocked = mod.evaluate_evidence(challenge, no_provenance)
    assert blocked["status"] == "BLOCKED"
    assert "INVOCATION_PROVENANCE_INVALID" in blocked["reasons"]

    bad_digest = evidence_for(challenge)
    bad_digest["capabilities"]["git.inspect"]["digest"] = "not-a-sha256"
    blocked = mod.evaluate_evidence(challenge, bad_digest)
    assert blocked["status"] == "BLOCKED"
    assert "CAPABILITY_DIGEST_INVALID=git.inspect" in blocked["reasons"]

    invalid_challenge = mod.create_challenge("codex", "candidate-1", "bad-head", "nonce")
    assert invalid_challenge["status"] == "BLOCKED"
    assert "REPOSITORY_HEAD_INVALID" in invalid_challenge["reasons"]

    print("PASS: runtime conformance challenge binds runtime/head/nonce deterministically")
    print("PASS: malformed, replayed, incomplete, failed, and forged evidence fails closed")
    print("PASS: valid evidence packet cannot self-promote a DECLARED runtime")


if __name__ == "__main__":
    main()
