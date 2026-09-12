# DevOS Runtime Persistence v1

## Purpose

Persist factual outcomes from the bounded Execution Runtime so a later DevOS iteration can recover task/checkpoint state without depending on chat history.

## Contract

```text
Runtime outcome
  -> raw evidence required
  -> normalize bounded record
  -> atomic write
  -> latest outcome + bounded history
  -> recovery reads latest
```

Persistence is a state boundary, not an authority boundary. It cannot authorize, execute, replay, mutate application code, or fabricate evidence.

## Durable record

`tools/devos-runtime-persistence.py` stores `P12-PERSISTENCE-v1` records. Each record retains task id, objective, outcome status, verification/security status, raw runtime evidence, and the runtime checkpoint. History is bounded to the latest 100 records.

The persistence adapter rejects outcomes without non-empty raw execution evidence. It also rejects unknown runtime outcome states. Writes use a temporary file in the destination directory, flush/fsync, then `os.replace`, so a completed persistence operation exposes one complete JSON state rather than a partially written document.

The recommended project-local destination is `.ai/RUNTIME-STATE.json`. This file contains execution state, not credentials or secrets.

## Recovery

A fresh DevOS worker can load `latest` and inspect `history` before selecting another work unit. Persistence does not imply that the latest outcome is safe to replay. Resume must still re-check repository state, dependencies, capability, authorization, verification, and Security Gate conditions.

## Safety

- Raw evidence comes from the runtime/provider; AI assertions are not evidence.
- Missing evidence prevents persistence.
- Persistence failure prevents a loop from claiming durable completion.
- No secrets, credentials, session cookies, or private keys belong in runtime state.
- Persistence never creates authorization and never bypasses Security Gate.
- A stored `COMPLETE` record is evidence of the runtime outcome, not blanket permission for future actions.

## Next layer

Scheduler/worker orchestration may consume this durable state only after recovery semantics are verified. Every scheduled iteration must re-enter the existing controller, handoff, runtime, verification, and security boundaries.

**What is not written was never done.** The persistence implementation, tests, and durable state contract must land together.
