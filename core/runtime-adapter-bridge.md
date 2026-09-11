# Runtime–Adapter Execution Bridge v1

## Purpose

The Runtime–Adapter Execution Bridge connects an authorized DevOS work unit to a concrete host or external integration adapter without allowing the adapter to bypass runtime controls.

## Contract

```text
Authorized work unit
  -> Runtime validates scope
  -> Runtime resolves capability
  -> Runtime checks authorization/security
  -> Adapter receives bounded operation
  -> Adapter executes or returns BLOCKED/FAILED/UNAVAILABLE/UNVERIFIED
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
  operation: filesystem.read | filesystem.write_scoped | git.inspect | verification.run | github.inspect.repository | github.inspect.commit | github.inspect.workflow_run | github.mutate.file | other-declared-capability
  target: "explicit target"
  scope: "explicit bounded scope"
  authorization: NOT_REQUIRED | REQUIRED | ALREADY_GRANTED
  security_gate: PASS | CONDITIONAL | BLOCKED | NOT_APPLICABLE | UNVERIFIED
  idempotency: IDEMPOTENT | SAFE_RETRY | NON_IDEMPOTENT | UNKNOWN
```

The bridge must reject a request whose target or scope is absent or ambiguous.

## Adapter response

```yaml
response:
  request_id: unique-request-id
  status: SUCCESS | BLOCKED | FAILED | UNAVAILABLE | UNVERIFIED
  evidence: []
  changed_paths: []
  exit_status: null
  limitations: []
```

A response is evidence only when it comes from the adapter execution result or an explicitly supported delegation provider.

## Runtime controls

The bridge must enforce:

- capability status before execution;
- explicit authorization before mutation;
- Security Gate requirements for applicable security-sensitive or high-impact work;
- project-root and target scope boundaries;
- checkpoint creation before and after mutation;
- bounded retry behavior;
- no secret persistence;
- no simulated adapter result.

## External integration bridge

The reference bridge may route declared GitHub operations to the provider-backed GitHub adapter.

Read-only operations:

- `github.inspect.repository` — inspect a repository identified by `owner/name`;
- `github.inspect.commit` — inspect a commit within a declared repository;
- `github.inspect.workflow_run` — inspect a workflow run within a declared repository.

Controlled mutation in P8:

- `github.mutate.file` — update one explicitly scoped repository file using an expected current file SHA.

For read-only operations the bridge must:

1. validate the repository and operation-specific scope;
2. resolve the external capability as `AVAILABLE`, `DELEGATABLE`, or `MISSING`;
3. require `NOT_REQUIRED` authorization;
4. pass the request only to the declared provider adapter;
5. return only the actual provider response as execution evidence;
6. preserve bounded retry semantics owned by the external adapter;
7. never accept or persist provider credentials in the request/checkpoint.

For `github.mutate.file` the bridge must:

1. require `ALREADY_GRANTED` authorization;
2. require `security_gate: PASS`;
3. require an exact repository target and repository-relative file scope;
4. require the provider's expected current file SHA;
5. execute one mutation without automatic retry;
6. classify known concurrency conflicts as `BLOCKED`;
7. classify uncertain provider completion as `UNVERIFIED` and require remote inspection before retry;
8. return the actual provider response as evidence.

## Reference implementation boundary

The v1 reference bridge supports:

- read text within the project root;
- write explicitly scoped text within the project root;
- inspect Git status/diff/log/HEAD;
- bounded read-only GitHub repository, commit, and workflow-run inspection;
- one controlled GitHub file-update capability with explicit authorization, Security Gate PASS, and optimistic concurrency.

Branch, pull-request, workflow, deployment, permission, and other higher-impact remote mutations remain separate capabilities until their specific controls and tests exist.

## Resume behavior

When resuming, the bridge uses checkpoint evidence and current repository state to determine whether an operation completed. Unknown completion is not treated as success. A non-idempotent or unknown-safe-retry operation must stop or escalate rather than replay automatically.

## Non-goals

The bridge is not a shell escape hatch, permission escalation mechanism, production deployment controller, remote mutation bypass, or secret transport layer.
