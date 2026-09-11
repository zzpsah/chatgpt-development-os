# GitHub External Adapter Profile v1

This profile maps supported GitHub operations to the External Integration Adapter and Remote Mutation Controls contracts.

## Read-only capabilities

- `github.inspect.repository`
- `github.inspect.commit`
- `github.inspect.pull_request`
- `github.inspect.workflow_run`
- `github.inspect.workflow_jobs`
- `github.inspect.status`

These operations collect actual GitHub responses as evidence.

## Mutating capabilities

P8 currently enables only the controlled mutation:

- `github.mutate.file`

The operation updates one repository-relative file and requires an expected current file SHA. The reference adapter performs exactly one provider mutation attempt and does not automatically retry.

The following remain separately classified and unavailable in the reference implementation:

- `github.mutate.branch`
- `github.mutate.pull_request`
- `github.mutate.workflow`

Each future mutation requires its own bounded scope, authorization rules, applicable Security Gate/approval decision, and safe retry/idempotency contract.

## Mutation authorization

`github.mutate.file` requires:

1. `authorization: ALREADY_GRANTED`;
2. `security_gate: PASS` at the runtime bridge;
3. exact `owner/name` repository target;
4. repository-relative file path;
5. expected current file SHA;
6. actual provider response before reporting `SUCCESS`.

Provider credentials do not constitute user authorization.

## Concurrency and retry

A stale file SHA is treated as a concurrency conflict and must be inspected before another attempt. An uncertain provider response is `UNVERIFIED`; the runtime must inspect remote state before retrying. Mutation requests are never blindly retried.

## Evidence rules

A successful request must record the provider operation, target, result status, and a safe response reference. When a provider operation fails, the adapter reports the actual failure. When the integration is unavailable, it reports `UNAVAILABLE` rather than simulating a response.

## Repository/source authority

Remote GitHub state is authoritative for GitHub resources. Local source/Git remains authoritative for the local implementation. The adapter must preserve this distinction when reconciling remote and local evidence.

## Credential boundary

Credentials are supplied by the host/provider integration. They are never copied into `.ai`, checkpoints, logs intended for project context, or adapter evidence.
