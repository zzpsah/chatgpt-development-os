#!/usr/bin/env python3
import importlib.util
from pathlib import Path

MODULE = Path(__file__).with_name("semantic-goal-to-plan.py")
spec = importlib.util.spec_from_file_location("semantic_goal_to_plan", MODULE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def check(cond, msg):
    if not cond:
        raise AssertionError(msg)


def main():
    p = mod.compile_plan("BUG_FIX", "inspect error then fix code", "DEVOS", [], [])
    check(p["decision"] == "PLANNED", "single/multi-step plan should compile")
    check(len(p["steps"]) == 2, "explicit read-before-write plan should remain two steps")
    check(p["steps"][1]["depends_on"] == ["S1"], "dependency edge missing")
    check(p["execution"] == "NONE" and p["authority"] == "UNCHANGED", "planning must not execute or grant authority")

    q = mod.compile_plan("FEATURE_CHANGE", "update docs", None, [], [])
    check(q["decision"] == "CLARIFY", "missing project must clarify")

    r = mod.compile_plan("FEATURE_CHANGE", "update code then deploy production", "DEVOS", ["DO_NOT_DEPLOY"], [])
    check(r["decision"] == "BLOCKED", "negative constraint must block conflicting step")

    s = mod.compile_plan("SECURITY_REVIEW", "check security", "DEVOS", [], [])
    check(s["steps"][0]["impact"] == "SECURITY_SENSITIVE", "security classification missing")
    check(s["steps"][0]["authorization_required"] is True, "security-sensitive plan must require independent gate")

    t = mod.compile_plan("VALIDATION", "inspect repository", "DEVOS", [], [])
    check(t["steps"][0]["impact"] == "READ_ONLY", "read-only planning classification incorrect")
    check(bool(t["verification_requirements"]), "verification obligations must be explicit")

    u = mod.compile_plan("FEATURE_CHANGE", "update config then run tests", "DEVOS", [], ["which config?"])
    check(u["decision"] == "CLARIFY" and not u["steps"], "material ambiguity must not become guessed work")

    v = mod.compile_plan("FEATURE_CHANGE", "update docs", "DEVOS", [], [])
    check(len(v["steps"]) == 2, "mutation should gain an automatic read-before-write evidence step")
    check(v["steps"][0]["impact"] == "READ_ONLY", "automatic precondition step must be read-only")
    check(v["steps"][1]["impact"] == "LOW_IMPACT_MUTATION", "original mutation must retain mutation classification")
    check(v["steps"][1]["depends_on"] == ["S1"], "mutation must depend on read-before-write inspection")

    print("PASS: P16 Semantic Goal-to-Plan Compiler regression corpus")


if __name__ == "__main__":
    main()
