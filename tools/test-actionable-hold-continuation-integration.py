#!/usr/bin/env python3
from pathlib import Path
import importlib.util
import sys

MODULE = Path(__file__).with_name("devos-continuation-path.py")
spec = importlib.util.spec_from_file_location("devos_continuation_path", MODULE)
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)

PROJECT = "zzpsah/chatgpt-development-os"
WORKFLOW = "PR23-MERGE"
TARGET = "PR#23->main"
HEAD = "head-a"


def approval(**overrides):
    data = {
        "project": PROJECT,
        "workflow": WORKFLOW,
        "capabilities": ["pr.merge"],
        "targets": [TARGET],
        "impact_ceiling": "HIGH",
        "repository_head": HEAD,
        "security_gate": "PASS",
        "approval_id": "APR-23",
    }
    data.update(overrides)
    return data


def payload(**overrides):
    data = {
        "phrase": "continue",
        "context": {
            "project": PROJECT,
            "workflow": WORKFLOW,
            "active_objective": "merge PR #23 into main",
        },
        "current_repository_head": HEAD,
        "completed_steps": ["S1"],
        "capabilities": {"S2": "AVAILABLE"},
        "security_gate_by_step": {"S2": "PASS"},
        "step_context_by_step": {
            "S2": {"capability": "pr.merge", "target": TARGET},
        },
        "scoped_approval": approval(),
        "events": [],
        "failures": [],
        "evidence": [],
    }
    data.update(overrides)
    return data


def assert_actionable_hold(result, expected_reason=None):
    assert result["status"] == "HOLD", result
    hold = result["hold"]
    required = {
        "status",
        "reason",
        "next_action",
        "consequence",
        "impact",
        "required_approval_or_evidence",
        "options",
        "natural_language_examples",
    }
    assert required.issubset(hold), hold
    assert hold["reason"].strip()
    assert hold["next_action"].strip()
    assert hold["consequence"].strip()
    assert hold["required_approval_or_evidence"]
    assert hold["options"]
    assert hold["natural_language_examples"]
    assert hold["authority"] == "UNCHANGED"
    assert hold["authorization"] == "UNCHANGED"
    assert hold["execution"] == "NONE"
    assert hold["mutation"] == "NONE"
    if expected_reason:
        assert expected_reason in hold["validation_reasons"], hold


def main():
    # 1. continue + valid scoped approval -> real P17/controller continuation.
    result = mod.evaluate(payload())
    assert result["status"] == "CONTINUE", result
    assert result["approval_reuse"] == "SCOPED_APPROVAL_REUSED"
    assert result["p15"]["decision"] == "INTERPRETED"
    assert "RESUME_WORK" in result["p15"]["intents"]
    assert result["p17"]["status"] == "READY"
    assert result["controller"]["decision"] == "EXECUTION_CANDIDATE"
    assert result["execution"] == "NONE"
    assert result["mutation"] == "NONE"

    # 2. continue + missing approval -> actionable HOLD.
    missing = mod.evaluate(payload(scoped_approval=None))
    assert_actionable_hold(missing, "SCOPED_APPROVAL_MISSING_OR_INVALID")
    assert missing["hold"]["status"] == "NEEDS_APPROVAL"

    # 3. stale repo HEAD invalidates approval.
    stale = mod.evaluate(payload(scoped_approval=approval(repository_head="old-head")))
    assert_actionable_hold(stale, "REPOSITORY_HEAD_CHANGED")

    # 4a. target change requires fresh approval.
    target_changed = payload()
    target_changed["step_context_by_step"] = {
        "S2": {"capability": "pr.merge", "target": "PR#24->main"}
    }
    changed = mod.evaluate(target_changed)
    assert_actionable_hold(changed, "TARGET_OUTSIDE_APPROVAL")

    # 4b. capability change requires fresh approval.
    capability_changed = payload()
    capability_changed["step_context_by_step"] = {
        "S2": {"capability": "repo.delete", "target": TARGET}
    }
    changed = mod.evaluate(capability_changed)
    assert_actionable_hold(changed, "CAPABILITY_OUTSIDE_APPROVAL")

    # 5. impact escalation requires fresh approval.
    escalated = mod.evaluate(payload(scoped_approval=approval(impact_ceiling="LOW")))
    assert_actionable_hold(escalated, "IMPACT_EXCEEDS_APPROVAL_CEILING")

    # 6. Security Gate state change requires fresh evaluation/approval.
    security = payload()
    security["security_gate_by_step"] = {"S2": "UNKNOWN"}
    changed = mod.evaluate(security)
    assert_actionable_hold(changed, "SECURITY_GATE_STATE_CHANGED")

    # 7. HOLD carries human-actionable fields and natural-language examples.
    hold = missing["hold"]
    assert hold["next"]["capability"] == "pr.merge"
    assert hold["next"]["target"] == TARGET
    assert hold["impact"] == "HIGH"
    assert any("approve" in example for example in hold["natural_language_examples"])
    assert "hold" in hold["options"]

    print("PASS: actionable hold integrated P15 -> P16 -> P17 -> controller continuation path")


if __name__ == "__main__":
    main()
