# Development Task Controller v1

## Purpose

The Development Task Controller is the P9 integration layer that connects the existing DevOS contracts into one evidence-driven development task lifecycle. P11 adds repository-first recovery, integrity validation, bounded derived-context self-healing, and provenance-aware handoff requirements to that lifecycle. P12 adds Operational Intelligence as an advisory decision-support layer. P16 adds the Semantic Goal-to-Plan Compiler as a non-executing, non-authorizing planning layer between resolved semantic intent/state and bounded task orchestration.

## Core contract

```text
User request
  -> Human Language Execution Engine
  -> Project + intent resolution
  -> P11 repository-first recovery / revalidation
  -> Durable state resolution
  -> P16 Semantic Goal-to-Plan Compiler
  -> Compiled bounded plan + dependencies + constraints + authority classes + verification obligations
  -> P12 operational analysis (advisory)
  -> Advisory next-action signal
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
5. Compile the resolved objective through P16 before orchestration. The controller may consume only `PLANNED` compiler output; `CLARIFY` and `BLOCKED` remain non-executable states.
6. Preserve every compiled negative constraint, explicit dependency, authority requirement, verification obligation, and stop/escalation condition when converting plan steps into downstream work units.
7. Treat P16 authority classes as gating metadata only. They never grant permission and never weaken Security Gate or operation-specific authorization requirements.
8. Run P12 Operational Intelligence against the current task inventory to expose dependency readiness, advisory priority, checkpoint signals, failure/evidence analysis, and an advisory next action.
9. Treat P12 recommendations as advisory only; never convert a ranking, checkpoint signal, or next-action recommendation into authority.
10. Treat an OI `work_on:<task>` result only as a candidate work item; the controller must independently validate scope, dependencies, capability, authorization, and current repository state before execution.
11. If OI recommends `resolve:<task>`, route the blocker through the existing dependency, capability, authorization, verification, security, or recovery authority instead of bypassing it.
12. If OI returns `no_action`, preserve the explicit no-action/unknown state rather than inventing work.
13. Convert only compiled bounded plan steps into work units through Agent Orchestration.
14. Require capability and authorization checks before execution.
15. Execute only supported, bounded actions through the runtime/adapters.
16. Collect evidence from actual execution and provider responses.
17. Invoke applicable verification and Security Gate checks.
18. Prevent a successful subtask from being mistaken for overall task completion.
19. When derived context is missing or malformed, invoke only deterministic P11 self-healing; never overwrite semantic decisions.
20. Persist meaningful semantic state and leave deterministic state generation to automation.
21. Produce a provenance-aware handoff containing the current Git/source reference and revalidation requirements when a session boundary is reached.
22. Produce a final result with completion status, evidence, limitations, blockers, and next action.

## P16 compiled-plan boundary

`tools/semantic-goal-to-plan.py` is the deterministic reference compiler. It receives an already interpreted intent/objective plus resolved project, constraints, and ambiguity. It returns `DEVOS-GOAL-PLAN-v1` with one of `PLANNED`, `CLARIFY`, or `BLOCKED`.

A `PLANNED` envelope still returns `authorization: UNCHANGED`, `authority: UNCHANGED`, and `execution: NONE`. The controller must independently revalidate repository state, dependencies, capability, authorization, Security Gate state, and verification applicability before a plan step can become an execution candidate.

A compiler decision of `CLARIFY` or `BLOCKED` must never be converted into executable work merely because P12 ranks the task highly or a prior task succeeded.

## Executable P12 decision envelope

`tools/development-task-controller.py` is the reference implementation of the controller decision boundary. It consumes the task inventory plus **independent** controller inputs: current repository head, per-task capability state, existing authorization state, and Security Gate state. It first obtains the OI recommendation, then independently validates scope, readiness, repository revalidation, capability, authorization, and security.

Its only outcomes are `EXECUTION_CANDIDATE`, `BLOCKED`, and `NO_ACTION`. An `EXECUTION_CANDIDATE` has `authority: UNCHANGED`, `authorization: UNCHANGED`, and `execution: NONE`; it can be passed to `tools/devos-runtime-handoff.py`, which creates a `READY_FOR_RUNTIME` work-unit envelope without running it. OI remains `ADVISORY_ONLY` throughout.

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
  compiled_plan:
    protocol: DEVOS-GOAL-PLAN-v1
    decision: PLANNED | CLARIFY | BLOCKED
    steps: []
    constraints: []
    authority_requirements: []
    verification_requirements: []
  work_units: []
  evidence: []
  verification: VERIFIED | PARTIAL | UNVERIFIED | FAILED
  blockers: []
  unknowns: []
  authorization: NOT_REQUIRED | REQUIRED | ALREADY_GRANTED
  recovery: REVALIDATED | RECONCILED | ESCALATED
  next_action: "specific next action or none"
  operational_intelligence:
    advisory_next_action: null
    priority_reasons: []
    checkpoint_signals: []
    failure_classifications: []
    evidence_records: []
```

