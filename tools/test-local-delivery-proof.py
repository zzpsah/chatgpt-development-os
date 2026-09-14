#!/usr/bin/env python3
"""Regression corpus for the disposable local automated-delivery proof."""
from __future__ import annotations

import importlib.util
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("local_delivery", ROOT / "tools" / "local-delivery-proof.py")
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

with tempfile.TemporaryDirectory(prefix="devos-local-delivery-") as temporary:
    repo = Path(temporary) / "disposable-project"
    unprepared = mod.run(repo, "लोकल डिलीवरी मार्कर अपडेट करो", None)
    assert unprepared["status"] == "HOLD" and unprepared["reason"] == "DISPOSABLE_REPOSITORY_NOT_PREPARED", unprepared

with tempfile.TemporaryDirectory(prefix="devos-local-delivery-") as temporary:
    repo = Path(temporary) / "disposable-project"
    prepared = mod.prepare(repo)
    marker = repo / mod.TARGET
    before = marker.read_text(encoding="utf-8")
    invalid = mod.run(repo, "लोकल डिलीवरी मार्कर अपडेट करो", {"protocol": mod.APPROVAL_PROTOCOL})
    assert invalid["status"] == "HOLD" and invalid["reason"] == "SCOPED_APPROVAL_PROJECT_MISMATCH", invalid
    assert marker.read_text(encoding="utf-8") == before, invalid

with tempfile.TemporaryDirectory(prefix="devos-local-delivery-") as temporary:
    repo = Path(temporary) / "disposable-project"
    prepared = mod.prepare(repo)
    assert prepared["status"] == "PREPARED", prepared
    head = prepared["repository_head"]
    project = str(repo.resolve())
    marker = repo / mod.TARGET
    before = mod.digest(marker)
    p15 = mod.P15.interpret({"phrase": "लोकल डिलीवरी मार्कर अपडेट करो", "context": {"project": project}})
    assert p15["decision"] == "INTERPRETED" and "FEATURE_CHANGE" in p15["intents"], p15
    plan = mod.P16.compile_plan(p15["intents"][0], p15["objective"], project, p15["constraints"], p15["ambiguity"])
    assert plan["decision"] == "PLANNED" and len(plan["steps"]) == 2, plan
    s1, s2 = plan["steps"]
    approval = mod.approval_for(project=project, repository_head=head, step_id=s2["id"])
    assert mod.validate_approval(approval, project=project, repository_head=head, step_id=s2["id"]) is None
    assert mod.validate_approval(approval | {"target": "other.txt"}, project=project, repository_head=head, step_id=s2["id"]) == "SCOPED_APPROVAL_TARGET_MISMATCH"

    result = mod.run(repo, "लोकल डिलीवरी मार्कर अपडेट करो", approval)
    assert result["status"] == "VERIFIED", result
    assert mod.digest(marker) != before
    recovered = mod.verify_evidence(Path(result["evidence_path"]))
    assert recovered["status"] == "VERIFIED", recovered

print("PASS: local disposable delivery proof enforces P15/P16/P17, scoped approval, readback, test, and fresh evidence recovery")
