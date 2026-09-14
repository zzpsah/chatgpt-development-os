# Session — AI State Resolver v2 detailed contradiction provenance

Date: 2026-09-14
Repository: `zzpsah/chatgpt-development-os`
Base `main`: `2500ddc235ce99dbe45a6cd0537d4b0d2372c4a4`
Branch: `feat/resolver-detailed-contradiction-provenance`

## Trigger

The user requested continued DevOS development and durable documentation. Fresh recovery confirmed PR #49 contradiction envelope-integrity hardening and PR #51 post-merge reconciliation were already merged. No open competing PR existed at the start of this bounded slice.

A stale/diverged concurrent PR #50 was inspected before selecting the next objective. PR #49 had already superseded its downstream contradiction-recomputation work. One non-duplicate concept remained useful: deterministic detailed contradiction provenance. PR #50 was closed without merge; only the concept was promoted from fresh current `main`.

## Objective

Extend resolver contradiction auditability without creating a second source of truth or changing any authority boundary.

The resolver now emits `contradictions` alongside `contradiction_fact_keys`. Each detail record contains:

- `fact_key`;
- sorted involved `claim_ids`;
- sorted canonical JSON `canonical_values`.

Contradiction records themselves are sorted by `fact_key`. Non-contradictory and invalid-top-level results use an empty list.

## Defense in depth

### Resolver

- Keeps explicit `fact_key` / `fact_value` identity and deterministic canonical JSON comparison.
- Emits detailed provenance only for contradiction groups derived from otherwise-resolved claims.
- Does not choose a winner and does not grant authority or execution.

### P16

- Recomputes contradiction groups from preserved claims.
- Recomputes the expected detailed contradiction records from claim IDs and canonical values.
- Rejects forged or inconsistent `contradictions` with `CLARIFY`.
- Continues to reject hidden contradictions, inconsistent contradiction reasons, and inconsistent `contradiction_fact_keys`.

### P17

- Independently repeats the detailed-provenance recomputation at readiness time.
- Rejects forged or post-plan inconsistent detail with `BLOCKED`.
- Existing post-P16 `fact_value` tamper detection remains intact.

## Regression coverage

Updated tests cover:

- deterministic empty detail for non-contradictory state;
- deterministic ordering for multiple contradiction groups;
- sorted claim IDs and canonical values;
- invalid top-level claims input returns empty detailed provenance;
- contradiction detail propagates through P16 unresolved handling;
- fake detail on an otherwise valid resolver envelope causes P16 `CLARIFY`;
- fake detail added after P16 causes P17 `BLOCKED`;
- existing forged status/authority/execution and hidden contradiction tests remain active.

## Documentation

Updated in this change boundary:

- `core/ai-state-resolver.md` — current normative resolver output and downstream validation contract;
- `docs/AI-STATE-RESOLVER-CROSS-CLAIM-CONTRADICTIONS.md` — detailed contradiction provenance format, audit-only semantics, and P16/P17 validation;
- `docs/DEVOS-ENGINEERING-STAGE-HISTORY.md` — previous-stage ledger brought through PR #51 while keeping this objective marked active, not completed;
- `.ai/CURRENT-STATE.md` and `.ai/TASKS.md` — active bounded objective and preserved boundaries.

## Preserved boundaries

- `production_ready = false`.
- authority: unchanged.
- authorization: unchanged.
- resolver/P16/P17 execution: none.
- no provider, deployment, credential, permission, database, production, or destructive mutation is introduced.
- P12 remains owner of execution-evidence provenance/freshness.
- P16 remains plan compiler.
- P17 remains readiness/authorization gate.
- no P18/P19 bookkeeping phase is created.

## Verification state

Implementation, adversarial tests, normative docs, previous-stage ledger, and durable active-state records are committed on the bounded branch. Exact-final-head applicable CI is required before merge/completion. Compatibility failures must be repaired without weakening claims-based independent contradiction recomputation or turning detailed provenance into trusted authority.
