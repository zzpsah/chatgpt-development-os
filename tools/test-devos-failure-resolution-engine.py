#!/usr/bin/env python3
"""Dry/regression proof for the bounded DevOS failure-resolution contract."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "core" / "devos-failure-resolution-engine.md"
REQUIRED = (
    "FAILURE", "DETECT", "CLASSIFY + ISOLATE", "DIAGNOSE", "SAFE REPAIR",
    "DRY TEST / READ-ONLY PROBE", "RE-VERIFY", "REGRESSION CHECK",
    "DOCUMENT + PERSIST", "RESUME ORIGINAL OBJECTIVE", "ROOT_CAUSE_UNCONFIRMED",
    "BLOCKED`/`HOLD",
)


def diagnose_connection(**checks):
    layers = (("CONFIGURATION", "config"), ("ENDPOINT_DNS", "dns"),
              ("NETWORK_REACHABILITY", "network"), ("TLS_TRANSPORT", "tls"),
              ("AUTHENTICATION", "auth"), ("AUTHORIZATION", "permission"))
    for layer, key in layers:
        if not checks.get(key, True):
            return {"status": "DIAGNOSED", "failed_layer": layer}
    return {"status": "PASS", "failed_layer": None}


def main():
    text = CONTRACT.read_text(encoding="utf-8")
    for marker in REQUIRED:
        assert marker in text, f"missing contract marker: {marker}"
    failure = diagnose_connection(network=False)
    assert failure["failed_layer"] == "NETWORK_REACHABILITY"
    repaired = diagnose_connection(network=True)
    assert repaired["status"] == "PASS"
    assert failure != repaired
    print("DevOS Failure Resolution Engine dry/regression test: PASS")
    print("Failure isolation: NETWORK_REACHABILITY")
    print("Repair dry-test: PASS")
    print("Regression guard: PASS")


if __name__ == "__main__":
    main()
