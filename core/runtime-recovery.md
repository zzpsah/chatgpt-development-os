# DevOS Runtime Recovery v1

## Purpose

Recover the latest bounded runtime outcome from `.ai/RUNTIME-STATE.json` so a new DevOS worker can continue without depending on chat history.

## Recovery contract

```text
Durable runtime state
  -> load latest factual outcome
  -> classify outcome
  -> re-check repository/source
  -> re-check dependencies
  -> re-check capability
  -> re-check authorization
  -> re-check verification/security
  -> only then select a new bounded action
```

`tools/devos-runtime-recovery.py` is a deterministic, non-executing recovery reader. It never calls the runtime executor, never mutates project code, never grants authorization, and never automatically replays a previous action.

## Outcome handling

- No persisted state -> `NO_STATE`; select from fresh durable/project state.
- `COMPLETE` -> `RECHECK_GATES_THEN_CONTINUE`; completion evidence does not grant future authority.
- `FAILED`, `BLOCKED`, or `CANCELLED` -> `REVIEW_OUTCOME_BEFORE_CONTINUE`.
- Unknown outcome -> `RECOVERY_HOLD_REQUIRES_REVIEW`.

Every recovered result explicitly reports `execution: NONE`, `authorization: UNCHANGED`, and `replay: NEVER_AUTOMATIC`.

## No blind replay

A stored checkpoint or runtime outcome is historical evidence, not permission. Repository drift, changed dependencies, changed capability, changed authorization, failed security/verification, or uncertain external completion can invalidate continuation. A non-idempotent or uncertain action must stop/escalate rather than replay.

## Determinism

Recovery output is derived only from the persisted state and fixed classification rules. The executable proof runs the same state through recovery twice and requires identical output.

## Documentation boundary

**What is not written was never done.** Recovery implementation, executable proof, and durable state/contract updates land in the same change set. Completion is **IMPLEMENTED + VERIFIED + DOCUMENTED**.
