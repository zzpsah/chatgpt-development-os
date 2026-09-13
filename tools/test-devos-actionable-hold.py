#!/usr/bin/env python3
from pathlib import Path
import importlib.util
import sys

MODULE = Path(__file__).with_name("devos-actionable-hold.py")
spec = importlib.util.spec_from_file_location("devos_actionable_hold", MODULE)
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


def approval():
    return mod.Approval(
        project="zzpsah/demo",
        workflow="PR19-MERGE",
        capabilities=frozenset({"pr.merge", "ci.verify"}),
        targets=frozenset({"PR#19->main"}),
        impact_ceiling="HIGH",
        repository_head="abc123",
        security_gate="PASS",
        approval_id="APR-001",
    )


def main():
    a = approval()

    same = mod.NextStep("ci.verify", "PR#19->main", "LOW", "abc123", "PASS", "run post-merge checks")
    ok, reasons = mod.can_reuse_approval(a, same, project="zzpsah/demo", workflow="PR19-MERGE")
    assert ok and reasons == []
    assert mod.continuation_decision(a, same, project="zzpsah/demo", workflow="PR19-MERGE") == "CONTINUE_WITH_EXISTING_APPROVAL"

    merge = mod.NextStep("pr.merge", "PR#19->main", "HIGH", "abc123", "PASS", "merge PR #19 into main")
    assert mod.continuation_decision(a, merge, project="zzpsah/demo", workflow="PR19-MERGE") == "CONTINUE_WITH_EXISTING_APPROVAL"

    wrong_target = mod.NextStep("pr.merge", "PR#20->main", "HIGH", "abc123", "PASS", "merge PR #20 into main")
    ok, reasons = mod.can_reuse_approval(a, wrong_target, project="zzpsah/demo", workflow="PR19-MERGE")
    assert not ok and "TARGET_OUTSIDE_APPROVAL" in reasons

    higher = mod.NextStep("repo.delete", "PR#19->main", "DESTRUCTIVE", "abc123", "PASS", "delete repository")
    ok, reasons = mod.can_reuse_approval(a, higher, project="zzpsah/demo", workflow="PR19-MERGE")
    assert not ok and "CAPABILITY_OUTSIDE_APPROVAL" in reasons and "IMPACT_EXCEEDS_APPROVAL_CEILING" in reasons

    stale = mod.NextStep("pr.merge", "PR#19->main", "HIGH", "def456", "PASS", "merge after repository changed")
    ok, reasons = mod.can_reuse_approval(a, stale, project="zzpsah/demo", workflow="PR19-MERGE")
    assert not ok and "REPOSITORY_HEAD_CHANGED" in reasons
    assert mod.continuation_decision(a, stale, project="zzpsah/demo", workflow="PR19-MERGE") == "NEEDS_APPROVAL"

    security_changed = mod.NextStep("pr.merge", "PR#19->main", "HIGH", "abc123", "UNKNOWN", "merge without current security evidence")
    ok, reasons = mod.can_reuse_approval(a, security_changed, project="zzpsah/demo", workflow="PR19-MERGE")
    assert not ok and "SECURITY_GATE_STATE_CHANGED" in reasons

    other_project = mod.NextStep("ci.verify", "PR#19->main", "LOW", "abc123", "PASS", "same capability, other project")
    ok, reasons = mod.can_reuse_approval(a, other_project, project="other/repo", workflow="PR19-MERGE")
    assert not ok and "PROJECT_SCOPE_CHANGED" in reasons

    other_workflow = mod.NextStep("ci.verify", "PR#19->main", "LOW", "abc123", "PASS", "same target, other workflow")
    ok, reasons = mod.can_reuse_approval(a, other_workflow, project="zzpsah/demo", workflow="OTHER")
    assert not ok and "WORKFLOW_SCOPE_CHANGED" in reasons

    unauth = mod.continuation_decision(None, merge, project="zzpsah/demo", workflow="PR19-MERGE")
    assert unauth == "NEEDS_APPROVAL"

    hold = mod.actionable_hold(
        status="NEEDS_APPROVAL",
        reason="The next step is a high-impact remote mutation outside the current approval.",
        next_step=merge,
        required=["explicit approval for pr.merge on PR#19->main"],
        options=["merge it", "run checks first", "show the plan", "hold"],
    )
    assert hold["status"] == "NEEDS_APPROVAL"
    assert hold["next"]["capability"] == "pr.merge"
    assert hold["impact"] == "HIGH"
    assert hold["authority"] == "UNCHANGED"
    assert hold["execution"] == "NONE"
    assert hold["mutation"] == "NONE"

    summary = mod.full_approval_summary(a)
    assert summary["scope"]["workflow"] == "PR19-MERGE"
    assert "blanket permission" in summary["meaning"]

    print("PASS: actionable hold + scoped approval regression corpus")


if __name__ == "__main__":
    main()
