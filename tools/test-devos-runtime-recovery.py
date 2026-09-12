#!/usr/bin/env python3
"""Executable contract tests for deterministic runtime recovery."""
from __future__ import annotations
import importlib.util, json, sys, tempfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("devos_runtime_recovery", ROOT / "tools/devos-runtime-recovery.py")
assert spec and spec.loader
module = importlib.util.module_from_spec(spec); sys.modules[spec.name] = module; spec.loader.exec_module(module)
persist_spec = importlib.util.spec_from_file_location("devos_runtime_persistence", ROOT / "tools/devos-runtime-persistence.py")
assert persist_spec and persist_spec.loader
persist_mod = importlib.util.module_from_spec(persist_spec); sys.modules[persist_spec.name] = persist_mod; persist_spec.loader.exec_module(persist_spec.loader.load_module() if False else persist_mod)

VALID_CHECKPOINT = {
    "id": "runtime-test",
    "runtime_version": "P12-RUNTIME-v1",
    "objective": "bounded test",
    "iteration": 1,
    "work_unit": "task-1",
    "repository_head": "UNKNOWN",
    "status": "COMPLETE",
    "changes": [],
    "evidence": [{"source": "test"}],
    "verification": "VERIFIED",
    "blockers": [],
    "next_action": "persist/continue with next bounded work unit",
}

with tempfile.TemporaryDirectory() as tmp:
    state = Path(tmp) / "RUNTIME-STATE.json"
    empty = module.recover(state)
    assert empty["status"] == "NO_STATE" and empty["execution"] == "NONE" and empty["authorization"] == "UNCHANGED"
    persist_mod.persist(state, {"status":"COMPLETE","verification":"VERIFIED","security":"NOT_APPLICABLE","evidence":[{"source":"test","exit_status":0}],"checkpoint":VALID_CHECKPOINT}, "task-1", "bounded test")
    first = module.recover(state); second = module.recover(state)
    assert first == second
    assert first["status"] == "RECOVERED" and first["outcome"] == "COMPLETE"
    assert first["action"] == "RECHECK_GATES_THEN_CONTINUE"
    assert first["checkpoint_action"] == "CHECKPOINT_REQUIRES_FRESH_GATES"
    assert first["replay"] == "NEVER_AUTOMATIC"
    persist_mod.persist(state, {"status":"FAILED","verification":"FAILED","security":"NOT_APPLICABLE","evidence":[{"source":"test","exit_status":3}],"checkpoint":None}, "task-2", "failed test")
    failed = module.recover(state)
    assert failed["outcome"] == "FAILED" and failed["action"] == "REVIEW_OUTCOME_BEFORE_CONTINUE"
    assert failed["execution"] == "NONE" and failed["authorization"] == "UNCHANGED"

    malformed = Path(tmp) / "MALFORMED.json"
    malformed.write_text(json.dumps({"state_version": "P12-PERSISTENCE-v1", "latest": {"task_id":"x","objective":"y","status":"COMPLETE","evidence":[],"checkpoint":VALID_CHECKPOINT}, "history": []}), encoding="utf-8")
    try:
        module.recover(malformed)
    except ValueError:
        pass
    else:
        raise AssertionError("empty evidence must fail closed")

    bad_checkpoint = Path(tmp) / "BAD-CHECKPOINT.json"
    broken = dict(VALID_CHECKPOINT); broken.pop("next_action")
    bad_checkpoint.write_text(json.dumps({"state_version":"P12-PERSISTENCE-v1","latest":{"recorded_at":1,"task_id":"x","objective":"y","status":"COMPLETE","verification":"VERIFIED","security":"NOT_APPLICABLE","evidence":[{"source":"test"}],"checkpoint":broken},"history":[]}), encoding="utf-8")
    try:
        module.recover(bad_checkpoint)
    except ValueError:
        pass
    else:
        raise AssertionError("malformed checkpoint must fail closed")
print("DevOS runtime recovery contract: PASS")
