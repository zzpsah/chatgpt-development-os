# Current State

## Snapshot

- Repository: `zzpsah/chatgpt-development-os`.
- Source tree + Git are authoritative; ChatGPT Memory/chat history are supplementary only.
- P11 repository-first recovery/revalidation remains a durable invariant.
- P9 through P17 are complete on `main`.
- Production E2E Harness, Failure + Recovery Proof, and Multi-Session / Fresh-AI Continuation Proof are verified and closed.
- Active maturity gate: **Controlled Remote Mutation Proof**, PR #14 on `devos/controlled-remote-mutation-proof`.
- This gate is currently **provider-simulated / contract-level only**. No new live DevOS runtime remote mutation has been authorized or executed as proof.

## Canonical governed path

`Human request → P15 interpretation → P16 plan → P17 readiness → controller → bounded runtime → verification → persistence → recovery / continuation`

Interpretation, planning, readiness, provider credentials, prior approvals, prior successful runs, recovery checkpoints, and continuation packets never manufacture permission.

## Multi-Session / Fresh-AI Continuation closure

PR #13 merged at `cd8524b11f923e5e29eeaf445869b6239954ed1f` from final source head `99822037a9e24625f2e7c216300c4aabd94e134e` after:
- Contracts 518 / `34757017554`: success.
- Full DevOS 443 / `34757017532`: success.
- External Managed Project 31 / `34757017535`: success.

## Active Controlled Remote Mutation Proof

Normative contract: `core/controlled-remote-mutation-proof.md`.
Supervisor: `tools/controlled-remote-mutation-proof.py`.
Regression corpus: `tools/test-controlled-remote-mutation-proof.py`.
Existing mutation capability under proof: `github.mutate.file` only.
New read-only verification capability: `github.inspect.file`.

### Maturity gap being closed

The existing GitHub mutation adapter already required explicit `ALREADY_GRANTED` authorization, Security Gate PASS, repository-relative path confinement, expected current SHA, and a single provider mutation attempt. The missing maturity evidence was fresh provider readback: a successful update response alone could not prove the resulting remote file state.

### Implemented proof sequence

`fresh github.inspect.file → exact SHA match → exact-step authorization + Security Gate → one github.mutate.file attempt → fresh github.inspect.file readback → compare observed content/SHA → VERIFIED or HOLD`

Rules now proven by provider-simulated tests:
- missing exact authorization blocks before provider read/mutation;
- missing Security Gate PASS blocks before mutation;
- stale expected SHA blocks before mutation;
- exactly one mutation call is allowed per governed attempt;
- successful provider update is mutation-attempt evidence, not verified completion;
- fresh readback must observe intended content and a current SHA before `VERIFIED`;
- conflict or failed/mismatched readback produces `HOLD` with replay forbidden;
- an uncertain provider response may be reconciled by fresh readback if the intended state is observed, but the mutation is never reissued automatically;
- invalid/out-of-repository paths block.

### Contract/runtime changes

- `adapters/github-reference.py` adds bounded read-only `github.inspect.file` / `get_file` provider support.
- `tools/runtime-adapter-bridge.py` routes `github.inspect.file` under `NOT_REQUIRED` authorization while preserving the existing mutation gate.
- `core/runtime-adapter-bridge.md`, `core/remote-mutation-controls.md`, and `adapters/github-integration.md` now require fresh readback/observed-state verification for controlled file mutation maturity claims.
- `tools/verify-remote-mutation.py` and existing GitHub/runtime bridge tests are strengthened.
- Contracts CI includes `Verify Controlled Remote Mutation Proof`.

### Verification observed before final semantic-state head

Implementation head `776d2836a73bb564e61dfb6b89871ac4d4b6e670`:
- Contracts 523: Controlled Remote Mutation Proof and all observed contract steps passed.
- Full DevOS 448: all observed jobs passed except `Verify Remote Mutation Controls v1`.
- The Full 448 failure was a literal documentation-verifier mismatch only: `core/remote-mutation-controls.md` still described provider evidence but no longer contained the exact phrase `actual provider evidence` required by `tools/verify-remote-mutation.py`.
- Commit `f072bda4fb8110880878e69af82c99881b5f65f5` restored that wording without changing runtime behavior.

Because this durable-state update changes the branch head, fresh exact-head Contracts + Full DevOS + External Managed Project verification is required before PR #14 can merge.

## Explicit unproven boundary

This PR does **not** prove a live DevOS runtime mutation against a real repository/provider resource. Normal GitHub development commits made while implementing DevOS are not counted as runtime-proof authorization/evidence.

Still unproven / out of scope without separate explicit authorization:
- live real-provider `github.mutate.file` proof;
- branch mutation;
- pull-request mutation;
- workflow mutation;
- deployment/production mutation;
- database mutation;
- permission/credential/secret mutation;
- destructive mutation.

## Closure gate

PR #14 may close only after the exact final head:
1. remains mergeable;
2. passes Contracts, including the controlled mutation proof;
3. passes Full DevOS, including Remote Mutation Controls and repository-only recovery;
4. passes applicable External Managed Project read-only proofs;
5. has durable task/decision/session provenance.

After this provider-simulated proof closes, DevOS should produce a production-readiness evidence matrix that clearly distinguishes proven, simulated, real-provider, and unproven paths. A live mutation proof, if ever desired, requires separate explicit authorization for the exact target/path/operation.

## Recovery precedence

1. Current source tree + Git.
2. Explicit requirements/decisions.
3. `.ai/CURRENT-STATE.md`, `.ai/TASKS.md`, and semantic `.ai` state.
4. `.ai/SESSIONS/` provenance.
5. Generated indexes as navigation/evidence only.
6. ChatGPT Memory/chat history as supplementary context only.

Exact implementation remains authoritative in Git history.
