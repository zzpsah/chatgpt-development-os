# DevOS Current State

## Current milestone

P12 — Operational Intelligence is active. The repository now includes graph/readiness, prioritization/checkpoint, failure/evidence, advisory next-action, controller gating, bounded controller-to-runtime handoff, Execution Runtime v1, autonomous loop v2, durable runtime persistence/recovery, Scheduler/Worker v1, bounded batch scheduling, Human Command Interpretation Layer v1, checkpoint/recovery integrity v2, the Base Operating Contract, Failure Resolution Engine v1, connection preflight diagnostics, and Worker lifecycle/state-machine observability v1.

## Operating contract

P12 remains `ADVISORY_ONLY`: it never grants execution, mutation, deployment, publication, or security bypass authority. The Base Operating Contract makes failure a bounded diagnostic-and-recovery task. Material failures follow `DETECTED → DIAGNOSED → REPAIRED → DRY-TESTED → VERIFIED → REGRESSION-PROTECTED → DOCUMENTED → RESUMED`, or remain `BLOCKED`/`HOLD` when authorization/evidence is insufficient. Root cause must be `ROOT_CAUSE_UNCONFIRMED` when evidence does not support a stronger claim.

Connection diagnosis is layered through configuration, credential shape (never secret values), endpoint/DNS, network reachability, TLS/transport, authentication, authorization, provider/connector, request validation, and response validation. `tools/devos-connection-preflight.py` provides bounded read-only configuration/DNS/network/TLS preflight diagnostics and records only non-secret evidence. `tools/test-devos-connection-preflight.py` provides deterministic regression coverage.

## Runtime / recovery / worker boundaries

The controller independently gates readiness, objective/scope, capability, authorization, and repository state. Handoff requires capability availability, required authorization approval, and Security Gate `PASS` for security-relevant work. Runtime v1 is verification-only: explicit Python argv, in-root script, no shell/inline/module execution. Persistence atomically records runtime outcomes; recovery validates durable state, reconstructs the latest outcome, and never grants replay permission or executes work. Scheduler/Worker processes at most one bounded unit per invocation; invalid/unknown or FAILED/BLOCKED/CANCELLED recovery fails closed to HOLD/review. Batch mode enforces a positive explicit bound, distinct canonical work units, and stops on the first non-`COMPLETE` result.

Worker lifecycle v1 is explicitly represented as `READY → RECOVERING → PREFLIGHT → DISPATCHED → RUNNING → VERIFYING → PERSISTING → COMPLETE`, with deterministic failure/hold exits. The lifecycle contract and regression guard require ordered transitions, one-unit bounds, explicit terminal states, non-secret observability, fresh recovery gates, and no automatic replay/authority creation.

## Documentation / recovery authority

**What is not written was never done.** Material implementation and its durable record must land in the same change set. Completion requires `IMPLEMENTED + VERIFIED + DOCUMENTED`. Repository source + Git are authoritative for implementation; `.ai` is durable project context; chat/account memory is supplementary.

## Verification state

PR #2 (`devos/documentation-integrity-v2`) remains open, draft, and unmerged. Fresh CI verification is required for the recent failure-resolution, preflight, and Worker lifecycle additions. Local live-network verification is not claimed because the execution environment previously failed DNS resolution; that failure was treated as a real diagnostic event rather than hidden.

## Next implementation target

After fresh CI verification, evaluate unattended-loop observability and P12 Final Operational Readiness. If all readiness gates are green, prepare the P13 Autonomous Development Orchestration boundary. Higher-impact P8 remote mutations remain separately incomplete and authorization-gated.
