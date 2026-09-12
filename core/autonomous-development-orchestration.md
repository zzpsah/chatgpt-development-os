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

## Durable checkpoint and resume

`tools/orchestration-checkpoint.py` writes a minimal `P13-ORCHESTRATION-CHECKPOINT-v1` record, normally at `.ai/ORCHESTRATION-CHECKPOINT.json`. It stores only the goal, iteration, control decision, repository head, candidate task identifier, and reasons; it never stores credentials, raw runtime evidence, or semantic task state.

Resume compares the recorded repository head with the current head. A mismatch returns `ESCALATE`. A match still returns `REVALIDATE_REQUIRED`, never execution or a replay instruction: the orchestrator must receive fresh inventory, capability, authorization, security, and evidence inputs before another candidate is selected.

## Real managed-project proof contract

`tools/verify-managed-project-orchestration.py` is the executable P13 completion proof. It must run against a separate checked-out repository whose `.ai/manifest.yaml` declares `managed_by: development-os`; the proof is invalid if it runs only against fixtures inside the DevOS repository.

The verifier performs a bounded, read-only orchestration sequence against the managed project:

1. recover the external repository Git HEAD and durable `.ai` context;
2. let P13 select `verify_managed_context` through the normal P12 controller and runtime-handoff gates;
3. perform actual manifest/context checks and feed the result back only as `COMPLETE + VERIFIED + non-empty evidence`;
4. require P13 to select the dependent `checkpoint_resume` unit;
5. build a P13 checkpoint, prove same-HEAD resume returns `REVALIDATE_REQUIRED`, and prove changed-HEAD resume returns `ESCALATE`;
6. feed that verified checkpoint evidence back and require the bounded goal to terminate with `STOP` / controller `NO_ACTION`;
7. assert authority remains `UNCHANGED` and orchestration execution remains `NONE` throughout.

`.github/workflows/verify-p13-managed-project.yml` supplies the independent environment. It checks out DevOS and `zzpsah/automation-suite` separately and runs the proof against the latter's real `main` state. The workflow has read-only repository permissions and does not modify the managed project.
