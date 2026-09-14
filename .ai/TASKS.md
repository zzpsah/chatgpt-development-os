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
- `REPOSITORY EXISTS != DEVOS MANAGED`.
- `REPOSITORY CREATED != ONBOARDED`.
- `REPOSITORY DISCOVERED != SAFE TO CONTINUE`.
- `ONBOARDING != APPLICATION VERIFIED`.
- `VALID TARGET EVIDENCE != PRODUCTION READY`.
- `PRODUCTION READY != PUBLICATION AUTHORIZATION`.
- `PRODUCTION READY != DEPLOYMENT AUTHORIZATION`.
- provider credentials/capability never manufacture DevOS authority.
- candidate evidence never self-promotes readiness or runtime status.

## Active bounded work

- No DevOS core implementation objective remains active after Managed Project Lifecycle v1 closure.
- `zzpsah/Devos-Browser` is now a managed DevOS project; its next application work is requirement/source recovery, not automatic browser implementation.
- Select future DevOS work only after fresh recovery of `main`, open PRs/issues, CI, relevant source/tests, direct external evidence, concurrent AI work, and current user intent.
- Do not create P18/P19 merely for bookkeeping.

## Completed — DevOS 0.21.0 Managed Project Lifecycle v1

- [x] Recover fresh pre-objective `main` at `95877bb18551af5ce3a4d7f52876dea983551e19`.
- [x] Confirm lifecycle gap between `repository.create` / discovery and universal onboarding.
- [x] Add `DEVOS-MANAGED-PROJECT-LIFECYCLE-v1` and `DEVOS-REPOSITORY-DISCOVERY-SNAPSHOT-v1`.
- [x] Classify repositories as `MANAGED`, `ONBOARDING_REQUIRED`, `HOLD`, or `BLOCKED`.
- [x] Allow development continuation only for `MANAGED` state.
- [x] Require explicit authorization for local onboarding mutation and fresh managed-state readback afterward.
- [x] Bind `repository.create` to mandatory `project.onboard` postcondition.
- [x] Add `devos project-lifecycle` CLI dispatch.
- [x] Add Python 3.11/3.12 lifecycle CI plus local/provider/idempotency/repository-create/CLI regression coverage.
- [x] Advance distribution identity coherently to `0.21.0`.
- [x] Verify exact feature head `cdb291e73ad73afd5f2ae32b3933cb52ac1d1421`: **15/15 workflows success**.
- [x] Merge PR #71 at `22ef14850d5d39ce8ff17d85c5608d48c9947066` using exact-head protection; GitHub merge signature verified.
- [x] Verify exact-main push workflows: **11/11 success**.
- [x] Verify exact-source artifact ID `10371752023`, name `devos-source-22ef14850d5d39ce8ff17d85c5608d48c9947066`, digest `sha256:27bf129b748fe6c7d7cc04f122ba2a0e007d9c4147f238c766736a541b4c61b4`, size `775028` bytes.
- [x] Apply the lifecycle remediation to real repository `zzpsah/Devos-Browser`.
- [x] Merge browser onboarding PR #2 at `dd94eb11984ea5ab08e1ff1b89307dfefcc15d0b` and verify Context Sync run `34904321784` success.
- [x] Merge browser semantic-closure PR #3 at `9293e4057aa8e6989a8a40ca55aae4a70858738f` and verify Context Sync run `34904465022` success.
- [x] Verify final observed browser main `a19b3794822bfd0c035a144ef020ee979e700bef` and fresh manifest identity.
- [x] Record browser lifecycle verdict: **MANAGED**.

This objective closes the control-plane gap and proves one real remediation case. It does **not** claim browser/runtime application implementation is complete.

## Current Production Readiness v2 HOLD criteria

`production_ready = false` remains correct until direct target-specific evidence is both valid and separately semantically reviewed/reconciled for:

- `runtime_direct_conformance`
- `recovery_disaster`
- `operational_observability`
- `deployment_target`
- `high_impact_governance`

Managed Project Lifecycle does not change these production blockers.

## Completed — DevOS 0.20.0 Production Target Evidence Intake v1

- PR #68 implementation merged at `b9f4c6023aa4bc12111c713b6b262012ed3e51c4` from exact verified feature head `40957dfaf2965d16dc1159f1fca1aca183a4110c`.
- PR #69 durable reconciliation merged at `68a5b65e4c4ab7c8fa43d6ad722c4904442cbfb4`.
- Final reconciled 0.20.0 exact-source artifact ID `10361908379`, digest `sha256:1ad7f2f320c78087d360f32f8cda6da6f65e8a613205274873bd78f5596574e8`.

## Completed — DevOS 0.19.0 Production Readiness Evidence v2

- PR #66 implementation merged at `8cd731b7b91ca9e67983b6deca8646b38e078e33` from exact feature head `f81184975ffbb02a3e58466459e12858fdd8294a`.
- PR #67 durable reconciliation merged at `69b06853d5f360659ce42d5cf2c5ec7c8dccc04d`.
- Final 0.19.0 exact-source artifact ID `10355742368`, digest `sha256:8de1daa8c592c5a3a2128493a1ba6c728ce975d45662253d783cf6aa8ff40bbf`.

## Retained platform foundations

- P9 through P17 remain completed architecture stages at their recorded evidence levels.
- P11 remains repository-first recovery/revalidation/cross-AI continuity baseline.
- P12 remains evidence provenance/freshness owner.
- P15 remains language interpretation; P16 planning; P17 readiness/authorization.
- AI State Resolver v2 envelope/contradiction hardening remains closed through its recorded sequence.
- GitHub governed provider capability, readback reconciliation, multi-project isolation, Actionable HOLD, current-source evidence, universal onboarding, Managed Project Lifecycle, recovery, adaptive verification/self-healing, trust-first auditing, runtime-neutral handoff, runtime-profile registry, runtime-conformance evidence intake, distribution release machinery, Production Readiness Evidence v2, Production Target Evidence Intake v1, and evidence/durable-state reconciliation remain retained foundations.
- `docs/DEVOS-ENGINEERING-STAGE-HISTORY.md` is the durable milestone ledger.
- `docs/DEVOS-MASTER-ENGINEERING-MAP.md` remains the living architecture map.

## Current HOLD / limits

- Distribution release readiness is not production or publication authorization.
- Project onboarding is not application verification.
- No public Git tag/GitHub Release/package publication/deployment is authorized by this objective.
- Machine evidence never grants authority, execution, provider permission, or production readiness.
- A `DECLARED` runtime profile is not a verified integration.
- Historical evidence remains pinned to its source head.
- Uncertain provider mutation is never blindly replayed.
- Parallel AI branches must revalidate against fresh `main` before integration.

## Task-map invariant

`AI A + Account A → repository → AI B + Account B → correct recovery → safe continuation`

The repository, not any AI account/chat/model/vendor memory, carries authoritative project state.
