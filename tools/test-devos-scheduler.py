#!/usr/bin/env python3
"""Executable proof for the P12 Scheduler/Worker v1 contract."""
from __future__ import annotations
import importlib.util, json, sys, tempfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("scheduler", ROOT / "tools/devos-scheduler.py"); assert spec and spec.loader
module = importlib.util.module_from_spec(spec); sys.modules[spec.name] = module; spec.loader.exec_module(module)
def task(task_id: str, script: str) -> dict:
    return {"id":task_id,"objective":f"run bounded verification {task_id}","status":"READY","priority":1,"dependencies":[],"capability_required":"verification.run","capability_available":True,"capability_status":"AVAILABLE","authorization":"NOT_REQUIRED","security_relevant":False,"verification":{"id":f"contract-{task_id}","command":[sys.executable,script],"timeout_seconds":30}}
with tempfile.TemporaryDirectory() as tmp:
    root=Path(tmp); (root/"ok.py").write_text("print('SCHED_OK')\n", encoding="utf-8"); (root/"ok2.py").write_text("print('SCHED_OK_2')\n", encoding="utf-8"); state=root/".ai"/"RUNTIME-STATE.json"
    payload={"tasks":[task("verify","ok.py")],"events":[],"failures":[],"evidence":[]}
    result=module.run_iteration(payload, root, state, root/"checkpoint.json")
    assert result["status"]=="COMPLETE" and result["iteration"]==1
    saved=json.loads(state.read_text(encoding="utf-8")); assert saved["latest"]["status"]=="COMPLETE"
    batch_payloads=[{"tasks":[task("verify-2","ok.py")],"events":[],"failures":[],"evidence":[]},{"tasks":[task("verify-3","ok2.py")],"events":[],"failures":[],"evidence":[]}]
    batch=module.run_batch(batch_payloads, root, state, max_iterations=2)
    assert batch["status"]=="COMPLETE" and batch["iterations"]==2 and batch["max_iterations"]==2
    limited=module.run_batch(batch_payloads[:1], root, state, max_iterations=1)
    assert limited["status"]=="COMPLETE" and limited["iterations"]==1
    try:
        module.run_batch(batch_payloads, root, state, max_iterations=0)
    except ValueError:
        pass
    else:
        raise AssertionError("max_iterations=0 must fail closed")
    try:
        module.run_batch(batch_payloads, root, state, max_iterations=1)
    except ValueError:
        pass
    else:
        raise AssertionError("payloads exceeding max_iterations must fail closed")
    persistence=module._load("devos_runtime_persistence", "tools/devos-runtime-persistence.py")
    failed={"status":"FAILED","verification":"FAILED","security":"PASS","evidence":[{"stdout":"","stderr":"failed","exit_status":3,"duration_seconds":0.01,"command":[sys.executable,"bad.py"]}],"checkpoint":None}
    persistence.persist(state, failed, "verify", "failed prior work")
    hold=module.run_iteration(payload, root, state)
    assert hold["status"]=="HOLD" and hold["iteration"]==0 and hold["execution"]=="NONE"
    assert hold["recovery"]["action"]=="REVIEW_OUTCOME_BEFORE_CONTINUE"
    state.write_text(json.dumps({"state_version":"P12-PERSISTENCE-v1","latest":{"task_id":"verify","status":"UNKNOWN"},"history":[]}), encoding="utf-8")
    unknown=module.run_iteration(payload, root, state)
    assert unknown["status"]=="HOLD" and unknown["iteration"]==0 and unknown["execution"]=="NONE"
    assert unknown["reason"]=="RECOVERY_HOLD_REQUIRES_REVIEW"
    state.write_text("{malformed", encoding="utf-8")
    malformed=module.run_iteration(payload, root, state)
    assert malformed["status"]=="HOLD" and malformed["iteration"]==0 and malformed["execution"]=="NONE"
    assert malformed["reason"]=="RECOVERY_STATE_INVALID"
print("DevOS scheduler/worker v1 contract: PASS")
