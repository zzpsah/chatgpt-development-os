#!/usr/bin/env python3
"""P12 Scheduler/Worker v1: one bounded autonomous iteration with recovery gating."""
from __future__ import annotations
import argparse, importlib.util, json, sys
from pathlib import Path
from typing import Any
ROOT = Path(__file__).resolve().parents[1]

def _load(name: str, relative: str):
    path = ROOT / relative
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"module unavailable: {relative}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

def run_iteration(payload: dict[str, Any], project_root: Path, state_path: Path, checkpoint: Path | None = None) -> dict[str, Any]:
    recovery_mod = _load("devos_runtime_recovery", "tools/devos-runtime-recovery.py")
    loop = _load("devos_autonomous_loop", "tools/devos-autonomous-loop.py")
    try:
        recovery = recovery_mod.recover(state_path)
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        return {
            "scheduler_version":"P12-SCHEDULER-v1",
            "status":"HOLD",
            "reason":"RECOVERY_STATE_INVALID",
            "recovery":{"recovery_version":"P12-RECOVERY-v1","status":"RECOVERY_ERROR","action":"RECOVERY_HOLD_REQUIRES_REVIEW","error_type":type(exc).__name__,"execution":"NONE","authorization":"UNCHANGED","replay":"NEVER_AUTOMATIC"},
            "iteration":0,
            "execution":"NONE",
            "authorization":"UNCHANGED",
        }
    if recovery.get("status") == "RECOVERED" and recovery.get("action") == "RECOVERY_HOLD_REQUIRES_REVIEW":
        return {"scheduler_version":"P12-SCHEDULER-v1","status":"HOLD","reason":"RECOVERY_HOLD_REQUIRES_REVIEW","recovery":recovery,"iteration":0,"execution":"NONE","authorization":"UNCHANGED"}
    if recovery.get("status") == "RECOVERED" and recovery.get("outcome") in {"FAILED", "BLOCKED", "CANCELLED"}:
        return {"scheduler_version":"P12-SCHEDULER-v1","status":"HOLD","reason":"REVIEW_OUTCOME_BEFORE_CONTINUE","recovery":recovery,"iteration":0,"execution":"NONE","authorization":"UNCHANGED"}
    result = loop.run_once(payload, project_root, checkpoint, state_path)
    return {"scheduler_version":"P12-SCHEDULER-v1","status":result.get("status","FAILED"),"recovery":recovery,"iteration":1,"runtime_loop":result,"execution":"DELEGATE_TO_EXISTING_RUNTIME","authorization":"UNCHANGED"}

def main() -> int:
    parser = argparse.ArgumentParser(description="Run exactly one bounded DevOS scheduler/worker iteration")
    parser.add_argument("input", type=Path); parser.add_argument("--project-root", type=Path, default=ROOT); parser.add_argument("--state", type=Path, required=True); parser.add_argument("--checkpoint", type=Path)
    args = parser.parse_args()
    result = run_iteration(json.loads(args.input.read_text(encoding="utf-8")), args.project_root, args.state, args.checkpoint)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result.get("status") == "COMPLETE" else 1
if __name__ == "__main__":
    raise SystemExit(main())
