# Host Adapter Contract v1

## Purpose

The Host Adapter Contract defines the safe boundary between the Executable Development Runtime and the capabilities provided by a machine, AI host, CI system, or external integration.

A host adapter exposes capabilities; it does not create authorization.

## Core contract

```text
Runtime request
  -> Capability lookup
  -> Adapter validation
  -> Authorization / Security Gate
  -> Bounded operation
  -> Actual result
  -> Evidence normalization
  -> Runtime checkpoint
```

## Capability model

```yaml
capability:
  name: inspect_git
  provider: host-adapter-name
  status: AVAILABLE | DELEGATABLE | MISSING
  operations:
    - status
    - diff
    - log
  risk: LOW | MEDIUM | HIGH
  evidence: []
```

The adapter must report `MISSING` when it cannot perform an operation. It must not simulate a result.

## v1 capability families

### Filesystem

- inspect files/directories;
- read text files;
- create or modify explicitly scoped text files;
- report resulting file state.

### Git

- inspect branch and HEAD;
- inspect status and diff;
- inspect commit history;
- create commits only when the host and authorization explicitly permit it.

### Verification

- invoke configured project verification commands when available;
- capture exit status and output as evidence;
- distinguish unavailable tooling from a failed project check.

### GitHub / CI

- inspect repository and workflow evidence when the host has the required integration;
- delegate operations when supported;
- never claim an external action occurred without an actual response.

## Scope boundary

Every mutating operation must carry an explicit scope. The adapter must reject or escalate operations whose scope cannot be established.

Examples:

```yaml
operation:
  kind: write_file
  target: "src/example.py"
  scope: "modify only the requested function"
  authorization: ALREADY_GRANTED
```

The adapter must not expand a requested target into unrelated files merely because they appear convenient.

## Safety boundary

- The adapter never grants permission.
- Production, destructive, irreversible, security-sensitive, and data-affecting operations remain gated.
- Secrets, tokens, credentials, private keys, and session cookies must not be returned as evidence or persisted into `.ai` checkpoints.
- Shell or command execution, when supported by a host, must be separately capability-declared and bounded; it is not implied by filesystem or Git access.
- Failed, timed-out, or unavailable operations must remain distinguishable from successful execution.

## Evidence contract

A successful adapter operation returns structured evidence describing what actually happened:

```yaml
evidence:
  operation: inspect_git
  status: SUCCESS | FAILED | BLOCKED | UNAVAILABLE
  provider: host-adapter-name
  observed: []
  exit_status: null
  output_reference: "optional-safe-reference"
  limitations: []
```

Evidence must be factual and reproducible where practical. The adapter must never fabricate command output, file changes, test results, or external responses.

## Failure handling

Adapters return `BLOCKED` for missing authority/capability/dependency and `FAILED` for an attempted operation that failed. The runtime decides whether to retry, delegate, stop, or escalate.

Retries must be bounded. Potentially non-idempotent operations must not be blindly replayed.

## Portability

Host-specific implementation details belong in adapter modules. The project `.ai` context and runtime contracts must remain independent of any single vendor, account, machine, operating system, or IDE.

## Non-goals

This contract does not define a universal shell runner, secret manager, production deployment mechanism, or unrestricted host-control API.
