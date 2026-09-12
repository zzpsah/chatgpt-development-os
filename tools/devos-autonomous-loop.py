#!/usr/bin/env python3
"""DevOS bounded autonomous loop: OI -> controller -> handoff -> runtime.

This is the first operational loop. It executes only verification.run work units
that pass independent controller/handoff gates. It does not invent authority,
run arbitrary shell, commit changes, or treat AI assertions as evidence.
"""
from __future__ import annotations
import argparse, importlib.util, json, sys
from pathlib import Path
from typing import Any
ROOT = Path(__file__).resolve().parents[1]
def load(name: str, relative: str):
    path = ROOT / relative
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None: raise RuntimeError(f"module unavailable: {relative}")
    module = importlib.util.module_from_spec(spec); sys.modules[name] = module; spec.loader.exec_module(module); return module
def run_once(payload: dict[str, Any], project_root: Path, checkpoint: Path | None = None) -> dict[str, Any]:
    controller = load("devos_task_controller", "tools/devos-task-controller.py")
    handoff_mod = load("devos_runtime_handoff", "tools/devos-runtime-handoff.py")
    runtime = load("devos_execution_runtime", "tools/devos-execution-runtime.py")
    tasks = list(payload.get("tasks", [])); controller_result = controller.controller_decision(payload)
    task_id = controller_result.get("task_id"); task = next((x for x in tasks if str(x.get("id")) == str(task_id)), None)
    if task is None: return {"status":"BLOCKED","stage":"controller","reason":"TASK_NOT_FOUND","controller":controller_result}
    handoff = handoff_mod.build_handoff(controller_result, task)
    if handoff.get("status") != "APPROVED_FOR_RUNTIME": return {"status":"BLOCKED","stage":"handoff","handoff":handoff,"controller":controller_result}
    verification = task.get("verification")
    if not isinstance(verification, dict): return {"status":"BLOCKED","stage":"runtime","reason":"VERIFICATION_SPEC_REQUIRED","handoff":handoff}
    result = runtime.execute(handoff, project_root, verification, checkpoint)
    accepted = handoff_mod.accept_runtime_result(handoff, result)
    return {"loop_version":"P12-AUTO-LOOP-v1","status":accepted.get("status","FAILED"),"controller":controller_result,"handoff":handoff,"runtime":result,"accepted":accepted}
def main() -> int:
    parser = argparse.ArgumentParser(description="Run one bounded DevOS autonomous iteration")
    parser.add_argument("input", type=Path); parser.add_argument("--project-root", type=Path, default=ROOT); parser.add_argument("--checkpoint", type=Path)
    args = parser.parse_args(); result = run_once(json.loads(args.input.read_text(encoding="utf-8")), args.project_root, args.checkpoint)
    print(json.dumps(result, indent=2, sort_keys=True)); return 0 if result.get("status") == "COMPLETE" else 1
if __name__ == "__main__": raise SystemExit(main())