## Completion semantics

`COMPLETE` requires:

- the objective and acceptance criteria are satisfied;
- applicable verification has actual evidence;
- required security review has completed;
- no unresolved material blocker remains hidden;
- meaningful progress is persisted;
- material conclusions have been revalidated against current repository/source evidence after a recovery or handoff boundary.

A task is not complete merely because a plan compiled, code was changed, a work unit succeeded, a provider returned success, or Operational Intelligence ranked the work highly.

## Failure and recovery

When a work unit fails, preserve its evidence and dependency state. The controller may retry only when the underlying operation is safely retryable and remains authorized. Otherwise it transitions to `BLOCKED` or `ESCALATED`.

A resumed task must run repository revalidation and P11 recovery precedence before material action. It must not blindly replay the previous action. AI memory/chat history is supplementary and never authoritative.

A previously compiled plan must also be revalidated when repository state, project identity, constraints, or authorization-relevant conditions have materially changed. Compilation is not durable permission.

## Authorization boundary

The controller never manufactures authority. Planning, compiler classification, testing, prior low-risk approval, provider credentials, OI priority, or an OI next-action recommendation do not authorize a new high-risk operation. Remote mutation continues to be governed by Remote Mutation Controls.

P12 priority, checkpoint, failure classification, evidence normalization, and next-action signals are never authorization. `UNAUTHORIZED` readiness must continue through the existing approval/capability path rather than being bypassed by a high priority score.

## Evidence boundary

Only actual repository, runtime, test, security, or provider responses are execution evidence. Intentions, proposed commands, compiled plan steps, generated URLs, and AI assertions are not evidence of execution. P12 recommendations must retain their supporting operational evidence and must not be presented as execution evidence.

## Relationship to existing contracts

- Human Language Execution Engine: top-level intent semantics
- Project Router: project identity
- AI State Resolver: current-state reasoning
- Semantic Goal-to-Plan Compiler (P16): bounded dependency-aware planning, constraints, authority classes, verification obligations, and ambiguity preservation
- Agent Orchestration: decomposition and role coordination from compiled plan steps
- Autonomous Development Loop: bounded continuation
- Operational Intelligence: dependency/readiness analysis, advisory prioritization, checkpoint signals, failure/evidence intelligence, and advisory next-action generation
- Execution Runtime: executable actions
- Host/External Adapters: capabilities and provider boundaries
- Verification Engine: verification authority
- Security Gate: security authority
- P11 Federation & Self-Healing: repository-first recovery, integrity, reconciliation, self-healing, and handoff provenance
- `.ai` + Git/source: durable implementation/state authority

## Non-goals

P9/P11/P12/P16 do not create unrestricted autonomy, bypass approval, replace existing authorities, invent execution results, silently rewrite semantic decisions, or automatically deploy production changes.