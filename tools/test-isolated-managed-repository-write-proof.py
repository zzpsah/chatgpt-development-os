#!/usr/bin/env python3
from __future__ import annotations
import importlib.util, json, subprocess, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('proof',ROOT/'tools'/'isolated-managed-repository-write-proof.py'); assert spec and spec.loader
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
def main():
 with tempfile.TemporaryDirectory() as d:
  root=Path(d); repo=root/'isolated'; prepared=m.prepare(repo); assert prepared['status']=='PREPARED',prepared
  phrase='Inspect current repository state then update managed marker'
  pre=m.PREFLIGHT.preflight(repo,phrase,[m.MARKER],repo.name); assert pre['status']=='HOLD' and 'READ_ONLY_PREFLIGHT_COMPLETE' in pre['reasons'],pre
  before=(repo/m.MARKER).read_text(encoding='utf-8'); blocked=m.execute(repo,phrase,None,root/'blocked.json'); assert blocked['reason']=='EXACT_SCOPED_APPROVAL_INVALID',blocked; assert (repo/m.MARKER).read_text(encoding='utf-8')==before
  evidence=root/'evidence'/'packet.json'; verified=m.execute(repo,phrase,m.approval_for(pre),evidence); assert verified['status']=='VERIFIED',verified; assert (repo/m.MARKER).read_text(encoding='utf-8')=='after\n'; assert subprocess.check_output(['git','status','--porcelain'],cwd=repo,text=True).strip()=='M managed-marker.txt'; assert json.loads(evidence.read_text())['handoff_id']==verified['handoff_id']
  bad=m.prepare(repo); assert bad['reason']=='ISOLATED_REPOSITORY_MUST_BE_NEW',bad
 print('PASS: isolated managed write proof requires preflight and exact approval, verifies one file update, and never commits or pushes')
if __name__=='__main__':main()
