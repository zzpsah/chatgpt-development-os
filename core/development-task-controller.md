# Development Task Controller v1

## Purpose

The Development Task Controller is the P9 integration layer that connects the existing DevOS contracts into one evidence-driven development task lifecycle. It coordinates existing authorities; it does not replace them.

## Core contract

```text
User request
  -> Project + intent resolution
  -> Durable state resolution
  -> Objective + acceptance criteria
  -> Orchestration / work units
  -> Capability + authorization checks
  -> Bounded execution
  -> Checkpoint
  -> Verification
  -> Security review when applicable
  -> Integration / review
  -> Durable state persistence
  -> Final evidence-backed outcome
```

## Controller responsibilities

1. Establish one explicit task identity and project scope.
2. Preserve the canonical intent produced by the Human Language Execution Engine.
3. Resolve current project state before material work.
4. Convert the objective into bounded work units through Agent Orchestration.
5. Require capability and authorization checks before execution.
6. Execute only supported, bounded actions through the runtime/adapters.
7. Collect evidence from actual execution and provider responses.
8. Invoke applicable verification and Security Gate checks.
9. Prevent a successful subtask from being mistaken for overall task completion.
10. Persist meaningful semantic state and leave deterministic state generation to automation.
11. Produce a final result with completion status, evidence, limitations, blockers, and next action.

## Task state

```yaml
task:
  id: unique-task-id
  project: resolved-project
  intent: canonical-intent
  objective: specific-outcome
  acceptance_criteria: []
  scope: bounded-scope
  status: PLANNED | IN_PROGRESS | BLOCKED | NEEDS_APPROVAL | VERIFYING | COMPLETE | FAILED | ESCALATED
  work_units: []
  evidence: []
  verification: VERIFIED | PARTIAL | UNVERIFIED | FAILED
  blockers: []
  unknowns: []
  authorization: NOT_REQUIRED | REQUIRED | ALREADY_GRANTED
  next_action: "specific next action or none"
```

## Completion semantics

`COMPLETE` requires:

- the objective and acceptance criteria are satisfied;
- applicable verification has actual evidence;
- required security review has completed;
- no unresolved material blocker remains hidden;
- meaningful progress is persisted.

A task is not complete merely because code was changed, a work unit succeeded, or a provider returned success.

## Failure and recovery

When a work unit fails, preserve its evidence and dependency state. The controller may retry only when the underlying operation is safely retryable and remains authorized. Otherwise it transitions to `BLOCKED` or `ESCALATED`.

A resumed task must re-resolve relevant state and must not blindly replay the previous action.

## Authorization boundary

The controller never manufactures authority. Planning, testing, prior low-risk approval, or provider credentials do not authorize a new high-risk operation. Remote mutation continues to be governed by Remote Mutation Controls.

## Evidence boundary

Only actual repository, runtime, test, security, or provider responses are execution evidence. Intentions, proposed commands, generated URLs, and AI assertions are not evidence of execution.

## Relationship to existing contracts

- Project Router: project identity
- Human Language Execution Engine: intent semantics
- AI State Resolver: current-state reasoning
- Agent Orchestration: decomposition and role coordination
- Autonomous Development Loop: bounded continuation
- Execution Runtime: executable actions
- Host/External Adapters: capabilities and provider boundaries
- Verification Engine: verification authority
- Security Gate: security authority
- `.ai` + Git/source: durable implementation/state authority

## Non-goals

P9 does not create unrestricted autonomy, bypass approval, replace existing authorities, invent execution results, or automatically deploy production changes.
