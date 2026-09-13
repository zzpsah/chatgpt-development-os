# Current State

## Snapshot

- Repository: `zzpsah/chatgpt-development-os`.
- Source tree + Git are authoritative; ChatGPT Memory/chat history are supplementary only.
- P11 repository-first recovery/revalidation remains a durable invariant.
- P9 through P17 are complete on `main`.
- Production E2E Harness and Failure + Recovery Proof are verified and closed.
- Active maturity gate: **long-running multi-session / fresh-AI continuation proof**, PR #13 on `devos/multi-session-fresh-ai`.

## Canonical governed path

`Human request → P15 interpretation → P16 plan → P17 readiness → controller → bounded runtime → verification → persistence → recovery / continuation`

Interpretation, planning, readiness, recovery, continuation packets, and successful prior sessions never manufacture permission.

## Failure + Recovery closure

PR #12 merged at `83fd14e4cc696f3cd96778fe7d447db1216c3fc0` from final head `29c07deed803df430b2f7fd40bf302bb8deac160` after:
- Contracts 503 / `34756601970`: success.
- Full DevOS 428 / `34756602046`: success.
- External Managed Project 24 / `34756601981`: success.

## Active multi-session / fresh-AI continuation proof

Normative contract: `core/multi-session-continuation-proof.md`.
Evaluator: `tools/multi-session-continuation.py`.
Regression corpus: `tools/test-multi-session-continuation.py`.
Two-process proof: `tools/test-multi-session-two-process.py`.
Real managed-project verifier: `tools/verify-multi-session-managed-project.py`.

### Implemented continuation behavior

- Session A may persist only continuity facts: project, objective, observed repository head, optional candidate step id, last safe stage, constraints, verification obligations, and evidence refs.
- Continuation packets always preserve `authority: UNCHANGED`, `authorization: UNCHANGED`, `execution: NONE`.
- Same-head Session B returns `REVALIDATE_REQUIRED`; saved candidates are never directly executable.
- Changed-head Session B returns `RECOMPILE_REQUIRED / REPOSITORY_HEAD_CHANGED` and explicitly forbids prior authorization reuse.
- Project mismatch, unsupported protocol, packet authority/authorization tampering, packet execution authority, and inherited mutation-replay-forbidden state all HOLD.
- Authorization/Security Gate evidence does not migrate across session/step boundaries merely because the objective or step id matches.
- Failure + Recovery's `HOLD / MUTATION_REPLAY_FORBIDDEN` boundary survives continuation.

### Two-process proof

`tools/test-multi-session-two-process.py` launches separate Python processes. Session A writes the packet to disk; Session B receives only persisted packet/current-state JSON plus repository Git evidence. It proves:
- same-head → `REVALIDATE_REQUIRED`;
- changed-head → `RECOMPILE_REQUIRED`;
- prior authorization is not reusable;
- packet tampering cannot manufacture authority.

### Real managed-project proof

External workflow checks out `zzpsah/automation-suite` and runs a fresh-process continuation proof using only repository-local `.ai/EVIDENCE/` state plus current Git/origin evidence.

Observed on implementation head `34cd3bc068bd4c744ba62b425412166b23ed19ed`:
- Contracts run 512: both new continuation tests passed before the remainder of the contract suite continued.
- External Managed Project run 25: success, including Multi-Session Fresh-AI Continuation and artifact upload.
- The managed proof used no commit/push and required all worktree changes to remain bounded evidence only.

Because this semantic-state update changes the branch head, fresh final-head Contracts + Full DevOS + External Managed Project verification is still required before PR #13 can close.

## Closure gate

PR #13 may merge only after the exact final head:
1. remains mergeable;
2. passes Contracts, including both continuation proofs;
3. passes Full DevOS, including repository-only fresh-AI recovery;
4. passes External Managed Project, including continuation artifact upload;
5. has durable session/task/decision provenance.

## Recovery precedence

1. Current source tree + Git.
2. Explicit requirements/decisions.
3. `.ai/CURRENT-STATE.md`, `.ai/TASKS.md`, and semantic `.ai` state.
4. `.ai/SESSIONS/` provenance.
5. Generated indexes as navigation/evidence only.
6. ChatGPT Memory/chat history as supplementary context only.

Exact implementation remains authoritative in Git history.
