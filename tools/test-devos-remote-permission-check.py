#!/usr/bin/env python3
from pathlib import Path
import importlib.util
import sys

MODULE = Path(__file__).with_name("devos-remote-permission-check.py")
spec = importlib.util.spec_from_file_location("devos_remote_permission_check", MODULE)
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


def auth(**overrides):
    data = dict(provider="github", owner="zzpsah", repository="demo", resource="feature/a", capability="branch.create", workflow="W", project="demo", impact_ceiling="HIGH", freshness="h1", authorization_id="A1")
    data.update(overrides)
    return mod.Authorization(**data)


def op(**overrides):
    data = dict(provider="github", owner="zzpsah", repository="demo", resource="feature/a", capability="branch.create", workflow="W", project="demo", impact="LOW", freshness="h1")
    data.update(overrides)
    return mod.Operation(**data)


def main():
    status, reasons = mod.evaluate(auth(), op())
    assert status == "CONTINUE_WITH_EXISTING_APPROVAL" and reasons == []

    assert mod.evaluate(auth(), op(capability="branch.delete", impact="DESTRUCTIVE"))[0] == "NEEDS_APPROVAL"
    assert "CAPABILITY_SCOPE_CHANGED" in mod.evaluate(auth(), op(capability="branch.delete", impact="DESTRUCTIVE"))[1]
    assert "IMPACT_EXCEEDS_APPROVAL_CEILING" in mod.evaluate(auth(), op(capability="branch.delete", impact="DESTRUCTIVE"))[1]
    assert mod.evaluate(auth(), op(repository="other"))[0] == "NEEDS_APPROVAL"
    assert mod.evaluate(auth(), op(freshness="h2"))[0] == "NEEDS_APPROVAL"
    assert mod.evaluate(auth(), op(resource="main", capability="branch.update", impact="HIGH"))[0] == "NEEDS_APPROVAL"
    assert mod.evaluate(None, op())[0] == "NEEDS_APPROVAL"

    hold = mod.actionable_hold(op(capability="repository.delete", resource=None, impact="DESTRUCTIVE"), ["NO_APPROVAL"])
    assert hold["status"] == "NEEDS_APPROVAL"
    assert hold["impact"] == "DESTRUCTIVE"
    assert hold["authority"] == "UNCHANGED"
    assert hold["execution"] == "NONE"
    assert hold["mutation"] == "NONE"
    assert "approve this exact action" in hold["options"]
    assert "what_will_happen" in hold

    print("PASS: remote resource permission governance regression")


if __name__ == "__main__":
    main()
