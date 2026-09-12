# DevOS Current State

## Current milestone

P12 — Operational Intelligence is active; executable controller integration, bounded controller-to-runtime handoff v1, and the first real bounded Execution Runtime v1 are now repository-backed. P11 remains complete.

## P12 status

P12 graph/readiness, prioritization/checkpoint, failure/evidence, advisory next-action, controller-gating, bounded handoff, and bounded execution slices are repository-backed. Operational Intelligence uses `ADVISORY_ONLY`; it does not authorize execution, mutation, deployment, publication, or security bypass. The controller consumes the advisory result but independently gates readiness, objective/scope, capability, authorization, and repository state. The handoff requires explicit capability availability, authorization approval when required, and `PASS` from the Security Gate for security-relevant work before constructing an envelope for the existing runtime.

The new runtime executes only an already-approved `P12-HANDOFF-v1` with the `verification.run` capability. Runtime v1 is verification-only and accepts only an explicit Python script inside the project root; shell strings, inline/module execution, and out-of-root paths are rejected. Actual process output, exit status, and duration are captured as raw evidence. A checkpoint can persist the pre-action and post-action states. The runtime never grants authority and never commits.

The handoff begins with an empty evidence list. Only the runtime/provider may supply raw execution evidence. A runtime result without raw evidence is not accepted as successful completion.

## Portable project memory

The repository is the durable project-memory boundary. A fresh AI must recover from repository source, Git, and `.ai` context before continuing. ChatGPT Memory, account memory, and prior chat history are supplementary only.

## Documentation integrity

**What is not written was never done.** Material implementation and its durable record must land in the same change set. Completion means **IMPLEMENTED + VERIFIED + DOCUMENTED**.

## Verification state

The bounded execution runtime implementation and executable tests are included in the same atomic change as their durable documentation and state updates. Live repository CI is the acceptance gate for this change; until it passes, the runtime is `IMPLEMENTED` but not yet `VERIFIED` by CI.

## Next implementation target

Wire controller-approved work units to the runtime through a host capability adapter that can supply verified repository-head evidence and durable task/checkpoint feedback, while preserving operation-specific authorization, Security Gate checks, and the single-executor boundary. No unrestricted command runner and no second executor may be introduced.
