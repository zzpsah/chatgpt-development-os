#!/usr/bin/env python3
"""Deterministic recovery reader for durable DevOS runtime state.

Recovery never executes or replays work. It classifies the latest persisted
outcome and requires fresh controller/runtime gates before any continuation.
"""
from __future__ import annotations
import argparse
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def _load_persistence():
    path = ROOT / "tools" / "devos-runtime-persistence.py"
    spec = importlib.util.spec_from_file_location("devos_runtime_persistence", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("persistence module unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module

def recover(path: Path) -> dict[str, object]:
    persistence = _load_persistence()
    latest = persistence.load_latest(path)
    if latest is None:
        return {"recovery_version":"P12-RECOVERY-v1","status":"NO_STATE","action":"SELECT_FROM_FRESH_STATE","execution":"NONE","authorization":"UNCHANGED"}
    status = latest.get("status")
    if status == "COMPLETE":
        action = "RECHECK_GATES_THEN_CONTINUE"
    elif status in {"FAILED", "BLOCKED", "CANCELLED"}:
        action = "REVIEW_OUTCOME_BEFORE_CONTINUE"
    else:
        action = "RECOVERY_HOLD_REQUIRES_REVIEW"
    return {
        "recovery_version":"P12-RECOVERY-v1",
        "status":"RECOVERED",
        "task_id":latest.get("task_id"),
        "outcome":status,
        "verification":latest.get("verification","UNVERIFIED"),
        "action":action,
        "execution":"NONE",
        "authorization":"UNCHANGED",
        "replay":"NEVER_AUTOMATIC",
    }

def main() -> int:
    parser = argparse.ArgumentParser(description="Recover durable DevOS runtime state without replay")
    parser.add_argument("state", type=Path)
    args = parser.parse_args()
    print(json.dumps(recover(args.state), indent=2, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
