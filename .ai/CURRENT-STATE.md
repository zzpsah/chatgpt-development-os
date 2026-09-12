# DevOS Current State

## Current milestone

P12 — Operational Intelligence is active; executable controller integration, bounded controller-to-runtime handoff v1, bounded Execution Runtime v1, end-to-end autonomous development loop v2, durable runtime persistence v1, and deterministic runtime recovery v1 are now repository-backed. P11 remains complete.

## P12 status

P12 graph/readiness, prioritization/checkpoint, failure/evidence, advisory next-action, controller-gating, bounded handoff, bounded execution, autonomous-loop, persistence, and recovery slices are repository-backed. Operational Intelligence uses `ADVISORY_ONLY`; it does not authorize execution, mutation, deployment, publication, or security bypass. The controller independently gates readiness, objective/scope, capability, authorization, and repository state. The handoff requires explicit capability availability, authorization approval when required, and `PASS` from the Security Gate for security-relevant work before constructing a runtime envelope.

The autonomous loop executes one already-approved `P12-HANDOFF-v1` through the existing bounded runtime. Runtime v1 remains verification-only: explicit Python argv, in-root script, no shell/inline/module execution. Actual process output, exit status, and duration are captured as raw evidence. The persistence adapter records runtime outcomes atomically in `.ai/RUNTIME-STATE.json` and retains a bounded history. The recovery reader can reconstruct the latest outcome but never grants replay permission or executes work.

## Portable project memory

The repository is the durable project-memory boundary. A fresh AI must recover from repository source, Git, and `.ai` context before continuing. ChatGPT Memory, account memory, and prior chat history are supplementary only.

## Documentation integrity

**What is not written was never done.** Material implementation and its durable record must land in the same change set. Completion means **IMPLEMENTED + VERIFIED + DOCUMENTED**.

## Verification state

The runtime recovery implementation, executable proof, and durable documentation/state updates are included in the same atomic change. Live repository CI is the acceptance gate; until it passes, this recovery slice is `IMPLEMENTED` but not `VERIFIED` by CI.

## Next implementation target

Add scheduler/worker orchestration only after recovery semantics are verified. The scheduler must select one bounded work unit at a time and re-enter controller, handoff, runtime, verification, and Security Gate boundaries on every iteration. No unrestricted command runner and no second executor.
