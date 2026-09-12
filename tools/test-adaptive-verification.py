#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("adaptive_verification", ROOT / "tools" / "adaptive-verification.py")
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
sys.modules["adaptive_verification"] = module
spec.loader.exec_module(module)


def test_low_risk_code_requires_static_unit() -> None:
    out = module.evaluate({
        "change": {"paths": ["src/app.py"], "risk": "LOW"},
        "evidence": [
            {"level": "STATIC", "result": "PASS", "observed": True, "fresh": True},
            {"level": "UNIT", "result": "PASS", "observed": True, "fresh": True},
        ],
    })
    assert out["verification"]["status"] == "VERIFIED"
    assert out["verification"]["required_levels"] == ["STATIC", "UNIT"]
    assert out["healing"]["decision"] == "NO_HEAL"
    assert out["authority"] == "UNCHANGED" and out["execution"] == "NONE"


def test_auth_change_escalates_verification() -> None:
    out = module.evaluate({
        "change": {"paths": ["src/auth.py"], "risk": "HIGH", "boundaries": ["AUTH"]},
        "evidence": [
            {"level": "STATIC", "result": "PASS"},
            {"level": "UNIT", "result": "PASS"},
        ],
    })
    assert out["verification"]["status"] == "PARTIAL"
    assert out["verification"]["required_levels"] == ["STATIC", "UNIT", "INTEGRATION", "SECURITY"]
    assert out["verification"]["missing_levels"] == ["INTEGRATION", "SECURITY"]


def test_failure_allows_only_derived_context_auto_heal() -> None:
    evidence = [{"level": "STATIC", "result": "FAIL", "observed": True, "fresh": True}]
    safe = module.evaluate({
        "change": {"paths": [".ai/STATE-INDEX.md"], "risk": "LOW"},
        "evidence": evidence,
        "repair": {"kind": "DERIVED_CONTEXT", "target": ".ai/STATE-INDEX.md", "attempts": 0, "max_attempts": 2},
    })
    assert safe["verification"]["status"] == "FAILED"
    assert safe["healing"]["decision"] == "AUTO_ELIGIBLE"
    assert safe["healing"]["allowed_tool"] == "tools/self-heal-derived-context.py"
    assert safe["healing"]["execution"] == "NONE"

    semantic = module.evaluate({
        "change": {"paths": [".ai/CURRENT-STATE.md"], "risk": "LOW"},
        "evidence": evidence,
        "repair": {"kind": "DERIVED_CONTEXT", "target": ".ai/CURRENT-STATE.md"},
    })
    assert semantic["healing"]["decision"] == "PROPOSE_ONLY"

    code = module.evaluate({
        "change": {"paths": ["src/app.py"], "risk": "MEDIUM"},
        "evidence": evidence,
        "repair": {"kind": "CODE", "target": "src/app.py"},
    })
    assert code["healing"]["decision"] == "PROPOSE_ONLY"


def test_budget_and_stale_evidence() -> None:
    budget = module.evaluate({
        "change": {"paths": [".ai/CHANGELOG.md"]},
        "evidence": [{"level": "STATIC", "result": "FAIL"}],
        "repair": {"kind": "DERIVED_CONTEXT", "target": ".ai/CHANGELOG.md", "attempts": 2, "max_attempts": 2},
    })
    assert budget["healing"]["decision"] == "HOLD"
    assert budget["healing"]["reason"] == "REPAIR_BUDGET_EXHAUSTED"

    stale = module.evaluate({
        "change": {"paths": ["src/app.py"]},
        "evidence": [
            {"level": "STATIC", "result": "PASS", "fresh": False},
            {"level": "UNIT", "result": "PASS", "fresh": True},
        ],
    })
    assert stale["verification"]["status"] == "PARTIAL"
    assert stale["verification"]["missing_levels"] == ["STATIC"]


def main() -> None:
    test_low_risk_code_requires_static_unit()
    test_auth_change_escalates_verification()
    test_failure_allows_only_derived_context_auto_heal()
    test_budget_and_stale_evidence()
    print("P14 adaptive verification/self-healing policy: PASS")


if __name__ == "__main__":
    main()
