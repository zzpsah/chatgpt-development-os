#!/usr/bin/env python3
"""Validate a vendor-neutral DevOS host capability profile."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


PROTOCOL_VERSION = "DEVOS-HOST-PROFILE-v1"
REQUIRED_CAPABILITIES = (
    "project_discovery", "bootstrap", "inspection", "intent_routing",
    "state_resolution", "execution", "verification", "persistence",
)
VALID_STATES = {"AVAILABLE", "DELEGATABLE", "MISSING"}


def validate(profile: dict[str, Any]) -> list[str]:
    """Return deterministic validation errors without inventing host support."""
    errors: list[str] = []
    if profile.get("protocol_version") != PROTOCOL_VERSION:
        errors.append("unsupported protocol_version")
    if not isinstance(profile.get("host_id"), str) or not profile["host_id"].strip():
        errors.append("host_id must be a non-empty string")
    if not isinstance(profile.get("adapter_version"), str) or not profile["adapter_version"].strip():
        errors.append("adapter_version must be a non-empty string")
    capabilities = profile.get("capabilities")
    if not isinstance(capabilities, dict):
        return errors + ["capabilities must be an object"]
    for name in REQUIRED_CAPABILITIES:
        record = capabilities.get(name)
        if not isinstance(record, dict):
            errors.append(f"missing capability: {name}")
            continue
        if record.get("status") not in VALID_STATES:
            errors.append(f"invalid capability status: {name}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("profile", help="path to a DEVOS-HOST-PROFILE-v1 JSON file")
    args = parser.parse_args()
    try:
        profile = json.loads(Path(args.profile).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"INVALID: {exc}")
        return 2
    errors = validate(profile)
    if errors:
        print("INVALID: " + "; ".join(errors))
        return 1
    print(f"VALID: {profile['host_id']} declares {len(REQUIRED_CAPABILITIES)} portable capabilities")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
