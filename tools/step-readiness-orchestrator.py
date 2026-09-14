#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SECURITY_RELEVANT = {"HIGH_IMPACT_MUTATION", "SECURITY_SENSITIVE", "PRODUCTION_OR_DESTRUCTIVE"}
ALLOWED_IMPACTS = {"READ_ONLY", "LOW_IMPACT_MUTATION", "HIGH_IMPACT_MUTATION", "SECURITY_SENSITIVE", "PRODUCTION_OR_DESTRUCTIVE"}
STATE_CONFIDENCE = {"observed": 2, "likely": 1, "unknown": 0}
CONSTRAINT_TERMS = {"DO_NOT_DEPLOY":"deploy","DO_NOT_PRODUCTION":"production","DO_NOT_MERGE":"merge","DO_NOT_DATABASE":"database","DO_NOT_MIGRATION":"migration","DO_NOT_DELETE":"delete","DO_NOT_SECRET":"secret","DO_NOT_CREDENTIAL":"credential","DO_NOT_PERMISSION":"permission"}

def _load_p16_classifier():
    path=ROOT/"tools"/"semantic-goal-to-plan.py"; spec=importlib.util.spec_from_file_location("p16_semantic_classifier",path)
    if spec is None or spec.loader is None: raise ImportError("cannot load P16 semantic classifier")
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module); return module.classify
classify_objective=_load_p16_classifier()

def _base(plan:dict[str,Any],step_id:str|None,compiled_head:str|None,current_head:str|None)->dict[str,Any]:
    return {"protocol":"DEVOS-STEP-READINESS-v1","plan_protocol":plan.get("protocol"),"step_id":step_id,"repository_head":current_head,"compiled_repository_head":compiled_head,"gates":{"plan":False,"freshness":False,"dependencies":False,"capability":False,"authorization":False,"security":False,"verification":False},"reasons":[],"authority":"UNCHANGED","authorization":"UNCHANGED","execution":"NONE"}

def _has_cycle(steps:dict[str,dict[str,Any]])->bool:
    visiting=set(); visited=set()
    def visit(sid:str)->bool:
        if sid in visiting:return True
        if sid in visited:return False
        visiting.add(sid)
        for dep in steps[sid].get("depends_on",[]):
            if visit(str(dep)):return True
        visiting.remove(sid); visited.add(sid); return False
    return any(visit(sid) for sid in sorted(steps))

def _canonical(value:Any)->str|None:
    try:return json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False)
    except (TypeError,ValueError):return None

def _contradiction_error(claims:list[dict[str,Any]],state_resolution:dict[str,Any])->str|None:
    groups=defaultdict(list); reason_claims=set()
    for claim in claims:
        reasons=claim.get("reasons",[])
        if not isinstance(reasons,list):return "PLAN_STATE_RESOLUTION_CLAIM_REASONS_INVALID"
        has_reason="CROSS_CLAIM_CONTRADICTION" in reasons; fact_key=claim.get("fact_key"); fact_value=claim.get("fact_value")
        if fact_key is None:
            if has_reason:return "PLAN_STATE_RESOLUTION_CONTRADICTION_REASON_INCONSISTENT"
            continue
        if not isinstance(fact_key,str) or not fact_key.strip():return "PLAN_STATE_RESOLUTION_FACT_KEY_INVALID"
        canonical=_canonical(fact_value)
        if canonical is None:return "PLAN_STATE_RESOLUTION_FACT_VALUE_INVALID"
        if claim.get("state_confidence")!="unknown" or has_reason:groups[fact_key.strip()].append((claim,canonical))
        if has_reason:reason_claims.add(id(claim))
    expected=[]; expected_details=[]; seen=set()
    for fact_key in sorted(groups):
        members=groups[fact_key]; values=sorted({canonical for _,canonical in members})
        if len(values)<=1:continue
        expected.append(fact_key)
        claim_ids=sorted(str(claim.get("id")) for claim,_ in members if isinstance(claim.get("id"),str) and claim.get("id").strip())
        expected_details.append({"fact_key":fact_key,"claim_ids":claim_ids,"canonical_values":values})
        for claim,_ in members:
            seen.add(id(claim))
            if claim.get("state_confidence")!="unknown" or "CROSS_CLAIM_CONTRADICTION" not in claim.get("reasons",[]):return "PLAN_STATE_RESOLUTION_HIDDEN_CONTRADICTION"
    if reason_claims!=seen:return "PLAN_STATE_RESOLUTION_CONTRADICTION_REASON_INCONSISTENT"
    actual=state_resolution.get("contradiction_fact_keys",[])
    if not isinstance(actual,list) or any(not isinstance(x,str) or not x.strip() for x in actual):return "PLAN_STATE_RESOLUTION_CONTRADICTION_FACTS_INVALID"
    if sorted(actual)!=expected:return "PLAN_STATE_RESOLUTION_CONTRADICTION_SUMMARY_INCONSISTENT"
    actual_details=state_resolution.get("contradictions",[])
    if not isinstance(actual_details,list):return "PLAN_STATE_RESOLUTION_CONTRADICTION_DETAILS_INVALID"
    if actual_details!=expected_details:return "PLAN_STATE_RESOLUTION_CONTRADICTION_DETAILS_INCONSISTENT"
    return None

