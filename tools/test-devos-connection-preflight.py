#!/usr/bin/env python3
"""Deterministic regression tests for DevOS preflight diagnostics."""
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("preflight", ROOT / "tools" / "devos-connection-preflight.py")
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def main():
    dns = mod.diagnose("definitely-invalid-host.invalid")
    assert dns["status"] == "DIAGNOSED"
    assert dns["failed_layer"] == "ENDPOINT_DNS"
    local = mod.diagnose("127.0.0.1:1", timeout=0.2)
    assert local["status"] == "DIAGNOSED"
    assert local["failed_layer"] == "NETWORK_REACHABILITY"
    malformed = mod.diagnose("tcp://")
    assert malformed["failed_layer"] == "CONFIGURATION"
    print("DevOS connection preflight regression test: PASS")
    print("DNS isolation: PASS")
    print("Network isolation: PASS")
    print("Configuration isolation: PASS")


if __name__ == "__main__":
    main()
