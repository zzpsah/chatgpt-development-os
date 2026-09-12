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
persist_mod = importlib.util.module_from_spec(persist_spec); sys.modules[persist_spec.name] = persist_mod; persist_spec.loader.exec_module(persist_mod)
with tempfile.TemporaryDirectory() as tmp:
    state = Path(tmp) / "RUNTIME-STATE.json"
    empty = module.recover(state)
    assert empty["status"] == "NO_STATE" and empty["execution"] == "NONE" and empty["authorization"] == "UNCHANGED"
    persist_mod.persist(state, {"status":"COMPLETE","verification":"VERIFIED","security":"NOT_APPLICABLE","evidence":[{"source":"test","exit_status":0}],"checkpoint":None}, "task-1", "bounded test")
    first = module.recover(state); second = module.recover(state)
    assert first == second
    assert first["status"] == "RECOVERED" and first["outcome"] == "COMPLETE"
    assert first["action"] == "RECHECK_GATES_THEN_CONTINUE"
    assert first["replay"] == "NEVER_AUTOMATIC"
    persist_mod.persist(state, {"status":"FAILED","verification":"FAILED","security":"NOT_APPLICABLE","evidence":[{"source":"test","exit_status":3}],"checkpoint":None}, "task-2", "failed test")
    failed = module.recover(state)
    assert failed["outcome"] == "FAILED" and failed["action"] == "REVIEW_OUTCOME_BEFORE_CONTINUE"
    assert failed["execution"] == "NONE" and failed["authorization"] == "UNCHANGED"
print("DevOS runtime recovery contract: PASS")
