# DevOS Current State

## Current milestone

P12 — Operational Intelligence is active. P12 includes graph/readiness, prioritization/checkpoint, failure/evidence, advisory next-action, controller gating, bounded controller-to-runtime handoff v1, bounded Execution Runtime v1, autonomous development loop v2, durable runtime persistence v1, deterministic runtime recovery v1, Scheduler/Worker v1, and the bounded Human Command Interpretation Layer v1.

## P12 status

Operational Intelligence remains `ADVISORY_ONLY`; it does not authorize execution, mutation, deployment, publication, or security bypass. The controller independently gates readiness, objective/scope, capability, authorization, and repository state. The handoff requires explicit capability availability, authorization approval when required, and `PASS` from the Security Gate for security-relevant work before constructing a runtime envelope.

The autonomous loop executes one already-approved `P12-HANDOFF-v1` through the existing bounded runtime. Runtime v1 remains verification-only: explicit Python argv, in-root script, no shell/inline/module execution. Actual process output, exit status, and duration are captured as raw evidence. Persistence records runtime outcomes atomically in `.ai/RUNTIME-STATE.json`; recovery reconstructs the latest outcome but never grants replay permission or executes work.

Scheduler/Worker v1 is the orchestration boundary above that loop. Single-iteration mode performs deterministic recovery and delegates at most one bounded work unit. FAILED/BLOCKED/CANCELLED, unknown, or invalid durable state fails closed to review/HOLD. Batch mode accepts distinct work-unit payloads with an explicit positive `max_iterations`; payload count cannot exceed the bound, each payload re-enters the existing scheduler path, and execution stops on the first non-`COMPLETE` result. No blind replay or automatic retry is permitted.

## Human Command Interpretation Layer v1

The executable layer `tools/devos-command-interpreter.py` maps common casual English/Hinglish/typo-tolerant messages into stable canonical intents without executing work or granting authority. Covered examples include `continue`, `continiue`, `wahi se continue`, `ok`, `haan`, `do it`, `isko production grade bana`, `kya pending hai?`, and `ruk ja`. It also supports ordered compatible multi-intent routing such as `fix this bug and check security`.

`ok`/`haan`/similar confirmation is context-sensitive: with a known current objective it maps to `CONFIRM_CURRENT_PLAN` and delegates only after existing gates; without a current objective it remains `AMBIGUOUS` and performs no execution. Requests that attempt to bypass/disable authorization or security are `BLOCKED` as `AUTHORIZATION_ESCALATION`. Unknown language also remains `AMBIGUOUS` rather than being guessed into an action.

The layer is intentionally deterministic and bounded. `core/human-language-execution-engine.md` remains the normative semantic contract; this executable primitive does not claim general semantic AI understanding and does not replace project routing, controller gates, Security Gate, runtime restrictions, verification, or persistence.

## Portable project memory

The repository is the durable project-memory boundary. A fresh AI must recover from repository source, Git, and `.ai` context before continuing. ChatGPT Memory, account memory, and prior chat history are supplementary only.

## Documentation integrity

**What is not written was never done.** Material implementation and its durable record must land in the same change set. Completion means **IMPLEMENTED + VERIFIED + DOCUMENTED**.

## Recovery / checkpoint integrity v2

Durable runtime persistence now validates record identity, evidence, outcome status, and checkpoint structure before accepting or recovering state. A checkpoint must carry a stable runtime identity, objective/work-unit identity, positive iteration, status, evidence, verification, blockers, next action, and either a 40-character repository SHA or `UNKNOWN`. Malformed records or checkpoints fail closed instead of becoming resumable state.

Recovery exposes checkpoint presence as `CHECKPOINT_REQUIRES_FRESH_GATES` but never treats a checkpoint as permission to replay. `COMPLETE` still requires fresh gates before continuation; `FAILED`/`BLOCKED`/`CANCELLED` requires review. No recovery path creates authority or executes work.

## Verification state

Current PR #2 HEAD is `856d59d8d603599b736d875dc0a879af1d58a676`. The previous command-interpreter change had live CI verification before this follow-on checkpoint hardening. This checkpoint/recovery v2 change is pending its own live CI verification; it is documented here in the same atomic implementation change set.

## Next implementation target

After checkpoint/recovery v2 receives live CI verification, continue P12 with worker lifecycle/state-machine hardening and stronger unattended-loop observability. Then progress toward P12 Final Operational Readiness and the P13 Autonomous Development Orchestration boundary. Higher-impact P8 remote mutations remain separately incomplete and require explicit authorization.
