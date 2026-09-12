# DevOS Current State

## Current milestone

P12 — Operational Intelligence is active; executable controller integration, bounded controller-to-runtime handoff v1, bounded Execution Runtime v1, end-to-end autonomous development loop v2, and durable runtime persistence v1 are now repository-backed. P11 remains complete.

## P12 status

P12 graph/readiness, prioritization/checkpoint, failure/evidence, advisory next-action, controller-gating, bounded handoff, bounded execution, autonomous-loop, and persistence slices are repository-backed. Operational Intelligence uses `ADVISORY_ONLY`; it does not authorize execution, mutation, deployment, publication, or security bypass. The controller independently gates readiness, objective/scope, capability, authorization, and repository state. The handoff requires explicit capability availability, authorization approval when required, and `PASS` from the Security Gate for security-relevant work before constructing a runtime envelope.

The autonomous loop executes one already-approved `P12-HANDOFF-v1` through the existing bounded runtime. Runtime v1 remains verification-only: explicit Python argv, in-root script, no shell/inline/module execution. Actual process output, exit status, and duration are captured as raw evidence. The persistence adapter records runtime outcomes atomically in `.ai/RUNTIME-STATE.json` and retains a bounded history. A persistence operation requires raw evidence and never creates authority or replay permission.

## Portable project memory

The repository is the durable project-memory boundary. A fresh AI must recover from repository source, Git, and `.ai` context before continuing. ChatGPT Memory, account memory, and prior chat history are supplementary only.

## Documentation integrity

**What is not written was never done.** Material implementation and its durable record must land in the same change set. Completion means **IMPLEMENTED + VERIFIED + DOCUMENTED**.

## Verification state

The persistence implementation, executable integration test, CI wiring, and durable state/documentation updates are included in the same atomic change. Live repository CI is the acceptance gate; until it passes, this persistence slice is `IMPLEMENTED` but not `VERIFIED` by CI.

## Next implementation target

Add deterministic recovery/resume from the durable runtime state, then add scheduler/worker orchestration only after resume semantics are verified. Every repeated iteration must re-enter controller, handoff, runtime, verification, and Security Gate boundaries. No unrestricted command runner and no second executor.
