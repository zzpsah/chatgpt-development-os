# DevOS Tasks

## Active
- **Long-running multi-session / fresh-AI continuation proof** is the active maturity gate.
- PR #13 branch: `devos/multi-session-fresh-ai`.
- Prove repository-only continuation across process/agent/session boundaries without relying on chat/account memory.
- Saved candidates must never replay as authority; same-head continuation requires revalidation and changed-head continuation requires recompilation/revalidation.
- Preserve exact authorization/Security Gate/runtime/verification boundaries across continuation.
- **P11 Federation & Self-Healing Context v1 remains the repository-first recovery/revalidation baseline.**

## Implemented in this gate
- Normative `DEVOS-MULTI-SESSION-v1` contract.
- Repository-only continuation packet/evaluator.
- Same-head `REVALIDATE_REQUIRED` semantics.
- Changed-head `RECOMPILE_REQUIRED` semantics with prior authorization explicitly non-reusable.
- HOLD on project mismatch, unsupported protocol, packet authority/authorization tampering, packet execution authority, and inherited mutation replay prohibition.
- Deterministic regression corpus.
- Separate-process Session A/Session B proof using persisted JSON only.
- Real `zzpsah/automation-suite` verifier with no commit/push.
- External workflow continuation proof and artifact upload.

## Verification evidence so far
- Contracts 512 on implementation head `34cd3bc068bd4c744ba62b425412166b23ed19ed`: both continuation tests passed.
- External Managed Project 25: full external job passed, including Multi-Session Fresh-AI Continuation and evidence artifact upload.
- Final candidate head `71bc834dd975d0f0362c7c3396612b9cb1fc69fa`: Contracts 516 continuation checks passed and External Managed Project 29 passed.
- Full DevOS 441 found one durable recovery compatibility regression only: `TASKS.md` no longer explicitly named P11, which `tools/test-fresh-ai-recovery.py` requires alongside `CURRENT-STATE.md`.
- This document restores the P11 continuity marker without weakening the recovery test or changing continuation runtime behavior.

## Pending closure
- Take fresh final-head Contracts + Full DevOS + External Managed Project verification after the P11 continuity repair/session provenance update.
- Repair only evidence-backed failures.
- Confirm PR #13 mergeable.
- Merge only at the exact verified final head.
- Persist closure on `main`.

## Completed recently
- P11 Federation & Self-Healing Context v1 — repository-first recovery/revalidation baseline remains active.
- Production E2E Harness — PR #11.
- Failure + Recovery Proof — PR #12 at `83fd14e4cc696f3cd96778fe7d447db1216c3fc0`.

## Planned after multi-session proof
- Controlled higher-impact remote mutation, operation by operation.
- Production-readiness evidence and documented limitations.

## Safety invariant
Repository state preserves context, not permission. Every resumed candidate must earn current eligibility again against the current repository, capability, authorization, Security Gate, and verification state.
