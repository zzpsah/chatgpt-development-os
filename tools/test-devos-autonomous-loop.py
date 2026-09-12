#!/usr/bin/env python3
"""Executable contract tests for the bounded autonomous loop."""
from __future__ import annotations
import importlib.util, sys, tempfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("devos_auto_loop", ROOT / "tools/devos-autonomous-loop.py"); assert spec and spec.loader
module = importlib.util.module_from_spec(spec); sys.modules[spec.name] = module; spec.loader.exec_module(module)
def base_task(script: str) -> dict:
    return {"id":"verify","objective":"run bounded verification","status":"READY","priority":1,"dependencies":[],"capability_required":"verification.run","capability_available":True,"capability_status":"AVAILABLE","authorization":"NOT_REQUIRED","security_relevant":False,"verification":{"id":"contract","command":[sys.executable,script],"timeout_seconds":30}}
def write_script(root: Path, name: str, body: str) -> str:
    (root/name).write_text(body, encoding="utf-8"); return name
with tempfile.TemporaryDirectory() as tmp:
    root=Path(tmp); script=write_script(root,"ok.py","print('RAW_OK')\n")
    payload={"tasks":[base_task(script)],"events":[],"failures":[],"evidence":[]}; result=module.run_once(payload,root,root/"checkpoint.json")
    assert result["status"]=="COMPLETE" and result["runtime"]["evidence"][0]["stdout"].strip()=="RAW_OK" and (root/"checkpoint.json").is_file()
    blocked=base_task(script); blocked["authorization"]="REQUIRED"; blocked["authorization_status"]="PENDING"; result=module.run_once({"tasks":[blocked],"events":[],"failures":[],"evidence":[]},root)
    assert result["status"]=="BLOCKED" and "AUTHORIZATION_NOT_APPROVED" in result["handoff"]["reasons"]
    bad=write_script(root,"bad.py","raise SystemExit(3)\n"); failed_task=base_task(bad); result=module.run_once({"tasks":[failed_task],"events":[],"failures":[],"evidence":[]},root)
    assert result["status"]=="FAILED" and result["runtime"]["evidence"][0]["exit_status"]==3
print("DevOS autonomous loop contract: PASS")
