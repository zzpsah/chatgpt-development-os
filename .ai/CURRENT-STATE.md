# Current State

## Current source and authority

- Repository: `zzpsah/chatgpt-development-os`.
- Current source tree + Git/PR/CI/release-artifact metadata are authoritative for exact implementation/integration state; `.ai` records carry durable semantic context.
- **ChatGPT Memory/chat history and any model/account memory are supplementary only and never authoritative project state.**
- Latest fully merged/reconciled `main` before the active objective: `69b06853d5f360659ce42d5cf2c5ec7c8dccc04d` (PR #67 durable reconciliation for DevOS 0.19.0).
- Final 0.19.0 exact-source artifact: ID `10355742368`, source `69b06853d5f360659ce42d5cf2c5ec7c8dccc04d`, digest `sha256:8de1daa8c592c5a3a2128493a1ba6c728ce975d45662253d783cf6aa8ff40bbf`.
- Active branch: `feature/production-target-evidence-intake-v1`, created from exact `69b06853d5f360659ce42d5cf2c5ec7c8dccc04d` after confirming 0 open PRs and 0 open issues.
- Candidate distribution version: `0.20.0`.
- `docs/DEVOS-MASTER-ENGINEERING-MAP.md` remains the living architecture index; no P18/P19 is created for this unnumbered evidence-intake milestone.

## Core documentation law

> **What is not written was never done.**

Material work follows:

`OBSERVE → ACT / CHANGE / DECIDE → VERIFY → DOCUMENT → PERSIST IN GIT`

Completion requires:

`IMPLEMENTED + VERIFIED + DOCUMENTED + DURABLE STATE`

## Canonical governed path

`Human request → P15 interpretation → state resolution → P16 plan → P17 readiness → Actionable HOLD / Scoped Approval → controller → bounded runtime → verification → evidence/durable-state reconciliation → persistence → recovery / continuation`

Interpretation, planning, readiness, credentials, CI, generated facts, evidence intake, reconciliation metadata, prior approvals, recovery state, documentation, or release status never manufacture permission.

## Active bounded work — DevOS 0.20.0 Production Target Evidence Intake v1

Fresh recovery after DevOS 0.19.0 found a specific G9 gap: Production Readiness Evidence v2 names five external blockers, but the repository had no common target-bound intake contract for direct evidence covering those blockers.

The active objective adds a **read-only candidate-evidence intake boundary** for:

- `runtime_direct_conformance`
- `recovery_disaster`
- `operational_observability`
- `deployment_target`
- `high_impact_governance`

Implemented on the active branch so far:

- `tools/production-target-evidence.py` — exact production target/source/timestamp/observer/criterion/evidence binding;
- `tools/test-production-target-evidence.py` — adversarial fail-closed corpus;
- `.github/workflows/verify-production-target-evidence.yml` — Python 3.11/3.12 verification;
- `core/production-target-evidence-intake.md` — normative contract;
- `devos production-target-evidence` CLI dispatch;
- source identity advanced coherently to `0.20.0`;
- release manifest, README, changelog and current Production Readiness v2 source identity updated.

Pending before closure:

1. exact feature-head CI and regression verification;
2. fix any CI defects without weakening evidence or authority boundaries;
3. expected-head PR merge after green CI;
4. fresh merged-main CI and exact-source 0.20.0 artifact verification;
5. final durable reconciliation/history update.

## Production Target Evidence v1 semantics

A valid packet binds already-observed evidence to one exact production target and exact source SHA. Required criterion states are `PASS | FAIL | UNOBSERVED`.

- malformed/unsafe packet → `BLOCKED`;
- structurally valid but incomplete/failed evidence → `HOLD`;
- all five criteria PASS → `CANDIDATE_COMPLETE`.

`CANDIDATE_COMPLETE` is deliberately **not** production readiness. It still fixes:

- `readiness_promotion_allowed = false`
- `semantic_review_required = true`
- `production_ready = false`
- `authority = UNCHANGED`
- `authorization = UNCHANGED`
- `execution = NONE`
- `mutation = NONE`
- `publication_authorized = false`
- `deployment_authorized = false`

A later separate semantic review + durable Production Readiness v2 reconciliation is required before any blocker can change status.

## Current Production Readiness v2 verdict

Current deterministic verdict remains **HOLD**.

`production_ready = false`

Already PROVEN at bounded scopes:

- `source_integrity`
- `authorization_security`
- `deterministic_verification`
- `provider_read`
- `remote_mutation`

Still requiring direct target-specific external evidence:

- `runtime_direct_conformance`
- `recovery_disaster`
- `operational_observability`
- `deployment_target`
- `high_impact_governance`

The new intake contract makes these evidence requirements machine-checkable; it does not authorize the underlying production/high-impact operations and does not fabricate the missing evidence.

## Permanent boundaries

- `CONTINUE != BLANKET AUTHORIZATION`.
- `INTERPRETATION != AUTHORIZATION`.
- `PLAN != EXECUTION`.
- `READY != EXECUTION`.
- `CI PASS != AUTHORIZATION`.
- `DOCUMENTATION != AUTHORIZATION`.
- `VALID TARGET EVIDENCE != PRODUCTION READY`.
- `PRODUCTION READY != PUBLICATION AUTHORIZATION`.
- `PRODUCTION READY != DEPLOYMENT AUTHORIZATION`.
- Provider credentials/capability never manufacture DevOS authority.
- Uncertain provider mutation is never blindly replayed.

## Explicit non-actions

This objective does not itself run a production probe, deploy software, change credentials/secrets/permissions/databases, perform destructive restore testing, execute a production-scoped high-impact action, promote a runtime, publish a release/tag/package, or change production readiness.

## Recovery precedence

1. Current source tree + Git/PR/CI/release-artifact metadata.
2. Explicit current user requirements and durable decisions.
3. `.ai/CURRENT-STATE.md`, `.ai/TASKS.md`, `.ai/RECONCILIATION-LEDGER.jsonl`.
4. Relevant core contracts/tests/configuration.
5. `.ai/SESSIONS/` and historical evidence.
6. Chat/model memory only as supplementary context.

## Next action

Open the bounded 0.20.0 feature PR, use exact-head CI as source of truth, repair any failures, merge only after clean concurrency/head checks, then verify merged-main release evidence and reconcile durable state.
