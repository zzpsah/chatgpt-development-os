#!/usr/bin/env python3
"""Deterministic DevOS agent-runtime profile registry validator/exporter.

The registry separates declared runtime names from evidence-backed conformance. It
never executes a runtime, grants approval, mutates a repository, or upgrades
production readiness.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

REGISTRY_PROTOCOL = "DEVOS-AGENT-RUNTIME-PROFILE-REGISTRY-v1"
HANDOFF_PROFILE_PROTOCOL = "DEVOS-AGENT-RUNTIME-PROFILE-v1"
REQUIRED_CAPABILITIES = {
    "filesystem.read",
    "filesystem.write_scoped",
    "git.inspect",
    "verification.run",
}
ALLOWED_PROFILE_STATUS = {"DECLARED", "VERIFIED", "REVOKED"}
ALLOWED_CAPABILITY_STATUS = {"VERIFIED_AVAILABLE", "VERIFIED_MISSING"}
BOUNDARIES = {
    "authority": "UNCHANGED",
    "authorization": "UNCHANGED",
    "execution": "NONE",
    "mutation": "NONE",
    "production_ready": False,
}


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_registry(payload: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(payload, dict):
        return ["REGISTRY_NOT_OBJECT"]
    if set(payload) != {"protocol", "profiles"}:
        errors.append("REGISTRY_FIELDS_INVALID")
    if payload.get("protocol") != REGISTRY_PROTOCOL:
        errors.append("REGISTRY_PROTOCOL_INVALID")
    profiles = payload.get("profiles")
    if not isinstance(profiles, list) or not profiles:
        return errors + ["PROFILES_INVALID"]
    seen: set[str] = set()
    for index, profile in enumerate(profiles):
        prefix = f"PROFILE_{index}_"
        if not isinstance(profile, dict):
            errors.append(prefix + "NOT_OBJECT")
            continue
        required_fields = {"runtime_id", "display_name", "adapter_version", "status", "capabilities", "evidence", "limitations"}
        if set(profile) != required_fields:
            errors.append(prefix + "FIELDS_INVALID")
        runtime_id = profile.get("runtime_id")
        if not _text(runtime_id):
            errors.append(prefix + "RUNTIME_ID_INVALID")
        elif runtime_id in seen:
            errors.append("DUPLICATE_RUNTIME_ID=" + runtime_id)
        else:
            seen.add(runtime_id)
        for field in ("display_name", "adapter_version"):
            if not _text(profile.get(field)):
                errors.append(prefix + field.upper() + "_INVALID")
        status = profile.get("status")
        if status not in ALLOWED_PROFILE_STATUS:
            errors.append(prefix + "STATUS_INVALID")
        caps = profile.get("capabilities")
        evidence = profile.get("evidence")
        limitations = profile.get("limitations")
        if not isinstance(caps, dict):
            errors.append(prefix + "CAPABILITIES_INVALID")
            caps = {}
        if not isinstance(evidence, list):
            errors.append(prefix + "EVIDENCE_INVALID")
            evidence = []
        if not isinstance(limitations, list) or any(not _text(item) for item in limitations):
            errors.append(prefix + "LIMITATIONS_INVALID")
        unknown_caps = sorted(set(caps) - REQUIRED_CAPABILITIES)
        if unknown_caps:
            errors.append(prefix + "UNKNOWN_CAPABILITIES=" + ",".join(unknown_caps))
        for name, state in caps.items():
            if state not in ALLOWED_CAPABILITY_STATUS:
                errors.append(prefix + "CAPABILITY_STATE_INVALID=" + name)
        if status == "VERIFIED":
            if set(caps) != REQUIRED_CAPABILITIES:
                errors.append(prefix + "VERIFIED_CAPABILITY_SET_INCOMPLETE")
            if any(caps.get(name) != "VERIFIED_AVAILABLE" for name in REQUIRED_CAPABILITIES):
                errors.append(prefix + "VERIFIED_CAPABILITY_NOT_AVAILABLE")
            if not evidence:
                errors.append(prefix + "VERIFIED_EVIDENCE_REQUIRED")
        elif status == "DECLARED":
            if evidence:
                errors.append(prefix + "DECLARED_PROFILE_MUST_NOT_CLAIM_EVIDENCE")
        elif status == "REVOKED":
            if not evidence:
                errors.append(prefix + "REVOKED_EVIDENCE_REQUIRED")
        for eidx, item in enumerate(evidence):
            if not isinstance(item, dict) or set(item) != {"kind", "ref", "scope"}:
                errors.append(prefix + f"EVIDENCE_{eidx}_INVALID")
                continue
            if any(not _text(item.get(field)) for field in ("kind", "ref", "scope")):
                errors.append(prefix + f"EVIDENCE_{eidx}_INVALID")
    return errors


def resolve_profile(payload: Any, runtime_id: str) -> dict[str, Any]:
    errors = validate_registry(payload)
    if errors:
        return {"status": "BLOCKED", "reasons": errors, "runtime_profile": None, **BOUNDARIES}
    profile = next((p for p in payload["profiles"] if p["runtime_id"] == runtime_id), None)
    if profile is None:
        return {"status": "HOLD", "reasons": ["RUNTIME_NOT_REGISTERED"], "runtime_profile": None, **BOUNDARIES}
    if profile["status"] != "VERIFIED":
        return {
            "status": "HOLD",
            "reasons": ["RUNTIME_PROFILE_NOT_VERIFIED=" + profile["status"]],
            "runtime_profile": None,
            "registry_entry": profile,
            **BOUNDARIES,
        }
    runtime_profile = {
        "protocol": HANDOFF_PROFILE_PROTOCOL,
        "runtime_id": profile["runtime_id"],
        "adapter_version": profile["adapter_version"],
        "capabilities": {name: "AVAILABLE" for name in sorted(REQUIRED_CAPABILITIES)},
    }
    return {
        "status": "VERIFIED_PROFILE_READY",
        "reasons": ["EVIDENCE_BACKED_PROFILE_EXPORTED"],
        "runtime_profile": runtime_profile,
        "evidence": profile["evidence"],
        "limitations": profile["limitations"],
        **BOUNDARIES,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("registry")
    parser.add_argument("--runtime-id")
    args = parser.parse_args()
    payload = json.loads(Path(args.registry).read_text(encoding="utf-8"))
    if args.runtime_id:
        result = resolve_profile(payload, args.runtime_id)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0 if result["status"] == "VERIFIED_PROFILE_READY" else 2
    errors = validate_registry(payload)
    print(json.dumps({"status": "VALID" if not errors else "HOLD", "errors": errors}, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