def _validate_state_resolution_summary(state_resolution:Any)->str|None:
    if not isinstance(state_resolution,dict) or state_resolution.get("protocol")!="DEVOS-AI-STATE-RESOLUTION-v2":return "PLAN_STATE_RESOLUTION_INVALID"
    if state_resolution.get("authority")!="UNCHANGED" or state_resolution.get("authorization")!="UNCHANGED":return "PLAN_STATE_RESOLUTION_AUTHORITY_CHANGED"
    if state_resolution.get("execution")!="NONE" or state_resolution.get("mutation")!="NONE":return "PLAN_STATE_RESOLUTION_EXECUTION_CHANGED"
    if state_resolution.get("status")!="RESOLVED":return "PLAN_STATE_RESOLUTION_NOT_RESOLVED"
    unresolved=state_resolution.get("unresolved_claim_ids")
    if not isinstance(unresolved,list):return "PLAN_STATE_RESOLUTION_UNRESOLVED_INVALID"
    if unresolved:return "PLAN_STATE_CLAIMS_UNRESOLVED="+",".join(sorted(str(i) for i in unresolved))
    claims=state_resolution.get("claims")
    if not isinstance(claims,list):return "PLAN_STATE_RESOLUTION_CLAIMS_INVALID"
    counts={level:0 for level in STATE_CONFIDENCE}
    for claim in claims:
        if not isinstance(claim,dict):return "PLAN_STATE_RESOLUTION_CLAIM_INVALID"
        confidence=claim.get("state_confidence")
        if confidence not in STATE_CONFIDENCE:return "PLAN_STATE_RESOLUTION_CONFIDENCE_INVALID"
        claim_id=claim.get("id")
        if claim_id is not None and (not isinstance(claim_id,str) or not claim_id.strip()):return "PLAN_STATE_RESOLUTION_CLAIM_ID_INVALID"
        counts[confidence]+=1
    contradiction_error=_contradiction_error(claims,state_resolution)
    if contradiction_error:return contradiction_error
    if counts["unknown"]:return "PLAN_STATE_RESOLUTION_HIDDEN_UNKNOWN_CLAIM"
    if state_resolution.get("state_confidence_summary")!=counts:return "PLAN_STATE_RESOLUTION_SUMMARY_INCONSISTENT"
    weakest=state_resolution.get("weakest_state_confidence"); expected=min((c["state_confidence"] for c in claims),key=lambda v:STATE_CONFIDENCE[v],default="unknown")
    if weakest!=expected:return "PLAN_STATE_RESOLUTION_WEAKEST_INCONSISTENT"
    return None

