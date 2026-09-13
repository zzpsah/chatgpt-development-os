# DevOS Tasks

## Active
- **Recovery Friction → Foundation Health/Doctor Integration** is the current bounded objective. It is unnumbered; do not create P18/P19.
- `tools/devos-health.py` now composes the existing `DEVOS-RECOVERY-FRICTION-v1` analyzer; recovery rules are not duplicated.
- `tools/devos-doctor.py` renders only health-supplied recovery/continuation status, friction counts, and evidence classification.
- Recovery-friction status propagates conservatively: `WARN`, `UNKNOWN`, or `BLOCKED` never becomes PASS.
- `DETERMINISTIC_HOST_PROFILE_SIMULATION` remains distinct from actual independent cross-vendor/account evidence.
- Doctor remains READ_ONLY, non-authorizing, non-mutating, and presentation-only.
- P11 repository-first recovery, readiness evidence, Security Gate, and no-replay boundaries remain unchanged.
- No live/destructive/production/provider mutation is required or authorized.

## Health-integration implementation evidence
- Verified implementation head: `40eea000d57f160781f2e2d846c126d366f42b86`.
- Trust-First Audit 51 / `34764991027`: success.
- Contracts 588 / `34764990970`: success; Foundation Health integration regressions and standalone recovery-friction gate passed.
- Full DevOS 513 / `34764991036`: success.
- The integration adds one subordinate `cross_host_recovery` health row sourced from `tools/recovery-friction.py`.
- Missing host profile → `UNKNOWN`; malformed host-profile JSON → `BLOCKED`; critical recovery capability gap → `BLOCKED`; stale expected HEAD propagates `BLOCKED`.
- Deterministic recovery evidence claiming `real_cross_vendor_account_proven=true` is rejected as `BLOCKED`.
- Doctor visibly preserves evidence class, recovery status, continuation status, friction units, and `real_cross_vendor_account_proven=false` without recomputing the analyzer.
- These runs prove the implementation head only; documentation commits after this point require fresh exact-final-head CI before closure.

## Cross-Host Recovery Friction & Onboarding Proof — completed
- Analyzer: `tools/recovery-friction.py`.
- Protocol: `DEVOS-RECOVERY-FRICTION-v1`.
- Normative contract: `core/cross-host-recovery-friction.md`.
- Adversarial corpus: `tools/test-recovery-friction.py`.
- Runnable gate: `python tools/test-host-profile.py && python tools/test-fresh-ai-recovery.py && python tools/test-recovery-friction.py`.
- Implementation head `d7b4a84d3f9321091aac0bff2a3438647dcf8ec2`: Trust-First 39 / `34764579792`, Contracts 576 / `34764579787`, Full DevOS 501 / `34764579789` — success.
- Final source head `55b3a8e64ecefae6058529ea18c6ca04b80d2860`: Trust-First 41 / `34764671486`, Contracts 578 / `34764671499`, Full DevOS 503 / `34764671501` — success.
- PR #20 merge commit: `4161abf357bbca1e8bb844c7d87f74cfb34b94e6`.
- Fresh post-merge main: Trust-First 42 / `34764727276`, Contracts 579 / `34764727340`, Full DevOS 504 / `34764727299` — success.
- Closure-state main `9258a5e53be542b6ed246ed5c72155f1521b80e7`: Trust-First 45 / `34764829953`, Contracts 582 / `34764829874`, Full DevOS 507 / `34764829850` — success.
- Evidence class remains `DETERMINISTIC_HOST_PROFILE_SIMULATION`; `real_cross_vendor_account_proven = false`.

## Foundation Health & State Consistency — completed
- Final source head: `77a8f6f8d8ce012d872b20343bded2e00c53ed7d`.
- PR #18 merge commit: `657ae461c0d6df62ca428d8bdd0404bd241b5c84`.
- Final PR verification: Trust-First 29 / `34763332363`, Contracts 566 / `34763332344`, Full DevOS 491 / `34763332347` — success.
- Fresh post-merge main: Trust-First 33 / `34764171968`, Contracts 570 / `34764171939`, Full DevOS 495 / `34764171923` — success.
- `tools/test-step-readiness-orchestrator.py` remains historical-source drift in the readiness ledger and remains WARN rather than silently refreshed.

## Completed recently
- Production E2E Harness — PR #11.
- Failure + Recovery Proof — PR #12.
- Multi-Session / Fresh-AI Continuation Proof — PR #13.
- Controlled Remote Mutation Proof — PR #14.
- Production-Readiness Evidence Matrix & Limitations — PR #16.
- Trust-First audit gap closure / adversarial Security Gate proof — PR #17.
- Foundation Health & State Consistency — PR #18.
- Cross-Host Recovery Friction & Onboarding Proof — PR #20.

## Health-integration acceptance targets
- Health composes the existing recovery-friction analyzer/result rather than reimplementing its recovery rules. **Implemented/tested.**
- Doctor presents recovery and continuation status plus friction counts clearly. **Implemented/tested.**
- Missing/invalid host profile or recovery evidence is `UNKNOWN`/`BLOCKED`, never hidden. **Implemented/tested.**
- Simulated host evidence remains labeled simulated and never becomes real cross-vendor/account proof. **Implemented/tested.**
- Existing health outcomes retain conservative worst-status semantics. **Implemented/tested.**
- No authority, authorization, execution, mutation, evidence rewrite, or automatic historical refresh is introduced. **Preserved/tested.**
- Runnable final gate: `python tools/test-devos-audit.py && python tools/test-recovery-friction.py && python tools/test-foundation-health.py`.
- Fresh exact-final-head Trust-First, Contracts, and Full DevOS CI remains mandatory before closure.

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
