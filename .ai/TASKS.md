# DevOS Tasks

## Active
- **Controlled Remote Mutation Proof** is the active gap-driven maturity gate.
- PR #14 branch: `devos/controlled-remote-mutation-proof`.
- Prove the existing `github.mutate.file` capability using provider-simulated exact-state/readback tests before making any live-provider mutation claim.
- Preserve P11 Federation & Self-Healing Context v1 as the repository-first recovery/revalidation baseline.
- Do not perform a live runtime remote mutation, destructive/production/database/credential/secret/security-sensitive mutation without separate explicit authorization for the exact operation/target/path.

## Implemented in this gate
- Normative `DEVOS-CONTROLLED-MUTATION-v1` contract.
- New read-only `github.inspect.file` provider capability for current-state/readback evidence.
- Runtime bridge support for bounded GitHub file inspection.
- One-attempt controlled mutation supervisor over existing `github.mutate.file`.
- Fresh provider pre-read and exact expected-SHA binding.
- Mandatory fresh post-mutation provider readback before `VERIFIED`.
- BLOCKED before mutation on missing auth, missing Security Gate, invalid path, unavailable pre-read, or stale expected SHA.
- HOLD + replay forbidden after an attempted mutation when conflict/final state/readback verification is not proven.
- Reconciliation of uncertain provider response through readback without issuing a second mutation.
- Provider-simulated regression corpus with explicit read/mutation call counts.
- GitHub adapter/runtime bridge tests extended for `github.inspect.file`.
- Remote Mutation Controls docs/verifier strengthened.
- Contracts CI wiring.

## Verification evidence so far
- Implementation head `776d2836a73bb564e61dfb6b89871ac4d4b6e670`: Contracts 523 passed the new Controlled Remote Mutation Proof and all observed contract steps.
- Full DevOS 448 passed every observed job except the focused `Verify Remote Mutation Controls v1` job.
- That Full 448 failure was only a contract wording mismatch: the verifier required literal `actual provider evidence` while the rewritten contract described the same rule with different wording.
- Commit `f072bda4fb8110880878e69af82c99881b5f65f5` restored the required wording without runtime changes.

## Pending closure
- Persist durable CURRENT-STATE/TASKS/DECISIONS/session provenance on the branch.
- Take fresh final-head Contracts + Full DevOS + applicable External Managed Project CI after all documentation commits.
- Repair only evidence-backed failures.
- Confirm PR #14 mergeable.
- Merge only at the exact verified final head.
- Persist provider-simulated controlled-mutation proof closure on `main`.

## Explicitly not proven / not authorized by this stage
- A live DevOS runtime `github.mutate.file` against a real provider resource.
- Branch, pull-request, workflow, deployment, production, database, permission, credential/secret, or destructive mutation.

Normal repository edits used to develop DevOS do not count as the runtime mutation proof.

## Completed recently
- P11 Federation & Self-Healing Context v1 — repository-first recovery/revalidation baseline remains active.
- Production E2E Harness — PR #11.
- Failure + Recovery Proof — PR #12.
- Multi-Session / Fresh-AI Continuation Proof — PR #13 at `cd8524b11f923e5e29eeaf445869b6239954ed1f`.

## Planned after controlled mutation proof
- Production-readiness evidence matrix covering proven vs simulated vs unproven paths and known limits.
- A live real-provider mutation proof only if separately explicitly authorized for an exact bounded target/path/operation.

## Safety invariant
Repository state, provider credentials, prior approvals, prior successful runs, continuation packets, recovery checkpoints, test success, and simulated provider evidence never create new mutation authority. Higher-impact execution remains exact-step, current-state, capability, authorization, Security Gate, verification, and recovery bounded.
