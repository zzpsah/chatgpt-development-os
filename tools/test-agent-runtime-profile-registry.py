#!/usr/bin/env python3
from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

MODULE = Path(__file__).with_name("agent-runtime-profile-registry.py")
REGISTRY = Path(__file__).parents[1] / "config" / "agent-runtime-profile-registry.json"
spec = importlib.util.spec_from_file_location("runtime_registry", MODULE)
mod = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(mod)


def load_registry():
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def main():
    registry = load_registry()
    assert mod.validate_registry(registry) == []

    # reference-local-agent
    ready = mod.resolve_profile(registry, "reference-local-agent")
    assert ready["status"] == "VERIFIED_PROFILE_READY", ready
    assert ready["runtime_profile"]["protocol"] == "DEVOS-AGENT-RUNTIME-PROFILE-v1"
    assert all(value == "AVAILABLE" for value in ready["runtime_profile"]["capabilities"].values())
    assert ready["authority"] == "UNCHANGED"
    assert ready["authorization"] == "UNCHANGED"
    assert ready["execution"] == "NONE"
    assert ready["mutation"] == "NONE"
    assert ready["production_ready"] is False

    for runtime_id in ("codex", "claude-code", "openhands"):
        held = mod.resolve_profile(registry, runtime_id)
        assert held["status"] == "HOLD", held
        assert held["runtime_profile"] is None
        assert "RUNTIME_PROFILE_NOT_VERIFIED=DECLARED" in held["reasons"]

    missing = mod.resolve_profile(registry, "unknown-runtime")
    assert missing["status"] == "HOLD"
    assert missing["reasons"] == ["RUNTIME_NOT_REGISTERED"]

    forged = copy.deepcopy(registry)
    codex = next(p for p in forged["profiles"] if p["runtime_id"] == "codex")
    codex["status"] = "VERIFIED"
    errors = mod.validate_registry(forged)
    assert any("VERIFIED_CAPABILITY_SET_INCOMPLETE" in item for item in errors), errors
    assert any("VERIFIED_EVIDENCE_REQUIRED" in item for item in errors), errors

    incomplete = copy.deepcopy(registry)
    reference = next(p for p in incomplete["profiles"] if p["runtime_id"] == "reference-local-agent")
    reference["capabilities"]["verification.run"] = "VERIFIED_MISSING"
    errors = mod.validate_registry(incomplete)
    assert any("VERIFIED_CAPABILITY_NOT_AVAILABLE" in item for item in errors), errors

    duplicate = copy.deepcopy(registry)
    duplicate["profiles"].append(copy.deepcopy(duplicate["profiles"][0]))
    errors = mod.validate_registry(duplicate)
    assert any(item.startswith("DUPLICATE_RUNTIME_ID=") for item in errors), errors

    unknown_cap = copy.deepcopy(registry)
    reference = next(p for p in unknown_cap["profiles"] if p["runtime_id"] == "reference-local-agent")
    reference["capabilities"]["unscoped.shell"] = "VERIFIED_AVAILABLE"
    errors = mod.validate_registry(unknown_cap)
    assert any("UNKNOWN_CAPABILITIES=" in item for item in errors), errors

    revoked = copy.deepcopy(registry)
    reference = next(p for p in revoked["profiles"] if p["runtime_id"] == "reference-local-agent")
    reference["status"] = "REVOKED"
    held = mod.resolve_profile(revoked, "reference-local-agent")
    assert held["status"] == "HOLD"
    assert "RUNTIME_PROFILE_NOT_VERIFIED=REVOKED" in held["reasons"]

    print("PASS: runtime profile registry validates evidence-backed conformance")
    print("PASS: declared vendor templates cannot become handoff-ready without evidence")
    print("PASS: verified profile export preserves authority/execution/mutation boundaries")


if __name__ == "__main__":
    main()
