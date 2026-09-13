#!/usr/bin/env python3
from __future__ import annotations
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("hli", ROOT / "tools" / "human-language-interpreter.py")
assert spec and spec.loader
hli = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hli)

cases = [
    {"utterance": "deploy kar do"},
    {"utterance": "delete kar do"},
    {"utterance": "merge kar do"},
    {"utterance": "production me kar do"},
    {"utterance": "kr do", "context": {"last_intent": "FEATURE_CHANGE", "last_objective": "Change config"}},
]
for case in cases:
    result = hli.interpret(case)
    assert result["authorization"] == "UNCHANGED", result
    assert result["execution"] == "NONE", result
print("human language v2 safety invariants passed")
