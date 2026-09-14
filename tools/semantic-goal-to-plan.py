#!/usr/bin/env python3
import argparse
import json
import re
from collections import defaultdict

HIGH_IMPACT = {"deploy", "production", "merge", "database", "migration", "delete", "secret", "credential", "permission"}
SECURITY_TERMS = {"security", "auth", "authentication", "authorization", "credential", "secret"}
MUTATING_IMPACTS = {"LOW_IMPACT_MUTATION", "HIGH_IMPACT_MUTATION", "PRODUCTION_OR_DESTRUCTIVE"}
READ_ONLY_PREFIXES = ("inspect ", "read ", "list ", "show ", "examine ", "view ")
NON_MATERIAL_GATING_ANNOTATIONS = {"HIGH_IMPACT_REQUIRES_AUTHORIZATION_CHECK"}
STATE_CONFIDENCE = {"observed": 2, "likely": 1, "unknown": 0}
CONSTRAINT_TERMS = {"DO_NOT_DEPLOY":"deploy","DO_NOT_PRODUCTION":"production","DO_NOT_MERGE":"merge","DO_NOT_DATABASE":"database","DO_NOT_MIGRATION":"migration","DO_NOT_DELETE":"delete","DO_NOT_SECRET":"secret","DO_NOT_CREDENTIAL":"credential","DO_NOT_PERMISSION":"permission"}

def classify(text: str) -> str:
    t=text.lower().strip()
    if any(term in t for term in SECURITY_TERMS): return "SECURITY_SENSITIVE"
    if t.startswith(READ_ONLY_PREFIXES): return "READ_ONLY"
    if any(term in t for term in ("delete","production","deploy")): return "PRODUCTION_OR_DESTRUCTIVE"
    if any(term in t for term in HIGH_IMPACT): return "HIGH_IMPACT_MUTATION"
    if any(term in t for term in ("change","fix","add","update","implement","write","create")): return "LOW_IMPACT_MUTATION"
    return "READ_ONLY"

def expand_read_before_write(phrases:list[str])->list[str]:
    expanded=[]
    for phrase in phrases:
        impact=classify(phrase); previous=bool(expanded) and classify(expanded[-1])=="READ_ONLY"
        if impact in MUTATING_IMPACTS and not previous: expanded.append(f"inspect current repository state relevant to: {phrase}")
        expanded.append(phrase)
    return expanded

def _negative_constraint_conflict(steps:list[dict],constraints:list[str])->str|None:
    for constraint in constraints:
        term=CONSTRAINT_TERMS.get(constraint)
        if not term: continue
        for step in steps:
            if step["impact"]=="READ_ONLY": continue
            if term in step["objective"].lower(): return f"compiled step conflicts with explicit negative constraint {constraint}"
    return None

def _canonical(value):
    try: return json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False)
    except (TypeError,ValueError): return None

def _contradiction_integrity(claims:list[dict], state_resolution:dict)->str|None:
    groups=defaultdict(list); contradiction_reason_claims=set()
    for claim in claims:
        reasons=claim.get("reasons",[])
        if not isinstance(reasons,list): return "state resolution claim reasons invalid"
        has_reason="CROSS_CLAIM_CONTRADICTION" in reasons
        fact_key=claim.get("fact_key")
        fact_value=claim.get("fact_value")
        if fact_key is None:
            if has_reason: return "state resolution contradiction reason inconsistent"
            continue
        if not isinstance(fact_key,str) or not fact_key.strip(): return "state resolution fact key invalid"
        canonical=_canonical(fact_value)
        if canonical is None: return "state resolution fact value invalid"
        if claim.get("state_confidence")!="unknown" or has_reason:
            groups[fact_key.strip()].append((claim,canonical))
        if has_reason: contradiction_reason_claims.add(id(claim))
    expected=[]; seen_reason_claims=set()
    for fact_key in sorted(groups):
        members=groups[fact_key]; values={canonical for _,canonical in members}
        if len(values)<=1: continue
        expected.append(fact_key)
        for claim,_ in members:
            seen_reason_claims.add(id(claim))
            if claim.get("state_confidence")!="unknown" or "CROSS_CLAIM_CONTRADICTION" not in claim.get("reasons",[]):
                return "state resolution cross-claim contradiction hidden"
    if contradiction_reason_claims!=seen_reason_claims: return "state resolution contradiction reason inconsistent"
    actual=state_resolution.get("contradiction_fact_keys",[])
    if not isinstance(actual,list) or any(not isinstance(x,str) or not x.strip() for x in actual): return "state resolution contradiction facts invalid"
    if sorted(actual)!=expected: return "state resolution contradiction summary inconsistent"
    return None

