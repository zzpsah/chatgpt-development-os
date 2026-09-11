# External Integration Adapter v1

## Purpose

The External Integration Adapter defines the boundary for DevOS operations against remote systems such as GitHub and CI providers. Local repository access does not imply permission to mutate a remote system.

## Contract

```text
External work unit
  -> provider capability discovery
  -> target + scope validation
  -> authorization / Security Gate
  -> bounded remote request
  -> actual provider response
  -> normalized evidence
  -> checkpoint
  -> outcome
```

## Capability states

```yaml
capability:
  provider: github
  operation: inspect_ci
  status: AVAILABLE | DELEGATABLE | MISSING
  authorization: NOT_REQUIRED | REQUIRED | ALREADY_GRANTED
```

`MISSING` or `DELEGATABLE` must never be represented as successful execution.

## v1 operation classes

### Read-only

- inspect repository metadata;
- inspect commits, branches, pull requests, and workflow runs;
- inspect CI status and actual job evidence.

### Mutating

- create/update files or branches;
- create/update pull requests;
- trigger supported workflows;
- other explicitly declared provider operations.

Remote mutations require an authorized work unit and applicable security/approval gates.

## Evidence

```yaml
evidence:
  provider: github
  operation: inspect_ci
  status: SUCCESS | FAILED | BLOCKED | UNAVAILABLE
  response_reference: "safe provider reference"
  observed: []
  limitations: []
```

Only an actual provider response is execution evidence. A planned API call, generated URL, or AI statement is not evidence that the remote action occurred.

## Retry semantics

Retries must be bounded and operation-aware. Read-only operations may be retried when safe. Non-idempotent remote mutations require an idempotency mechanism or explicit confirmation before retrying after uncertain completion.

## Security

- provider credentials remain in the host/provider credential system, never in `.ai` or checkpoints;
- sensitive response data must be minimized before persistence;
- authorization is checked per operation class;
- production-impacting or data-affecting remote operations remain behind applicable approval and Security Gate rules.

## Non-goals

This contract does not define provider credentials, unrestricted remote control, automatic production deployment, or permission escalation.
