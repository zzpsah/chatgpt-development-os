# Current State

## Snapshot

- Repository: `zzpsah/chatgpt-development-os`.
- Source tree + Git are authoritative; ChatGPT Memory/chat history are supplementary only.
- P11 repository-first recovery/revalidation remains a durable invariant.
- P9 through P17 are complete on `main`.
- Production E2E Harness is verified, merged, and closed on `main` through PR #11.
- Active maturity gate: **Failure + Recovery Proof**, PR #12 on `devos/failure-recovery-proof`.

## Canonical governed path

`Human request → P15 interpretation → P16 plan → P17 readiness → P16 controller → P17 runtime handoff → bounded runtime-adapter operation → explicit verification → authorized persistence → recovery / continuation`

Interpretation, planning, readiness, orchestration, retries, and successful tests never manufacture permission. Runtime mutation, persistence, remote mutation, and production/destructive actions remain independently bounded by capability, exact authorization, Security Gate, verification, and recovery rules.

## Production E2E Harness closure

Production E2E final source head `4270440533925628a88daa17a6620aa51295319a` passed:
- Contracts 490 / `34751784035`.
- Full DevOS 415 / `34751784082`.
- External Managed Project 15 / `34751784049`.

PR #11 merged at `1d6031d3578b859a6afe1dca1032287de5beceba`.

## Active Failure + Recovery Proof

Normative contract: `core/failure-recovery-proof.md`.
Supervisor: `tools/failure-recovery-proof.py`.
Deterministic regression corpus: `tools/test-failure-recovery-proof.py`.
Real managed-project verifier: `tools/verify-failure-recovery-managed-project.py`.
External proof target: `zzpsah/automation-suite` in an ephemeral checkout; no commit/push is permitted.

### Implemented recovery behavior

- Deterministic failure classification across interpretation/planning/readiness/controller/runtime/verification/persistence/recovery stages.
- Failed checkpoint records failure class, failed stage, last safe stage, repository/compiled-head provenance, exact step, runtime operation, raw reason, and unchanged authority boundaries.
- Repository drift requires recompilation/revalidation before retry.
- Missing capability, approval, Security Gate, provider/runtime evidence, verification, persistence authorization, and corrupt persisted evidence fail closed.
- Checkpoint authority/authorization tampering is rejected.
- Replay-safe read-only failures may retry only after normal P15/P16/P17/controller/runtime/verification gates run again.
- Once a mutation operation actually reaches the runtime adapter, automatic replay is forbidden: `HOLD / MUTATION_REPLAY_FORBIDDEN`.
- Persistence evidence is independently validated before recovery is accepted.

### Cross-layer defect repaired during this gate

P15 emits `HIGH_IMPACT_REQUIRES_AUTHORIZATION_CHECK` for high-impact/security requests. P16 previously treated every ambiguity marker as material and returned `CLARIFY`, preventing the request from reaching authorization/Security Gate checks. P16 now preserves that marker as a gating annotation while genuine unresolved ambiguity still blocks. A direct P16 regression covers this boundary.

### Verification evidence so far

- Deterministic Failure + Recovery Proof passed inside Contracts run 497 on source head `99ba8009f72dfd5b3f9dc307b82da50b659220cd`.
- Contracts run 498 on verifier-fix head `790d6eb7523719ce677c050a81715e07c41b71bd` also passed the dedicated recovery step and all prior contract steps.
- External run 19 demonstrated that the real `automation-suite` failure → checkpoint → capability repair → resumed verified E2E flow succeeds; the remaining failure was only an over-strict Git-porcelain assertion in the proof wrapper.
- Commit `424a770fdd247fc318bb7a4a1bd8025634b1be1b` removes that invalid status-line assumption and instead validates the three expected evidence files directly, requires all working-tree deltas to remain under `.ai/EVIDENCE`, requires zero tracked source diff, and requires unchanged HEAD/origin.

Because durable semantic state is being updated after `424a770f...`, fresh final-head Contracts + Full DevOS + External Managed Project CI is still required before PR #12 may merge.

## Next acceptance gate

PR #12 may close only when the exact final head:
1. is mergeable;
2. passes Contracts, including Failure + Recovery Proof;
3. passes Full DevOS, including fresh-AI/repository recovery checks;
4. passes External Managed Project, including recovery proof and evidence artifact upload;
5. has durable session/current-state/task/decision provenance.

After closure, the next roadmap gate is long-running multi-session / fresh-AI continuation proof.

## Recovery precedence

1. Current source tree + Git.
2. Explicit requirements/decisions.
3. `.ai/CURRENT-STATE.md`, `.ai/TASKS.md`, and semantic `.ai` state.
4. `.ai/SESSIONS/` provenance.
5. Generated indexes as navigation/evidence only.
6. ChatGPT Memory/chat history as supplementary context only.

Exact implementation remains authoritative in Git history.
