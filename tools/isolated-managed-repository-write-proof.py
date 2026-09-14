#!/usr/bin/env python3
"""One-file write proof in a newly created isolated local Git repository.

This is intentionally not a general managed-repository executor. It consumes the
read-only preflight boundary, requires an exact scoped approval, and changes
only a fixture marker in a freshly prepared disposable repository.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = "DEVOS-ISOLATED-MANAGED-WRITE-PROOF-v1"
APPROVAL_PROTOCOL = "DEVOS-ISOLATED-MANAGED-WRITE-APPROVAL-v1"
MARKER = "managed-marker.txt"
FIXTURE = ".devos-isolated-managed-fixture"


def load(name: str, filename: str):
    spec=importlib.util.spec_from_file_location(name, ROOT/'tools'/filename); assert spec and spec.loader
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module); return module

PREFLIGHT=load('isolated_preflight','managed-repository-preflight.py')
P15=load('isolated_p15','human-language-interpreter.py')
P16=load('isolated_p16','semantic-goal-to-plan.py')
P17=load('isolated_p17','step-readiness-orchestrator.py')
RUNTIME=load('isolated_runtime','agent-runtime-handoff.py')


def sha(data: bytes) -> str: return hashlib.sha256(data).hexdigest()
def git(repo: Path,*args:str)->str:
    r=subprocess.run(['git',*args],cwd=repo,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False)
    if r.returncode: raise RuntimeError(r.stderr.strip())
    return r.stdout.strip()
def hold(reason:str,**extra:Any)->dict[str,Any]:
    return {'protocol':PROTOCOL,'status':'HOLD','reason':reason,'authority':'UNCHANGED','authorization':'UNCHANGED','execution':'NONE','mutation':'NONE','production_ready':False,**extra}


def prepare(repo:Path)->dict[str,Any]:
    repo=repo.resolve()
    if repo.exists(): return hold('ISOLATED_REPOSITORY_MUST_BE_NEW')
    repo.mkdir(parents=True); git(repo,'init','-q'); git(repo,'config','user.email','devos-isolated@example.invalid'); git(repo,'config','user.name','DevOS Isolated Proof')
    (repo/FIXTURE).write_text('isolated-managed-write-proof-v1\n',encoding='utf-8')
    (repo/MARKER).write_text('before\n',encoding='utf-8')
    (repo/'verify_marker.py').write_text("from pathlib import Path\nassert Path('managed-marker.txt').read_text(encoding='utf-8') == 'after\\n'\n",encoding='utf-8')
    git(repo,'add',FIXTURE,MARKER,'verify_marker.py'); git(repo,'commit','-qm','isolated managed fixture')
    return {'protocol':PROTOCOL,'status':'PREPARED','repository':str(repo),'repository_head':git(repo,'rev-parse','HEAD'),'target':MARKER,'authority':'UNCHANGED','authorization':'UNCHANGED','execution':'NONE','mutation':'NONE','production_ready':False}


def approval_for(preflight:dict[str,Any])->dict[str,Any]:
    req=preflight['approval_request']
    return {'protocol':APPROVAL_PROTOCOL,'approval_id':'ISOLATED-MANAGED-APPROVAL-1','approval_request_id':req['approval_request_id'],'project':req['project'],'workflow':req['workflow'],'repository_head':req['repository_head'],'step_id':req['step_id'],'capability':req['capability'],'targets':req['targets'],'impact_ceiling':'LOW'}


def execute(repo:Path,phrase:str,approval:dict[str,Any]|None,evidence_output:Path)->dict[str,Any]:
    repo=repo.resolve()
    if not (repo/FIXTURE).is_file() or (repo/FIXTURE).read_text(encoding='utf-8')!='isolated-managed-write-proof-v1\n': return hold('ISOLATED_FIXTURE_NOT_RECOGNIZED')
    if not (repo/MARKER).is_file() or not (repo/'verify_marker.py').is_file(): return hold('ISOLATED_FIXTURE_INCOMPLETE')
    pre=PREFLIGHT.preflight(repo,phrase,[MARKER],repo.name)
    if pre.get('status')!='HOLD' or 'READ_ONLY_PREFLIGHT_COMPLETE' not in pre.get('reasons',[]): return hold('PREFLIGHT_NOT_COMPLETE',preflight=pre)
    req=pre['approval_request']; head=git(repo,'rev-parse','HEAD')
    expected=approval_for(pre)
    if not isinstance(approval,dict) or any(approval.get(k)!=v for k,v in expected.items()): return hold('EXACT_SCOPED_APPROVAL_INVALID',preflight=pre)
    if head!=req['repository_head']: return hold('REPOSITORY_HEAD_CHANGED_AFTER_PREFLIGHT',preflight=pre)

    p15=P15.interpret({'phrase':phrase,'context':{'project':repo.name}})
    plan=P16.compile_plan(p15['intents'][0],p15['objective'],repo.name,p15.get('constraints',[]),p15.get('ambiguity',[]))
    read,change=plan['steps'][0],plan['steps'][-1]; change['authorization_required']=True; change['expected_evidence']=['approved bounded diff','passing configured tests','fresh final readback']; change['verification']='run configured isolated test and read back marker'
    ready=P17.evaluate({'plan':plan,'step_id':change['id'],'compiled_repository_head':head,'current_repository_head':head,'completed_steps':[read['id']],'capabilities':{read['id']:'AVAILABLE',change['id']:'AVAILABLE'},'authorization_by_step':{change['id']:'ALREADY_GRANTED'},'security_gate_by_step':{}})
    if ready.get('status')!='READY': return hold('P17_APPROVED_CHANGE_NOT_READY',preflight=pre,p17=ready)
    runtime_input={'protocol':RUNTIME.INPUT_PROTOCOL,'project':repo.name,'workflow':req['workflow'],'readiness':ready,'approval':{'approval_id':approval['approval_id'],'project':repo.name,'workflow':req['workflow'],'capabilities':['filesystem.read','filesystem.write_scoped','git.inspect','verification.run'],'targets':[MARKER],'impact_ceiling':'LOW','repository_head':head,'security_gate':None},'runtime':{'protocol':RUNTIME.PROFILE_PROTOCOL,'runtime_id':'isolated-local-proof','adapter_version':'1.0','capabilities':{'filesystem.read':'AVAILABLE','filesystem.write_scoped':'AVAILABLE','git.inspect':'AVAILABLE','verification.run':'AVAILABLE'}},'work_unit':{'repository_root':str(repo),'repository_head':head,'allowed_paths':[MARKER],'allowed_operations':['file.update'],'constraints':['new isolated local Git fixture only','no commit push provider deployment credentials database permissions or destructive operation']}}
    handoff=RUNTIME.compile_handoff(runtime_input)
    if handoff.get('status')!='HANDOFF_READY': return hold('RUNTIME_HANDOFF_NOT_READY',handoff=handoff)
    before=sha((repo/MARKER).read_bytes()); (repo/MARKER).write_text('after\n',encoding='utf-8')
    test=subprocess.run([sys.executable,'verify_marker.py'],cwd=repo,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False)
    diff=git(repo,'diff','--',MARKER); after=sha((repo/MARKER).read_bytes())
    result={'protocol':RUNTIME.RESULT_PROTOCOL,'handoff_id':handoff['handoff_id'],'runtime_id':'isolated-local-proof','status':'COMPLETED','repository_head_before':head,'touched_files':[MARKER],'diff':{'status':'OBSERVED','sha256':sha(diff.encode()),'changed_paths':[MARKER]},'tests':[{'name':'verify_marker.py','status':'PASS' if test.returncode==0 else 'FAIL','exit_code':test.returncode,'output_sha256':sha((test.stdout+test.stderr).encode())}],'readback':[{'path':MARKER,'status':'PRESENT','sha256':after}],'prohibited_operations_used':[]}
    verdict=RUNTIME.verify_result(handoff,result)
    if verdict.get('status')!='VERIFIED_RUNTIME_RESULT' or before==after: return hold('RUNTIME_EVIDENCE_NOT_VERIFIED',verdict=verdict)
    evidence={'protocol':PROTOCOL,'status':'VERIFIED','repository':str(repo),'repository_head_before':head,'target':MARKER,'preflight_evidence_id':pre['evidence_id'],'approval_id':approval['approval_id'],'handoff_id':handoff['handoff_id'],'before_sha256':before,'after_sha256':after,'diff_sha256':result['diff']['sha256'],'runtime_verdict':verdict,'limitations':['isolated newly created local Git fixture only','no commit or push','no provider, deployment, production, credential, database, permission, or destructive operation'] ,'authority':'UNCHANGED','authorization':'STEP_SCOPED_APPROVAL_VERIFIED','execution':'ISOLATED_LOCAL_FILE_UPDATE_COMPLETED','mutation':'ISOLATED_LOCAL_GIT_FIXTURE_ONLY','production_ready':False}
    if evidence_output.resolve()==repo or repo in evidence_output.resolve().parents: return hold('EVIDENCE_OUTPUT_MUST_BE_OUTSIDE_ISOLATED_REPOSITORY')
    evidence_output.parent.mkdir(parents=True,exist_ok=True); evidence_output.write_text(json.dumps(evidence,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    return evidence|{'evidence_path':str(evidence_output.resolve())}
