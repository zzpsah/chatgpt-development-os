# Development Task Workflow v1

## Purpose

Run a normal development request through the P9 Development Task Controller while preserving the existing DevOS authorities.

## Flow

1. Resolve the project.
2. Normalize the user's request into canonical intent.
3. Load durable context and resolve current state.
4. Define objective, acceptance criteria, bounded scope, and execution budget.
5. Decompose into work units when useful.
6. For each ready work unit, check capability and authorization.
7. Execute only through supported runtime/adapter capabilities.
8. Record actual changes and evidence immediately.
9. Checkpoint meaningful progress.
10. Run applicable verification.
11. Run Security Gate when the scope requires it.
12. Review aggregate results against the objective and acceptance criteria.
13. Persist semantic progress; deterministic automation records repository facts.
14. Continue only when another bounded, useful, authorized action exists.
15. Finish with COMPLETE, BLOCKED, FAILED, or ESCALATED plus evidence and next action.

## Task status transitions

```text
PLANNED -> IN_PROGRESS
IN_PROGRESS -> VERIFYING
IN_PROGRESS -> BLOCKED | NEEDS_APPROVAL | FAILED
VERIFYING -> COMPLETE | IN_PROGRESS | BLOCKED | FAILED | ESCALATED
NEEDS_APPROVAL -> IN_PROGRESS | ESCALATED
BLOCKED -> IN_PROGRESS only after the blocker is resolved
```

No transition may bypass authorization, capability, verification, or Security Gate requirements.

## Guardrails

- A work-unit success does not imply task completion.
- A provider success does not imply the project objective is complete.
- Missing capabilities are reported, not simulated.
- New high-risk scope requires fresh approval.
- Remote mutations remain governed by Remote Mutation Controls.
- Resumption re-checks state and does not blindly replay actions.

## Final result

The final report must state:

- objective and scope;
- work completed;
- files/resources changed;
- verification performed and actual status;
- security checks performed when applicable;
- blockers/unknowns/limitations;
- durable state updated;
- recommended next action.

See `core/development-task-controller.md` for the normative contract.
