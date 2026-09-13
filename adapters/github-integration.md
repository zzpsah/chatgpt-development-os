# GitHub External Adapter Profile v1

This profile maps supported GitHub operations to the External Integration Adapter and Remote Mutation Controls contracts.

## Read-only capabilities

- `github.inspect.repository`
- `github.inspect.commit`
- `github.inspect.pull_request`
- `github.inspect.workflow_run`
- `github.inspect.workflow_jobs`
- `github.inspect.status`
- `github.inspect.file`

These operations collect actual GitHub responses as evidence. `github.inspect.file` reads one repository-relative file and exists specifically to support fresh precondition evidence and post-mutation readback verification without granting mutation authority.

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
2. an authorized work unit for the specific mutation;
3. `security_gate: PASS` at the runtime bridge;
4. exact `owner/name` repository target;
5. repository-relative file path;
6. expected current file SHA;
7. actual provider response before reporting mutation-attempt `SUCCESS`.

Provider credentials do not constitute user authorization.

## Controlled mutation verification

A mature mutation proof must not treat the update response alone as final completion evidence.

Reference sequence:

`github.inspect.file → github.mutate.file → github.inspect.file → compare observed remote state → fresh applicable verification`

Rules:

- the pre-read supplies the current remote file SHA/content evidence;
- the mutation must use the exact expected SHA from current provider evidence;
- the mutation is attempted at most once;
- after a successful mutation response, a fresh `github.inspect.file` readback must observe the resulting remote state before the operation can be called verified;
- if mutation outcome is `UNVERIFIED`, inspect remote state before deciding any next action;
- if the expected SHA is stale/conflicting, stop and refresh current state rather than retrying blindly;
- failed post-mutation verification inherits the Failure + Recovery `MUTATION_REPLAY_FORBIDDEN` boundary.

## Concurrency and retry

A stale file SHA is treated as a concurrency conflict and must be inspected before another attempt. An uncertain provider response is `UNVERIFIED`; the runtime must inspect remote state before retrying. Mutation requests are never blindly retried.

## Evidence rules

A successful request must record the provider operation, target, result status, and a safe response reference. When a provider operation fails, the adapter reports the actual failure. When the integration is unavailable, it reports `UNAVAILABLE` rather than simulating a response.

A mutation is not considered **verified completion** until fresh readback/verification evidence confirms the intended remote state.

## Repository/source authority

Remote GitHub state is authoritative for GitHub resources. Local source/Git remains authoritative for the local implementation. The adapter must preserve this distinction when reconciling remote and local evidence.

## Credential boundary

Credentials are supplied by the host/provider integration. They are never copied into `.ai`, checkpoints, logs intended for project context, or adapter evidence.
