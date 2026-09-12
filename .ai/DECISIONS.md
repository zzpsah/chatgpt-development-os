# Decisions

## Durable project state authority

- DevOS project-local `.ai` is the portable durable context layer.
- Source tree + Git are authoritative for implementation state and exact changes.
- AI account memory is supplementary and must not be treated as project authority.
- `STATE-INDEX.md` is an evidence index, not semantic authority.

## P9 milestone status

- P9 Development Task Controller v1 is implemented and integrated into repository CI contract verification.

## P10 milestone status

- P10 Context Continuity & Recovery v1 is complete and was closed only after fresh primary CI evidence and external reusable context-sync execution.
- P10 does not imply completion of higher-impact P8 remote mutations.

## P11 milestone status

- P11 DevOS Federation & Self-Healing Context v1 is complete.
- Identity, freshness/integrity, safe reconciliation, and repository-first recovery are implemented; P12 is now the active milestone.

## P12 scheduler/worker decision

- P12 Scheduler/Worker v1 is the bounded orchestration boundary above the autonomous loop.
- One scheduler invocation may process exactly one bounded work unit.
- The scheduler must load durable runtime state before work selection.
- Latest FAILED, BLOCKED, or CANCELLED outcomes require review and must not be automatically retried.
- Latest COMPLETE or absent state may proceed only through a fresh autonomous-loop iteration, which re-enters controller, handoff, runtime, verification, Security Gate, and persistence boundaries.
- The scheduler is not an executor, does not create or escalate authority, and must never perform blind replay.
- Every scheduler iteration supplies a durable state path so runtime outcomes remain recoverable.

## Future persistence rule

- Meaningful engineering work must be persisted in repository-local `.ai` state rather than relying on chat history.
- Session-level semantic outcomes belong in `.ai/SESSIONS/`.
- Changes to remaining work, intentional choices, or current project state must be reflected in `TASKS.md`, `DECISIONS.md`, or `CURRENT-STATE.md` as applicable.
- Generated `STATE-INDEX.md` remains deterministic evidence only.

## Documentation integrity decision

**What is not written was never done.** Material implementation and its durable record land in the same change set. Completion means **IMPLEMENTED + VERIFIED + DOCUMENTED**. Missing durable documentation is incomplete/unknown, not an implied success.
