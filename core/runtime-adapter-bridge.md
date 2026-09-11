# Runtime–Adapter Execution Bridge v1

## Purpose

The Runtime–Adapter Execution Bridge connects an authorized DevOS work unit to a concrete host adapter without allowing the adapter to bypass runtime controls.

## Contract

```text
Authorized work unit
  -> Runtime validates scope
  -> Runtime resolves capability
  -> Runtime checks authorization/security
  -> Adapter receives bounded operation
  -> Adapter executes or returns BLOCKED/FAILED/UNAVAILABLE
  -> Runtime normalizes evidence
  -> Runtime checkpoints
  -> Verification
  -> Outcome
```

## Request envelope

```yaml
request:
  id: unique-request-id
  work_unit: unique-unit-id
  operation: filesystem.read | filesystem.write_scoped | git.inspect | verification.run | other-declared-capability
  target: "explicit target"
  scope: "explicit bounded scope"
  authorization: NOT_REQUIRED | REQUIRED | ALREADY_GRANTED
  idempotency: IDEMPOTENT | SAFE_RETRY | NON_IDEMPOTENT | UNKNOWN
```

The bridge must reject a request whose target or scope is absent or ambiguous.

## Adapter response

```yaml
response:
  request_id: unique-request-id
  status: SUCCESS | BLOCKED | FAILED | UNAVAILABLE
  evidence: []
  changed_paths: []
  exit_status: null
  limitations: []
```

A response is evidence only when it comes from the adapter execution result or an explicitly supported delegation provider.

## Runtime controls

The bridge must enforce:

- capability status before execution;
- authorization before mutation;
- Security Gate requirements for security-sensitive work;
- project-root and target scope boundaries;
- checkpoint creation before and after mutation;
- bounded retry behavior;
- no secret persistence;
- no simulated adapter result.

## Reference implementation boundary

The v1 reference bridge supports the safe reference adapter operations:

- read text within the project root;
- write explicitly scoped text within the project root;
- inspect Git status/diff/log/HEAD.

Verification command execution and remote GitHub mutations remain separate capabilities and require their own adapter implementation and controls.

## Resume behavior

When resuming, the bridge uses checkpoint evidence and current repository state to determine whether an operation completed. Unknown completion is not treated as success. A non-idempotent or unknown-safe-retry operation must stop or escalate rather than replay automatically.

## Non-goals

The bridge is not a shell escape hatch, permission escalation mechanism, production deployment controller, or secret transport layer.