def _validated_steps(plan:dict[str,Any])->tuple[dict[str,dict[str,Any]]|None,str|None]:
    if plan.get("protocol")!="DEVOS-GOAL-PLAN-v1" or plan.get("decision")!="PLANNED":return None,"PLAN_NOT_PLANNED_OR_PROTOCOL_INVALID"
    if plan.get("authority")!="UNCHANGED" or plan.get("authorization")!="UNCHANGED":return None,"PLAN_AUTHORITY_BOUNDARY_CHANGED"
    if plan.get("execution")!="NONE":return None,"PLAN_EXECUTION_ALREADY_CLAIMED"
    if not isinstance(plan.get("project"),str) or not plan["project"].strip():return None,"PLAN_PROJECT_INVALID"
    if not isinstance(plan.get("objective"),str) or not plan["objective"].strip():return None,"PLAN_OBJECTIVE_INVALID"
    ambiguity=plan.get("ambiguity",[])
    if not isinstance(ambiguity,list):return None,"PLAN_AMBIGUITY_INVALID"
    if any(str(i).strip() for i in ambiguity):return None,"PLANNED_PLAN_HAS_AMBIGUITY"
    state_resolution=plan.get("state_resolution")
    if state_resolution is not None:
        err=_validate_state_resolution_summary(state_resolution)
        if err:return None,err
    constraints=plan.get("constraints",[])
    if not isinstance(constraints,list) or any(not isinstance(i,str) for i in constraints):return None,"PLAN_CONSTRAINTS_INVALID"
    raw_steps=plan.get("steps")
    if not isinstance(raw_steps,list) or not raw_steps:return None,"PLAN_STEPS_MISSING_OR_INVALID"
    steps={}
    for raw in raw_steps:
        if not isinstance(raw,dict):return None,"PLAN_STEP_NOT_OBJECT"
        sid=raw.get("id")
        if not isinstance(sid,str) or not sid.strip():return None,"PLAN_STEP_ID_INVALID"
        sid=sid.strip()
        if sid in steps:return None,"PLAN_STEP_ID_DUPLICATE="+sid
        objective=raw.get("objective")
        if not isinstance(objective,str) or not objective.strip():return None,"PLAN_STEP_OBJECTIVE_MISSING="+sid
        deps=raw.get("depends_on",[])
        if not isinstance(deps,list) or any(not isinstance(dep,str) or not dep.strip() for dep in deps):return None,"PLAN_STEP_DEPENDENCIES_INVALID="+sid
        impact=raw.get("impact")
        if impact not in ALLOWED_IMPACTS:return None,"PLAN_STEP_IMPACT_INVALID="+sid
        expected_impact=classify_objective(objective)
        if impact!=expected_impact:return None,f"PLAN_STEP_IMPACT_MISMATCH={sid}:{impact}:{expected_impact}"
        auth=raw.get("authorization_required")
        if auth not in (True,False):return None,"PLAN_STEP_AUTHORIZATION_FLAG_INVALID="+sid
        if impact in SECURITY_RELEVANT and auth is not True:return None,"PLAN_HIGH_IMPACT_AUTHORIZATION_INCONSISTENT="+sid
        verification=raw.get("verification")
        if not isinstance(verification,str) or not verification.strip():return None,"PLAN_STEP_VERIFICATION_MISSING="+sid
        expected=raw.get("expected_evidence")
        if not isinstance(expected,list) or not expected or any(not isinstance(i,str) or not i.strip() for i in expected):return None,"PLAN_STEP_EXPECTED_EVIDENCE_INVALID="+sid
        stop=raw.get("stop_or_escalate_if")
        if not isinstance(stop,str) or not stop.strip():return None,"PLAN_STEP_STOP_CONDITION_MISSING="+sid
        steps[sid]=raw
    known=set(steps)
    for sid,step in steps.items():
        for dep in step.get("depends_on",[]):
            if dep not in known:return None,f"PLAN_DEPENDENCY_UNKNOWN={sid}:{dep}"
            if dep==sid:return None,"PLAN_SELF_DEPENDENCY="+sid
    if _has_cycle(steps):return None,"PLAN_DEPENDENCY_CYCLE"
    for constraint in constraints:
        term=CONSTRAINT_TERMS.get(constraint)
        if not term:continue
        for sid,step in steps.items():
            if step.get("impact")=="READ_ONLY":continue
            if term in str(step.get("objective","")).lower():return None,f"PLAN_CONSTRAINT_CONFLICT={constraint}:{sid}"
    return steps,None

