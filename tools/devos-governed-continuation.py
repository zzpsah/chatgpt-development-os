#!/usr/bin/env python3
"""Bridge remote-operation permission governance into DevOS continuation decisions.

This module is deliberately side-effect-free. It combines a recovered scoped
approval and a proposed remote operation into a deterministic continuation
or HOLD decision. Execution remains the responsibility of the existing
P17/controller/provider adapter path.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PERMISSION_MODULE = ROOT / "tools" / "devos-remote-permission-check.py"


def _load_permission_module() -> Any:
    spec = importlib.util.spec_from_file_location("devos_remote_permission_check", PERMISSION_MODULE)
    if spec is None or spec.loader is None:
        raise RuntimeError("remote permission evaluator is unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def decide(authorization: dict[str, Any] | None, operation: dict[str, Any]) -> dict[str, Any]:
    """Return a governed continuation decision without executing a mutation."""
    mod = _load_permission_module()
    auth = mod.Authorization(**authorization) if authorization else None
    op = mod.Operation(**operation)
    status, reasons = mod.evaluate(auth, op)

    if status == "CONTINUE_WITH_EXISTING_APPROVAL":
        return {
            "decision": "CONTINUE_WITH_EXISTING_APPROVAL",
            "status": "CONTINUE",
            "reason_codes": [],
            "target": {
                "provider": op.provider,
                "owner": op.owner,
                "repository": op.repository,
                "resource": op.resource,
            },
            "capability": op.capability,
            "impact": op.impact,
            "authority": "UNCHANGED",
            "authorization": "ALREADY_GRANTED",
            "execution": "NONE",
            "mutation": "NONE",
            "next": "handoff to existing P17/controller/provider execution path",
        }

    hold = mod.actionable_hold(op, reasons)
    hold.update({
        "decision": "ACTIONABLE_HOLD",
        "status": "NEEDS_APPROVAL",
        "execution": "NONE",
        "mutation": "NONE",
    })
    return hold


def main() -> int:
    parser = argparse.ArgumentParser(description="DevOS governed continuation decision")
    parser.add_argument("--operation", required=True, help="JSON encoded operation")
    parser.add_argument("--authorization", help="JSON encoded recovered approval scope")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    operation = json.loads(args.operation)
    authorization = json.loads(args.authorization) if args.authorization else None
    result = decide(authorization, operation)

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print("DEVOS GOVERNED CONTINUATION v1")
        print(f"Decision: {result['decision']}")
        print(f"Capability: {result.get('capability', result.get('next_action', '?'))}")
        print(f"Impact: {result.get('impact', '?')}")
        print(f"Execution: {result['execution']}")
        print(f"Mutation: {result['mutation']}")
        if result.get("reason_codes"):
            print("Reasons: " + ", ".join(result["reason_codes"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
