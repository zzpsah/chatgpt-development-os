# DevOS Tasks

## Active
- **Cross-Host Recovery Friction & Onboarding Proof** is the current bounded objective. It is unnumbered; do not create P18/P19.
- Build on existing repository-only recovery, Multi-AI portability, host profiles, auto-onboarding, and fresh-AI recovery checks instead of creating a parallel portability system.
- Produce machine-readable, READ_ONLY recovery/friction evidence from repository state only.
- Measure at minimum: canonical identity recovery, bootstrap completeness, current-state recovery, active-task recovery, decision/safety-boundary recovery, host-profile capability gaps, continuation entrypoint discovery, and unresolved/ambiguous inputs.
- Treat missing or ambiguous recovery inputs as `UNKNOWN`/`BLOCKED`, never PASS.
- A simulated host profile is not a real cross-vendor/account proof; do not promote simulated recovery into live-provider or independent-account evidence.
- Preserve P11 repository-first recovery/revalidation and all existing authorization/Security Gate boundaries.
- Keep `production_ready = false` and all live-mutation proof false unless separately authorized and genuinely proven.
- Do not run live/destructive/production/provider mutation for this objective.

## Foundation Health & State Consistency — completed
- Final source head: `77a8f6f8d8ce012d872b20343bded2e00c53ed7d`.
- PR #18 merge commit: `657ae461c0d6df62ca428d8bdd0404bd241b5c84`.
- Final PR verification: Trust-First 29 / `34763332363`, Contracts 566 / `34763332344`, Full DevOS 491 / `34763332347` — all success.
- Fresh post-merge main verification: Trust-First 33 / `34764171968`, Contracts 570 / `34764171939`, Full DevOS 495 / `34764171923` — all success.
- External Managed Project is not push-triggered for this merge; no run is fabricated.
- `tools/test-step-readiness-orchestrator.py` remains historical-source drift in the readiness ledger and is intentionally surfaced as WARN rather than silently refreshed.

## Completed recently
- Production E2E Harness — PR #11.
- Failure + Recovery Proof — PR #12.
- Multi-Session / Fresh-AI Continuation Proof — PR #13.
- Controlled Remote Mutation Proof — PR #14.
- Trust-First audit gap closure / adversarial Security Gate proof — PR #17.
- Production-Readiness Evidence Matrix & Limitations — PR #16, merged at `b8e31ae76201b32e4617ef6044b29ef285004f54`.
- Foundation Health & State Consistency — PR #18, merged at `657ae461c0d6df62ca428d8bdd0404bd241b5c84`.

## Cross-host recovery acceptance targets
- Exact canonical repository identity must be recoverable from repository evidence alone.
- Required bootstrap/state files must be dependency-closed and machine-checkable.
- Current active work and durable decisions must be recoverable without chat/account memory.
- The recovery report must name missing inputs and capability gaps rather than inferring success.
- Host-profile comparison must not alter authority, authorization, Security Gate requirements, or replay rules.
- Recovery/adoption friction should be represented by deterministic counts/fields that can be compared across hosts and future revisions.
- Real cross-vendor/account proof remains a separate evidence level from deterministic profile simulation.
- Every milestone ends with a runnable PASS/FAIL command and fresh exact-final-head CI before closure.

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
