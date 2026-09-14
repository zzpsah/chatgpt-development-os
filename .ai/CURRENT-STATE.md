# Current State

## Current source and authority

- Repository: `zzpsah/chatgpt-development-os`.
- Current source tree + Git/PR/CI/release-artifact metadata are authoritative for exact implementation/integration state; `.ai` records carry durable semantic context.
- **ChatGPT Memory/chat history and any model/account memory are supplementary only and never authoritative project state.**
- Canonical distribution version: `0.21.0`.
- Managed Project Lifecycle v1 implementation merged through PR #71 at `22ef14850d5d39ce8ff17d85c5608d48c9947066` from exact verified feature head `cdb291e73ad73afd5f2ae32b3933cb52ac1d1421`.
- PR #71 exact feature head completed **15/15 workflows successfully**.
- PR #71 post-merge exact-main push workflow set completed **11/11 successfully**.
- Exact-source 0.21.0 artifact: ID `10371752023`, name `devos-source-22ef14850d5d39ce8ff17d85c5608d48c9947066`, digest `sha256:27bf129b748fe6c7d7cc04f122ba2a0e007d9c4147f238c766736a541b4c61b4`, size `775028` bytes.

## Core documentation law

> **What is not written was never done.**

Material work follows:

`OBSERVE → ACT / CHANGE / DECIDE → VERIFY → DOCUMENT → PERSIST IN GIT`

Completion requires:

`IMPLEMENTED + VERIFIED + DOCUMENTED + DURABLE STATE`

## Canonical governed path

`Human request → P15 interpretation → state resolution → P16 plan → P17 readiness → Actionable HOLD / Scoped Approval → controller → bounded runtime → verification → evidence/durable-state reconciliation → persistence → recovery / continuation`

Interpretation, planning, readiness, credentials, CI, repository existence, generated facts, evidence intake, reconciliation metadata, prior approvals, recovery state, documentation, or release status never manufacture permission.

## DevOS 0.21.0 Managed Project Lifecycle v1 — closed / engineering-distribution release-ready

The gap exposed by `zzpsah/Devos-Browser` is now closed at the DevOS control-plane level.

Permanent lifecycle invariants:

```text
REPOSITORY EXISTS != DEVOS MANAGED
REPOSITORY CREATED != ONBOARDED
REPOSITORY DISCOVERED != SAFE TO CONTINUE
```

Lifecycle behavior:

```text
CREATE or DISCOVER
      ↓
fresh repository readback
      ↓
Managed Project Lifecycle check
      ↓
MANAGED ?
  ├─ YES → recover durable state → development may continue
  ├─ NO  → onboarding required → fresh readback → re-check
  └─ CONFLICT / malformed evidence → HOLD / BLOCKED
```

Implemented boundaries:

- `tools/devos-project-lifecycle.py` classifies local/provider-observed repositories.
- `DEVOS-REPOSITORY-DISCOVERY-SNAPSHOT-v1` supplies read-only provider evidence.
- only `MANAGED` sets `development_continuation_allowed=true`.
- local onboarding mutation requires explicit authorization and fresh managed-state readback.
- `repository.create` now carries a mandatory `project.onboard` postcondition and holds development continuation until `MANAGED`.
- `devos project-lifecycle` exposes the lifecycle gate through the CLI.
- dedicated Python 3.11/3.12 lifecycle CI is merged.

## Real remediation proof — `zzpsah/Devos-Browser`

The repository that exposed this gap has been actually onboarded rather than left as a theoretical test case.

Evidence:

- initial main SHA `131a4f3182fd43cc19520a8803186b136a606eaa` contained only `README.md` and was UNMANAGED;
- onboarding PR #2 merged at `dd94eb11984ea5ab08e1ff1b89307dfefcc15d0b`, with GitHub-verified merge signature;
- Development OS Context Sync run `34904321784` completed successfully;
- onboarding semantic-closure PR #3 merged at `9293e4057aa8e6989a8a40ca55aae4a70858738f`;
- second Context Sync run `34904465022` completed successfully;
- final observed browser-repository main after sync: `a19b3794822bfd0c035a144ef020ee979e700bef`;
- fresh `.ai/manifest.yaml` readback confirms `managed_by: development-os`, canonical repository `zzpsah/Devos-Browser`, and DevOS authority `zzpsah/chatgpt-development-os`.

Managed Project Lifecycle verdict for `zzpsah/Devos-Browser`: **MANAGED**.

This proves project management/onboarding only. Browser/runtime application behavior, provider capability, tests, deployment, and production readiness are not implied.

## Active bounded work

- No unreconciled DevOS control-plane implementation objective remains after Managed Project Lifecycle v1 closure.
- `zzpsah/Devos-Browser` is now managed, but its next application task is requirement/source recovery before browser-runtime feature implementation.
- Future DevOS core work must begin from fresh `main`, current CI/issues/PRs, relevant source/tests, direct external evidence, concurrent AI work, and current user intent.
- Do not create P18/P19 merely for bookkeeping.

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

Managed Project Lifecycle v1 does not change these production blockers and does not create production authority.

## Retained architecture foundations

- P9 through P17 remain complete at their recorded evidence levels.
- P11 remains the repository-first recovery, revalidation, and cross-AI continuity baseline.
- P12 remains the evidence provenance/freshness owner.
- P15 remains language interpretation; P16 bounded planning; P17 exact-step readiness/authorization.
- AI State Resolver v2 contradiction/envelope hardening remains retained.
- GitHub provider/controller readback, multi-project isolation, Actionable HOLD, universal onboarding, Managed Project Lifecycle, runtime-neutral handoff, runtime-profile/conformance evidence intake, distribution release machinery, Production Readiness Evidence v2, Production Target Evidence Intake v1, and durable reconciliation remain retained foundations.

## Permanent boundaries

- `CONTINUE != BLANKET AUTHORIZATION`.
- `INTERPRETATION != AUTHORIZATION`.
- `PLAN != EXECUTION`.
- `READY != EXECUTION`.
- `CI PASS != AUTHORIZATION`.
- `DOCUMENTATION != AUTHORIZATION`.
- `REPOSITORY EXISTS != DEVOS MANAGED`.
- `ONBOARDING != APPLICATION VERIFIED`.
- `VALID TARGET EVIDENCE != PRODUCTION READY`.
- `PRODUCTION READY != PUBLICATION AUTHORIZATION`.
- `PRODUCTION READY != DEPLOYMENT AUTHORIZATION`.
- Provider credentials/capability never manufacture DevOS authority.
- Uncertain provider mutation is never blindly replayed.

## Explicit non-actions

No production probe, deployment, credential/secret/permission/database mutation, destructive action, runtime promotion, public tag/GitHub Release/package publication, or production-readiness promotion was performed for 0.21.0 or the Devos-Browser onboarding proof.

## Recovery precedence

1. Current source tree + Git/PR/CI/release-artifact metadata.
2. Explicit current user requirements and durable decisions.
3. `.ai/CURRENT-STATE.md`, `.ai/TASKS.md`, `.ai/RECONCILIATION-LEDGER.jsonl`.
4. Relevant core contracts/tests/configuration.
5. `.ai/SESSIONS/` and historical evidence.
6. Chat/model memory only as supplementary context.

## Next action

For DevOS core, recover fresh state before selecting another bounded objective. For `zzpsah/Devos-Browser`, recover authoritative browser/runtime requirements and prior implementation evidence before starting application feature work.
