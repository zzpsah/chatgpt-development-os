#!/usr/bin/env python3
from pathlib import Path

root = Path(__file__).resolve().parents[1]
contract = (root / "core" / "human-language-execution-engine.md").read_text(encoding="utf-8")
interpreter = (root / "tools" / "human-language-interpreter.py").read_text(encoding="utf-8")
required_contract = [
    "Human Language Execution Engine v2",
    "Contextual ellipsis and referents",
    "Explicit constraints",
    "Confidence and ambiguity",
    "authorization: UNCHANGED",
    "execution: NONE",
]
for token in required_contract:
    assert token in contract, token
for token in ["DEVOS-HUMAN-LANGUAGE-v2", '"CLARIFY"', '"ROUTE"', '"authorization": "UNCHANGED"', '"execution": "NONE"']:
    assert token in interpreter, token
print("human language v2 contract verified")
