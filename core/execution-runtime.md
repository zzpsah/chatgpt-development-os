# Executable Development Runtime v1

## Purpose

The Executable Development Runtime turns an authorized autonomous-loop iteration into a bounded sequence of real tool actions. It is an execution contract, not unrestricted autonomy.

## Core contract

```text
Work unit
  -> Capability resolution
  -> Authorization gate
  -> Pre-action checkpoint
  -> Execute bounded action
  -> Capture evidence
  -> Post-action checkpoint
  -> Verification
  -> Persist
  -> Return outcome
```

The runtime must distinguish **decision**, **execution**, and **evidence**. An AI decision is not evidence that an action happened.

## Execution states

- `PLANNED` — action is defined but not started;
- `READY` — capability and authorization prerequisites are satisfied;
- `IN_PROGRESS` — execution has started;
- `BLOCKED` — required capability, authority, input, or dependency is unavailable;
- `COMPLETE` — action finished and required evidence was captured;
- `FAILED` — action was attempted and failed;
- `CANCELLED` — execution was intentionally stopped before completion.

## Capability registry

Every tool-dependent action resolves a capability record:

```yaml
capability:
  name: run_tests
  status: AVAILABLE | DELEGATABLE | MISSING
  provider: "host/tool identifier"
  evidence: []
```

`DELEGATABLE` requires an explicit supported delegation boundary. `MISSING` means execution cannot be claimed.

## Work-unit execution

A runtime executor receives an already authorized work unit and must:

1. validate the objective and scope;
2. resolve required capabilities;
3. confirm authorization and applicable Security Gate conditions;
4. create a pre-action checkpoint;
5. execute only the bounded action;
6. capture actual output/evidence;
7. create a post-action checkpoint;
8. invoke applicable verification;
9. persist the outcome;
10. return `COMPLETE`, `FAILED`, `BLOCKED`, or `CANCELLED`.

The executor must not silently expand scope or convert a failed action into success.

## Checkpoint contract

A checkpoint must identify:

```yaml
checkpoint:
  id: unique-checkpoint-id
  objective: "specific outcome"
  iteration: 1
  work_unit: "unit-id"
  repository_head: "commit or UNKNOWN"
  status: PLANNED | IN_PROGRESS | COMPLETE | FAILED | BLOCKED | CANCELLED
  changes: []
  evidence: []
  verification: VERIFIED | PARTIAL | UNVERIFIED | FAILED
  blockers: []
  next_action: "bounded next action or STOP/ESCALATE"
```

Checkpoints must contain enough information to prevent blind replay. They must not store secrets, credentials, session cookies, private keys, or unnecessary sensitive data.

## Resume contract

A resumed runtime must:

- load the latest valid checkpoint;
- compare repository/source state with the checkpoint;
- re-resolve capabilities and authorization;
- inspect incomplete work and dependencies;
- determine whether the previous action actually completed;
- continue only with a safe, authorized next action.

If completion cannot be established from evidence, the runtime must not claim completion. It may re-check or safely retry only when the action is idempotent or otherwise explicitly safe. **The runtime must never blindly replay an uncertain action.**

## Evidence contract

Execution evidence is factual output from the host or delegated provider. Examples include command exit status, test output, Git diff, file state, or an external system response actually obtained by the runtime.

The runtime must never fabricate command output, file changes, test results, deployment state, or external-system responses.

## Safety boundaries

- No authorization is created by the runtime.
- Production, destructive, irreversible, security-sensitive, and data-affecting operations remain gated by explicit approval.
- Secrets are not written to checkpoints or `.ai` merely to support execution.
- Tool failure is not project failure unless the evidence establishes a project failure.
- The runtime cannot claim an action was executed when the host lacked the required capability.

## Non-goals

Runtime v1 does not define a universal command runner, unrestricted production deployment, secret management system, or autonomous authority model. Hosts may implement adapters, but each adapter must preserve this contract.
