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

## Active bounded work

- No numbered or unnumbered implementation objective is active by default after DevOS 0.19.0 reconciliation.
- Future work must recover fresh `main`, CI/issues/PRs, relevant source/tests, direct external evidence, concurrent AI work, and current user intent.
- Do not create P18/P19 merely for bookkeeping.

## Completed — DevOS 0.19.0 Production Readiness Evidence v2

- [x] Recover fresh `main` and confirm no open PR/issue blocker before starting.
- [x] Identify the historical `DEVOS-READINESS-EVIDENCE-v1` limitation: live/production claims were intentionally unrepresentable.
- [x] Define separate current-source `DEVOS-PRODUCTION-READINESS-EVIDENCE-v2` without rewriting historical v1 evidence.
- [x] Model exactly ten production-required criteria and derive blockers deterministically.
- [x] Represent already-proven source/security/verification/provider-read/bounded-live-mutation evidence at exact bounded scope.
- [x] Model unresolved production-runtime, disaster-recovery, observability, deployment-target, and high-impact-governance evidence as explicit HOLD criteria.
- [x] Add fail-closed verifier and adversarial regression corpus.
- [x] Add dedicated Python 3.11/3.12 CI.
- [x] Add `devos production-readiness` and fail-closed `--require-production` CLI behavior.
- [x] Advance source identity coherently to `0.19.0` instead of silently mutating verified 0.18.0 artifact identity.
- [x] Update release manifest, README, changelog, readiness docs, and status docs.
- [x] Verify exact feature head `f81184975ffbb02a3e58466459e12858fdd8294a`: **14/14 applicable workflows success**.
- [x] Verify dedicated feature-head readiness workflow `34845941978`: Python 3.11 + 3.12 success.
- [x] Verify feature-head distribution release workflow `34845941874`: Ubuntu/Windows × Python 3.11/3.12 **4/4 success**.
- [x] Merge PR #66 through expected-head protection at merge commit `8cd731b7b91ca9e67983b6deca8646b38e078e33`.
- [x] Verify post-merge exact-main push workflows: **11/11 success**.
- [x] Verify post-merge readiness workflow `34846071705`: success.
- [x] Verify post-merge distribution release workflow `34846071713`: release matrix **4/4 success**.
- [x] Verify exact merged-source artifact ID `10348113380`, name `devos-source-8cd731b7b91ca9e67983b6deca8646b38e078e33`, digest `sha256:fd07fcebcaebca703c11787e634940de904e85be5e3115894808b6a7955307f0`, size `744297` bytes.
- [x] Perform semantic durable-state review for CURRENT/TASKS/history/master-map materiality.
- [x] Generate durable reconciliation record digest `8a8ce6db2bccbe211030ab681577736717e978cab8760c074e65faca09c8d49f`.

Repo-side completion status: **IMPLEMENTED + VERIFIED + DOCUMENTED + DURABLE STATE pending only this reconciliation PR merge/readback**. After that merge, no additional reconciliation loop is required for the reconciliation-only change itself.

## Current Production Readiness v2 HOLD criteria

The model is complete, but production readiness remains correctly **HOLD** / `production_ready=false` until direct target-specific evidence exists for:

- `runtime_direct_conformance` — direct observed proof for a production runtime.
- `recovery_disaster` — production storage/backup restore with measured RPO/RTO.
- `operational_observability` — production SLOs, alert routing, telemetry, and incident-response evidence.
- `deployment_target` — explicit production target with rollout, rollback, and readback evidence.
- `high_impact_governance` — separately authorized production-scoped high-impact proof.

These are external evidence requirements, not permission to perform the operations. Do not execute production/high-impact operations merely to make the readiness matrix green.

## Completed — DevOS 0.18.0 Agent Runtime Conformance Evidence Intake v1

- PR #64 merged at `a8f19687c177359bd5f646e10913ebdae0851a53` from exact feature head `f59fad07b6f7708cfc79f173625f9ddafa7bc5ae`.
- PR #65 durable reconciliation merged at `b221a240a41426b200a9235eacfa5300042936c0`.
- Exact-source artifact after PR #65: ID `10346418633`, digest `sha256:61e8bc4a4b20c326d2286fc619d202265b9bdd3edbf3feddc70316249cd010f6`.
- No vendor runtime was promoted; `EVIDENCE_PACKET_VALID != VERIFIED RUNTIME` remains enforced.

## Retained platform foundations

- P9 through P17 remain completed architecture stages at their recorded evidence levels.
- P11 remains repository-first recovery/revalidation/cross-AI continuity baseline.
- P12 remains evidence provenance/freshness owner.
- P15 remains language interpretation; P16 planning; P17 readiness/authorization.
- AI State Resolver v2 envelope/contradiction hardening remains closed through its recorded PR sequence.
- GitHub governed provider capability, readback reconciliation, multi-project isolation, Actionable HOLD, current-source evidence, onboarding, recovery, adaptive verification/self-healing, trust-first auditing, runtime-neutral handoff, runtime-profile registry, runtime-conformance evidence intake, distribution release machinery, production-readiness evidence v2, and evidence/durable-state reconciliation remain retained foundations.
- `docs/DEVOS-ENGINEERING-STAGE-HISTORY.md` is the durable milestone ledger.
- `docs/DEVOS-MASTER-ENGINEERING-MAP.md` remains the living architecture map.

## Current HOLD / limits

- `production_ready = false` while any required v2 criterion is HOLD.
- Distribution release readiness is not production or publication authorization.
- No public Git tag/GitHub Release/package publication/deployment is authorized by the 0.19.0 readiness objective.
- Machine evidence never grants authority, execution, provider permission, or production readiness.
- A `DECLARED` runtime profile is not a verified integration.
- Historical evidence remains pinned to its source head.
- Uncertain provider mutation is never blindly replayed.
- Parallel AI branches must revalidate against fresh `main` before integration.

## Task-map invariant

`AI A + Account A → repository → AI B + Account B → correct recovery → safe continuation`

The repository, not any AI account/chat/model/vendor memory, carries authoritative project state.