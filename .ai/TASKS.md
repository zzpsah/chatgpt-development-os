# DevOS Tasks

## Active
- **Long-running multi-session / fresh-AI continuation proof** is the active maturity gate after verified Failure + Recovery closure.
- Prove repository-only continuation across process/agent/session boundaries.
- Reconstruct active objective, project identity, latest safe checkpoint, and required gates without ChatGPT Memory/chat history.
- Revalidate repository head before resuming; stale candidates must not replay automatically.
- Preserve exact authorization/Security Gate/runtime/verification boundaries across continuation.
- Require fresh verification before completion is claimed.
- Prefer a realistic managed-project proof where the path remains read-only or otherwise explicitly bounded.

## Completed recently
- Production E2E Harness merged through PR #11 at `1d6031d3578b859a6afe1dca1032287de5beceba`.
- Failure + Recovery Proof merged through PR #12 at `83fd14e4cc696f3cd96778fe7d447db1216c3fc0`.

## Failure + Recovery final verification
- Final source head: `29c07deed803df430b2f7fd40bf302bb8deac160`.
- Contracts 503 / `34756601970`: success.
- Full DevOS 428 / `34756602046`: success.
- External Managed Project 24 / `34756601981`: success.
- Real managed project: `zzpsah/automation-suite`; failure → checkpoint → capability repair → resumed verified E2E, with unchanged HEAD/origin, zero tracked source diff, no commit/push.

## Multi-session acceptance targets
- Session A writes bounded continuation/checkpoint evidence into repository-local `.ai` state.
- Session B starts from a fresh process and uses repository evidence only.
- Same-head continuation returns revalidation-required semantics rather than executable replay.
- Changed-head continuation escalates/recompiles instead of trusting stale state.
- Authorization/Security Gate evidence does not leak between sessions or steps.
- Fresh verification and durable outcome persistence are required after continuation.
- Add deterministic regression coverage and a real managed-project proof.
- Require fresh final-head Contracts + Full DevOS + External Managed Project CI before closure.

## Planned after multi-session proof
- Controlled higher-impact remote mutation, operation by operation.
- Production-readiness evidence and documented limitations.

## Safety invariant
Repository state may preserve facts and checkpoints, but it never preserves or manufactures executable authority. Every resumed candidate must be freshly revalidated against current repository state, capability, authorization, Security Gate, and verification requirements.
