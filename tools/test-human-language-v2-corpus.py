#!/usr/bin/env python3
from __future__ import annotations
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("hli", ROOT / "tools" / "human-language-interpreter.py")
assert spec and spec.loader
hli = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hli)
rows = json.loads((ROOT / "tools" / "human-language-v2-corpus.json").read_text(encoding="utf-8"))
ctx = {"last_intent": "RESUME_WORK", "last_objective": "Continue current verified milestone", "project": "DEVOS"}
for row in rows:
    payload = {"utterance": row["utterance"]}
    if row.get("needs_context"):
        payload["context"] = ctx
    result = hli.interpret(payload)
    if row.get("needs_context"):
        assert result["decision"] == "ROUTE", (row, result)
    else:
        assert result["primary_intent"] == row["intent"], (row, result)
    if row.get("constraint"):
        assert row["constraint"] in result["constraints"], (row, result)
    assert result["authorization"] == "UNCHANGED"
    assert result["execution"] == "NONE"
print(f"human language v2 corpus passed: {len(rows)} cases")
