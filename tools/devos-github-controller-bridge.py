#!/usr/bin/env python3
"""Bounded DevOS controller -> P17 -> GitHub provider bridge.

This bridge accepts the normal controller execution candidate plus the exact P17
READY envelope, reuses the existing runtime-handoff validation, and only then
passes an explicit provider operation to the governed GitHub adapter.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
HANDOFF = ROOT / "tools" / "devos-runtime-handoff.py"
ADAPTER = ROOT / "tools" / "devos-github-provider-adapter.py"


def _load(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load {path.name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def execute(controller: dict[str, Any], readiness: dict[str, Any], authorization: dict[str, Any] | None = None) -> dict[str, Any]:
    handoff_mod = _load(HANDOFF, "devos_runtime_handoff")
    handoff = handoff_mod.build_p17_handoff(controller, readiness)
    if handoff.get("status") != "READY_FOR_RUNTIME":
        return {
            "status": "BLOCKED",
            "reason_codes": [handoff.get("reason", "runtime_handoff_blocked")],
            "handoff": handoff,
            "authority": "UNCHANGED",
            "execution": "NONE",
            "mutation": "NONE",
        }

    step = controller.get("compiled_step")
    if not isinstance(step, dict):
        return {"status": "BLOCKED", "reason_codes": ["COMPILED_STEP_MISSING"], "authority": "UNCHANGED", "execution": "NONE", "mutation": "NONE"}
    provider_operation = step.get("provider_operation")
    if not isinstance(provider_operation, dict):
        return {"status": "BLOCKED", "reason_codes": ["PROVIDER_OPERATION_MISSING"], "authority": "UNCHANGED", "execution": "NONE", "mutation": "NONE"}

    operation = dict(provider_operation)
    operation.setdefault("workflow", controller.get("workflow", "devos-controller-v1"))
    operation.setdefault("project", controller.get("project", ""))
    operation.setdefault("freshness", controller.get("repository_head"))

    adapter_mod = _load(ADAPTER, "devos_github_provider_adapter")
    result = adapter_mod.execute(operation, authorization)
    result["handoff"] = {
        "status": "READY_FOR_RUNTIME",
        "execution_started": result.get("execution") not in {None, "NONE"},
        "step_id": controller.get("task_id"),
        "repository_head": controller.get("repository_head"),
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--controller-json", required=True)
    parser.add_argument("--readiness-json", required=True)
    parser.add_argument("--authorization-json")
    args = parser.parse_args()
    try:
        controller = json.loads(args.controller_json)
        readiness = json.loads(args.readiness_json)
        authorization = json.loads(args.authorization_json) if args.authorization_json else None
        result = execute(controller, readiness, authorization)
    except (json.JSONDecodeError, TypeError, ValueError, RuntimeError) as exc:
        result = {"status": "BLOCKED", "reason_codes": ["MALFORMED_CONTROLLER_BRIDGE_INPUT"], "reason": str(exc), "authority": "UNCHANGED", "execution": "NONE", "mutation": "NONE"}
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result.get("status") in {"COMPLETE", "NEEDS_APPROVAL", "BLOCKED", "HOLD"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
