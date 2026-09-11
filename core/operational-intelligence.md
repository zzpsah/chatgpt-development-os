# DevOS Operational Intelligence v1

## Purpose

Operational Intelligence is the P12 decision-support layer for turning the current Development Task Controller state into an evidence-backed operational view.

It coordinates existing DevOS authorities; it does not replace authorization, execution, verification, Security Gate, or repository recovery rules.

## Core contract

```text
Repository + durable .ai state
          ↓
      Task inventory
          ↓
   Dependency graph
          ↓
 Readiness / blockers
          ↓
 Priority + checkpoint signals
          ↓
 Evidence-backed next action
```

## Task graph model

Each task/work unit is represented as a node:

```yaml
node:
  id: stable-task-id
  objective: specific-outcome
  status: PLANNED | IN_PROGRESS | BLOCKED | NEEDS_APPROVAL | VERIFYING | COMPLETE | FAILED | ESCALATED
  priority: integer
  dependencies: [stable-task-id]
  evidence: []
  checkpoint: null
  next_action: specific-action
  effort: non-negative-integer
  age_days: non-negative-integer
  deadline_days: integer-or-null
```

Dependencies are directed edges from prerequisites to dependent work. A task is `READY` only when its required dependencies are satisfied and its authorization/capability conditions permit execution.

## Dependency intelligence

The engine must:

1. preserve explicit dependencies from durable task state;
2. distinguish `READY`, `WAITING`, `BLOCKED`, and `UNAUTHORIZED` work;
3. detect missing dependency references rather than guessing them;
4. detect dependency cycles and surface them as blockers;
5. never infer completion merely from priority or proximity in the graph;
6. retain evidence for every readiness decision.

## Priority intelligence

Priority is a decision-support signal, not authority. The deterministic baseline scores unfinished work from explicit priority plus bounded operational signals:

- explicit user/project priority (dominant baseline);
- dependency criticality, measured by unfinished direct dependents;
- blocked/failed status penalty;
- age/staleness;
- deadline urgency when supplied;
- estimated bounded effort penalty when supplied.

The engine exposes each scoring reason. It never silently changes the stored user-defined priority, and a ranking never authorizes execution.

## Checkpoint intelligence

A checkpoint signal identifies when the controller should persist or revalidate state. Recognized events are:

- `REPOSITORY_CHANGE`
- `WORK_UNIT_COMPLETE`
- `WORK_UNIT_FAILED`
- `BLOCKED_TRANSITION`
- `AUTHORIZATION_CHANGE`
- `VERIFICATION_RESULT`
- `SECURITY_RESULT`
- `SESSION_BOUNDARY`
- `HANDOFF_BOUNDARY`

Unknown events are surfaced as non-checkpoint signals rather than guessed. Checkpoint recommendations do not authorize an action; they preserve recoverability.

## Failure classification

Operational Intelligence classifies failures without rewriting their raw evidence. Initial classes:

- `CAPABILITY_MISSING`
- `AUTHORIZATION_REQUIRED`
- `DEPENDENCY_BLOCKED`
- `VERIFICATION_FAILED`
- `SECURITY_BLOCKED`
- `PROVIDER_FAILURE`
- `REPOSITORY_DRIFT`
- `INPUT_AMBIGUOUS`
- `UNKNOWN`

A classifier must preserve the original failure evidence and confidence. `UNKNOWN` is preferred over an unsupported guess.

## Evidence intelligence

Every operational recommendation must identify the evidence used and its freshness. Evidence can come from repository/source, Git, durable `.ai` state, runtime/tests, security checks, or provider responses. AI assertions alone are not execution evidence.

## Safety and authority

Operational Intelligence may recommend, rank, classify, and request checkpointing. It may not:

- grant authorization;
- bypass Security Gate;
- fabricate provider/runtime results;
- silently mutate semantic project state;
- convert a recommendation into execution without the existing controller/runtime authorities.

## P12 implementation slices

1. **Graph/readiness v1:** deterministic task graph construction, missing-reference validation, cycle detection, and readiness analysis.
2. **Prioritization/checkpoints v2:** deterministic dependency-aware ranking with explicit reasons and checkpoint event signals.
3. **Next:** failure classification/evidence improvements, followed by controller integration that consumes recommendations as advisory signals only.

The implementation remains independently testable before broader automation is added.
