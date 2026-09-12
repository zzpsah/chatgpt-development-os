# P12 Scheduler/Worker v1

The scheduler is the bounded worker boundary above the existing autonomous loop. It performs **one work unit per iteration** and never becomes a second executor.

## Contract

```text
Durable runtime state
  -> deterministic recovery classification
  -> HOLD on FAILED/BLOCKED/CANCELLED/unknown/invalid recovery state
  -> otherwise exactly one autonomous-loop iteration
  -> Controller -> Handoff -> Runtime -> Verification -> Persistence
```

A recovered COMPLETE outcome is not permission to replay the old work; it only permits a fresh iteration after the autonomous loop re-checks its gates. No state is not an error and starts fresh selection. An unknown persisted outcome is a fail-closed `HOLD` requiring recovery review. A malformed/unreadable durable state is also a fail-closed `HOLD`; the scheduler does not execute when recovery cannot establish a trustworthy state classification.

## Safety boundaries

- No blind replay.
- No unrestricted command runner.
- No second executor.
- No authorization creation or escalation.
- Existing controller, handoff, Security Gate, bounded runtime, verification, and persistence remain the execution boundaries.
- Every runtime iteration receives a durable state path, so successful and failed runtime evidence is persisted.
- A failed, blocked, or cancelled latest outcome requires review before another iteration.
- An unknown or invalid recovery state requires review before another iteration.

## Determinism

Recovery classification is deterministic. The scheduler performs at most one bounded autonomous-loop call per invocation and returns explicit `iteration`, `execution`, and `authorization` fields. Recovery errors are converted to a deterministic scheduler `HOLD` rather than allowing execution to proceed on untrusted state.

## Completion standard

**What is not written was never done.** Scheduler work is complete only when it is **IMPLEMENTED + VERIFIED + DOCUMENTED** with code, executable proof, durable state/documentation, and CI evidence.
