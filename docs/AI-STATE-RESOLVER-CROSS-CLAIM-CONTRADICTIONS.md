# AI State Resolver v2 — Cross-Claim Contradiction Contract

## Objective

Add deterministic cross-claim contradiction detection without turning the resolver into a prose reasoner, authority engine, or execution engine.

The resolver remains read-only and preserves:

- `authority: UNCHANGED`
- `authorization: UNCHANGED`
- `execution: NONE`
- `mutation: NONE`

## Explicit fact identity

A claim may optionally add:

```yaml
fact_key: deployment.complete
fact_value: true
```

`fact_key` is the stable identity of the fact being asserted. `fact_value` is the deterministic JSON value asserted for that fact.

Both fields are optional for backward compatibility, but when one is supplied the other must also be supplied; statement text is never semantically paired by guesswork. Two claims are compared only when they explicitly provide the same valid `fact_key`.

## Deterministic comparison

`fact_value` is canonicalized as JSON with stable object-key ordering. Therefore equivalent structured values compare equal even when their input object key order differs.

Examples:

- `deployment.complete = true` and `deployment.complete = true` → no contradiction.
- `deployment.complete = true` and `deployment.complete = false` → contradiction.
- `release.targets = {"a":1,"b":2}` and `release.targets = {"b":2,"a":1}` → same value, no contradiction.
- Different `fact_key` values are unrelated and are not compared.

## Contradiction behavior

When two or more otherwise-resolved claims have the same `fact_key` but different canonical values:

1. every involved claim becomes `state_confidence: unknown`;
2. every involved claim receives reason `CROSS_CLAIM_CONTRADICTION`;
3. the fact identity is listed in `contradiction_fact_keys`;
4. claim IDs are listed in `unresolved_claim_ids`;
5. resolver status becomes `NEEDS_EVIDENCE`.

The resolver does not select a winner based on confidence, source type, ordering, recency text, or convenience. A separate fresh evidence step must resolve the conflict.

## Malformed fact identity

The following fail closed to `unknown`:

- only one of `fact_key` / `fact_value` supplied → `FACT_IDENTITY_INCOMPLETE`;
- empty/non-text `fact_key` → `FACT_KEY_INVALID`;
- a value that cannot be represented as deterministic JSON → `FACT_VALUE_INVALID`.

Legacy claims with neither field remain valid and retain existing v2 behavior.

## P16 / P17 propagation and envelope integrity

Contradictions use the existing unresolved-state path rather than creating a parallel control plane:

```text
contradictory claims
  ↓
resolver: NEEDS_EVIDENCE
  ↓
P16 returns `CLARIFY`
  ↓
no executable plan from unresolved state
```

The downstream layers do not trust only the resolver's top-level status/count metadata.

### P16 defense in depth

P16 independently recomputes explicit `fact_key`/`fact_value` groups from the preserved resolver claims. It verifies that:

- a conflicting fact group remains `unknown`;
- every conflicting claim retains `CROSS_CLAIM_CONTRADICTION`;
- `contradiction_fact_keys` matches the actual conflicting fact identities;
- malformed or unserializable structured facts cannot be presented as a valid resolved envelope.

A forged resolver envelope that changes contradictory claims back to `likely`, clears unresolved IDs, changes status to `RESOLVED`, or removes contradiction metadata therefore becomes `CLARIFY` instead of a plan.

### P17 defense in depth

P17 independently recomputes the same structured contradiction integrity from the full resolver provenance preserved in a P16 plan.

This closes a separate post-planning tamper path: if a previously consistent fact group is altered after P16 by changing one `fact_value` while leaving confidence/status/count metadata untouched, P17 returns `BLOCKED` with a hidden-contradiction reason rather than declaring the step READY.

The checks are deliberately redundant across resolver → P16 → P17. Each governed boundary validates the evidence it consumes rather than assuming the previous boundary remained untampered.

## Boundaries

This feature and its envelope-integrity hardening do not grant authorization, do not choose which claim is true, do not execute verification, do not mutate a provider, and do not change `production_ready`.

P12 still owns execution-evidence provenance and freshness. P16 still owns plan compilation. P17 still owns step readiness/authorization checks.

## Non-goals

- Natural-language semantic equivalence of arbitrary statements.
- Automatic ontology construction.
- Cross-project fact reconciliation.
- Automatic source-precedence winner selection.
- Timestamp-based truth selection without an explicit future contract.
- Permission, completion, or production-readiness inference.
