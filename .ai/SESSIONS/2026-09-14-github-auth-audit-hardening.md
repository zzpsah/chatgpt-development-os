# Session — 2026-09-14 — PR #32 Audit Hardening

## Objective
Close the pre-merge audit gaps in the GitHub Identity & Token Control Plane v1 without performing live OAuth, secret mutation, destructive provider operations, deployment, or production changes.

## Audit gaps verified on the branch before this change
1. OAuth callback validation compared state values but did not enforce transaction freshness or one-time consumption.
2. Capability discovery checked permission-name presence but not required permission level, allowing `read` to satisfy a write-capability mapping.
3. Existing-repository capabilities did not verify that the requested target repository belonged to the provider-reported repository scope.
4. Durable state self-pinned stale branch SHAs and CI snapshots.
5. The dedicated GitHub auth/control-plane verifier did not run on relevant pushes to `main`.

## Implemented
- OAuth callback validation now receives the pending `OAuthTransaction`, enforces a bounded state lifetime, rejects callbacks that predate the transaction, and fail-closes already-consumed/reused state.
- The deployment boundary remains responsible for storing pending/consumed OAuth transaction state outside Git; the checked-in primitive enforces freshness/reuse semantics deterministically.
- Provider permission mappings now include minimum levels; known GitHub `read`/`write` levels are compared fail-closed.
- Existing-repository capabilities require an explicit target repository inside the normalized repository scope before `AVAILABLE` may be returned.
- Unknown permission levels, missing target, invalid mapping, or missing provider mapping return `UNCONFIRMED`; insufficient permission or out-of-scope target returns `UNAVAILABLE`.
- Capability evidence now includes target repository and repository scope while preserving `credential_material: NOT_INCLUDED`, `authorization: UNCHANGED`, `execution: NONE`, and `mutation: NONE`.
- Regression tests cover stale OAuth state, reused OAuth state, read-vs-write insufficiency, outside-scope target, and missing target.
- Dedicated auth/control-plane CI now also runs on relevant pushes to `main`.
- `.ai/CURRENT-STATE.md` and `.ai/TASKS.md` no longer self-pin a mutable branch head; Git/PR metadata are explicitly authoritative for exact-head recovery.

## Evidence boundary
This session records repository implementation and deterministic test intent only. Final exact-head CI must be observed after the commit containing these changes. Live GitHub App registration/installation, Actions secret configuration, manual provider authentication, and provider readback remain separate external evidence.

`PROVIDER CREDENTIAL != DEVOS AUTHORIZATION`

`CI PASS != AUTHORIZATION`

`production_ready=false`

`live_provider_proven=false`

## Next recovery step
Inspect PR #32. If open, require all applicable exact-head workflows to be green before merge. If merged, inspect fresh push CI on the merge commit. Do not infer live-provider proof from repository CI.
