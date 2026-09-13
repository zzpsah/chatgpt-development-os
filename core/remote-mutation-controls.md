# Remote Mutation Controls v1

## Purpose

Remote Mutation Controls are the mandatory safety boundary for provider operations that change remote state. P8 builds on the read-only External Integration Adapter without treating remote access as permission to mutate.

## Mutation flow

```text
Mutation request
  -> declared capability
  -> target + scope validation
  -> explicit authorization
  -> Security Gate / approval when applicable
  -> fresh current-state read
  -> concurrency / expected-state validation
  -> bounded provider request (one mutation attempt)
  -> actual provider response
  -> fresh remote readback
  -> observed-state verification
  -> normalized evidence
  -> checkpoint
  -> outcome
```

## Authorization

A remote mutation is executable only when the work unit carries `ALREADY_GRANTED` authorization. Missing or ambiguous authorization is `BLOCKED`.

Authorization is operation-specific. Read access does not grant mutation access, and authorization for one target or operation must not be silently reused for another.

## Target and scope

Every mutation must identify:

- provider;
- operation;
- exact target resource;
- bounded mutation scope;
- exact current step/work unit;
- expected current state when the provider supports optimistic concurrency.

The adapter must reject malformed targets and scopes before making a provider request.

## Optimistic concurrency

For file updates, the provider's current file version/identifier must be supplied as an expected state (for GitHub Contents API this is the current blob SHA). A stale expected state must result in `BLOCKED` or an explicit provider conflict, never an unconditional overwrite.

A controlled proof must obtain the expected SHA from fresh provider evidence and verify it still matches before mutation.

This prevents a DevOS operation from silently destroying a concurrent remote change.

## Retry and idempotency

Mutations must not be retried automatically after an uncertain provider response unless the operation has a verified idempotency mechanism.

The reference `github.mutate.file` proof performs at most one mutation call per governed attempt.

For a failed request with a known non-committed outcome, any later attempt is a new governed attempt requiring freshly observed state and current authorization/security evidence. Unknown outcome means `UNVERIFIED` until remote state is inspected.

If a mutation was attempted and post-mutation verification is missing or fails, the outcome is HOLD under the Failure + Recovery `MUTATION_REPLAY_FORBIDDEN` rule rather than automatic replay.

## Security Gate

The Security Gate applies to remote mutations according to the operation's impact. The reference runtime bridge requires `security_gate: PASS` for `github.mutate.file`.

Sensitive-data, credential, production, destructive, deployment, and permission-changing operations require their applicable security/approval decision before execution and remain outside the controlled file-mutation proof unless separately authorized.

A mutation adapter must not bypass the Security Gate by treating provider credentials as authorization.

## Evidence

A provider mutation response is actual provider evidence that an attempt was accepted/processed; it is not sufficient by itself for DevOS to claim verified completion.

Mutation-attempt evidence may include:

```yaml
evidence:
  provider: github
  operation: github.mutate.file
  status: SUCCESS
  target: owner/repository
  scope: path
  expected_state: "provider version"
  response: {}
  attempt: 1
```

Verified completion additionally requires fresh remote readback (for the reference GitHub file path, `github.inspect.file`) proving the intended current state.

A planned API call, generated URL, provider credential, or AI statement is not evidence that a mutation occurred or completed correctly.

## Failure states

Adapter-level states:

- `SUCCESS` — provider confirms the mutation request result;
- `FAILED` — provider returned a known failure;
- `BLOCKED` — DevOS policy, authorization, target, or concurrency validation prevented execution;
- `UNAVAILABLE` — provider capability/client is unavailable;
- `UNVERIFIED` — provider outcome is uncertain and remote state must be inspected before any new mutation attempt.

Controlled-proof outcome:

- `VERIFIED` — exactly one authorized mutation attempt plus fresh readback proves the intended remote state;
- `BLOCKED` — required precondition failed before any mutation attempt;
- `HOLD` — a mutation was attempted but final state is uncertain/mismatched or fresh verification failed; mutation replay is forbidden.

## Credential boundary

Provider credentials remain in the host/provider credential system. They are never stored in `.ai`, checkpoints, logs, or mutation evidence.

## v1 scope

P8 v1 defines the safety contract and a provider-backed reference path for controlled GitHub file updates. The controlled maturity proof strengthens that path with fresh pre-read, exact SHA binding, one-attempt mutation, fresh readback, and no-replay semantics.

Branch, pull-request, workflow, deployment, permission, database, credential/secret, and other higher-impact mutations remain separate capabilities until their specific contracts, authorization and tests exist.
