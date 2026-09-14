# AI State Resolver — Evolution Record

This document records how the resolver evolved. It is historical/durable context, not an authorization source. Current executable behavior is defined by `core/ai-state-resolver.md` plus the current source/tests.

## Stage 0 — DevOS foundations before deterministic resolver v2

The resolver sits on top of already-completed DevOS foundations rather than replacing them:

- P11: repository-first recovery/revalidation and cross-AI continuity.
- P12: operational/execution evidence provenance and freshness ownership.
- P15: human-language interpretation.
- P16: semantic goal-to-plan compilation.
- P17: step readiness and authorization gating.

These boundaries remain authoritative: interpretation is not authorization, planning is not execution, readiness is not execution, and confidence does not manufacture permission.

## Stage 1 — Semantic resolver contract / v1 context

The original resolver contract described semantic reconstruction: separate observed/likely/unknown facts, recover unfinished work, identify candidate next actions, and respect verification/authorization boundaries.

Important contribution:

- established repository evidence as authoritative over chat memory;
- separated fact from interpretation;
- required conflicts to be surfaced rather than silently chosen;
- treated generated state as evidence rather than truth.

The v1 prose was intentionally broader than the later deterministic implementation.

## Stage 2 — Deterministic AI State Resolver v2 grounding

Resolver v2 introduced a read-only deterministic claim envelope (`DEVOS-AI-STATE-RESOLUTION-v2`).

Key behavior:

- claim IDs and statements are validated;
- `observed` requires citable grounding;
- durable-state claims cannot self-upgrade to observed and are capped at `likely`;
- P12 execution evidence retains ownership of freshness;
- stale/non-current execution evidence downgrades observed confidence;
- recovery/handoff/path changes create explicit revalidation reasons;
- duplicate claim IDs fail closed to `unknown`;
- resolver output carries unchanged authority/authorization and `execution: NONE`, `mutation: NONE`.

This stage made resolver confidence machine-checkable while preserving P12/P17 authority boundaries.

## Stage 3 — P16/P17 propagation

The resolver was integrated into the governed continuation path:

`P11 recovery -> resolver v2 -> P16 plan -> P17 readiness -> controller`

Key behavior:

- unknown resolver claims propagate to P16 as `CLARIFY`;
- valid resolver provenance is retained in the P16 plan;
- P17 rejects a planned envelope carrying unresolved state;
- `likely` remains uncertainty but does not automatically block all planning;
- no resolver result grants authorization or execution.

## Stage 4 — Envelope integrity hardening (PR #44)

PR #44 (`Harden AI State Resolver v2 envelope integrity`) closed a fail-open envelope-integrity gap.

Final merged source head: `71d93755e171da5e83e62b00baa4680a0e929f5e`.
Merge commit recorded in durable state: `a4a3413bb27802ef38a698550807e8fb0102f839`.

Key changes:

- unknown malformed claims produce `NEEDS_EVIDENCE` even without a usable ID;
- durable-state revalidation reasons remain visible for claims already supplied as `likely`;
- P16 validates protocol, status, authority, authorization, execution, mutation, claim confidence, weakest confidence, confidence summary, and unresolved consistency;
- P16 preserves full resolver provenance unchanged;
- P17 independently revalidates preserved resolver provenance and fails closed on hidden uncertainty or changed authority/execution fields;
- adversarial tests cover forged/tampered resolver envelopes.

Exact final-head PR gates were recorded as green in the PR/session evidence. This did not upgrade `production_ready`.

## Stage 5 — Durable-state reconciliation after PR #44 (PR #45)

PR #45 reconciled `.ai/CURRENT-STATE.md`, `.ai/TASKS.md`, and session provenance after PR #44.

Merge commit: `aa38761270ac9acdf6af90a4bae64890c766ec91`.

The goal was durable recovery accuracy, not new runtime capability. Historical exact-head evidence remained historical rather than being rewritten to look current.

A later direct documentation commit (`040c7d21b5fac6224ced1bdbfeaa7c3b71b78c78`) intentionally separated active state from historical evidence, but it also reintroduced stale pre-proof wording about GitHub live-provider evidence. The current contradiction-hardening work treats actual source/Git/provider evidence as authoritative and repairs that semantic drift rather than accepting the stale wording as truth.

## Stage 6 — Structured cross-claim contradiction hardening (current bounded objective)

This stage promotes the previously explicit v2 non-goal: different claims about the same fact.

### Stable fact identity

Claims may add:

```yaml
fact_key: deployment.status
fact_value: complete
```

No NLP inference is used to guess fact identity. Only an explicit shared `fact_key` creates a comparison group.

### Deterministic comparison

`fact_value` is compared using canonical JSON. Object key order therefore does not create a false contradiction.

### Contradiction policy

If claims with the same valid `fact_key` have different canonical values:

- all involved claims become `unknown`;
- all receive `CROSS_CLAIM_CONTRADICTION`;
- their IDs enter `unresolved_claim_ids`;
- result status becomes `NEEDS_EVIDENCE`;
- a deterministic contradiction summary records the fact key, involved claim IDs, and canonical values.

### No silent winner

The resolver does not automatically prefer:

- current over stale evidence;
- execution evidence over durable-state evidence;
- observed over likely input confidence;
- later file/order position over earlier position.

A disagreement remains unresolved until upstream evidence reconciliation removes the conflict. This keeps resolver behavior deterministic and avoids inventing a precedence policy that P12 or project-specific logic did not authorize.

### Downstream defense in depth

P16 independently recomputes structured contradictions before planning. P17 independently recomputes them again before READY. A tampered envelope cannot hide a contradiction merely by changing status, counts, unresolved IDs, or the contradiction summary.

## Permanent invariants across all stages

- `INTERPRETATION != AUTHORIZATION`
- `PLAN != EXECUTION`
- `READY != EXECUTION`
- `DOCUMENTATION != AUTHORIZATION`
- `CI PASS != AUTHORIZATION`
- resolver confidence never grants permission, execution, completion, or production readiness;
- P12 remains owner of execution-evidence provenance/freshness;
- historical evidence is preserved and is not silently rewritten as fresh evidence;
- no P18/P19 is created merely for bookkeeping.

## Recovery rule

When this document, `.ai` state, chat memory, and current source differ, use recovery precedence:

1. current source + Git/provider evidence;
2. explicit current requirements/decisions;
3. durable `.ai` semantic state;
4. dated session/history records;
5. chat/model memory only as supplementary context.
