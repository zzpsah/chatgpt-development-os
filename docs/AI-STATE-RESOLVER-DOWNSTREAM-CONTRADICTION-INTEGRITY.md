# AI State Resolver v2 — Downstream Contradiction Integrity

## Objective

Harden the resolver → P16 → P17 handoff so a contradiction cannot be hidden by modifying preserved claim values or top-level contradiction metadata after resolver execution.

This is an unnumbered defense-in-depth objective. It does not create P18/P19.

## Gap

PR #46 made the resolver detect explicit `fact_key` / `fact_value` contradictions and propagate them as unresolved claims. However, P16 and P17 still trusted the resolver's contradiction classification too much.

A forged envelope could theoretically alter `fact_value` after resolver execution while leaving confidence/status summaries unchanged. Without independent recomputation, downstream layers could miss the new contradiction.

## Hardening

### Resolver provenance

The resolver now includes both:

- `contradiction_fact_keys` — compact fact identities;
- `contradictions` — deterministic detailed provenance with fact key, involved claim IDs, and canonical values.

Legacy claims without explicit fact identity omit `fact_key` / `fact_value` from normalized output. Malformed identities remain unresolved and are not propagated as valid comparison pairs.

### P16 independent recomputation

P16 recomputes contradiction groups from the preserved claims themselves.

It rejects a resolver envelope when:

- fact identity is structurally inconsistent;
- conflicting values exist but claims were not marked unknown;
- detailed contradiction metadata does not match recomputed claim values.

A hidden contradiction therefore produces `CLARIFY`; it cannot compile into a trusted executable plan.

### P17 independent recomputation

P17 performs the same claim-value recomputation on the P16-preserved resolver provenance.

If a valid plan is tampered after P16 by changing a `fact_value`, P17 detects the new contradiction and returns `BLOCKED` with `PLAN_STATE_RESOLUTION_HIDDEN_CONTRADICTION` rather than READY.

## Adversarial cases

Regression coverage includes:

- resolver contradiction → P16 `CLARIFY`;
- forged resolver envelope that resets contradictory claims to `likely` and hides contradiction metadata;
- valid same-value claims compiled by P16, followed by post-P16 fact-value tampering before P17;
- existing hidden-unknown, authority, execution, and envelope consistency tampering.

## Boundaries

- `authority = UNCHANGED`
- `authorization = UNCHANGED`
- resolver/P16/P17 execution = `NONE`
- no provider mutation is introduced by this hardening
- `production_ready = false` remains unchanged
- P12 still owns execution-evidence provenance/freshness
- P16 still owns planning
- P17 still owns readiness/authorization gating

## Provenance

The useful downstream-recomputation idea was identified while reviewing closed/superseded PR #47 after merged PR #46. PR #47 itself remains unmerged because it duplicated the main feature and contained stale/overlapping durable-state work. Only the narrower verified defense-in-depth concept is promoted from fresh `main`.
