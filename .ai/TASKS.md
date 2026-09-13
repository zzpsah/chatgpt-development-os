# DevOS Tasks

## Active
- **Failure + Recovery Proof** is the active gap-driven maturity gate after verified Production E2E Harness closure.
- PR #12 branch: `devos/failure-recovery-proof`.
- Use the merged `DEVOS-PRODUCTION-E2E-v1` harness as the fault-injection substrate; do not create a parallel recovery framework.
- Preserve last-safe checkpoints and observed failure evidence.
- Revalidate repository state, dependencies, capability, authorization, Security Gate, runtime/verification evidence and persistence before any retry.
- Never blindly replay uncertain or failed mutation work.

## Implemented in this gate
- Normative `DEVOS-FAILURE-RECOVERY-v1` contract.
- Failure classifier/checkpoint/resume supervisor.
- Deterministic failure-injection regression corpus.
- Replay-safe read-only retry with full gate revalidation.
- `HOLD / MUTATION_REPLAY_FORBIDDEN` once a mutation actually reaches the runtime adapter.
- Persisted-evidence integrity checks and checkpoint tamper rejection.
- Real managed-project verifier against `zzpsah/automation-suite` with no commit/push.
- External workflow integration and recovery evidence artifact path.
- P15→P16 high-impact gating annotation fix plus regression coverage.
- Managed-project verifier corrected to validate evidence files directly instead of relying on per-file Git porcelain entries.

## Pending verification / closure
- Take fresh Contracts, Full DevOS and External Managed Project CI on the exact final semantic-state head.
- If any run fails, repair only the demonstrated defect and repeat fresh final-head verification.
- Confirm PR #12 remains mergeable.
- Merge PR #12 only after all final-head verification is green.
- Persist Failure + Recovery Proof closure on `main`.

## Completed recently
- P9 Development Task Controller v1.
- P10 Context Continuity & Recovery v1.
- P11 Federation & Self-Healing Context v1.
- P12 Operational Intelligence.
- P13 Autonomous Development Orchestration.
- P14 Adaptive Verification & Self-Healing v1.
- P15 Human Language Interpretation v2.
- P16 Semantic Goal-to-Plan Compiler v1.
- P17 Step Readiness & Authorization Orchestrator v1.
- Production E2E Harness merged through PR #11 at `1d6031d3578b859a6afe1dca1032287de5beceba`.

## Failure + Recovery evidence so far
- Contracts 497: dedicated Failure + Recovery Proof passed after fixing the high-impact gating annotation path.
- Contracts 498: dedicated recovery step and all predecessor contract steps passed on head `790d6eb7523719ce677c050a81715e07c41b71bd`.
- External run 19 proved the recovery flow itself succeeded on real `automation-suite`; only the final Git status assertion failed because `.ai/EVIDENCE/` already existed from the earlier Production E2E step.
- Commit `424a770fdd247fc318bb7a4a1bd8025634b1be1b` corrected the wrapper to require the expected evidence files, unchanged HEAD/origin, bounded evidence-only worktree status, and zero tracked diff.

## Planned after Failure + Recovery Proof
- Long-running multi-session / fresh-AI continuation proof on realistic work.
- Controlled higher-impact remote mutation, operation by operation.
- Production-readiness evidence and documented limitations.

## Safety invariant
Recovery work may repair deterministic local state only within existing authority. A failure, retry request, prior approval, successful earlier run, checkpoint, or recovery attempt never creates new authorization or permits blind replay of an uncertain mutation.
