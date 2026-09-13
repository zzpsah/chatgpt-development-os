#!/usr/bin/env python3
"""Governed MCP/App gateway for remote DevOS operations.

This gateway is the control-plane boundary between an AI host/MCP adapter and
remote resource operations. It never contacts a provider. It evaluates the
existing DevOS remote-permission policy before a host may hand an operation to
the existing provider adapter.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PERM = ROOT / "tools" / "devos-remote-permission-check.py"


def _load_permission() -> Any:
    spec = importlib.util.spec_from_file_location("devos_remote_permission_check", PERM)
    if spec is None or spec.loader is None:
        raise RuntimeError("remote permission evaluator unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def evaluate_remote_operation(
    authorization: dict[str, Any] | None,
    operation: dict[str, Any],
) -> dict[str, Any]:
    mod = _load_permission()
    auth = mod.Authorization(**authorization) if authorization else None
    op = mod.Operation(**operation)
    status, reasons = mod.evaluate(auth, op)
    if status == "CONTINUE_WITH_EXISTING_APPROVAL":
        return {
            "decision": "ALLOW_TO_PROVIDER_GATE",
            "status": "READY",
            "capability": op.capability,
            "target": {"provider": op.provider, "owner": op.owner, "repository": op.repository, "resource": op.resource},
            "impact": op.impact,
            "authorization": "ALREADY_GRANTED",
            "authority": "UNCHANGED",
            "execution": "NONE",
            "mutation": "NONE",
        }
    hold = mod.actionable_hold(op, reasons)
    hold.update({
        "decision": "ACTIONABLE_HOLD",
        "execution": "NONE",
        "mutation": "NONE",
    })
    return hold


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--operation-json", required=True)
    parser.add_argument("--authorization-json")
    args = parser.parse_args()
    try:
        operation = json.loads(args.operation_json)
        authorization = json.loads(args.authorization_json) if args.authorization_json else None
        result = evaluate_remote_operation(authorization, operation)
    except (json.JSONDecodeError, TypeError, RuntimeError) as exc:
        result = {
            "decision": "ACTIONABLE_HOLD",
            "status": "BLOCKED",
            "reason_codes": ["MALFORMED_GATE_INPUT"],
            "reason": str(exc),
            "authority": "UNCHANGED",
            "execution": "NONE",
            "mutation": "NONE",
        }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "READY" else 2


if __name__ == "__main__":
    raise SystemExit(main())
