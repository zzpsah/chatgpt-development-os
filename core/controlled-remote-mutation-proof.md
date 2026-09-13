# Controlled Remote Mutation Proof

Protocol: `DEVOS-CONTROLLED-MUTATION-v1`

## Purpose

Prove one bounded, non-production remote file mutation through existing DevOS Remote Mutation Controls without widening authority or introducing a general remote executor.

The proof composes:

`current provider read → exact expected-state check → explicit exact-step authorization → Security Gate → one mutation attempt → fresh provider readback → observed-state verification → recovery/no-replay decision`

## Scope

The reference proof supports only the already-declared GitHub operation:

- `github.mutate.file`

It does not enable branch, pull-request, workflow, deployment, database, credential, secret, or production mutations.

## Preconditions

Before a mutation attempt, all of the following are required:

1. exact repository `owner/name` target;
2. repository-relative file path;
3. exact current step/work-unit id;
4. current repository/work state already revalidated by normal DevOS gates;
5. `authorization: ALREADY_GRANTED` for the exact mutation attempt;
6. `security_gate: PASS`;
7. desired file content and commit message;
8. fresh `github.inspect.file` provider evidence;
9. expected SHA supplied by the caller must exactly equal the fresh provider file SHA.

Credentials supplied by the provider are not authorization.

## Execution rule

The mutation adapter is invoked at most once per proof attempt.

No exception, timeout, provider uncertainty, stale SHA, readback mismatch, failed verification, or prior success may trigger an automatic second mutation call.

## Post-mutation readback

A successful provider update response is mutation-attempt evidence, not verified completion.

After the mutation attempt, DevOS must perform a fresh read-only `github.inspect.file` call and compare observed remote state with the intended state.

Verified completion requires:

- readback status `SUCCESS`;
- observed path equals the requested path where the provider exposes it;
- observed content equals intended content;
- observed file SHA is present;
- observed file SHA is not the stale precondition SHA when the provider reports a changed object;
- no second mutation attempt occurred.

## Outcomes

### `VERIFIED`

One authorized mutation attempt occurred and fresh provider readback proves the intended state.

### `BLOCKED`

No mutation attempt occurs when:

- authorization is absent;
- Security Gate is absent/fails;
- project/path/step metadata is invalid;
- pre-read fails;
- expected SHA does not match fresh provider state;
- mutation capability is unavailable.

### `HOLD`

Automatic replay is forbidden when:

- provider mutation outcome is uncertain (`UNVERIFIED`);
- a mutation attempt succeeded but readback fails or does not match intended state;
- fresh post-mutation verification is missing/failed;
- any evidence makes it unclear whether the mutation took effect.

`HOLD` inherits the Failure + Recovery Proof's `MUTATION_REPLAY_FORBIDDEN` boundary.

## Recovery rule

After any attempted mutation that does not reach `VERIFIED`, the next action is inspection/reconciliation, never automatic mutation replay.

A new mutation attempt, if ever justified, must be a new governed attempt with freshly observed remote state and fresh exact-step authorization/Security Gate evidence as applicable.

## Safety invariant

> A provider mutation response is not completion. DevOS may claim success only after fresh observed remote state verifies the intended result, and it must never blindly retry an uncertain mutation.
