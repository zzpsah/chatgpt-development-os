# Autonomous Development Loop Workflow v1

## Trigger

Use the loop only when the user has authorized ongoing work toward a defined objective, or when the selected workflow explicitly permits bounded continuation. A normal one-step task does not need an autonomous loop.

## Flow

1. Resolve the project with the Project Router.
2. Normalize the request with the Human Language Execution Engine.
3. Load durable `.ai` context and run the AI State Resolver.
4. Establish objective, acceptance criteria, scope, and execution bound.
5. Plan/decompose through Agent Orchestration when useful.
6. Check required host capabilities before each tool-dependent action.
7. Check authorization and approval gates before each newly material scope.
8. Execute one bounded iteration.
9. Create a checkpoint with changes, evidence, verification, blockers, and authority state.
10. Run applicable verification and Security Gate checks.
11. Review the result against the objective and acceptance criteria.
12. Persist meaningful semantic progress to `.ai`; deterministic automation updates generated state.
13. Decide `CONTINUE`, `STOP`, or `ESCALATE` using the Autonomous Development Loop contract.
14. If `CONTINUE`, re-resolve relevant state before the next iteration; never blindly replay.
15. If `STOP` or `ESCALATE`, produce the evidence-backed result and remaining work.

## Decision guardrail

The loop may continue only when the next action is useful, bounded, capable, authorized, and not blocked by required verification or security review.

## Capability guardrail

If a required capability is unavailable, report `MISSING` or explicitly delegate to a supported host. Never simulate execution or claim an external result that was not obtained.

## Approval guardrail

New production-impacting, destructive, irreversible, security-sensitive, or data-affecting work requires the applicable explicit approval. Earlier authorization must not be stretched to cover materially new risk.

## Recovery guardrail

Failures are checkpointed and preserved. Safe retries may be considered only for the affected dependency chain. Destructive or irreversible actions are never automatically repeated.

## Completion rule

A loop is complete only when the objective is appropriately verified, or when the system has reached a justified stop/escalation condition with evidence and remaining work recorded.

See `core/autonomous-development-loop.md` for the normative contract.
