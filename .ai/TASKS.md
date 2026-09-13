# DevOS Tasks

## Active
- **Recovery Friction → Foundation Health/Doctor Integration** is the current bounded objective. It is unnumbered; do not create P18/P19.
- Integrate existing `DEVOS-RECOVERY-FRICTION-v1` evidence into `tools/devos-health.py` and `tools/devos-doctor.py`; do not duplicate recovery logic or create another truth system.
- Recovery-friction status must propagate conservatively: `WARN`, `UNKNOWN`, or `BLOCKED` must never become PASS in health/doctor presentation.
- Preserve `DETERMINISTIC_HOST_PROFILE_SIMULATION` as distinct from actual independent cross-vendor/account evidence.
- Keep doctor READ_ONLY, non-authorizing, non-mutating, and presentation-only.
- Preserve P11 repository-first recovery, readiness evidence, Security Gate, and no-replay boundaries.
- No live/destructive/production/provider mutation is required or authorized.

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
- Evidence class remains `DETERMINISTIC_HOST_PROFILE_SIMULATION`; `real_cross_vendor_account_proven = false`.
- Recovery and continuation are separate statuses; friction units are transparent issue counts, not readiness/authorization probabilities.

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
- `tools/devos-health.py` composes the existing recovery-friction analyzer/result rather than reimplementing its recovery rules.
- `tools/devos-doctor.py` presents recovery and continuation status plus friction counts clearly.
- Missing/invalid host profile or recovery evidence is `UNKNOWN`/`BLOCKED`, never hidden.
- Simulated host evidence remains labeled simulated and never becomes real cross-vendor/account proof.
- Existing health outcomes retain conservative worst-status semantics.
- No authority, authorization, execution, mutation, evidence rewrite, or automatic historical refresh is introduced.
- Every implementation milestone ends with a runnable PASS/FAIL command and fresh exact-final-head CI.

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