def _state_resolution_summary(state_resolution:dict)->tuple[dict|None,str|None]:
    if not isinstance(state_resolution,dict) or state_resolution.get("protocol")!="DEVOS-AI-STATE-RESOLUTION-v2": return None,"state resolution invalid"
    if state_resolution.get("authority")!="UNCHANGED" or state_resolution.get("authorization")!="UNCHANGED": return None,"state resolution authority boundary changed"
    if state_resolution.get("execution")!="NONE" or state_resolution.get("mutation")!="NONE": return None,"state resolution execution boundary changed"
    status=state_resolution.get("status")
    if status not in {"RESOLVED","NEEDS_EVIDENCE","BLOCKED"}: return None,"state resolution status invalid"
    unresolved=state_resolution.get("unresolved_claim_ids",[])
    if not isinstance(unresolved,list) or any(not isinstance(i,str) or not i.strip() for i in unresolved): return None,"state resolution unresolved claims invalid"
    weakest=state_resolution.get("weakest_state_confidence","unknown")
    if weakest not in STATE_CONFIDENCE: return None,"state resolution confidence invalid"
    claims=state_resolution.get("claims",[])
    if not isinstance(claims,list): return None,"state resolution claims invalid"
    counts={level:0 for level in STATE_CONFIDENCE}; computed=[]; any_unknown=False
    for claim in claims:
        if not isinstance(claim,dict): return None,"state resolution claim invalid"
        confidence=claim.get("state_confidence")
        if confidence not in STATE_CONFIDENCE: return None,"state resolution claim confidence invalid"
        claim_id=claim.get("id")
        if claim_id is not None and (not isinstance(claim_id,str) or not claim_id.strip()): return None,"state resolution claim id invalid"
        counts[confidence]+=1
        if confidence=="unknown":
            any_unknown=True
            if isinstance(claim_id,str) and claim_id.strip(): computed.append(claim_id.strip())
    integrity_error=_contradiction_integrity(claims,state_resolution)
    if integrity_error: return None,integrity_error
    preserved=dict(state_resolution)
    if status=="BLOCKED": return preserved,"state resolution blocked"
    if state_resolution.get("state_confidence_summary")!=counts: return None,"state resolution confidence summary inconsistent"
    expected_weakest=min((c["state_confidence"] for c in claims),key=lambda v:STATE_CONFIDENCE[v],default="unknown")
    if weakest!=expected_weakest: return None,"state resolution weakest confidence inconsistent"
    if sorted(unresolved)!=sorted(computed): return None,"state resolution unresolved claims inconsistent"
    if status!=("NEEDS_EVIDENCE" if any_unknown else "RESOLVED"): return None,"state resolution status inconsistent"
    return preserved,None

def compile_plan(intent:str,objective:str,project:str|None,constraints:list[str],ambiguity:list[str],state_resolution:dict|None=None)->dict:
    annotations=sorted({a.strip() for a in ambiguity if a.strip() in NON_MATERIAL_GATING_ANNOTATIONS})
    material=[a.strip() for a in ambiguity if a.strip() and a.strip() not in NON_MATERIAL_GATING_ANNOTATIONS]
    if not project: material.append("project unresolved")
    if not objective.strip(): material.append("objective unresolved")
    state_summary=None
    if state_resolution is not None:
        state_summary,state_error=_state_resolution_summary(state_resolution)
        if state_error: material.append(state_error)
        elif state_summary is not None and state_summary["status"]=="NEEDS_EVIDENCE":
            unresolved=state_summary["unresolved_claim_ids"]
            material.append("state claims unresolved: "+", ".join(sorted(unresolved)) if unresolved else "state resolution needs evidence")
    if material:
        return {"protocol":"DEVOS-GOAL-PLAN-v1","objective":objective or None,"project":project,"steps":[],"dependencies":[],"constraints":constraints,"assumptions":[],"ambiguity":sorted(set(material)),"gating_annotations":annotations,"authority_requirements":[],"verification_requirements":[],"state_resolution":state_summary,"decision":"CLARIFY","authorization":"UNCHANGED","authority":"UNCHANGED","execution":"NONE"}
    phrases=[p.strip() for p in re.split(r"\b(?:then|and then|after that|phir)\b|;",objective,flags=re.I) if p.strip()] or [objective.strip()]
    phrases=expand_read_before_write(phrases); steps=[]; authority_requirements=[]; verification_requirements=[]; dependencies=[]
    for i,phrase in enumerate(phrases,1):
        sid=f"S{i}"; deps=[f"S{i-1}"] if i>1 else []; impact=classify(phrase); requires_auth=impact in {"HIGH_IMPACT_MUTATION","SECURITY_SENSITIVE","PRODUCTION_OR_DESTRUCTIVE"}
        verification="fresh evidence of stated outcome" if impact=="READ_ONLY" else "fresh applicable test/check plus observed resulting state"
        step={"id":sid,"objective":phrase,"depends_on":deps,"expected_evidence":["repository/source/runtime evidence appropriate to the step"],"impact":impact,"authorization_required":requires_auth,"verification":verification,"stop_or_escalate_if":"material ambiguity, missing capability, missing authorization, failed verification, or repository state conflict"}; steps.append(step)
        for dep in deps: dependencies.append({"from":dep,"to":sid})
        if requires_auth: authority_requirements.append({"step":sid,"requirement":"independent authorization/Security Gate check"})
        verification_requirements.append({"step":sid,"requirement":verification})
    conflict=_negative_constraint_conflict(steps,constraints)
    common={"protocol":"DEVOS-GOAL-PLAN-v1","objective":objective,"project":project,"steps":steps,"dependencies":dependencies,"constraints":constraints,"assumptions":[],"ambiguity":[],"gating_annotations":annotations,"authority_requirements":authority_requirements,"verification_requirements":verification_requirements,"state_resolution":state_summary,"authorization":"UNCHANGED","authority":"UNCHANGED","execution":"NONE"}
    if conflict: return common|{"decision":"BLOCKED","blockers":[conflict]}
    return common|{"intent":intent,"decision":"PLANNED"}

def main()->None:
    p=argparse.ArgumentParser(); p.add_argument("--intent",default="INVESTIGATE"); p.add_argument("--objective",required=True); p.add_argument("--project"); p.add_argument("--constraints",default="[]",help="JSON list"); p.add_argument("--ambiguity",default="[]",help="JSON list"); args=p.parse_args()
    print(json.dumps(compile_plan(args.intent,args.objective,args.project,json.loads(args.constraints),json.loads(args.ambiguity)),indent=2,sort_keys=True))
if __name__=="__main__": main()
