# DevOS Production Readiness Evidence v2

## Purpose

`DEVOS-PRODUCTION-READINESS-EVIDENCE-v2` is the current-source production-readiness assessment contract for DevOS.

It exists because the historical v1 matrix was intentionally conservative and could not represent later current-source, live-read, or bounded live-mutation evidence. v2 closes that modeling gap without converting evidence into authority.

## Non-negotiable separation

```text
VALID ASSESSMENT != PRODUCTION READY
PRODUCTION READY != PUBLICATION AUTHORIZATION
PRODUCTION READY != DEPLOYMENT AUTHORIZATION
PRODUCTION READY != EXECUTION AUTHORIZATION
EVIDENCE != AUTHORIZATION
```

The evidence document therefore fixes these boundary fields independently of readiness verdict:

- `authority = UNCHANGED`
- `authorization = UNCHANGED`
- `execution = NONE`
- `mutation = NONE`
- `publication_authorized = false`
- `deployment_authorized = false`
- `evidence_can_authorize = false`

A verifier or CI run is never allowed to manufacture permission.

## Evidence classes

v2 recognizes these evidence classes:

- `current_source` — directly represented and regression-verified in the exact source tree.
- `current_live_read` — bounded current external read evidence.
- `bounded_live_current` — direct bounded live evidence for a specifically defined production criterion.
- `bounded_live_historical` — durable historical live proof whose scope and limitations remain pinned.
- `external_required` — evidence cannot be established from repository source alone and the criterion must remain `HOLD`.

`PROVEN` may never use `external_required`. A `HOLD` criterion must state a concrete blocker and remain `external_required` until direct evidence exists.

## Required criteria

Every assessment contains exactly these production-required criteria:

1. `source_integrity`
2. `authorization_security`
3. `deterministic_verification`
4. `provider_read`
5. `remote_mutation`
6. `runtime_direct_conformance`
7. `recovery_disaster`
8. `operational_observability`
9. `deployment_target`
10. `high_impact_governance`

The criteria set is closed. Unknown, missing, or duplicate criteria are invalid rather than silently ignored.

## Verdict rule

The verdict is deterministic:

```text
all required criteria PROVEN -> verdict READY -> production_ready true
one or more required criteria HOLD -> verdict HOLD -> production_ready false
invalid/tampered evidence -> verdict INVALID -> production_ready false
```

`production_blockers` must exactly equal the sorted IDs of required criteria in `HOLD`. It cannot be hand-edited to conceal an unresolved criterion.

## Current live GitHub evidence

The scoped governed GitHub mutation path has durable historical live proof for create/update/delete plus fresh readback/reconciliation. The v2 `remote_mutation` criterion may therefore be `PROVEN` using `bounded_live_historical` evidence.

That evidence does **not** prove arbitrary production mutation and does not grant production permissions. Production-scoped high-impact governance remains its own required criterion.

## Current HOLD criteria

At introduction of v2, repository evidence does not establish:

- a directly verified production runtime,
- a production backup/restore target with measured RPO/RTO,
- production SLO/alert/incident-response telemetry,
- a production deployment target with rollout/rollback/readback evidence,
- separately authorized production-scoped high-impact operations.

Those gaps are explicitly modeled rather than hidden behind a blanket `production_ready=false` statement.

## Verification behavior

`tools/verify-production-readiness-v2.py` validates:

- exact schema and criterion identity,
- current `VERSION` binding,
- authority/publication/deployment boundaries,
- evidence-reference existence and repository containment,
- exact blocker derivation,
- verdict / `production_ready` consistency,
- known live-mutation provenance markers,
- evidence-class constraints.

A structurally valid current `HOLD` assessment exits successfully in normal validation mode so CI can prove the model is healthy. `--require-production` exits non-zero until the deterministic verdict is `READY`.

## Change rule

A criterion may move from `HOLD` to `PROVEN` only when the relevant direct evidence exists and survives adversarial verification. A familiar provider/runtime name, user intent, a credential, a green unrelated workflow, or a previous approval is not enough.

Any future transition to `production_ready=true` must preserve all authorization boundaries unless a separate explicitly scoped decision changes them.
