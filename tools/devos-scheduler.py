#!/usr/bin/env python3
"""P12 Scheduler/Worker v2: bounded iteration with deterministic recovery gating."""
from __future__ import annotations
import argparse,importlib.util,json,sys
from pathlib import Path
from typing import Any
ROOT=Path(__file__).resolve().parents[1]
def _load(name:str,relative:str):
 p=ROOT/relative;s=importlib.util.spec_from_file_location(name,p)
 if s is None or s.loader is None:raise RuntimeError(f"module unavailable: {relative}")
 m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
def run_iteration(payload:dict[str,Any],project_root:Path,state_path:Path,checkpoint:Path|None=None):
 if not isinstance(payload,dict):raise ValueError("work-unit payload must be an object")
 recovery_mod=_load("devos_runtime_recovery","tools/devos-runtime-recovery.py");loop=_load("devos_autonomous_loop","tools/devos-autonomous-loop.py")
 try:recovery=recovery_mod.recover(state_path)
 except (OSError,ValueError,TypeError,json.JSONDecodeError) as e:return {"scheduler_version":"P12-SCHEDULER-v2","status":"HOLD","reason":"RECOVERY_STATE_INVALID","recovery":{"recovery_version":"P12-RECOVERY-v1","status":"RECOVERY_ERROR","action":"RECOVERY_HOLD_REQUIRES_REVIEW","error_type":type(e).__name__,"execution":"NONE","authorization":"UNCHANGED"},"iteration":0,"execution":"NONE","authorization":"UNCHANGED"}
 if recovery.get("status")=="RECOVERED" and recovery.get("action")=="RECOVERY_HOLD_REQUIRES_REVIEW":return {"scheduler_version":"P12-SCHEDULER-v2","status":"HOLD","reason":"RECOVERY_HOLD_REQUIRES_REVIEW","recovery":recovery,"iteration":0,"execution":"NONE","authorization":"UNCHANGED"}
 if recovery.get("status")=="RECOVERED" and recovery.get("outcome") in {"FAILED","BLOCKED","CANCELLED"}:return {"scheduler_version":"P12-SCHEDULER-v2","status":"HOLD","reason":"REVIEW_OUTCOME_BEFORE_CONTINUE","recovery":recovery,"iteration":0,"execution":"NONE","authorization":"UNCHANGED"}
 result=loop.run_once(payload,project_root,checkpoint,state_path);return {"scheduler_version":"P12-SCHEDULER-v2","status":result.get("status","FAILED"),"recovery":recovery,"iteration":1,"runtime_loop":result,"execution":"DELEGATE_TO_EXISTING_RUNTIME","authorization":"UNCHANGED"}
def run_batch(payloads:list[dict[str,Any]],project_root:Path,state_path:Path,checkpoint:Path|None=None,max_iterations:int=1):
 if not isinstance(payloads,list):raise ValueError("payloads must be a list")
 if not isinstance(max_iterations,int) or isinstance(max_iterations,bool) or max_iterations<1:raise ValueError("max_iterations must be a positive integer")
 if len(payloads)>max_iterations:raise ValueError("payload count exceeds max_iterations")
 seen=set()
 for payload in payloads:
  if not isinstance(payload,dict):raise ValueError("work-unit payload must be an object")
  identity=json.dumps(payload,sort_keys=True,separators=(",",":"),ensure_ascii=True)
  if identity in seen:raise ValueError("duplicate work-unit payload")
  seen.add(identity)
 results=[]
 for payload in payloads:
  result=run_iteration(payload,project_root,state_path,checkpoint);results.append(result)
  if result.get("status")!="COMPLETE":break
 return {"scheduler_version":"P12-SCHEDULER-v2","status":"COMPLETE" if results and all(r.get("status")=="COMPLETE" for r in results) else (results[-1].get("status","HOLD") if results else "NO_ACTION"),"iterations":len(results),"max_iterations":max_iterations,"results":results,"execution":"DELEGATE_TO_EXISTING_RUNTIME" if results else "NONE","authorization":"UNCHANGED","replay":"NEVER_AUTOMATIC"}
def main():
 a=argparse.ArgumentParser();a.add_argument("input",type=Path);a.add_argument("--project-root",type=Path,default=ROOT);a.add_argument("--state",type=Path,required=True);a.add_argument("--checkpoint",type=Path);a.add_argument("--max-iterations",type=int,default=1);args=a.parse_args();data=json.loads(args.input.read_text(encoding="utf-8"));result=run_batch(data,args.project_root,args.state,args.checkpoint,args.max_iterations) if isinstance(data,list) else run_iteration(data,args.project_root,args.state,args.checkpoint);print(json.dumps(result,indent=2,sort_keys=True));return 0 if result.get("status")=="COMPLETE" else 1
if __name__=="__main__":raise SystemExit(main())
