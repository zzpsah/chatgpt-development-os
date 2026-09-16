# DevOS Tasks

## How to read this file

This file tracks work state, not normative law. Current source/Git/PR/CI/release-artifact metadata are authoritative for exact implementation state. Durable principles and authorization/security decisions live in `.ai/DECISIONS.md` and core contracts. Historical milestone detail lives in `docs/DEVOS-ENGINEERING-STAGE-HISTORY.md` and `.ai/SESSIONS/`.

## Core safety invariants

- **What is not written was never done.**
- `CONTINUE != BLANKET AUTHORIZATION`.
- `INTERPRETATION != AUTHORIZATION`.
- `PLAN != EXECUTION`.
- `READY != EXECUTION`.
- `CI PASS != AUTHORIZATION`.
- `REPOSITORY EXISTS != DEVOS MANAGED`.
- `REPOSITORY CREATED != ONBOARDED`.
- `REPOSITORY ACCESSIBLE != DEVOS MANAGED`.
- `FLEET DISCOVERY != ONBOARDING AUTHORIZATION`.
- `FLEET ATTENTION != AUTOMATIC MUTATION`.
- `REMEDIATION PLAN != AUTHORIZATION`.
- `REMEDIATION PRIORITY != EXECUTION ORDER AUTHORIZATION`.
- `PLAN READY != SAFE TO APPLY`.
- `VALID TARGET EVIDENCE != PRODUCTION READY`.
- `PRODUCTION READY != PUBLICATION AUTHORIZATION`.
- `PRODUCTION READY != DEPLOYMENT AUTHORIZATION`.
- provider credentials/capability never manufacture DevOS authority.

## Active bounded work

- No DevOS core implementation objective remains active after Project Remediation Planner v1 closure.
- No next feature is promoted automatically by this reconciliation.
- `zzpsah/Devos-Browser` remains a managed DevOS project; browser/runtime application work still requires fresh requirement/source recovery.
- Select future work only after fresh recovery of `main`, open PRs/issues, CI, relevant source/tests, direct external/fleet evidence where applicable, concurrent AI work, and current user intent.
- Do not create P18/P19 merely for bookkeeping.

## Completed — DevOS 0.23.0 Project Remediation Planner v1

- [x] Recover fresh pre-objective main at `b18e5e1e8fe9dcf66bb030f9c08ca0312a959eb5`.
- [x] Add `DEVOS-PROJECT-REMEDIATION-PLAN-v1`.
- [x] Add deterministic remediation priorities: regression 100, conflict 95, blocker 90, partial onboarding 80, unmanaged onboarding 70.
- [x] Require `requires_explicit_authorization=true`, `safe_apply=false`, and `next_gate=P17_READINESS_AND_SCOPED_APPROVAL` for every proposed action.
- [x] Fail closed on duplicate repositories, unsupported fleet states, malformed drift, and unknown regression references.
- [x] Add `devos project-remediation` CLI dispatch and `--require-clean` fail-closed mode.
- [x] Add Python 3.11/3.12 dedicated CI and adversarial/deterministic regression coverage.
- [x] Advance distribution identity coherently to `0.23.0`.
- [x] Verify exact feature head `5e889374df31f85ed005866c4d8a5f43d9e41b63`: **16/16 workflows success**.
- [x] Merge PR #75 at `958c8b69464acbe09493866ddbe7c2e6bb06905d` with expected-head protection; GitHub merge signature verified.
- [x] Verify exact-main push workflow set: **13/13 success**.
- [x] Verify post-merge distribution release workflow `35141897232`: success.
- [x] Verify exact-source artifact ID `10465124556`, name `devos-source-958c8b69464acbe09493866ddbe7c2e6bb06905d`, digest `sha256:f515b8752c027e2e472dd784dafc033d2eb9dc50d95dec1f0e40c54dfc4c1098`, size `801597` bytes, not expired when verified.
- [x] Preserve `production_ready=false` and all onboarding/provider/deployment/publication authority boundaries.

This objective closes the gap between detecting fleet attention and knowing the deterministic next governance action. It does not execute remediation or claim application correctness, runtime conformance, deployment readiness, or production readiness.

## Completed — DevOS 0.22.0 Project Fleet Watch v1

- Project Fleet Watch v1 remains the read-only multi-repository visibility layer.
- Feature PR #73 merged at `fbb2f334ede3f58018b8d67f337152fd9796fb67` from exact feature head `fff8ace4be2e8c1b69c606a0572bf697f5b47998`.
- Exact-main workflow set: 12/12 success.
- Exact-source artifact ID `10464578232`, digest `sha256:f31ca7d322cfe39fedd2b00e2c6a521d2f968cf04583934d3128c7a86ae139b5`.

## Completed — DevOS 0.21.0 Managed Project Lifecycle v1

- Managed Project Lifecycle v1 remains the one-repository management gate.
- Feature PR #71 merged at `22ef14850d5d39ce8ff17d85c5608d48c9947066` from exact feature head `cdb291e73ad73afd5f2ae32b3933cb52ac1d1421`.
- Real repository `zzpsah/Devos-Browser` was onboarded and verified `MANAGED` at the management-context layer.

## Current Production Readiness v2 HOLD criteria

`production_ready = false` remains correct until direct target-specific evidence is both valid and separately semantically reviewed/reconciled for:

- `runtime_direct_conformance`
- `recovery_disaster`
- `operational_observability`
- `deployment_target`
- `high_impact_governance`

Managed Project Lifecycle, Project Fleet Watch, and Project Remediation Planner do not change these production blockers.

## Retained platform foundations

- P9 through P17 remain completed architecture stages at their recorded evidence levels.
- P11 remains repository-first recovery/revalidation/cross-AI continuity baseline.
- P12 remains evidence provenance/freshness owner.
- P15 remains language interpretation; P16 planning; P17 readiness/authorization.
- Universal onboarding, Managed Project Lifecycle, Project Fleet Watch, Project Remediation Planner, GitHub governed provider/readback, runtime-neutral handoff, runtime-profile registry/conformance evidence, distribution release machinery, Production Readiness Evidence v2, Production Target Evidence Intake v1, and evidence/durable-state reconciliation remain retained foundations.
- `docs/DEVOS-ENGINEERING-STAGE-HISTORY.md` is the durable milestone ledger.
- `docs/DEVOS-MASTER-ENGINEERING-MAP.md` remains the living architecture map.

## Current HOLD / limits

- Distribution release readiness is not production or publication authorization.
- Fleet visibility is not onboarding authorization.
- A remediation proposal is not authorization or execution.
- Project onboarding is not application verification.
- No public Git tag/GitHub Release/package publication/deployment is authorized by this objective.
- Machine evidence never grants authority, execution, provider permission, or production readiness.
- Historical evidence remains pinned to its source head.
- Uncertain provider mutation is never blindly replayed.

## Task-map invariant

`AI A + Account A → repository → AI B + Account B → correct recovery → safe continuation`

The repository, not any AI account/chat/model/vendor memory, carries authoritative project state.
