# DevOS Tasks

## How to read this file

This file tracks **work state**, not normative law. Current source/Git/PR/CI/release-artifact metadata are authoritative for exact implementation state. Durable principles and authorization/security decisions live in `.ai/DECISIONS.md` and core contracts. Historical milestone detail lives in `docs/DEVOS-ENGINEERING-STAGE-HISTORY.md` and `.ai/SESSIONS/`.

## Core safety invariants

- **What is not written was never done.**
- `CONTINUE != BLANKET AUTHORIZATION`.
- `INTERPRETATION != AUTHORIZATION`.
- `PLAN != EXECUTION`.
- `READY != EXECUTION`.
- `CI PASS != AUTHORIZATION`.
- `VALID ASSESSMENT != PRODUCTION READY`.
- `PRODUCTION READY != PUBLICATION AUTHORIZATION`.
- `PRODUCTION READY != DEPLOYMENT AUTHORIZATION`.
- provider credentials/capability never manufacture DevOS authority.
- a valid runtime conformance evidence packet never self-promotes a registry entry.
- evidence never manufactures publication/deployment/execution authorization.

## Active bounded work — DevOS 0.19.0 Production Readiness Evidence v2

- [x] Recover fresh `main` and confirm no open PR/issue blocker before starting.
- [x] Identify the structural limitation in historical `DEVOS-READINESS-EVIDENCE-v1`: live/production claims are intentionally unrepresentable.
- [x] Define a new current-source `DEVOS-PRODUCTION-READINESS-EVIDENCE-v2` model instead of rewriting historical v1 evidence.
- [x] Model exactly ten production-required criteria and derive blockers deterministically.
- [x] Represent already-proven source/security/verification/provider-read/bounded-live-mutation evidence at its exact scope.
- [x] Model unresolved production-runtime, disaster-recovery, observability, deployment-target, and high-impact-governance evidence as explicit HOLD criteria.
- [x] Add fail-closed verifier and adversarial regression corpus.
- [x] Add dedicated Python 3.11/3.12 CI for v2.
- [x] Add `devos production-readiness` and fail-closed `--require-production` CLI behavior.
- [x] Advance source identity coherently to `0.19.0`; do not silently mutate the verified 0.18.0 artifact identity.
- [x] Update release manifest, README, changelog, readiness docs, and current status docs.
- [ ] Verify exact feature-head CI, including release matrix and production-readiness v2 workflow.
- [ ] Open and merge through expected-head protection only after exact-head CI is green.
- [ ] Verify fresh merged `main`, triggered CI, and exact-source 0.19.0 artifact/digest.
- [ ] Reconcile final merge/CI/artifact evidence into durable state and engineering history.

Current expected v2 verdict is **HOLD**, not READY. Repo-side completion means the readiness model is accurate, fail-closed, verified, documented, and durable. It does not authorize or fabricate the five external production proofs.

Do not execute production/high-impact operations merely to make the readiness matrix green.

Do not create P18/P19 merely for bookkeeping.

## Current production blockers modeled by v2

- `runtime_direct_conformance` — direct observed proof for a production runtime.
- `recovery_disaster` — production storage/backup restore with measured RPO/RTO.
- `operational_observability` — production SLOs, alert routing, telemetry, and incident-response evidence.
- `deployment_target` — explicit production target with rollout, rollback, and readback evidence.
- `high_impact_governance` — separately authorized production-scoped high-impact proof.

These are external evidence requirements, not permission to perform the operations.

## Completed — DevOS 0.18.0 Agent Runtime Conformance Evidence Intake v1

- PR #64 merged at `a8f19687c177359bd5f646e10913ebdae0851a53` from exact feature head `f59fad07b6f7708cfc79f173625f9ddafa7bc5ae`.
- Exact feature-head applicable CI: 13/13 success.
- Exact post-merge main push workflows: 10/10 success.
- Exact-source artifact from PR #64 merged source: ID `10342221168`, digest `sha256:894e369966e5172c609a6008c5f7086a78622b81b7f2794fa93990a88b09caf7`.
- PR #65 reconciled durable state; merged at `b221a240a41426b200a9235eacfa5300042936c0`.
- Exact-source artifact after PR #65: ID `10346418633`, digest `sha256:61e8bc4a4b20c326d2286fc619d202265b9bdd3edbf3feddc70316249cd010f6`.
- No vendor runtime was promoted; `EVIDENCE_PACKET_VALID != VERIFIED RUNTIME` remains enforced.

## Retained platform foundations

- P9 through P17 remain completed architecture stages at their recorded evidence levels.
- P11 remains repository-first recovery/revalidation/cross-AI continuity baseline.
- P12 remains evidence provenance/freshness owner.
- P15 remains language interpretation; P16 planning; P17 readiness/authorization.
- AI State Resolver v2 envelope/contradiction hardening remains closed through its recorded PR sequence.
- GitHub governed provider capability, readback reconciliation, multi-project isolation, Actionable HOLD, current-source evidence, onboarding, recovery, adaptive verification/self-healing, trust-first auditing, runtime-neutral handoff, runtime-profile registry, runtime-conformance evidence intake, and evidence/durable-state reconciliation remain retained foundations.
- `docs/DEVOS-ENGINEERING-STAGE-HISTORY.md` is the durable milestone ledger.
- `docs/DEVOS-MASTER-ENGINEERING-MAP.md` remains the living architecture map.

## Current HOLD / limits

- `production_ready = false` while any required v2 criterion is HOLD.
- Distribution release readiness is not production or publication authorization.
- No public Git tag/GitHub Release/package publication/deployment is authorized by this objective.
- Machine evidence never grants authority, execution, provider permission, or production readiness.
- A `DECLARED` runtime profile is not a verified integration.
- Historical evidence remains pinned to its source head.
- Uncertain provider mutation is never blindly replayed.
- Parallel AI branches must revalidate against fresh `main` before integration.

## Task-map invariant

`AI A + Account A → repository → AI B + Account B → correct recovery → safe continuation`

The repository, not any AI account/chat/model/vendor memory, carries authoritative project state.
