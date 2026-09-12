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
 Failure + evidence analysis
          ↓
 Evidence-backed advisory next action
```

Operational Intelligence **does not authorize** execution, mutation, deployment, publication, or security bypass. It is advisory only and cannot grant authority that belongs to the existing controller/runtime and Security Gate.

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

Dependencies are directed edges from prerequisites to dependent work. A task is `READY` only when required dependencies are satisfied and authorization/capability conditions permit execution.

## Dependency intelligence

The engine must preserve explicit dependencies, distinguish `READY`, `WAITING`, `BLOCKED`, and `UNAUTHORIZED`, detect missing references/cycles, never infer completion, and retain evidence for readiness decisions.

## Priority intelligence

Priority is a decision-support signal, not authority. The deterministic baseline performs **dependency-aware prioritization** of unfinished work using explicit user/project priority plus bounded dependency criticality, blocked/failed status, age/staleness, deadline urgency, and estimated effort. Every scoring reason is exposed. Stored user-defined priority is never silently changed, and ranking never authorizes execution.

## Checkpoint intelligence

A checkpoint signal identifies when the controller should persist or revalidate state. Recognized events are `REPOSITORY_CHANGE`, `WORK_UNIT_COMPLETE`, `WORK_UNIT_FAILED`, `BLOCKED_TRANSITION`, `AUTHORIZATION_CHANGE`, `VERIFICATION_RESULT`, `SECURITY_RESULT`, `SESSION_BOUNDARY`, and `HANDOFF_BOUNDARY`.

Unknown events are surfaced as non-checkpoint signals rather than guessed. Checkpoint recommendations preserve recoverability and do not authorize actions.

## Failure classification

Operational Intelligence classifies failures without rewriting their raw evidence. Initial classes are:

- `CAPABILITY_MISSING`
- `AUTHORIZATION_REQUIRED`
- `DEPENDENCY_BLOCKED`
- `VERIFICATION_FAILED`
- `SECURITY_BLOCKED`
- `PROVIDER_FAILURE`
- `REPOSITORY_DRIFT`
- `INPUT_AMBIGUOUS`
- `UNKNOWN`

Classification uses explicit machine-readable hints or a constrained status mapping. Unsupported values become `UNKNOWN`; the original failure payload is preserved and a confidence level is exposed. The classifier is not a root-cause authority and must not invent a cause from free-form assertions.

## Evidence intelligence

Evidence is normalized with provenance and freshness metadata. Recognized execution-evidence sources are repository, Git, runtime, test, security, and provider responses. AI assertions or plans are not execution evidence. Evidence normalization does not alter the original evidence payload and does not upgrade uncertain evidence into verified results.

## Advisory next action

P12 may derive a next-action signal from readiness and priority, with blockers taking precedence over speculative work. The result contains the task identifier, supporting reasons, and an explicit `ADVISORY_ONLY` authority marker. `NEEDS_APPROVAL` remains a controller approval concern even when its priority is high. The recommendation never executes, authorizes, mutates, or claims completion.

When no task is safely actionable, the engine returns an explicit `no_action` result rather than guessing.

## Safety and authority

Operational Intelligence may recommend, rank, classify, normalize evidence, and request checkpointing. It may not grant authorization, bypass Security Gate, fabricate provider/runtime results, silently mutate semantic project state, or convert a recommendation into execution without the existing controller/runtime authorities.

## P12 implementation slices

1. **Graph/readiness v1:** deterministic task graph construction, missing-reference validation, cycle detection, and readiness analysis.
2. **Prioritization/checkpoints v2:** deterministic dependency-aware ranking with explicit reasons and checkpoint event signals.
3. **Failure/evidence v3:** deterministic failure classification, raw-evidence preservation, provenance/freshness normalization, and safe handling of unsupported classifications.
4. **Next-action v4:** deterministic advisory next-action generation with explicit non-authority semantics.
5. **Next:** fresh-repository recovery proof and stronger controller integration without granting authority.

The implementation remains independently testable before broader automation is added.
