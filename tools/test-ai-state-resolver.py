#!/usr/bin/env python3
"""Adversarial regression corpus for deterministic AI State Resolver v2."""
from __future__ import annotations

import importlib.util
from pathlib import Path

MODULE = Path(__file__).with_name("ai-state-resolver.py")
spec = importlib.util.spec_from_file_location("ai_state_resolver", MODULE)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


def claim(claim_id="C1", confidence="observed", grounding_type="durable_state", ref=".ai/CURRENT-STATE.md:1"):
    return {"id": claim_id, "statement": "P16 has a plan", "state_confidence": confidence,
            "grounding": {"type": grounding_type, "ref": ref},
            "revalidated_at": "2026-09-14T00:00:00Z",
            "revalidate_on": ["RECOVERY_BOUNDARY", "core/*.py"]}


def main():
    stable = module.resolve({"claims": [claim()]})
    assert stable["status"] == "RESOLVED" and stable["weakest_state_confidence"] == "likely", stable
    assert "DURABLE_STATE_CANNOT_SELF_UPGRADE_TO_OBSERVED" in stable["claims"][0]["reasons"], stable
    assert stable["authority"] == "UNCHANGED" and stable["execution"] == "NONE", stable

    boundary = module.resolve({"claims": [claim()], "events": [{"type": "RECOVERY_BOUNDARY"}]})
    assert boundary["claims"][0]["state_confidence"] == "likely", boundary
    assert "REVALIDATION_BOUNDARY_REACHED" in boundary["claims"][0]["reasons"], boundary

    changed = module.resolve({"claims": [claim()], "changed_paths": ["core/controller.py"]})
    assert changed["claims"][0]["state_confidence"] == "likely", changed

    malformed = module.resolve({"claims": [claim(ref=None)]})
    assert malformed["status"] == "NEEDS_EVIDENCE", malformed
    assert "OBSERVED_CLAIM_GROUNDING_MISSING" in malformed["claims"][0]["reasons"], malformed

    duplicate = module.resolve({"claims": [claim(), claim()]})
    assert duplicate["unresolved_claim_ids"] == ["C1", "C1"], duplicate

    p12_old = module.resolve({"claims": [claim(grounding_type="execution_evidence", ref="P12-E-1")]})
    assert p12_old["weakest_state_confidence"] == "likely", p12_old
    fresh_claim = claim(grounding_type="execution_evidence", ref="P12-E-1")
    fresh_claim["p12_freshness"] = "current"
    p12_fresh = module.resolve({"claims": [fresh_claim]})
    assert p12_fresh["weakest_state_confidence"] == "observed", p12_fresh

    unknown = module.resolve({"claims": [claim(confidence="unknown", grounding_type="none", ref=None)]})
    assert unknown["status"] == "NEEDS_EVIDENCE" and unknown["unresolved_claim_ids"] == ["C1"], unknown
    print("PASS: AI State Resolver v2 rejects uncited/conflicting claims and decays at revalidation boundaries")
    print("PASS: resolver preserves P12 evidence ownership and never grants authority or execution")


if __name__ == "__main__":
    main()
