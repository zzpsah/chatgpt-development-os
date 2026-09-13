#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("hli", ROOT / "tools" / "human-language-interpreter.py")
assert spec and spec.loader
hli = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hli)


def check(payload, **expected):
    result = hli.interpret(payload)
    for key, value in expected.items():
        assert result[key] == value, (payload, key, result[key], value)
    assert result["authorization"] == "UNCHANGED"
    assert result["execution"] == "NONE"


def main():
    check({"utterance": "fix this error"}, primary_intent="BUG_FIX", decision="ROUTE")
    check({"utterance": "security dekh"}, primary_intent="SECURITY_REVIEW", decision="ROUTE")
    check({"utterance": "isko aur acha kro"}, primary_intent="QUALITY_IMPROVEMENT", decision="ROUTE")
    check({"utterance": "deploy mat karna, fix error"}, primary_intent="BUG_FIX", constraints=["NO_DEPLOY"], decision="ROUTE")
    ctx = {"last_intent": "BUG_FIX", "last_objective": "Fix registration form validation", "project": "umv-portal"}
    check({"utterance": "kr do", "context": ctx}, primary_intent="BUG_FIX", objective="Fix registration form validation", context_inherited=True, confidence="HIGH", decision="ROUTE")
    check({"utterance": "wahi continue", "context": ctx}, primary_intent="BUG_FIX", context_inherited=True, decision="ROUTE")
    check({"utterance": "continue"}, confidence="LOW", decision="CLARIFY")
    check({"utterance": "isko kro"}, confidence="LOW", decision="CLARIFY")
    check({"utterance": ""}, confidence="LOW", decision="CLARIFY")
    print("human language interpreter v2 tests passed")


if __name__ == "__main__":
    main()
