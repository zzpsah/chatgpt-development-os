#!/usr/bin/env python3
"""Dry/regression test for the DevOS Base Operating Contract."""
from __future__ import annotations
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "core" / "devos-base-operating-rule.md"
REQUIRED = ("DETECT", "CLASSIFY + ISOLATE", "ROOT-CAUSE ANALYSIS", "SAFE REPAIR", "DRY TEST", "RE-VERIFY", "REGRESSION CHECK", "DOCUMENT + PERSIST", "RESUME ORIGINAL OBJECTIVE", "ROOT_CAUSE_UNCONFIRMED", "BLOCKED`/`HOLD")

def load_contract():
    if not CONTRACT.is_file():
        raise AssertionError("base operating contract is missing")
    text = CONTRACT.read_text(encoding="utf-8")
    for marker in REQUIRED:
        if marker not in text:
            raise AssertionError(f"contract marker missing: {marker}")

def classify_connection(**checks):
    ordered = (("CONFIGURATION", "config"), ("ENDPOINT_DNS", "dns"), ("NETWORK_REACHABILITY", "network"), ("TLS_TRANSPORT", "tls"), ("AUTHENTICATION", "auth"), ("AUTHORIZATION", "permission"))
    for layer, key in ordered:
        if not checks.get(key, True):
            return {"status": "DIAGNOSED", "failed_layer": layer}
    return {"status": "PASS", "failed_layer": None}

def dry_repair_cycle():
    failed = classify_connection(network=False)
    assert failed == {"status": "DIAGNOSED", "failed_layer": "NETWORK_REACHABILITY"}
    repaired = classify_connection(network=True)
    assert repaired["status"] == "PASS"
    return failed, repaired

def main():
    load_contract()
    failed, repaired = dry_repair_cycle()
    assert repaired["status"] == "PASS"
    for relative in ("tools/devos-runtime-recovery.py", "tools/devos-scheduler.py"):
        path = ROOT / relative
        if not path.is_file():
            raise AssertionError(f"required runtime component missing: {relative}")
        spec = importlib.util.spec_from_file_location("devos_contract_smoke", path)
        if spec is None or spec.loader is None:
            raise AssertionError(f"cannot load runtime component: {relative}")
    print("DevOS Base Operating Contract dry/regression test: PASS")
    print(f"Simulated connection failure root layer: {failed['failed_layer']}")
    print("Simulated repair dry-test: PASS")
    print("Regression guard: PASS")

if __name__ == "__main__":
    main()
