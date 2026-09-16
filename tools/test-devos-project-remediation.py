#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "tools" / "devos-project-remediation.py"
spec = importlib.util.spec_from_file_location("devos_project_remediation", MODULE)
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def base_payload():
    return {
        "protocol": "DEVOS-PROJECT-FLEET-WATCH-v1",
        "fleet_status": "ATTENTION",
        "repositories": [
            {
                "repository": "zzpsah/managed",
                "fleet_state": "MANAGED",
                "management_state": "MANAGED",
                "missing_files": [],
            },
            {
                "repository": "zzpsah/new-project",
                "fleet_state": "ONBOARDING_REQUIRED",
                "management_state": "UNMANAGED",
                "reason": "DevOS manifest is absent",
                "missing_files": [".ai/manifest.yaml", "AGENTS.md"],
            },
            {
                "repository": "zzpsah/partial",
                "fleet_state": "ONBOARDING_REQUIRED",
                "management_state": "PARTIAL",
                "reason": "DevOS context is incomplete",
                "missing_files": [".ai/TASKS.md"],
            },
        ],
        "drift": None,
    }


def main():
    report = mod.plan(base_payload())
    assert report["status"] == "READY", report
    assert report["remediation_required"] is True
    assert report["action_count"] == 2
    assert [x["action"] for x in report["actions"]] == ["COMPLETE_ONBOARDING", "ONBOARD_PROJECT"]
    assert all(x["requires_explicit_authorization"] for x in report["actions"])
    assert all(x["safe_apply"] is False for x in report["actions"])
    assert report["mutation"] == "NONE"
    assert report["authorization"] == "UNCHANGED"
    assert report["production_ready"] is False

    regression = base_payload()
    regression["repositories"][0]["fleet_state"] = "ONBOARDING_REQUIRED"
    regression["repositories"][0]["management_state"] = "PARTIAL"
    regression["drift"] = {"management_regressions": ["zzpsah/managed"]}
    reg = mod.plan(regression)
    assert reg["actions"][0]["repository"] == "zzpsah/managed"
    assert reg["actions"][0]["action"] == "RESTORE_MANAGED_STATE"
    assert reg["actions"][0]["priority"] == 100

    clean = base_payload()
    clean["repositories"] = clean["repositories"][:1]
    clean["fleet_status"] = "HEALTHY"
    clean_report = mod.plan(clean)
    assert clean_report["remediation_required"] is False
    assert clean_report["actions"] == []
    assert clean_report["next_action"] == "NONE"

    duplicate = base_payload()
    duplicate["repositories"].append(dict(duplicate["repositories"][0]))
    assert mod.plan(duplicate)["status"] == "BLOCKED"

    bad_protocol = base_payload(); bad_protocol["protocol"] = "wrong"
    assert mod.plan(bad_protocol)["status"] == "BLOCKED"

    bad_state = base_payload(); bad_state["repositories"][0]["fleet_state"] = "MAGIC"
    assert mod.plan(bad_state)["status"] == "BLOCKED"

    unknown_regression = base_payload(); unknown_regression["drift"] = {"management_regressions": ["zzpsah/missing"]}
    assert mod.plan(unknown_regression)["status"] == "BLOCKED"

    first = mod.plan(base_payload())
    second = mod.plan(base_payload())
    assert first == second, (first, second)

    print("PASS: Project Remediation Planner v1 is deterministic, priority-ordered, fail-closed, and mutation-neutral")


if __name__ == "__main__":
    main()
