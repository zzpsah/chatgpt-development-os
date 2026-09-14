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

## Active bounded work

- No bounded implementation objective is active after DevOS 0.20.0 durable reconciliation and PR #69 final readback.
- Select future work only after fresh recovery of `main`, open PRs/issues, CI, relevant source/tests, direct external evidence, concurrent AI work, and current user intent.
- Do not create P18/P19 merely for bookkeeping.

## Completed — DevOS 0.20.0 Production Target Evidence Intake v1

- [x] Recover fresh pre-objective `main` at `69b06853d5f360659ce42d5cf2c5ec7c8dccc04d` and confirm 0 open PRs/issues.
- [x] Add exact production target/source/timestamp/observer/evidence binding for the five external Production Readiness v2 blockers.
- [x] Require the exact closed criterion set and `PASS | FAIL | UNOBSERVED` semantics.
- [x] Keep all-PASS output at `CANDIDATE_COMPLETE` with `production_ready=false`, `readiness_promotion_allowed=false`, and mandatory semantic review.
- [x] Add adversarial target/source/schema/digest/timestamp/boundary tamper coverage.
- [x] Add Python 3.11/3.12 CI and `devos production-target-evidence` CLI dispatch.
- [x] Advance distribution identity coherently to `0.20.0` and update release/readiness/docs state.
- [x] Open PR #68 and use exact feature-head CI as source of truth.
- [x] Repair the fresh-AI recovery regression by restoring retained P11 context markers without weakening target-evidence semantics.
- [x] Verify final feature head `40957dfaf2965d16dc1159f1fca1aca183a4110c`: 15/15 applicable workflows success.
- [x] Merge PR #68 through expected-head protection at `b9f4c6023aa4bc12111c713b6b262012ed3e51c4`.
- [x] Verify post-merge exact-main push workflows: 12/12 success.
- [x] Verify exact-source 0.20.0 implementation artifact ID `10361816279`, digest `sha256:94f7b68abea833ff1a9814ca96e1f0ff017b5b75a5df6c1fde852e461d6f03cf`.
- [x] Perform semantic review and append the durable reconciliation record with digest `c38edd8818a313ed6cd9fdeaa1367e8491ea212db89ae8b00b038c3de3fd5171`.
- [x] Merge docs-only reconciliation PR #69 at `68a5b65e4c4ab7c8fa43d6ad722c4904442cbfb4` after exact-head 15/15 success; verify final exact-main 12/12 push workflows success and source artifact ID `10361908379`, digest `sha256:1ad7f2f320c78087d360f32f8cda6da6f65e8a613205274873bd78f5596574e8`, size `761954` bytes.

Repository-side feature implementation and durable reconciliation are complete. This factual closure record only captures already-proven PR #69 readback; it does not create another reconciliation obligation or activate another feature objective.

## Current Production Readiness v2 HOLD criteria

`production_ready = false` remains correct until direct target-specific evidence is both valid and separately semantically reviewed/reconciled for:

- `runtime_direct_conformance`
- `recovery_disaster`
- `operational_observability`
- `deployment_target`
- `high_impact_governance`

The 0.20.0 intake validates already-existing evidence only. It is not permission to execute production/high-impact operations in order to obtain evidence.

## Completed — DevOS 0.19.0 Production Readiness Evidence v2

- PR #66 implementation merged at `8cd731b7b91ca9e67983b6deca8646b38e078e33` from exact feature head `f81184975ffbb02a3e58466459e12858fdd8294a`.
- PR #67 durable reconciliation merged at `69b06853d5f360659ce42d5cf2c5ec7c8dccc04d`.
- Final 0.19.0 exact-source artifact ID `10355742368`, digest `sha256:8de1daa8c592c5a3a2128493a1ba6c728ce975d45662253d783cf6aa8ff40bbf`.
- Production Readiness v2 remains blocker-exact and authority-neutral.

## Retained platform foundations

- P9 through P17 remain completed architecture stages at their recorded evidence levels.
- P11 remains repository-first recovery/revalidation/cross-AI continuity baseline.
- P12 remains evidence provenance/freshness owner.
- P15 remains language interpretation; P16 planning; P17 readiness/authorization.
- AI State Resolver v2 envelope/contradiction hardening remains closed through its recorded sequence.
- GitHub governed provider capability, readback reconciliation, multi-project isolation, Actionable HOLD, current-source evidence, onboarding, recovery, adaptive verification/self-healing, trust-first auditing, runtime-neutral handoff, runtime-profile registry, runtime-conformance evidence intake, distribution release machinery, Production Readiness Evidence v2, Production Target Evidence Intake v1, and evidence/durable-state reconciliation remain retained foundations.
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

## Task-map invariant

`AI A + Account A → repository → AI B + Account B → correct recovery → safe continuation`

The repository, not any AI account/chat/model/vendor memory, carries authoritative project state.
