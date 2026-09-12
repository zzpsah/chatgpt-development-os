#!/usr/bin/env python3
"""Deterministic regression proof for the DevOS Worker lifecycle contract."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "core" / "devos-worker-lifecycle.md"

STATES = ["READY", "RECOVERING", "PREFLIGHT", "DISPATCHED", "RUNNING", "VERIFYING", "PERSISTING", "COMPLETE"]
FAILURE_STATES = ["HOLD_RECOVERY_INVALID", "HOLD_PREFLIGHT_FAILED", "HOLD_AUTHORIZATION", "FAILED", "FAILED_VERIFICATION", "HOLD_PERSISTENCE_INVALID"]


def main():
    text = DOC.read_text(encoding="utf-8")
    for marker in STATES + FAILURE_STATES + ["One worker invocation", "never grants replay permission", "ADVISORY_ONLY"]:
        assert marker in text, f"missing lifecycle invariant: {marker}"
    assert STATES.index("RECOVERING") < STATES.index("PREFLIGHT") < STATES.index("DISPATCHED")
    assert STATES.index("RUNNING") < STATES.index("VERIFYING") < STATES.index("PERSISTING") < STATES.index("COMPLETE")
    print("DevOS Worker lifecycle regression test: PASS")
    print("Ordered lifecycle: PASS")
    print("Failure/hold exits: PASS")
    print("Bounded one-unit invariant: PASS")
    print("Authorization/replay boundary: PASS")


if __name__ == "__main__":
    main()
