# DevOS Tasks

## Active
- **Current-Source Evidence Refresh Protocol** is the current bounded objective. It is unnumbered; do not create P18/P19.
- Extend the existing readiness-evidence system; do not create a second evidence ledger or competing truth source.
- Preserve all historical evidence rows, source heads, run IDs, archive digests, and `historical_source_drift` semantics unchanged.
- Add a reviewed current-source evidence path that records exact source head/test/run provenance separately from historical evidence.
- New current-source evidence must prove only the level actually observed; deterministic/integrated CI cannot become live-provider or production proof.
- Health/Doctor may consume current-source evidence only through the authoritative readiness-evidence verifier; they must not manufacture freshness independently.
- Evidence refresh never grants authority or authorization and never permits execution/mutation by itself.
- No live/destructive/production/provider mutation is required or authorized for this objective.

## Recovery Friction → Foundation Health/Doctor Integration — completed
- Final source head: `869a95894dad5feaafcbc286ec1fb0027c8321df`.
- PR #21 merge commit: `c3c7597a5b475c7060efc8fb9e6df81f88716e8c`.
- Final PR verification: Trust-First 54 / `34765090674`, Contracts 591 / `34765090663`, Full DevOS 516 / `34765090662` — success.
- Fresh post-merge main: Trust-First 55 / `34765164604`, Contracts 592 / `34765164610`, Full DevOS 517 / `34765164649` — success.
- Health composes the existing `DEVOS-RECOVERY-FRICTION-v1` analyzer as subordinate evidence; Doctor only presents Health output.
- Missing profile remains UNKNOWN; malformed profile, stale expected HEAD, critical host capability gaps, canonical identity tampering, and unsupported simulated→real claim promotion remain BLOCKED.
- Evidence remains deterministic/read-only; no real independent cross-vendor/account trial is claimed.

## Cross-Host Recovery Friction & Onboarding Proof — completed
- Analyzer: `tools/recovery-friction.py`.
- Protocol: `DEVOS-RECOVERY-FRICTION-v1`.
- Normative contract: `core/cross-host-recovery-friction.md`.
- Final source head `55b3a8e64ecefae6058529ea18c6ca04b80d2860`.
- PR #20 merge `4161abf357bbca1e8bb844c7d87f74cfb34b94e6`.
- Post-merge main: Trust-First 42 / `34764727276`, Contracts 579 / `34764727340`, Full DevOS 504 / `34764727299` — success.
- Closure-state main `9258a5e53be542b6ed246ed5c72155f1521b80e7`: Trust-First 45 / `34764829953`, Contracts 582 / `34764829874`, Full DevOS 507 / `34764829850` — success.
- `DETERMINISTIC_HOST_PROFILE_SIMULATION` remains distinct from real cross-vendor/account proof.

## Foundation Health & State Consistency — completed
- Final source head `77a8f6f8d8ce012d872b20343bded2e00c53ed7d`.
- PR #18 merge `657ae461c0d6df62ca428d8bdd0404bd241b5c84`.
- Post-merge main: Trust-First 33 / `34764171968`, Contracts 570 / `34764171939`, Full DevOS 495 / `34764171923` — success.
- `tools/test-step-readiness-orchestrator.py` remains the known historical-source drift and must not be silently refreshed.

## Current-source evidence acceptance targets
- Historical evidence remains byte/provenance stable; no old source head/run is rewritten.
- New current-source evidence has an explicit protocol/schema and exact source head.
- The verifier rejects stale/current-head mismatches and fabricated run/test mappings.
- Current-source evidence distinguishes deterministic, integrated, real read-only, provider-simulated, live-provider, and production claims conservatively; v1 must not introduce unsupported higher proof levels.
- Current evidence can resolve a current-source drift only for the exact test/capability/level it actually proves; historical provenance remains visible.
- Missing current evidence remains UNKNOWN/WARN as appropriate, never PASS by implication.
- Health/Doctor consume only verified ledger-derived current-evidence status.
- Runnable PASS/FAIL regression command and fresh exact-final-head CI are mandatory before closure.

## Completed recently
- Production E2E Harness — PR #11.
- Failure + Recovery Proof — PR #12.
- Multi-Session / Fresh-AI Continuation Proof — PR #13.
- Controlled Remote Mutation Proof — PR #14.
- Production-Readiness Evidence Matrix & Limitations — PR #16.
- Trust-First audit gap closure / adversarial Security Gate proof — PR #17.
- Foundation Health & State Consistency — PR #18.
- Cross-Host Recovery Friction & Onboarding Proof — PR #20.
- Recovery Friction → Foundation Health/Doctor Integration — PR #21.

## Universal portability invariant
`AI A + Account A → repository → AI B + Account B → correct recovery → safe continuation`

The repository, not any AI account/chat/model/vendor memory, carries authoritative project state.

## Safety invariants
- `PLAN != EXECUTION`
- `READY != EXECUTION`
- `INTERPRETATION != AUTHORIZATION`
- `OLD APPROVAL != NEW APPROVAL`
- `SIMULATED EVIDENCE != LIVE PROVIDER PROOF`
- `CHAT MEMORY != SOURCE OF TRUTH`
- `PROVIDER RESPONSE != COMPLETION PROOF`
- `RECOVERY != AUTOMATIC MUTATION REPLAY`
