#!/usr/bin/env python3
"""Parse a DevOS stance expression against the centralized registry."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required: python -m pip install pyyaml") from exc

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "config" / "devos-stance-registry.yaml"
TOKEN = re.compile(r"^[A-Z][A-Z0-9_-]*$")


def load_registry() -> dict:
    with REGISTRY_PATH.open(encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError("invalid stance registry")
    return data


def parse(expression: str, registry: dict) -> dict:
    value = expression.strip()
    if value.lower() in registry.get("aliases", {}):
        value = registry["aliases"][value.lower()]
    if value == "DEVOS":
        execution = registry["default_execution"]
        style = registry["default_style"]
    else:
        parts = value.split("::")
        if len(parts) not in (2, 3) or parts[0] != "DEVOS":
            raise ValueError("expected DEVOS, DEVOS::<EXECUTION>, or DEVOS::<EXECUTION>::<STYLE>")
        execution = parts[1]
        style = parts[2] if len(parts) == 3 else registry["default_style"]
    if not TOKEN.fullmatch(execution) or execution not in registry["executions"]:
        raise ValueError(f"unknown execution stance: {execution}")
    if not TOKEN.fullmatch(style) or style not in registry["styles"]:
        raise ValueError(f"unknown communication style: {style}")

    exec_cfg = registry["executions"][execution]
    style_cfg = registry["styles"][style]
    return {
        "input": expression,
        "canonical": f"DEVOS::{execution}::{style}",
        "execution": execution,
        "style": style,
        "execution_contract": exec_cfg,
        "style_contract": style_cfg,
        "authorization_note": "Stance/style selection never grants permission beyond the user's request and project/security policy.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("expression")
    args = parser.parse_args()
    result = parse(args.expression, load_registry())
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
