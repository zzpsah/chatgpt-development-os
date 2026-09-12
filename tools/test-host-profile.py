#!/usr/bin/env python3
"""Executable regression checks for the portable host profile contract."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load():
    spec = importlib.util.spec_from_file_location("host_profile", ROOT / "tools/verify-host-profile.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    module = load()
    profile = json.loads((ROOT / "adapters/host-profile.example.json").read_text(encoding="utf-8"))
    assert module.validate(profile) == []
    missing = dict(profile)
    missing["capabilities"] = dict(profile["capabilities"])
    del missing["capabilities"]["verification"]
    assert "missing capability: verification" in module.validate(missing)
    invalid = dict(profile)
    invalid["capabilities"] = dict(profile["capabilities"])
    invalid["capabilities"]["execution"] = {"status": "ASSUMED"}
    assert "invalid capability status: execution" in module.validate(invalid)
    print("Portable DevOS host-profile contract: PASS")


if __name__ == "__main__":
    main()
