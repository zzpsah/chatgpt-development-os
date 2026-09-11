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
  -> concurrency / expected-state validation
  -> bounded provider request
  -> actual provider response
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
- expected current state when the provider supports optimistic concurrency.

The adapter must reject malformed targets and scopes before making a provider request.

## Optimistic concurrency

For file updates, the provider's current file version/identifier must be supplied as an expected state (for GitHub Contents API this is the current blob SHA). A stale expected state must result in `BLOCKED` or an explicit provider conflict, never an unconditional overwrite.

This prevents a DevOS operation from silently destroying a concurrent remote change.

## Retry and idempotency

Mutations are not retried automatically after an uncertain provider response unless the operation has a verified idempotency mechanism.

For a failed request with a known non-committed outcome, bounded retry may be considered only when the provider contract makes the retry safe. Unknown outcome means `UNVERIFIED` until remote state is inspected.

## Security Gate

The Security Gate applies to remote mutations according to the operation's impact. Sensitive-data, credential, production, destructive, deployment, and permission-changing operations require the applicable security/approval decision before execution.

A mutation adapter must not bypass the Security Gate by treating provider credentials as authorization.

## Evidence

A successful mutation records only actual provider evidence:

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

A planned API call, generated URL, or AI statement is not evidence that a mutation occurred.

## Failure states

- `SUCCESS` — provider confirms the mutation;
- `FAILED` — provider returned a known failure;
- `BLOCKED` — DevOS policy, authorization, target, or concurrency validation prevented execution;
- `UNAVAILABLE` — provider capability/client is unavailable;
- `UNVERIFIED` — provider outcome is uncertain and remote state must be inspected before retrying.

## Credential boundary

Provider credentials remain in the host/provider credential system. They are never stored in `.ai`, checkpoints, logs, or mutation evidence.

## v1 scope

P8 v1 defines the safety contract and a provider-backed reference path for controlled GitHub file updates. Branch, pull-request, workflow, deployment, permission, and other higher-impact mutations remain separate capabilities until their specific contracts and tests exist.
