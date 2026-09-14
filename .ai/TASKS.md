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
- `VALID TARGET EVIDENCE != PRODUCTION READY`.
- `PRODUCTION READY != PUBLICATION AUTHORIZATION`.
- `PRODUCTION READY != DEPLOYMENT AUTHORIZATION`.
- provider credentials/capability never manufacture DevOS authority.
- candidate evidence never self-promotes readiness or runtime status.

## Active bounded work — DevOS 0.20.0 Production Target Evidence Intake v1

- [x] Recover fresh `main` at `69b06853d5f360659ce42d5cf2c5ec7c8dccc04d`.
- [x] Confirm 0 open PRs and 0 open issues before selecting the objective.
- [x] Identify the missing common intake boundary for the five external Production Readiness v2 blockers.
- [x] Add exact target/source/timestamp/observer/evidence binding.
- [x] Require exactly the five external blocker criteria.
- [x] Model `PASS | FAIL | UNOBSERVED` with fail-closed evidence rules.
- [x] Make all-PASS output `CANDIDATE_COMPLETE` while keeping `production_ready=false` and `readiness_promotion_allowed=false`.
- [x] Add adversarial regression coverage for source/target mismatch, missing/duplicate/unknown criteria, evidence omissions, invalid digests/timestamps, and boundary tampering.
- [x] Add Python 3.11/3.12 CI.
- [x] Add `devos production-target-evidence` CLI dispatch and CLI regression coverage.
- [x] Advance distribution identity coherently to `0.20.0`.
- [x] Update release manifest, README, changelog, Production Readiness v2 source identity, core contract, current state, and task state.
- [ ] Open feature PR and verify exact feature-head CI.
- [ ] Fix all CI failures without weakening target/evidence/authorization semantics.
- [ ] Merge through exact expected-head protection only after clean concurrency/readiness checks.
- [ ] Verify fresh merged-main CI and exact-source 0.20.0 artifact/digest.
- [ ] Reconcile final PR/CI/artifact evidence into durable state/history/ledger.

## Current Production Readiness v2 HOLD criteria

`production_ready = false` remains correct until direct target-specific evidence is both valid and separately semantically reviewed/reconciled for:

- `runtime_direct_conformance`
- `recovery_disaster`
- `operational_observability`
- `deployment_target`
- `high_impact_governance`

The 0.20.0 intake validates already-existing evidence only. It is not permission to execute production/high-impact operations in order to obtain that evidence.

## Completed — DevOS 0.19.0 Production Readiness Evidence v2

- PR #66 implementation merged at `8cd731b7b91ca9e67983b6deca8646b38e078e33` from exact feature head `f81184975ffbb02a3e58466459e12858fdd8294a`.
- PR #67 durable reconciliation merged at `69b06853d5f360659ce42d5cf2c5ec7c8dccc04d`.
- PR #67 exact-main push workflows: 11/11 success.
- Final 0.19.0 exact-source artifact ID `10355742368`, digest `sha256:8de1daa8c592c5a3a2128493a1ba6c728ce975d45662253d783cf6aa8ff40bbf`.
- Production Readiness v2 remains blocker-exact and authority-neutral.

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

- Distribution release readiness is not production or publication authorization.
- No public Git tag/GitHub Release/package publication/deployment is authorized by this objective.
- Machine evidence never grants authority, execution, provider permission, or production readiness.
- A `DECLARED` runtime profile is not a verified integration.
- Historical evidence remains pinned to its source head.
- Uncertain provider mutation is never blindly replayed.
- Parallel AI branches must revalidate against fresh `main` before integration.
- Do not create P18/P19 merely for bookkeeping.

## Task-map invariant

`AI A + Account A → repository → AI B + Account B → correct recovery → safe continuation`

The repository, not any AI account/chat/model/vendor memory, carries authoritative project state.
