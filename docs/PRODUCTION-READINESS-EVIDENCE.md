# Production Readiness Evidence v2

The current machine-readable assessment is [`config/production-readiness-v2.json`](../config/production-readiness-v2.json). The historical PR #16/v1 ledger remains preserved at [`config/readiness-evidence.json`](../config/readiness-evidence.json) and is not rewritten into current evidence.

Run:

```bash
python tools/devos.py production-readiness --json
python tools/devos.py production-readiness --require-production --json
```

The first command validates the assessment model. The second additionally requires an actual `READY` verdict and therefore fails closed while any production blocker remains.

## Current verdict

**HOLD — `production_ready = false`.**

This is no longer a generic or protocol-hard-coded false flag. It is derived from the exact set of production-required criteria still in `HOLD`.

Current production blockers:

1. `runtime_direct_conformance` — no production runtime has a separately observed direct conformance proof durably promoted from declaration-only state.
2. `recovery_disaster` — no production storage/backup target with measured restore RPO/RTO evidence is defined.
3. `operational_observability` — no production service target, SLOs, alert routing, or incident-response evidence is defined.
4. `deployment_target` — no production environment contract with rollout, rollback, and production readback evidence exists.
5. `high_impact_governance` — production-scoped high-impact operations remain separately authorization-gated and unproven.

`production_blockers` must exactly match all required criteria in `HOLD`; the verifier rejects attempts to conceal one.

## Target-specific external evidence intake

DevOS 0.20.0 adds [`core/production-target-evidence-intake.md`](../core/production-target-evidence-intake.md) and `tools/production-target-evidence.py` as a **read-only candidate-evidence intake boundary** for the five external blockers above.

The intake binds already-observed evidence to an exact production target ID, exact source SHA, timezone-aware observation timestamp, observer, criterion set, evidence references/digests/scopes, and unchanged authority boundaries.

```bash
python tools/devos.py production-target-evidence <packet.json> \
  --expected-source-sha <sha> \
  --expected-target-id <target>
```

A fully valid all-PASS packet returns `CANDIDATE_COMPLETE`, but still fixes:

```text
readiness_promotion_allowed = false
semantic_review_required = true
production_ready = false
execution = NONE
mutation = NONE
publication_authorized = false
deployment_authorized = false
```

Therefore a candidate packet can never self-promote this readiness matrix. A separate semantic review and durable readiness reconciliation must determine whether the evidence is current, applicable, sufficiently scoped, and safe to promote.

The intake does not authorize or execute production probes, deployments, destructive restore tests, credential/permission/database changes, or other high-impact operations.

## Already-proven criteria

### Source integrity — PROVEN

The repository has a canonical version/release manifest, fail-closed distribution release gate, cross-platform release matrix, and exact-source ZIP/SHA-256 artifact process. Every new merged source must still re-establish its exact-source evidence.

### Authorization and security — PROVEN

P17 readiness, Security Gate verification, scoped approval semantics, and remote-resource permission governance are implemented and regression-tested. These mechanisms preserve the rule that readiness, credentials, documentation, CI, or evidence cannot create authorization.

### Deterministic verification — PROVEN

The repository includes deterministic/integration/security verification contracts and adversarial readiness/target-evidence corpora. A green suite is evidence only; it is not permission to execute or deploy.

### Provider read — PROVEN at bounded current-live-read scope

The GitHub App authentication/read path has current bounded live-read evidence. Provider capability remains distinct from DevOS authority.

### Remote mutation — PROVEN at bounded historical-live scope

The governed GitHub path has durable real provider proof for scoped create/update/delete plus readback/reconciliation. Recorded provider commits are:

- create `e8235f7864678a27bbf036def806a1624fb66678`
- update/reconciliation `27a3b3cf4f7c8c8511f3c5a8f3283d8a6a883232`
- delete `3f530da3ee1efd4e52baad10fe4e644d4db5d116`

This proves the bounded mutation mechanism. It does **not** authorize arbitrary production mutation and does not satisfy the separate `high_impact_governance` production criterion.

## Evidence classes

- `current_source` — represented and verified in the exact source tree.
- `current_live_read` — current bounded external read evidence.
- `bounded_live_current` — direct bounded live evidence for a specifically defined production criterion.
- `bounded_live_historical` — durable historical live proof whose scope remains pinned.
- `external_required` — repository evidence alone cannot close the criterion; it must remain `HOLD`.

A criterion cannot be marked `PROVEN` with `external_required` evidence.

## Authority boundary

The assessment always keeps these independent of its readiness verdict:

```text
authority = UNCHANGED
authorization = UNCHANGED
execution = NONE
mutation = NONE
publication_authorized = false
deployment_authorized = false
evidence_can_authorize = false
```

Therefore:

```text
VALID ASSESSMENT != PRODUCTION READY
VALID TARGET EVIDENCE != PRODUCTION READY
PRODUCTION READY != PUBLICATION AUTHORIZATION
PRODUCTION READY != DEPLOYMENT AUTHORIZATION
EVIDENCE != AUTHORIZATION
```

Even a future evidence-backed `READY` verdict would not itself publish a release, deploy a production environment, mutate a provider, or grant credentials/permissions.

## v1 historical boundary

`config/readiness-evidence.json` and `tools/verify-readiness-evidence.py` remain historical v1 evidence integrity machinery. v1 intentionally rejected live/production claims and pinned old scenario evidence to old source heads. v2 does not falsify or relabel that history; it is a current-source assessment protocol that can represent later bounded live evidence while retaining its limitations.

## Completion rule

Production readiness can become `READY` only when all ten required criteria are directly evidenced, semantically reviewed, and durably reconciled. No high-impact operation should be performed merely to make the matrix green. External production evidence must come from a separately defined target and separately authorized activity, then be documented and durably reconciled.
