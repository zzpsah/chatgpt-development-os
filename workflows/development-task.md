# Development Task Workflow v1

## Purpose

Run a normal development request through the P9 Development Task Controller while preserving the existing DevOS authorities and the P11 federation/self-healing recovery contract.

## Flow

1. Resolve the project.
2. Normalize the user's request into canonical intent.
3. Run P11 repository-first recovery precedence and context freshness/integrity checks before relying on durable state.
4. Load durable context and resolve current state.
5. Define objective, acceptance criteria, bounded scope, and execution budget.
6. Decompose into work units when useful.
7. For each ready work unit, check capability and authorization.
8. Execute only through supported runtime/adapter capabilities.
9. Record actual changes and evidence immediately.
10. Checkpoint meaningful progress.
11. If derived context is missing or malformed, invoke bounded P11 self-healing; never overwrite semantic decisions.
12. Run applicable verification.
13. Run Security Gate when the scope requires it.
14. Review aggregate results against the objective and acceptance criteria.
15. Persist semantic progress; deterministic automation records repository facts.
16. Continue only when another bounded, useful, authorized action exists.
17. Finish with COMPLETE, BLOCKED, FAILED, or ESCALATED plus evidence and next action.

## Recovery on resumption

Every resumed task performs **repository revalidation** before material action. Recovery precedence is:

1. source tree + Git for exact implementation state;
2. explicit requirements + decisions for intent;
3. durable `.ai` state for project context and handoff;
4. generated indexes for navigation/evidence indexing;
5. AI memory/chat history as supplementary, never-authoritative context.

A stale handoff, missing derived file, or generated-index drift may be reconciled deterministically. Semantic conflicts escalate for review rather than being guessed or silently overwritten.

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
- P11 self-healing is bounded to deterministic derived context.
- P11 recovery never silently changes requirements or semantic decisions.

## Final result

The final report must state:

- objective and scope;
- work completed;
- files/resources changed;
- verification performed and actual status;
- security checks performed when applicable;
- blockers/unknowns/limitations;
- durable state updated;
- recovery/revalidation performed when applicable;
- recommended next action.

See `core/development-task-controller.md` for the normative contract.
