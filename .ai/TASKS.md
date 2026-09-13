# DevOS Tasks

## Active
- **Cross-Host Recovery Friction & Onboarding Proof** is the current bounded objective. It is unnumbered; do not create P18/P19.
- Build on existing repository-only recovery, Multi-AI portability, host profiles, auto-onboarding, and fresh-AI recovery checks instead of creating a parallel portability system.
- Machine-readable analyzer: `tools/recovery-friction.py`, protocol `DEVOS-RECOVERY-FRICTION-v1`.
- Normative contract: `core/cross-host-recovery-friction.md`.
- Adversarial corpus: `tools/test-recovery-friction.py`.
- Produce READ_ONLY recovery/friction evidence from repository state + validated `DEVOS-HOST-PROFILE-v1` only.
- Measure canonical identity recovery, bootstrap/state inputs, active-task/decision/handoff recoverability, stale expected HEAD, and host capability gaps.
- Treat missing/ambiguous recovery inputs as `UNKNOWN`/`BLOCKED`, never PASS.
- A simulated host profile is not a real cross-vendor/account proof; every deterministic report keeps `real_cross_vendor_account_proven = false`.
- Preserve P11 repository-first recovery/revalidation and all authorization/Security Gate/no-replay boundaries.
- Keep `production_ready = false` and live-mutation proof false unless separately authorized and genuinely proven.
- Do not run live/destructive/production/provider mutation for this objective.

## Recovery-friction implementation evidence
- Verified implementation head: `d7b4a84d3f9321091aac0bff2a3438647dcf8ec2`.
- Trust-First Audit 39 / `34764579792`: success.
- Contracts 576 / `34764579787`: success; cross-host recovery gate passed in the full contract chain.
- Full DevOS 501 / `34764579789`: success; dedicated `Verify Cross-Host Recovery Friction & Onboarding` job passed.
- Dedicated Full job passed host-profile validation, repository-only fresh-AI recovery, and the recovery-friction adversarial corpus.
- These runs prove the implementation head only; this durable documentation update creates a later final source head and therefore requires fresh exact-final-head CI before closure.

## Deterministic evidence boundary
- Evidence class: `DETERMINISTIC_HOST_PROFILE_SIMULATION`.
- `recovery_status` is distinct from `continuation_status`; state recovery is not equated with execution/verification capability.
- Transparent `friction_units` is the sum of issue counts, not a probability, quality percentage, authorization score, or production-readiness score.
- Critical recovery capability `MISSING` blocks; noncritical missing/delegatable capability remains visible continuation friction.
- Host declarations are validated inputs, not observed provider behavior.
- Real independent cross-vendor/account proof remains unproven until actually observed.

## Foundation Health & State Consistency — completed
- Final source head: `77a8f6f8d8ce012d872b20343bded2e00c53ed7d`.
- PR #18 merge commit: `657ae461c0d6df62ca428d8bdd0404bd241b5c84`.
- Final PR verification: Trust-First 29 / `34763332363`, Contracts 566 / `34763332344`, Full DevOS 491 / `34763332347` — all success.
- Fresh post-merge main verification: Trust-First 33 / `34764171968`, Contracts 570 / `34764171939`, Full DevOS 495 / `34764171923` — all success.
- `tools/test-step-readiness-orchestrator.py` remains historical-source drift in the readiness ledger and is intentionally WARN rather than silently refreshed.

## Completed recently
- Production E2E Harness — PR #11.
- Failure + Recovery Proof — PR #12.
- Multi-Session / Fresh-AI Continuation Proof — PR #13.
- Controlled Remote Mutation Proof — PR #14.
- Trust-First audit gap closure / adversarial Security Gate proof — PR #17.
- Production-Readiness Evidence Matrix & Limitations — PR #16, merged at `b8e31ae76201b32e4617ef6044b29ef285004f54`.
- Foundation Health & State Consistency — PR #18, merged at `657ae461c0d6df62ca428d8bdd0404bd241b5c84`.

## Cross-host recovery acceptance targets
- Exact canonical repository identity must be recoverable from repository evidence alone. **Implemented/tested.**
- Required bootstrap/state files must be dependency-closed and machine-checkable. **Implemented/tested.**
- Current active work and durable decisions must be recoverable without chat/account memory. **Implemented/tested at deterministic repository level.**
- The report must name missing inputs and capability gaps rather than infer success. **Implemented/tested.**
- Host-profile comparison must not alter authority, authorization, Security Gate requirements, or replay rules. **Implemented/tested.**
- Recovery/adoption friction must use deterministic comparable counts/fields. **Implemented as transparent issue counts.**
- Real cross-vendor/account proof remains a separate evidence level from deterministic profile simulation. **Explicitly unproven.**
- Runnable gate: `python tools/test-host-profile.py && python tools/test-fresh-ai-recovery.py && python tools/test-recovery-friction.py`.
- Fresh exact-final-head Trust-First, Contracts, and Full DevOS CI is mandatory before closure.

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
