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

Priority is a decision-support signal, not authority. A deterministic baseline may consider:

- explicit user/project priority;
- dependency criticality;
- blocked dependents;
- verification/security deadlines;
- age/staleness;
- estimated bounded effort.

The engine must expose the reasons behind a ranking and must not silently change user-defined priority.

## Checkpoint intelligence

A checkpoint signal identifies when the controller should persist or revalidate state. At minimum it should recognize:

- meaningful repository changes;
- completion/failure of a work unit;
- transition into or out of a blocked state;
- authorization boundary changes;
- verification/security results;
- session/handoff boundaries.

Checkpoint recommendations do not authorize an action; they preserve recoverability.

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

## P12 first slice

The first implementation slice is intentionally narrow: deterministic task graph construction and readiness analysis from the existing Development Task Controller task model. It should be independently testable before adding adaptive ranking or broader automation.
