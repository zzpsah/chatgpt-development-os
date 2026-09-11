#!/usr/bin/env python3
"""Executable tests for the centralized DevOS stance parser."""
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = spec_from_file_location("devos_stance_parser", ROOT / "tools" / "parse-devos-stance.py")
assert spec and spec.loader
module = module_from_spec(spec)
spec.loader.exec_module(module)

registry = module.load_registry()

cases = {
    "DEVOS::GOD::DESI": ("GOD", "DESI"),
    "DEVOS::CONTINUE::DESI": ("CONTINUE", "DESI"),
    "DEVOS::FUCK::DESI": ("FUCK", "DESI"),
    "DEVOS::DEVIL::DESI": ("DEVIL", "DESI"),
    "god mode": ("GOD", "DESI"),
    "desi mode": ("CONTINUE", "DESI"),
    "DEVOS": ("CONTINUE", "DESI"),
}

for expression, expected in cases.items():
    result = module.parse(expression, registry)
    actual = (result["execution"], result["style"])
    assert actual == expected, (expression, actual, expected)

for bad in ("DEVOS::UNKNOWN", "DEVOS::GOD::UNKNOWN", "GOD::DESI", "DEVOS::GOD::DESI::EXTRA"):
    try:
        module.parse(bad, registry)
    except ValueError:
        pass
    else:
        raise AssertionError(f"invalid stance unexpectedly accepted: {bad}")

print("PASS: composable stance parser resolves canonical stance + style")
print("PASS: default DEVOS resolves to CONTINUE + DESI")
print("PASS: legacy human aliases resolve safely")
print("PASS: unknown/invalid expressions are rejected")
