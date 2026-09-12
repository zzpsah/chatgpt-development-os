# P13 Autonomous Development Orchestration v1

## Purpose

P13 turns one human goal and the recovered project task inventory into one bounded, independently gated next work-unit candidate. It composes P12 Operational Intelligence, the Development Task Controller, and the runtime-handoff contract; it never executes the candidate itself.

```text
Human goal
  -> project state + task inventory
  -> dependency/readiness/priority analysis
  -> independent controller gates
  -> one runtime-handoff candidate
  -> CONTINUE | STOP | ESCALATE
```

## Control outcomes

- `CONTINUE` — one candidate passed independent controller gates and has a `READY_FOR_RUNTIME` handoff. Runtime execution remains separate and not started.
- `STOP` — there is no safe action or the declared iteration budget is exhausted.
- `ESCALATE` — an authorization, capability, scope, security, readiness, or handoff condition blocks the candidate.

## Safety boundary

`tools/autonomous-orchestrator.py` requires an explicit non-empty goal and positive execution budget. It preserves `authority: UNCHANGED` and `execution: NONE`. A P12 recommendation stays `ADVISORY_ONLY`; the controller independently validates scope, repository revalidation, readiness, capability, authorization, and Security Gate state before the runtime handoff can become ready.

The orchestrator does not mutate a repository, run commands, retry work, mark work complete, bypass authorization, or treat a handoff as execution evidence. After actual runtime work, a later orchestration call must receive fresh task state and evidence rather than blindly replaying the candidate.

## Runtime-outcome feedback

The optional `latest_runtime_outcome` is processed only in memory for the next selection. A `COMPLETE` outcome must name an existing task, carry `verification: VERIFIED`, and include non-empty actual evidence; only then can it mark that task complete in the next controller input and unlock dependents. `FAILED` and `BLOCKED` outcomes remain failure/blocker signals. Invalid, unknown, or unevidenced outcomes return `ESCALATE` and do not alter task state.
