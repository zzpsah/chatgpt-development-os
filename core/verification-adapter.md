# Verification Adapter v1

## Purpose

The Verification Adapter gives the Executable Development Runtime a controlled way to invoke **configured project verification commands** and convert their real results into DevOS evidence.

## Contract

```text
Verification request
  -> capability check
  -> command policy validation
  -> bounded execution
  -> exit status + safe output
  -> verification classification
  -> evidence record
```

## Command source

Commands must come from an explicit project configuration or a DevOS workflow. The adapter must not invent a project's test command from guesswork.

Supported command definitions should identify:

```yaml
verification:
  id: unit-tests
  command: "python -m pytest"
  working_directory: "."
  timeout_seconds: 300
  expected_exit_codes: [0]
```

## Result states

- `VERIFIED` — the configured check actually ran and met its declared success condition;
- `FAILED` — the configured check ran and failed its declared condition;
- `UNAVAILABLE` — required command/tooling was unavailable;
- `BLOCKED` — policy, authorization, or capability prevented execution;
- `PARTIAL` — execution produced useful but incomplete evidence.

`UNAVAILABLE` and `BLOCKED` must never be converted into `VERIFIED`.

## Safety

- Commands must be explicitly configured or authorized by the selected workflow.
- Timeouts must be bounded.
- Output must be treated as untrusted data and must not be executed again.
- Secrets must not be persisted in verification evidence.
- Production deployment commands are outside this adapter's default scope.
- Verification results do not grant implementation, merge, or deployment authority.

## Evidence

```yaml
evidence:
  verification_id: unit-tests
  status: VERIFIED | PARTIAL | FAILED | UNAVAILABLE | BLOCKED
  command: "configured command"
  exit_status: 0
  duration_seconds: 0
  output_reference: "safe-reference"
  limitations: []
```

The evidence describes what actually ran. A planned command or expected result is not evidence. The adapter must not invent command output or claim a check ran when it did not. It must also **do not invent** verification results when execution is unavailable or blocked.

## Runtime integration

The adapter is invoked through the Runtime–Adapter Execution Bridge. The runtime creates checkpoints around the operation and persists the verification outcome. The Verification / Test Engine remains authoritative for the overall project verification status.

## Non-goals

This contract is not a general shell-execution API, package installer, production deployment mechanism, or secret-management system.
