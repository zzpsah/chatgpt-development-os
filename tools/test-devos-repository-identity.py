#!/usr/bin/env python3
"""Regression proof for DevOS repository identity resolution."""
from pathlib import Path
import importlib.util
import json

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "devos-repository-identity.py"

spec = importlib.util.spec_from_file_location("devos_repository_identity", TOOL)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

valid = json.loads((ROOT / ".ai" / "repository-identity.json").read_text(encoding="utf-8"))
module.validate(valid)

wrong = dict(valid)
wrong["canonical_repository"] = "SamyPesse/devos"
try:
    module.validate(wrong)
except ValueError:
    pass
else:
    raise AssertionError("unrelated similarly named repository must fail identity validation")

missing = dict(valid)
missing.pop("owner")
try:
    module.validate(missing)
except ValueError:
    pass
else:
    raise AssertionError("incomplete identity must fail closed")

print("DevOS repository identity regression test: PASS")
print("Canonical identity: PASS")
print("Similar-name repository rejection: PASS")
print("Incomplete identity fail-closed guard: PASS")
