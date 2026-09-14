# Agent Runtime Conformance Evidence Intake v1 — 2026-09-14

## Trigger

After roadmap integrity reconciliation merged as PR #63, fresh recovery found no numbered feature milestone active. The durable engineering history nevertheless records a concrete evidence-backed evolution direction: runtime portability must advance through direct conformance evidence one runtime at a time, while `codex`, `claude-code`, and `openhands` remain declaration-only.

The user had an active bounded standing authorization for normal DevOS branch/commit/PR/green-merge development. Production, credentials, permissions, databases, destructive actions, tags/public GitHub Releases, and deployment remained excluded.

## Observed source boundary

Fresh `main` before this feature: `1b6ec230e7ea84d94b84b3254d0744806f2b86f5`.

Observed runtime state:

- Runtime Profile Registry v1 exists and exports only evidence-backed `VERIFIED` profiles.
- `reference-local-agent` has static repository-contract evidence only.
- `codex`, `claude-code`, and `openhands` are `DECLARED` and HOLD.
- Universal Agent Runtime Adapter v1 validates a P17/scoped-approval handoff and returned result evidence but does not invoke a vendor runtime.
- No repository tool existed to bind one future conformance evidence packet to an exact runtime ID, adapter version, Git head, nonce, and required capability set while explicitly preventing packet validity from becoming automatic registry promotion.

## Bounded objective

Add **Agent Runtime Conformance Evidence Intake v1** as an unnumbered hardening/enabling capability and move exact distribution metadata to `0.18.0` so a new source capability does not silently reuse the prior `0.17.0` release-ready identity.

The objective does not perform direct vendor-runtime execution and therefore must not mark any vendor runtime verified.

## Implemented source candidate

- `tools/agent-runtime-conformance-evidence.py`
  - deterministic SHA-256 challenge identity;
  - exact runtime/adapter/head/nonce/capability binding;
  - provenance and per-capability evidence-digest validation;
  - replay/tamper/mismatch/incomplete evidence rejection;
  - HOLD on failed required capability;
  - `registry_promotion_allowed=false` and `direct_runtime_verified=false` even for a valid packet.
- `tools/test-agent-runtime-conformance-evidence.py`
  - positive candidate packet;
  - no self-promotion of the durable `codex` declaration;
  - tampered challenge, runtime mismatch, nonce replay, failed capability, extra capability, missing provenance, invalid digest, and invalid-head regressions.
- `core/agent-runtime-conformance-evidence.md`
  - durable contract and permanent boundaries.
- `.github/workflows/verify-agent-runtime-profile-registry.yml`
  - executes the new regression corpus and contract-marker checks.
- `VERSION`, release manifest, README, changelog, and release docs
  - coherently move to `0.18.0` while keeping automatic tag/release/deploy disabled and `production_ready=false`.
- `.ai/CURRENT-STATE.md` and `.ai/TASKS.md`
  - track this objective as active until exact-head CI, merge, post-merge artifact verification, and durable reconciliation complete.

## Exact-head CI repairs observed on PR #64

Initial PR head `15874bb74eba4e8ee40f2fa0c66da7300ec49664` passed the new runtime-profile/conformance regression workflow and the normal release gate itself, but Distribution Release Readiness run `34829965476` failed in all four OS/Python matrix jobs at **Run release-gate adversarial regression corpus**.

Fresh job inspection showed the root cause was test-fixture drift rather than a release-gate failure: `tools/test-devos-release-check.py` hard-coded `0.17.0` as the expected canonical version and used `0.18.0` as the deliberately mismatched version. Once `0.18.0` became canonical, both assertions were stale.

Repair commit `8c09280f79c306b64a56687ad2b173436d09a506` makes the regression corpus derive its baseline from canonical `VERSION` and creates a guaranteed-different stable semantic version by incrementing the patch component. This keeps the adversarial intent while preventing future minor-version changes from silently invalidating the test fixture.

On repaired head `0e56dcfc542f6fee69737265db157bf166f11bc8`, Distribution Release Readiness run `34830201086` proved that the release gate and adversarial release-gate corpus now pass on all matrix legs, then failed at **Run CLI regression checks**. Fresh source inspection found a second version-fixture drift in `tools/test-devos-cli.py`: both CLI version assertions were still hard-coded to `0.17.0`.

Repair commit `9cf42577bd052f3b83eff058711d0e1d72419caf` now derives both direct and `--version` CLI assertions from canonical `VERSION` and also asserts that `release-check --json` reports that same canonical version. This removes another stale-version fixture without weakening any release boundary.

Both failed runs remain historical evidence and must not be substituted for the new exact-head CI triggered by the latest repair.

## Invariants

```text
EVIDENCE_PACKET_VALID != VERIFIED RUNTIME
EVIDENCE_PACKET_VALID != REGISTRY MUTATION
DECLARED RUNTIME != VERIFIED RUNTIME CAPABILITY
CI PASS != AUTHORIZATION
DISTRIBUTION RELEASE READY != PUBLICATION AUTHORIZATION
```

`production_ready = false` remains intentional.

## Verification / merge boundary

The repaired feature head must pass all applicable exact-head CI before merge. Merge must use the exact observed head guard. After merge, fresh `main`, the exact-source 0.18.0 release artifact, and triggered post-merge CI must be verified before a separate durable reconciliation closes the objective.

No public tag/GitHub Release/package publication/deployment is part of this objective.
