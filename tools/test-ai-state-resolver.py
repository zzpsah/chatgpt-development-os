#!/usr/bin/env python3
"""Adversarial regression corpus for deterministic AI State Resolver v2."""
from __future__ import annotations

import importlib.util
from pathlib import Path

MODULE = Path(__file__).with_name("ai-state-resolver.py")
DOCUMENT = Path(__file__).resolve().parents[1] / "docs" / "AI-STATE-RESOLVER-CROSS-CLAIM-CONTRADICTIONS.md"
spec = importlib.util.spec_from_file_location("ai_state_resolver", MODULE)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


def claim(claim_id="C1", confidence="observed", grounding_type="durable_state", ref=".ai/CURRENT-STATE.md:1", fact_key=None, fact_value=None, include_fact=False):
    result = {"id": claim_id, "statement": "P16 has a plan", "state_confidence": confidence,
              "grounding": {"type": grounding_type, "ref": ref},
              "revalidated_at": "2026-09-14T00:00:00Z",
              "revalidate_on": ["RECOVERY_BOUNDARY", "core/*.py"]}
    if include_fact:
        result["fact_key"] = fact_key
        result["fact_value"] = fact_value
    return result


def main():
    stable = module.resolve({"claims": [claim()]})
    assert stable["status"] == "RESOLVED" and stable["weakest_state_confidence"] == "likely", stable
    assert "DURABLE_STATE_CANNOT_SELF_UPGRADE_TO_OBSERVED" in stable["claims"][0]["reasons"], stable
    assert stable["authority"] == "UNCHANGED" and stable["execution"] == "NONE", stable
    assert stable["contradiction_fact_keys"] == [], stable

    boundary = module.resolve({"claims": [claim()], "events": [{"type": "RECOVERY_BOUNDARY"}]})
    assert boundary["claims"][0]["state_confidence"] == "likely", boundary
    assert "REVALIDATION_BOUNDARY_REACHED" in boundary["claims"][0]["reasons"], boundary

    likely_boundary_claim = claim(confidence="likely")
    likely_boundary = module.resolve({"claims": [likely_boundary_claim], "events": [{"type": "RECOVERY_BOUNDARY"}]})
    assert likely_boundary["claims"][0]["state_confidence"] == "likely", likely_boundary
    assert "REVALIDATION_BOUNDARY_REACHED" in likely_boundary["claims"][0]["reasons"], likely_boundary

    changed = module.resolve({"claims": [claim()], "changed_paths": ["core/controller.py"]})
    assert changed["claims"][0]["state_confidence"] == "likely", changed
    likely_changed = module.resolve({"claims": [claim(confidence="likely")], "changed_paths": ["core/controller.py"]})
    assert "REVALIDATION_PATH_CHANGED" in likely_changed["claims"][0]["reasons"], likely_changed

    malformed = module.resolve({"claims": [claim(ref=None)]})
    assert malformed["status"] == "NEEDS_EVIDENCE", malformed
    assert "OBSERVED_CLAIM_GROUNDING_MISSING" in malformed["claims"][0]["reasons"], malformed

    missing_id = claim(claim_id="", confidence="unknown", grounding_type="none", ref=None)
    missing_id_result = module.resolve({"claims": [missing_id]})
    assert missing_id_result["status"] == "NEEDS_EVIDENCE", missing_id_result
    assert missing_id_result["weakest_state_confidence"] == "unknown", missing_id_result
    assert missing_id_result["unresolved_claim_ids"] == [], missing_id_result

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

    incomplete_fact = claim(include_fact=True, fact_key="deployment.complete", fact_value=True)
    incomplete_fact.pop("fact_value")
    incomplete_result = module.resolve({"claims": [incomplete_fact]})
    assert incomplete_result["status"] == "NEEDS_EVIDENCE", incomplete_result
    assert "FACT_IDENTITY_INCOMPLETE" in incomplete_result["claims"][0]["reasons"], incomplete_result

    same_fact = module.resolve({"claims": [
        claim("C10", confidence="likely", include_fact=True, fact_key="deployment.complete", fact_value=False),
        claim("C11", confidence="likely", include_fact=True, fact_key="deployment.complete", fact_value=False),
    ]})
    assert same_fact["status"] == "RESOLVED", same_fact
    assert same_fact["contradiction_fact_keys"] == [], same_fact

    contradiction = module.resolve({"claims": [
        claim("C20", confidence="likely", include_fact=True, fact_key="deployment.complete", fact_value=True),
        claim("C21", confidence="likely", include_fact=True, fact_key="deployment.complete", fact_value=False),
    ]})
    assert contradiction["status"] == "NEEDS_EVIDENCE", contradiction
    assert contradiction["unresolved_claim_ids"] == ["C20", "C21"], contradiction
    assert contradiction["contradiction_fact_keys"] == ["deployment.complete"], contradiction
    assert all(item["state_confidence"] == "unknown" for item in contradiction["claims"]), contradiction
    assert all("CROSS_CLAIM_CONTRADICTION" in item["reasons"] for item in contradiction["claims"]), contradiction

    structured_same = module.resolve({"claims": [
        claim("C30", confidence="likely", include_fact=True, fact_key="release.targets", fact_value={"b": 2, "a": 1}),
        claim("C31", confidence="likely", include_fact=True, fact_key="release.targets", fact_value={"a": 1, "b": 2}),
    ]})
    assert structured_same["status"] == "RESOLVED", structured_same

    unrelated = module.resolve({"claims": [
        claim("C40", confidence="likely", include_fact=True, fact_key="deployment.complete", fact_value=True),
        claim("C41", confidence="likely", include_fact=True, fact_key="tests.complete", fact_value=False),
    ]})
    assert unrelated["status"] == "RESOLVED", unrelated

    document = DOCUMENT.read_text(encoding="utf-8")
    for marker in (
        "fact_key",
        "CROSS_CLAIM_CONTRADICTION",
        "statement text is never semantically paired by guesswork",
        "P16 returns `CLARIFY`",
        "P17 fails closed",
        "does not grant authorization",
    ):
        assert marker in document, marker

    print("PASS: AI State Resolver v2 rejects uncited/malformed claims and decays at revalidation boundaries")
    print("PASS: explicit fact identity detects deterministic cross-claim contradictions without prose guessing")
    print("PASS: resolver preserves P12 evidence ownership and never grants authority or execution")


if __name__ == "__main__":
    main()
