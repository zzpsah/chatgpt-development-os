# Production Target Evidence Intake v1

## Purpose

This contract provides a deterministic, read-only intake boundary for the five **external** criteria currently holding DevOS Production Readiness Evidence v2:

- `runtime_direct_conformance`
- `recovery_disaster`
- `operational_observability`
- `deployment_target`
- `high_impact_governance`

It does not execute probes, deploy software, change provider state, alter credentials or permissions, mutate databases, or grant production authority. It only validates an already-produced evidence packet for one explicitly named production target.

## Core rule

```text
VALID TARGET EVIDENCE != PRODUCTION READY
VALID TARGET EVIDENCE != AUTHORIZATION
VALID TARGET EVIDENCE != DEPLOYMENT AUTHORIZATION
```

A complete packet is **candidate evidence only**. Separate semantic review and durable Production Readiness v2 reconciliation are required before any readiness criterion can change.

## Packet protocol

`DEVOS-PRODUCTION-TARGET-EVIDENCE-v1`

One packet binds evidence to:

- canonical repository;
- exact 40-character source SHA;
- exact production target ID;
- target kind/reference;
- timezone-aware observation timestamp;
- observer kind/reference;
- exactly the five external readiness criteria;
- per-criterion evidence references, SHA-256 digests, observed scope, and limitations;
- global limitations;
- unchanged authority boundaries.

Only references/digests are accepted. The protocol has no field for raw credentials, tokens, secrets, private keys, database passwords, or equivalent secret material.

## Criterion states

Each required criterion is one of:

- `PASS` — evidence exists for this exact target/scope;
- `FAIL` — evidence exists and shows the criterion failed;
- `UNOBSERVED` — no acceptable observation has been supplied.

`PASS` and `FAIL` require evidence. `UNOBSERVED` must not pretend to have evidence.

## Verdicts

### `BLOCKED`

The packet is structurally invalid, target/source binding is wrong, evidence integrity is malformed, a required criterion is missing/duplicated/unknown, or an authority boundary changed.

### `HOLD`

The packet is structurally valid, but at least one required criterion is `FAIL` or `UNOBSERVED`.

### `CANDIDATE_COMPLETE`

All five required criteria carry target-bound `PASS` evidence. This still returns:

```text
readiness_promotion_allowed = false
semantic_review_required = true
production_ready = false
deployment_authorized = false
publication_authorized = false
execution = NONE
mutation = NONE
```

The intake layer therefore cannot self-promote Production Readiness v2.

## Freshness and scope

The packet records the exact observation timestamp, source SHA, target ID, target reference, and evidence digest. A later source head, deployment, target identity, runtime, backup topology, observability setup, permission model, or production configuration can invalidate the practical applicability of older evidence even if the old packet remains cryptographically intact.

Freshness policy belongs to the later semantic/readiness reconciliation step; the intake tool must not silently infer that old evidence still applies.

## High-impact boundary

This contract intentionally accepts **evidence after an observation occurred**. It does not authorize that observation or operation to occur.

In particular, production deployment, destructive restore testing, permission changes, credential/secret changes, database mutation, force operations, or other high-impact work still require their own current P17/security/approval path before execution.

## Reference implementation

- validator: `tools/production-target-evidence.py`
- adversarial corpus: `tools/test-production-target-evidence.py`
- CI: `.github/workflows/verify-production-target-evidence.yml`

The reference implementation is provider-neutral and performs no network/provider mutation.
