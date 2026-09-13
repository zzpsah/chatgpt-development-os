# Failure + Recovery Proof

## Status

Active post-Production-E2E maturity gate. This is a recovery supervisor/proof layer over existing DevOS contracts, not a new execution authority and not a replacement for P11/P13/P14 recovery primitives.

## Purpose

Prove that the merged governed development path behaves safely under bounded failure:

`request → interpretation → plan → readiness → controller → runtime → failure → classify → preserve checkpoint/evidence → bounded repair or HOLD → revalidate → verify → persist → resume`

Reference protocol: `DEVOS-FAILURE-RECOVERY-v1`.

## Composition rule

The proof composes:
- P11 repository-first recovery/revalidation;
- P13 orchestration checkpoint principle that saved candidates are never replay authority;
- P14 adaptive verification/self-healing boundaries;
- Production E2E Harness stage traces and evidence;
- existing host/runtime/verification/Security Gate boundaries.

It must not create a second runtime, bypass controller/readiness, or infer permission from a checkpoint.

## Failed checkpoint

A bounded failed checkpoint records only recoverable control facts:

```yaml
protocol: DEVOS-FAILURE-RECOVERY-v1
status: FAILED_CHECKPOINT
failure_class: <deterministic class>
failed_stage: <E2E stage>
last_safe_stage: <earlier stage or null>
repository_head: <observed head>
compiled_repository_head: <plan provenance>
step_id: <exact step or null>
runtime_operation: <bounded operation or null>
mutation_operation: true | false
mutation_attempted: true | false
runtime_status: <observed status or null>
raw_reason: <observed reason>
replay_policy: <bounded policy>
authority: UNCHANGED
authorization: UNCHANGED
execution: NONE
```

Checkpoint presence never authorizes execution.

## Required failure classes

The reference supervisor must deterministically distinguish at least:
- `INPUT_AMBIGUOUS`
- `PLAN_BLOCKED`
- `REPOSITORY_DRIFT`
- `DEPENDENCY_BLOCKED`
- `CAPABILITY_MISSING`
- `AUTHORIZATION_REQUIRED`
- `SECURITY_BLOCKED`
- `CONTROL_BOUNDARY_BLOCKED`
- `PROVIDER_OR_RUNTIME_UNAVAILABLE`
- `RUNTIME_FAILED`
- `VERIFICATION_FAILED`
- `PERSISTENCE_AUTHORIZATION_REQUIRED`
- `PERSISTENCE_FAILED`
- `RECOVERY_FAILED`
- `UNKNOWN_FAILURE`

## Last-safe-stage rule

The checkpoint records the last earlier E2E stage for which observed trace evidence exists. It never synthesizes successful execution evidence for stages that did not run.

## Replay safety

### Replay-safe path

A failed path may be re-run through the full E2E harness only after fresh revalidation when:
- no mutation reached the runtime adapter;
- the repaired payload still has explicit current repository-head evidence;
- any repository-head change is accompanied by explicit recompilation acknowledgement;
- stale plan provenance is repaired so compiled and current heads match;
- all ordinary P15/P16/P17/controller/runtime/verification/persistence gates are re-applied.

### Mutation no-replay boundary

If a mutation operation reached the runtime adapter, the recovery supervisor must return `HOLD` with `MUTATION_REPLAY_FORBIDDEN` rather than re-running the E2E path.

This applies even if:
- the mutation returned success but verification later failed;
- persistence later failed;
- recovery readback later failed;
- the user asks to retry;
- a prior approval exists.

A post-mutation recovery may be implemented only by a separately bounded operation that proves current resulting state and does not blindly repeat the mutation. The reference v1 supervisor deliberately stops instead of guessing.

A mutation request rejected before adapter invocation is not considered attempted and may proceed later only after the exact failed gate is repaired and all gates are freshly revalidated.

## Repository drift

A changed repository head invalidates the old checkpoint as execution input. Resume must HOLD unless the caller explicitly represents that recompilation/revalidation occurred. For a stale-plan failure, the repaired compiled head must equal the current head before retry.

## Authorization and Security Gate

Recovery never creates or carries forward authorization implicitly.

- Exact-step authorization must be supplied again where the normal path requires it.
- Security Gate evidence must be supplied again where the normal path requires it.
- A checkpoint with altered `authority` or `authorization` fields is invalid and must HOLD.
- Earlier approvals cannot be generalized to a different step, operation, repository state or higher-impact action.

## Verification and persistence

A recovered run is successful only if the normal E2E harness reaches `COMPLETE / RECOVERY` with fresh verification.

Persisted execution evidence is independently inspectable. Missing, malformed, wrong-protocol, non-VERIFIED, non-execution-evidence, runtime-failed or verification-failed packets must HOLD and cannot be treated as recovery authority.

## Required proof scenarios

The deterministic regression corpus must prove at least:
- stale plan → STOP/checkpoint → explicit repair → recovered verified;
- missing capability → repair → recovered verified;
- changed repository head → no resume without explicit recompilation acknowledgement;
- exact-step authorization failure → repair → recovered verified;
- Security Gate failure/missing evidence → repair → recovered verified;
- read-only provider/runtime failure → repair → recovered verified;
- read-only verification failure → repair → recovered verified;
- persistence authorization failure → repair → recovered verified;
- mutation preflight authorization rejection → no mutation attempted → repair → one bounded execution;
- successful mutation followed by verification failure → HOLD/no replay;
- corrupted persisted evidence → HOLD;
- tampered checkpoint authority → HOLD.

## Managed-project proof

Closure requires a realistic managed-project proof on `zzpsah/automation-suite` or another verified DevOS-managed repository. The proof must inject at least one replay-safe failure, persist a failed checkpoint/evidence packet in the ephemeral checkout, repair the failure without remote mutation, complete the governed E2E path, and upload inspectable evidence. No production/destructive mutation is required or authorized by this contract.

## Safety invariant

> **Recovery may restore eligibility only after fresh evidence and revalidation. A checkpoint, retry request, prior approval, or previous partial success never creates authority, and an uncertain/attempted mutation is never blindly replayed.**