def evaluate(payload:dict[str,Any])->dict[str,Any]:
    plan=payload.get("plan") or {}; plan=plan if isinstance(plan,dict) else {}; step_id=payload.get("step_id"); compiled=payload.get("compiled_repository_head"); current=payload.get("current_repository_head"); out=_base(plan,step_id,compiled,current)
    steps,error=_validated_steps(plan)
    if error:out["status"]="BLOCKED";out["reasons"].append(error);return out
    assert steps is not None;out["gates"]["plan"]=True
    if not isinstance(step_id,str) or not step_id.strip():out["status"]="BLOCKED";out["reasons"].append("STEP_ID_INVALID");return out
    step_id=step_id.strip();out["step_id"]=step_id;step=steps.get(step_id)
    if not step:out["status"]="BLOCKED";out["reasons"].append("STEP_NOT_FOUND");return out
    if not isinstance(compiled,str) or not compiled.strip() or not isinstance(current,str) or not current.strip():out["status"]="NEEDS_EVIDENCE";out["reasons"].append("REPOSITORY_HEAD_EVIDENCE_MISSING");return out
    if compiled!=current:out["status"]="STOP";out["reasons"].append("STALE_PLAN_REPOSITORY_HEAD_CHANGED");return out
    out["gates"]["freshness"]=True
    completed_raw=payload.get("completed_steps",[])
    if not isinstance(completed_raw,list) or any(not isinstance(x,str) or not x.strip() for x in completed_raw):out["status"]="BLOCKED";out["reasons"].append("COMPLETED_STEPS_INVALID");return out
    completed={x.strip() for x in completed_raw};unknown=sorted(x for x in completed if x not in steps)
    if unknown:out["status"]="BLOCKED";out["reasons"].append("COMPLETED_STEP_UNKNOWN="+",".join(unknown));return out
    if step_id in completed:out["status"]="BLOCKED";out["reasons"].append("STEP_ALREADY_COMPLETE");return out
    for cid in sorted(completed):
        missing=sorted(str(dep) for dep in steps[cid].get("depends_on",[]) if str(dep) not in completed)
        if missing:out["status"]="BLOCKED";out["reasons"].append(f"COMPLETED_STEP_DEPENDENCY_INCOMPLETE={cid}:{','.join(missing)}");return out
    missing=[str(dep) for dep in step.get("depends_on",[]) if str(dep) not in completed]
    if missing:out["status"]="BLOCKED";out["reasons"].append("DEPENDENCIES_INCOMPLETE="+",".join(sorted(missing)));return out
    out["gates"]["dependencies"]=True
    capabilities=payload.get("capabilities",{});authmap=payload.get("authorization_by_step",{});secmap=payload.get("security_gate_by_step",{})
    if not isinstance(capabilities,dict) or not isinstance(authmap,dict) or not isinstance(secmap,dict):out["status"]="BLOCKED";out["reasons"].append("READINESS_EVIDENCE_MAP_INVALID");return out
    if capabilities.get(step_id)!="AVAILABLE":out["status"]="BLOCKED";out["reasons"].append("CAPABILITY_NOT_AVAILABLE");return out
    out["gates"]["capability"]=True
    if step.get("authorization_required") is True and authmap.get(step_id)!="ALREADY_GRANTED":out["status"]="NEEDS_APPROVAL";out["reasons"].append("STEP_BOUND_AUTHORIZATION_REQUIRED");return out
    out["gates"]["authorization"]=True
    impact=step.get("impact")
    if impact in SECURITY_RELEVANT:
        security=secmap.get(step_id)
        if security in (None,"UNKNOWN","NOT_RUN"):out["status"]="NEEDS_EVIDENCE";out["reasons"].append("SECURITY_GATE_EVIDENCE_REQUIRED");return out
        if security!="PASS":out["status"]="BLOCKED";out["reasons"].append("SECURITY_GATE_NOT_PASS");return out
    out["gates"]["security"]=True;out["gates"]["verification"]=True;out["status"]="READY"
    out["step"]={"id":step.get("id"),"objective":step.get("objective"),"depends_on":list(step.get("depends_on",[])),"expected_evidence":list(step.get("expected_evidence",[])),"impact":impact,"authorization_required":step.get("authorization_required"),"verification":step.get("verification"),"stop_or_escalate_if":step.get("stop_or_escalate_if"),"execution_evidence":False}
    out["reasons"].append("ALL_P17_GATES_SATISFIED");return out

def main()->None:
    parser=argparse.ArgumentParser();parser.add_argument("input",help="JSON file containing plan plus fresh readiness evidence");args=parser.parse_args();payload=json.loads(Path(args.input).read_text(encoding="utf-8"));print(json.dumps(evaluate(payload),indent=2,sort_keys=True))
if __name__=="__main__":main()
