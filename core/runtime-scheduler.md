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

## Bounded batch scheduling

The worker now supports a bounded batch of **distinct work-unit payloads** through `run_batch(...)`. The caller must provide an explicit positive `max_iterations`, and the payload count may not exceed that bound. Each payload is sent through the existing `run_iteration(...)` path, so controller, handoff, runtime, verification, recovery, and persistence gates are re-entered for every unit.

The batch stops immediately when an iteration is not `COMPLETE`. It never reuses a payload automatically, never retries a failed/blocked/cancelled outcome, and never silently increases `max_iterations`. An empty batch returns `NO_ACTION`; an invalid or zero iteration bound is rejected.

The CLI accepts either the existing single-object input or a JSON list for bounded batch scheduling. `--max-iterations` defaults to `1`, preserving the original one-iteration behavior.

## Safety boundaries

- No blind replay.
- No unrestricted command runner.
- No second executor.
- No authorization creation or escalation.
- Existing controller, handoff, Security Gate, bounded runtime, verification, and persistence remain the execution boundaries.
- Every runtime iteration receives a durable state path, so successful and failed runtime evidence is persisted.
- A failed, blocked, or cancelled latest outcome requires review before another iteration.
- An unknown or invalid recovery state requires review before another iteration.
- Batch scheduling is bounded by an explicit caller-supplied maximum and distinct payloads.

## Determinism

Recovery classification is deterministic. Single-iteration mode performs at most one bounded autonomous-loop call per invocation. Batch mode performs at most `max_iterations` calls and stops on the first non-`COMPLETE` result. Both modes return explicit iteration/execution/authorization information and preserve `NEVER_AUTOMATIC` replay semantics.

## Completion standard

**What is not written was never done.** Scheduler work is complete only when it is **IMPLEMENTED + VERIFIED + DOCUMENTED** with code, executable proof, durable state/documentation, and CI evidence.
