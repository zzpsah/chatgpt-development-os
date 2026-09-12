# DevOS Current State

## Current milestone

P12 — Operational Intelligence is active. P12 now includes graph/readiness, prioritization/checkpoint, failure/evidence, advisory next-action, controller gating, bounded controller-to-runtime handoff v1, bounded Execution Runtime v1, autonomous development loop v2, durable runtime persistence v1, deterministic runtime recovery v1, Scheduler/Worker v1, and the bounded batch scheduling extension.

## P12 status

Operational Intelligence remains `ADVISORY_ONLY`; it does not authorize execution, mutation, deployment, publication, or security bypass. The controller independently gates readiness, objective/scope, capability, authorization, and repository state. The handoff requires explicit capability availability, authorization approval when required, and `PASS` from the Security Gate for security-relevant work before constructing a runtime envelope.

The autonomous loop executes one already-approved `P12-HANDOFF-v1` through the existing bounded runtime. Runtime v1 remains verification-only: explicit Python argv, in-root script, no shell/inline/module execution. Actual process output, exit status, and duration are captured as raw evidence. The persistence adapter records runtime outcomes atomically in `.ai/RUNTIME-STATE.json` and retains a bounded history. The recovery reader reconstructs the latest outcome but never grants replay permission or executes work.

Scheduler/Worker v1 is the orchestration boundary above that loop. Each scheduler invocation processes exactly one bounded work unit. It first performs deterministic recovery; a latest `FAILED`, `BLOCKED`, or `CANCELLED` outcome causes `HOLD`/review and never triggers an automatic retry. An unknown persisted outcome also causes a fail-closed `HOLD`/review. Malformed or unreadable durable state likewise causes `HOLD` with `RECOVERY_STATE_INVALID`; the scheduler does not execute when recovery cannot establish a trustworthy classification. Otherwise it delegates exactly one iteration to the existing autonomous loop with a durable state path, which re-enters controller, handoff, runtime, verification, Security Gate, and persistence boundaries.

The bounded batch scheduling extension `run_batch(...)` accepts distinct work-unit payloads, requires a positive integer `max_iterations`, re-enters the existing one-unit scheduler path for each payload, and stops on the first non-`COMPLETE` result. It rejects duplicate payloads using a canonical JSON identity check and rejects non-object work-unit payloads before execution. Invalid `max_iterations` types/values fail closed before batch execution. Direct `run_iteration(...)` calls now apply the same non-object payload guard before recovery or execution. It cannot silently retry or reuse a payload, and cannot exceed the caller-supplied iteration bound.

## Portable project memory

The repository is the durable project-memory boundary. A fresh AI must recover from repository source, Git, and `.ai` context before continuing. ChatGPT Memory, account memory, and prior chat history are supplementary only.

## Documentation integrity

**What is not written was never done.** Material implementation and its durable record must land in the same change set. Completion means **IMPLEMENTED + VERIFIED + DOCUMENTED**.

## Verification state

The duplicate-payload hardening at `7a26b5a7eefc11f3057910e3d9a6319c3cf930fa` was verified by CI run `34688273962` (run #351): `completed` / `success`. The subsequent durable acceptance record at `61875c2f2a4ae00393a5e2f5cf8b4c53b9d02623` was verified by CI run `34688308681` (run #352): `completed` / `success`. The malformed-batch-payload hardening at `c83c1efbd475452f31dadd3f2bada3b2417a6c33` was verified by CI run `34688396678` (run #353): `completed` / `success`. The durable acceptance record at `690f30b3b098e74f238b5fe5897e1d6a46549315` was verified by CI run `34688527297` (run #354): `completed` / `success`. The iteration-bound hardening at `40d6dd0c901d940f00f26974d947216d9ee7968a` was verified by CI run `34688741615` (run #355): `completed` / `success`, including the P12 scheduler/worker verification.

## Next implementation target

Continue P12 hardening with the next safe bounded worker/recovery improvement. Higher-impact P8 remote mutations remain separately incomplete and require explicit authorization.
