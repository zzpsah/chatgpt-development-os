# DevOS Current State

## Current milestone

P12 — Operational Intelligence is active. P12 now includes graph/readiness, prioritization/checkpoint, failure/evidence, advisory next-action, controller gating, bounded controller-to-runtime handoff v1, bounded Execution Runtime v1, autonomous development loop v2, durable runtime persistence v1, deterministic runtime recovery v1, and Scheduler/Worker v1.

## P12 status

Operational Intelligence remains `ADVISORY_ONLY`; it does not authorize execution, mutation, deployment, publication, or security bypass. The controller independently gates readiness, objective/scope, capability, authorization, and repository state. The handoff requires explicit capability availability, authorization approval when required, and `PASS` from the Security Gate for security-relevant work before constructing a runtime envelope.

The autonomous loop executes one already-approved `P12-HANDOFF-v1` through the existing bounded runtime. Runtime v1 remains verification-only: explicit Python argv, in-root script, no shell/inline/module execution. Actual process output, exit status, and duration are captured as raw evidence. The persistence adapter records runtime outcomes atomically in `.ai/RUNTIME-STATE.json` and retains a bounded history. The recovery reader reconstructs the latest outcome but never grants replay permission or executes work.

Scheduler/Worker v1 is the orchestration boundary above that loop. Each scheduler invocation processes exactly one bounded work unit. It first performs deterministic recovery; a latest `FAILED`, `BLOCKED`, or `CANCELLED` outcome causes `HOLD`/review and never triggers an automatic retry. An unknown persisted outcome also causes a fail-closed `HOLD`/review. Malformed or unreadable durable state likewise causes `HOLD` with `RECOVERY_STATE_INVALID`; the scheduler does not execute when recovery cannot establish a trustworthy classification. Otherwise it delegates exactly one iteration to the existing autonomous loop with a durable state path, which re-enters controller, handoff, runtime, verification, Security Gate, and persistence boundaries.

## Portable project memory

The repository is the durable project-memory boundary. A fresh AI must recover from repository source, Git, and `.ai` context before continuing. ChatGPT Memory, account memory, and prior chat history are supplementary only.

## Documentation integrity

**What is not written was never done.** Material implementation and its durable record must land in the same change set. Completion means **IMPLEMENTED + VERIFIED + DOCUMENTED**.

## Verification state

The live CI run for the previous HEAD `306a1a08...` failed on a stale autonomous-loop contract needle. A follow-up documentation-only correction at `f95ff6a1...` restored that phrase, but its CI run exposed the next missing contract needle (`Objective`). The autonomous-loop verifier is therefore the current acceptance blocker; no runtime execution failure has been observed.

## Next implementation target

Complete the autonomous-loop contract vocabulary atomically with this durable state record, then require live CI on the new HEAD. Only after CI passes may P12 hardening continue. Higher-impact P8 remote mutations remain separately incomplete and require explicit authorization.
