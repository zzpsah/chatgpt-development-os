# Development Task Controller v1

## Purpose

The Development Task Controller is the P9 integration layer that connects the existing DevOS contracts into one evidence-driven development task lifecycle. It coordinates existing authorities; it does not replace them. P11 adds repository-first recovery, integrity validation, bounded derived-context self-healing, and provenance-aware handoff requirements to that lifecycle.

## Core contract

```text
User request
  -> Project + intent resolution
  -> P11 repository-first recovery / revalidation
  -> Durable state resolution
  -> Objective + acceptance criteria
  -> Orchestration / work units
  -> Capability + authorization checks
  -> Bounded execution
  -> Checkpoint
  -> P11 derived-context self-healing when needed
  -> Verification
  -> Security review when applicable
  -> Integration / review
  -> Durable state persistence + provenance-aware handoff
  -> Final evidence-backed outcome
```

## Controller responsibilities

1. Establish one explicit task identity and project scope.
2. Preserve the canonical intent produced by the Human Language Execution Engine.
3. Run P11 repository-first recovery and revalidation before material work.
4. Resolve current project state before material work.
5. Convert the objective into bounded work units through Agent Orchestration.
6. Require capability and authorization checks before execution.
7. Execute only supported, bounded actions through the runtime/adapters.
8. Collect evidence from actual execution and provider responses.
9. Invoke applicable verification and Security Gate checks.
10. Prevent a successful subtask from being mistaken for overall task completion.
11. When derived context is missing or malformed, invoke only deterministic P11 self-healing; never overwrite semantic decisions.
12. Persist meaningful semantic state and leave deterministic state generation to automation.
13. Produce a provenance-aware handoff containing the current Git/source reference and revalidation requirements when a session boundary is reached.
14. Produce a final result with completion status, evidence, limitations, blockers, and next action.

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
  recovery: REVALIDATED | RECONCILED | ESCALATED
  next_action: "specific next action or none"
```

## Completion semantics

`COMPLETE` requires:

- the objective and acceptance criteria are satisfied;
- applicable verification has actual evidence;
- required security review has completed;
- no unresolved material blocker remains hidden;
- meaningful progress is persisted;
- material conclusions have been revalidated against current repository/source evidence after a recovery or handoff boundary.

A task is not complete merely because code was changed, a work unit succeeded, or a provider returned success.

## Failure and recovery

When a work unit fails, preserve its evidence and dependency state. The controller may retry only when the underlying operation is safely retryable and remains authorized. Otherwise it transitions to `BLOCKED` or `ESCALATED`.

A resumed task must run repository revalidation and P11 recovery precedence before material action. It must not blindly replay the previous action. AI memory/chat history is supplementary and never authoritative.

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
- P11 Federation & Self-Healing: repository-first recovery, integrity, reconciliation, self-healing, and handoff provenance
- `.ai` + Git/source: durable implementation/state authority

## Non-goals

P9/P11 do not create unrestricted autonomy, bypass approval, replace existing authorities, invent execution results, silently rewrite semantic decisions, or automatically deploy production changes.
