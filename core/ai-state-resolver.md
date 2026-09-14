# AI State Resolver — v2 Current Contract

> **Reading order:** [v2 deterministic implementation](#v2-deterministic-implementation) is the current executable contract. Historical resolver stages are preserved in `docs/AI-STATE-RESOLVER-EVOLUTION.md` and dated session records.

## Purpose

AI State Resolver is a deterministic, read-only claim-resolution layer between recovered DevOS evidence and P16 planning. It classifies claim confidence, exposes revalidation needs, detects explicitly structured contradictions, and preserves uncertainty downstream.

It does **not** authorize, execute, mutate, deploy, mark completion, or replace source inspection.

## Evidence levels

- **Observed** — only a claim with current P12 execution evidence and citable provenance.
- **Likely** — evidence-supported but not freshly established by current P12 execution evidence.
- **Unknown** — malformed, unresolved, contradictory, or otherwise not established.

A durable record cannot self-upgrade a claim to observed. `likely` remains an explicit uncertainty signal.

## Source and authority rules

- Current source/Git/provider evidence governs repository/provider facts.
- `.ai` durable state records semantic history and intent but does not manufacture live truth.
- P12 owns execution-evidence provenance and freshness.
- Resolver confidence never grants authorization or execution.
- Conflicting sources are surfaced; the resolver does not silently select the most convenient assertion.

## v2 deterministic implementation

`tools/ai-state-resolver.py` implements `DEVOS-AI-STATE-RESOLUTION-v2`.

### Base claim record

```yaml
- id: stable-claim-id
  statement: plain-language claim
  state_confidence: observed | likely | unknown
  grounding:
    type: execution_evidence | durable_state | none
    ref: P12-evidence-id or file-path-plus-line
  revalidated_at: ISO-8601 timestamp or null
  revalidate_on: [RECOVERY_BOUNDARY, HANDOFF_BOUNDARY, path-glob]
```

Legacy claims may omit structured fact identity. Such claims retain the existing v2 confidence/revalidation behavior but do not participate in cross-claim contradiction comparison.

### Structured fact identity

Claims that participate in deterministic contradiction detection add both fields:

```yaml
  fact_key: deployment.status
  fact_value: complete
```

Rules:

1. `fact_key` and `fact_value` are an all-or-nothing pair.
2. `fact_key` must be a non-empty string.
3. `fact_value` may be any JSON value.
4. Values are compared using stable canonical JSON (`sort_keys=True`, compact separators, UTF-8 text preserved).
5. No free-text/NLP inference is used to guess that two differently keyed claims mean the same thing.

An incomplete structured identity resolves to `unknown` with `FACT_IDENTITY_INCOMPLETE`.

## Confidence and grounding rules

- An `observed` claim without non-empty grounding becomes `unknown` with `OBSERVED_CLAIM_GROUNDING_MISSING`.
- Duplicate claim IDs become `unknown` with `DUPLICATE_CLAIM_ID`.
- Non-current P12 execution evidence causes observed confidence to decay to `likely` with `P12_EXECUTION_EVIDENCE_NOT_CURRENT`.
- Durable-state grounding is capped at `likely`; attempted durable-state observed confidence is downgraded with `DURABLE_STATE_CANNOT_SELF_UPGRADE_TO_OBSERVED`.
- Recovery/handoff boundaries and configured changed paths remain explicit revalidation reasons for durable-state claims.
- The resolver only preserves or downgrades caller-supplied confidence; it never upgrades confidence.

## Structured cross-claim contradiction handling

Claims with the same valid `fact_key` are grouped. If their canonical `fact_value` representations differ, every claim in that fact group becomes `unknown` and receives:

`CROSS_CLAIM_CONTRADICTION`

The result also contains deterministic `contradictions` entries:

```yaml
contradictions:
  - fact_key: deployment.status
    claim_ids: [C1, C2]
    canonical_values:
      - '"complete"'
      - '"not_performed"'
```

The resolver does **not** silently choose a winner based on freshness, confidence, source type, file order, or claim order. Even a current P12 claim conflicting with an older claim remains unresolved until upstream evidence or claim construction removes the disagreement. This prevents stale evidence from being ignored without an explicit reconciliation step.

Two structured objects with identical semantic JSON content but different object-key order canonicalize to the same value and are not treated as contradictory.

## Status and output

The resolver returns:

- `protocol: DEVOS-AI-STATE-RESOLUTION-v2`
- `authority: UNCHANGED`
- `authorization: UNCHANGED`
- `execution: NONE`
- `mutation: NONE`
- resolved `claims`
- `contradictions`
- `weakest_state_confidence`
- `unresolved_claim_ids`
- `state_confidence_summary`
- `status: RESOLVED | NEEDS_EVIDENCE | BLOCKED`

`RESOLVED` means no resolved claim is unknown. It does not mean authorized, verified, complete, production-ready, or executed.

`NEEDS_EVIDENCE` means at least one claim is unknown, including claims made unknown by structured contradiction detection.

`BLOCKED` means the top-level claims input is structurally invalid.

## P16 propagation

P16 independently validates the resolver envelope before planning. It recomputes:

- authority/execution invariants;
- confidence counts;
- weakest confidence;
- unresolved IDs;
- structured fact identity completeness;
- contradiction groups and contradiction summary consistency.

A contradictory resolver envelope therefore cannot be forged as `RESOLVED` by merely changing status/count fields. Contradictions propagate as unresolved claims, causing P16 to return `CLARIFY`.

P16 preserves the full validated resolver provenance in the plan when planning is allowed.

## P17 propagation

P17 independently revalidates the P16-preserved resolver provenance before declaring a step READY. It recomputes structured contradictions from the preserved claims rather than trusting only the `contradictions` list.

A post-P16 tamper that changes one `fact_value` while leaving status/confidence summaries unchanged fails closed with a resolver-state contradiction error.

This does not change P17 authorization, Security Gate, capability, verification, repository-freshness, or runtime gates.

```text
P11 recovery -> Resolver v2 -> P16 -> P17 -> controller
                    |            |      |
              claims only   no execution no authorization
```

## Deterministic reasons

Current resolver reasons include:

- `CLAIM_ID_OR_STATEMENT_INVALID`
- `STATE_CONFIDENCE_INVALID`
- `GROUNDING_TYPE_INVALID`
- `OBSERVED_CLAIM_GROUNDING_MISSING`
- `DUPLICATE_CLAIM_ID`
- `FACT_IDENTITY_INCOMPLETE`
- `P12_EXECUTION_EVIDENCE_NOT_CURRENT`
- `DURABLE_STATE_CANNOT_SELF_UPGRADE_TO_OBSERVED`
- `REVALIDATION_BOUNDARY_REACHED`
- `REVALIDATION_PATH_CHANGED`
- `CROSS_CLAIM_CONTRADICTION`

## Safety and non-goals

- No automatic prose-to-fact-key inference.
- No automatic choice of a winning contradictory claim.
- No P12 evidence re-normalization.
- No provider call, deployment, mutation, credential change, or permission change.
- No authorization, completion marking, or production-readiness upgrade.
- No new numbered DevOS phase is created by resolver hardening.

## Continuation path

`tools/devos-continuation-path.py` may call resolver v2 when state claims/events/changed paths are supplied. Unknown or contradictory claims prevent the resolver/P16/P17 path from silently continuing as if state were settled.

For how this contract evolved and which earlier stages introduced each boundary, see `docs/AI-STATE-RESOLVER-EVOLUTION.md`.
