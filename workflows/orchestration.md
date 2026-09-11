# Agent Orchestration Workflow v1

## Trigger

Use orchestration when a request contains multiple meaningful engineering activities, cross-cutting dependencies, or work that benefits from explicit role separation. Do not orchestrate trivial one-step tasks.

## Flow

1. Resolve the project with the Project Router.
2. Normalize the request with the Human Language Execution Engine.
3. Load durable `.ai` context and resolve current state.
4. Determine whether the objective is small enough for direct execution.
5. If orchestration is useful, decompose the objective into minimal work units.
6. Assign only the roles required by scope, risk, and dependencies.
7. Identify which units can be parallel and which must be serialized.
8. Execute authorized units while preserving evidence at each handoff.
9. Reconcile conflicting findings before integration.
10. Run applicable verification and the Security Gate when required.
11. Review the integrated result against the original objective and acceptance criteria.
12. Persist meaningful semantic progress to `.ai` and let deterministic automation update generated state.
13. Report completed work, evidence, blockers, and limitations.

## Parallelism guardrails

Parallelize read-only or otherwise independent work only when outputs do not conflict. Serialize operations that modify shared files, databases, deployments, or other shared state unless the project provides a safe concurrency mechanism.

## Scope control

A newly discovered issue is not automatically part of the current objective. Classify it as related-but-deferred, blocker, or newly authorized work. Ask for authorization when the new action crosses an authorization boundary.

## Handoff rule

A work unit hands off an evidence packet containing its objective, result, evidence, assumptions/unknowns, verification, and blockers. Downstream roles consume the packet rather than relying on undocumented chat state.

## Failure rule

Do not hide failed units behind a successful aggregate result. The aggregate outcome must reflect failed, blocked, or unverified dependencies.

## Completion rule

`COMPLETE` means the objective is integrated and appropriately verified, not merely that all assigned units finished execution.

See `core/agent-orchestration.md` for the normative contract.
