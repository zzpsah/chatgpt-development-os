# DevOS Current State

## Current milestone

P12 — Operational Intelligence is active. P12 now includes graph/readiness, prioritization/checkpoint, failure/evidence, advisory next-action, controller gating, bounded controller-to-runtime handoff v1, bounded Execution Runtime v1, autonomous development loop v2, durable runtime persistence v1, deterministic runtime recovery v1, Scheduler/Worker v1, and the bounded batch scheduling extension.

## P12 status

Operational Intelligence remains `ADVISORY_ONLY`; it does not authorize execution, mutation, deployment, publication, or security bypass. The controller independently gates readiness, objective/scope, capability, authorization, and repository state. The handoff requires explicit capability availability, authorization approval when required, and `PASS` from the Security Gate for security-relevant work before constructing a runtime envelope.

The autonomous loop executes one already-approved `P12-HANDOFF-v1` through the existing bounded runtime. Runtime v1 remains verification-only: explicit Python argv, in-root script, no shell/inline/module execution. Actual process output, exit status, and duration are captured as raw evidence. The persistence adapter records runtime outcomes atomically in `.ai/RUNTIME-STATE.json` and retains a bounded history. The recovery reader reconstructs the latest outcome but never grants replay permission or executes work.

Scheduler/Worker v1 is the orchestration boundary above that loop. Each scheduler invocation processes exactly one bounded work unit. It first performs deterministic recovery; a latest `FAILED`, `BLOCKED`, or `CANCELLED` outcome causes `HOLD`/review and never triggers an automatic retry. An unknown persisted outcome also causes a fail-closed `HOLD`/review. Malformed or unreadable durable state likewise causes `HOLD` with `RECOVERY_STATE_INVALID`; the scheduler does not execute when recovery cannot establish a trustworthy classification. Otherwise it delegates exactly one iteration to the existing autonomous loop with a durable state path, which re-enters controller, handoff, runtime, verification, Security Gate, and persistence boundaries.

The bounded batch scheduling extension `run_batch(...)` accepts distinct work-unit payloads, requires an explicit positive `max_iterations`, re-enters the existing one-unit scheduler path for each payload, and stops on the first non-`COMPLETE` result. It cannot silently retry, reuse a payload, or exceed the caller-supplied iteration bound.

## Portable project memory

The repository is the durable project-memory boundary. A fresh AI must recover from repository source, Git, and `.ai` context before continuing. ChatGPT Memory, account memory, and prior chat history are supplementary only.

## Documentation integrity

**What is not written was never done.** Material implementation and its durable record must land in the same change set. Completion means **IMPLEMENTED + VERIFIED + DOCUMENTED**.

## Verification state

The corrective durable record at HEAD `18f3bf3438ef48a936c3f1dda0239eed91d474b0` was verified by CI run `34688138297` (run #349) for workflow `Verify Development OS Contracts`: `completed` / `success`. The prior guard failure on `649f34bb...` remains recorded as a historical documentation-integrity exception because that commit changed `tools/test-devos-scheduler.py` without a durable documentation file in the same commit. The exception is not being misrepresented as an atomic historical change.

The current verified CI acceptance applies to the corrective HEAD only. Any subsequent implementation must again satisfy the repository's documentation-at-change boundary and obtain a new green CI result before being treated as verified.

## Next implementation target

Continue P12 hardening with the next safe bounded worker/recovery improvement, using an atomic documented change set where the available repository write path permits it. Higher-impact P8 remote mutations remain separately incomplete and require explicit authorization.
