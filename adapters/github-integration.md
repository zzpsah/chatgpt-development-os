# GitHub External Adapter Profile v1

This profile maps supported GitHub operations to the External Integration Adapter contract.

## Read-only capabilities

- `github.inspect.repository`
- `github.inspect.commit`
- `github.inspect.pull_request`
- `github.inspect.workflow_run`
- `github.inspect.workflow_jobs`
- `github.inspect.status`

These operations collect actual GitHub responses as evidence.

## Mutating capabilities

The following are separately classified and must never be inferred from read access:

- `github.mutate.file`
- `github.mutate.branch`
- `github.mutate.pull_request`
- `github.mutate.workflow`

Each mutation requires an authorized work unit, target scope, and applicable Security Gate/approval decision.

## Evidence rules

A successful request must record the provider operation, target, result status, and a safe response reference. When a provider operation fails, the adapter reports the actual failure. When the integration is unavailable, it reports `UNAVAILABLE` rather than simulating a response.

## Repository/source authority

Remote GitHub state is authoritative for GitHub resources. Local source/Git remains authoritative for the local implementation. The adapter must preserve this distinction when reconciling remote and local evidence.

## Credential boundary

Credentials are supplied by the host/provider integration. They are never copied into `.ai`, checkpoints, logs intended for project context, or adapter evidence.
