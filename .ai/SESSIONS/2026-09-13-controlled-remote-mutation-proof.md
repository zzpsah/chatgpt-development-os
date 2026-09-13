# Session — 2026-09-13 — Controlled Remote Mutation Proof

## Starting point

- Canonical repository: `zzpsah/chatgpt-development-os`.
- Multi-Session / Fresh-AI Continuation Proof closed through PR #13 at `cd8524b11f923e5e29eeaf445869b6239954ed1f`.
- Durable mainline baseline for this gate: `256bb815ef895990db7883c6001111a53ea12d4a`.
- Branch: `devos/controlled-remote-mutation-proof`.
- PR #14: `Controlled remote mutation proof with fresh readback`.

## Objective

Strengthen the existing `github.mutate.file` path so DevOS can distinguish a provider mutation attempt from verified completion, using fresh provider pre-read/readback evidence while preserving exact authorization, Security Gate, optimistic concurrency, and no-blind-retry boundaries.

This session intentionally does **not** perform a new live DevOS runtime mutation against a real provider resource.

## Audit findings

Existing Remote Mutation Controls already required:
- explicit `ALREADY_GRANTED` authorization;
- Security Gate PASS at the runtime bridge;
- exact repository target and repository-relative path;
- expected current file SHA / optimistic concurrency;
- one provider mutation attempt without automatic mutation retry;
- conflict → BLOCKED;
- uncertain provider outcome → UNVERIFIED / inspect before retry.

Maturity gap found:
- the runtime/provider bridge could not read the exact target file back after mutation;
- therefore a successful provider update response was stronger than a plan but weaker than freshly observed verified remote state.

## Material implementation actions

1. Added read-only `github.inspect.file` to `adapters/github-reference.py`.
2. Extended the provider client contract with `get_file(repository, path)`.
3. Added repository-relative path validation for GitHub file inspection.
4. Routed `github.inspect.file` through `tools/runtime-adapter-bridge.py` under `authorization: NOT_REQUIRED`.
5. Updated `adapters/github-integration.md` with the controlled verification sequence.
6. Added `core/controlled-remote-mutation-proof.md` / `DEVOS-CONTROLLED-MUTATION-v1`.
7. Added `tools/controlled-remote-mutation-proof.py` as a one-attempt supervisor over the existing bridge.
8. Added `tools/test-controlled-remote-mutation-proof.py`.
9. Extended `tools/test-github-reference.py` for bounded file inspection.
10. Extended `tools/test-external-runtime-bridge.py` for `github.inspect.file`.
11. Strengthened `core/runtime-adapter-bridge.md` and `core/remote-mutation-controls.md` so provider update response is mutation-attempt evidence, not verified completion.
12. Strengthened `tools/verify-remote-mutation.py`.
13. Wired `Verify Controlled Remote Mutation Proof` into Contracts CI.

## Controlled proof semantics

Reference sequence:

`fresh github.inspect.file → exact SHA match → exact-step authorization + Security Gate → one github.mutate.file attempt → fresh github.inspect.file readback → observed-state verification → VERIFIED or HOLD`

Regression cases prove:
- missing exact authorization: BLOCKED before provider call;
- missing Security Gate PASS: BLOCKED before mutation;
- stale expected SHA: BLOCKED before mutation;
- successful mutation: exactly one mutation call + fresh readback → VERIFIED only when intended content/new SHA are observed;
- provider conflict: HOLD after exactly one mutation attempt, replay forbidden;
- provider uncertainty after request: fresh readback may reconcile the state as VERIFIED, but there is still no second mutation call;
- readback mismatch or failure: HOLD, replay forbidden;
- path escape attempt: BLOCKED.

## Verification observed before final documentation head

Implementation head `776d2836a73bb564e61dfb6b89871ac4d4b6e670`:
- Contracts 523: Controlled Remote Mutation Proof passed and all observed contract steps passed.
- Full DevOS 448: all observed jobs passed except `Verify Remote Mutation Controls v1`.

Focused Full 448 failure:
- `tools/verify-remote-mutation.py` required the literal phrase `actual provider evidence` in `core/remote-mutation-controls.md`.
- The rewritten contract still described the same provider-evidence rule but used different wording.
- This was a contract/verifier wording mismatch, not a runtime failure.

Repair:
- commit `f072bda4fb8110880878e69af82c99881b5f65f5` restored the exact phrase `actual provider evidence` while preserving the strengthened readback semantics.
- Fresh runs 524 / 449 / External 33 were triggered on that implementation repair head, but subsequent durable-state documentation changes supersede them for final closure evidence.

## Durable-state actions

- `.ai/CURRENT-STATE.md` now records the implementation, proof sequence, evidence status, and explicit live-provider limitation.
- `.ai/TASKS.md` distinguishes implemented provider-simulated proof from pending final verification and from unproven live mutation.
- `.ai/DECISIONS.md` records readback-as-completion evidence, one-attempt/no-replay semantics, and the separate explicit-authorization requirement for any future live-provider proof.
- This session file records the full audit/implementation/verification chain.

## Explicit non-claims

This PR does not prove:
- a live DevOS runtime `github.mutate.file` against a real repository;
- branch or PR mutation;
- workflow mutation;
- deployment/production mutation;
- database mutation;
- permission or credential/secret mutation;
- destructive mutation.

Normal GitHub repository edits used to implement this branch are development actions through the connected GitHub tool and are not treated as runtime-proof authorization/evidence.

## Safety invariants

- Provider credentials are not authorization.
- Provider mutation response is not verified completion.
- Mutation attempt count is at most one per governed attempt.
- Stale SHA blocks rather than overwrites.
- Any uncertain/failed post-mutation verification inherits `MUTATION_REPLAY_FORBIDDEN`.
- A future new mutation attempt is a new governed attempt requiring fresh remote state and fresh exact authorization/Security Gate evidence.
- No live production/destructive operation is authorized by this session.

## Remaining closure steps

1. Take fresh Contracts, Full DevOS and External Managed Project verification on the exact post-documentation head.
2. Repair only evidence-backed failures if any.
3. Confirm PR #14 mergeable.
4. Merge only at the exact verified final head.
5. Persist provider-simulated controlled mutation proof closure on `main`.
6. Build a production-readiness evidence matrix that clearly marks live-provider mutation as unproven unless separately explicitly authorized.
