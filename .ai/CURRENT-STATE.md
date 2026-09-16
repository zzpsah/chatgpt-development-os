# Current State

## Current source and authority

- Repository: `zzpsah/chatgpt-development-os`.
- Current source tree + Git/PR/CI/release-artifact metadata are authoritative for exact implementation/integration state; `.ai` records carry durable semantic context.
- **ChatGPT Memory/chat history and any model/account memory are supplementary only and never authoritative project state.**
- Canonical distribution version: `0.22.0`.
- Project Fleet Watch v1 implementation merged through PR #73 at `fbb2f334ede3f58018b8d67f337152fd9796fb67` from exact verified feature head `fff8ace4be2e8c1b69c606a0572bf697f5b47998`.
- PR #73 exact feature head completed **15/15 workflows successfully**.
- PR #73 post-merge exact-main push workflow set completed **12/12 successfully**.
- Post-merge distribution release workflow `35140653277` completed successfully.
- Exact-source 0.22.0 artifact: ID `10464578232`, name `devos-source-fbb2f334ede3f58018b8d67f337152fd9796fb67`, digest `sha256:f31ca7d322cfe39fedd2b00e2c6a521d2f968cf04583934d3128c7a86ae139b5`, size `791983` bytes, not expired when verified.

## Core documentation law

> **What is not written was never done.**

Material work follows:

`OBSERVE → ACT / CHANGE / DECIDE → VERIFY → DOCUMENT → PERSIST IN GIT`

Completion requires:

`IMPLEMENTED + VERIFIED + DOCUMENTED + DURABLE STATE`

## Canonical governed path

`Human request → P15 interpretation → state resolution → P16 plan → P17 readiness → Actionable HOLD / Scoped Approval → controller → bounded runtime → verification → evidence/durable-state reconciliation → persistence → recovery / continuation`

Interpretation, planning, readiness, credentials, CI, repository existence/accessibility, fleet discovery, generated facts, evidence intake, reconciliation metadata, prior approvals, recovery state, documentation, or release status never manufacture permission.

## DevOS 0.22.0 Project Fleet Watch v1 — closed / engineering-distribution release-ready

Managed Project Lifecycle v1 governs one repository. Project Fleet Watch v1 now adds read-only visibility across a bounded repository fleet so newly accessible/unmanaged repositories and management regressions can be surfaced rather than silently missed.

Permanent fleet invariants:

```text
REPOSITORY ACCESSIBLE != DEVOS MANAGED
FLEET DISCOVERY != ONBOARDING AUTHORIZATION
FLEET ATTENTION != AUTOMATIC MUTATION
FLEET HEALTHY != APPLICATION VERIFIED
FLEET HEALTHY != PRODUCTION READY
```

Implemented behavior:

```text
fleet snapshot / bounded provider read
            ↓
validate observation evidence
            ↓
classify each active repository through Managed Project Lifecycle v1
            ↓
HEALTHY / ATTENTION / HOLD / EMPTY / BLOCKED
            ↓
optional previous/current drift comparison
            ↓
new_unmanaged / newly_managed / management_regressions / other drift
```

Implemented boundaries and capabilities:

- `tools/devos-project-fleet.py` provides `DEVOS-PROJECT-FLEET-WATCH-v1`.
- deterministic snapshots use `DEVOS-PROJECT-FLEET-SNAPSHOT-v1`.
- every active repository delegates management classification to Managed Project Lifecycle v1 rather than creating a second authority model.
- `HEALTHY` requires every active repository to be `MANAGED`.
- an unmanaged repository produces `ATTENTION` when no stronger blocker exists.
- a managed → non-managed regression forces fleet `HOLD`.
- previous/current comparison exposes `new_repositories`, `removed_repositories`, `new_unmanaged`, `newly_managed`, `management_regressions`, and `newly_attention_required`.
- archived repositories remain visible but are excluded from active fleet cleanliness.
- `devos project-fleet` exposes deterministic snapshot assessment and bounded read-only GitHub discovery.
- `--require-clean` fails closed unless every active repository is `MANAGED`.
- `GITHUB_TOKEN` for `--github-owner @me` is environment-only; Fleet Watch does not print or persist it.
- provider discovery is read-only evidence collection; Fleet Watch performs no onboarding/provider mutation.
- dedicated Python 3.11/3.12 Project Fleet Watch CI is merged and verified.

## Retained Managed Project Lifecycle v1

The gap originally exposed by `zzpsah/Devos-Browser` remains closed at the one-repository lifecycle layer.

```text
REPOSITORY EXISTS != DEVOS MANAGED
REPOSITORY CREATED != ONBOARDED
REPOSITORY DISCOVERED != SAFE TO CONTINUE
```

`zzpsah/Devos-Browser` remains the recorded real remediation proof: its DevOS onboarding/context-sync sequence established `managed_by: development-os` and canonical repository identity. That proof establishes project management/onboarding only; browser/runtime application behavior, deployment, and production readiness are not implied.

## Active bounded work

- No unreconciled DevOS core implementation objective remains after Project Fleet Watch v1 closure.
- No next DevOS feature is activated automatically by this reconciliation.
- Future DevOS core work must begin from fresh `main`, current PRs/issues/CI, relevant source/tests, fleet/provider evidence where applicable, concurrent AI work, and current user intent.
- `zzpsah/Devos-Browser` remains managed; its application work still requires requirement/source recovery before feature claims.
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

Project Fleet Watch v1 does not change these production blockers and does not create production, deployment, publication, onboarding, or provider-mutation authority.

## Retained architecture foundations

- P9 through P17 remain complete at their recorded evidence levels.
- P11 remains the repository-first recovery, revalidation, and cross-AI continuity baseline.
- P12 remains the evidence provenance/freshness owner.
- P15 remains language interpretation; P16 bounded planning; P17 exact-step readiness/authorization.
- AI State Resolver v2 contradiction/envelope hardening remains retained.
- GitHub provider/controller readback, multi-project isolation, Actionable HOLD, universal onboarding, Managed Project Lifecycle, Project Fleet Watch, runtime-neutral handoff, runtime-profile/conformance evidence intake, distribution release machinery, Production Readiness Evidence v2, Production Target Evidence Intake v1, and durable reconciliation remain retained foundations.

## Permanent boundaries

- `CONTINUE != BLANKET AUTHORIZATION`.
- `INTERPRETATION != AUTHORIZATION`.
- `PLAN != EXECUTION`.
- `READY != EXECUTION`.
- `CI PASS != AUTHORIZATION`.
- `DOCUMENTATION != AUTHORIZATION`.
- `REPOSITORY EXISTS != DEVOS MANAGED`.
- `REPOSITORY ACCESSIBLE != DEVOS MANAGED`.
- `ONBOARDING != APPLICATION VERIFIED`.
- `FLEET DISCOVERY != ONBOARDING AUTHORIZATION`.
- `FLEET ATTENTION != AUTOMATIC MUTATION`.
- `FLEET HEALTHY != APPLICATION VERIFIED`.
- `FLEET HEALTHY != PRODUCTION READY`.
- `VALID TARGET EVIDENCE != PRODUCTION READY`.
- `PRODUCTION READY != PUBLICATION AUTHORIZATION`.
- `PRODUCTION READY != DEPLOYMENT AUTHORIZATION`.
- Provider credentials/capability never manufacture DevOS authority.
- Uncertain provider mutation is never blindly replayed.

## Explicit non-actions

No automatic onboarding, provider mutation, production probe, deployment, credential/secret/permission/database mutation, destructive action, runtime promotion, public tag/GitHub Release/package publication, or production-readiness promotion was performed for Project Fleet Watch v1.

## Recovery precedence

1. Current source tree + Git/PR/CI/release-artifact metadata.
2. Explicit current user requirements and durable decisions.
3. `.ai/CURRENT-STATE.md`, `.ai/TASKS.md`, `.ai/RECONCILIATION-LEDGER.jsonl`.
4. Relevant core contracts/tests/configuration.
5. `.ai/SESSIONS/` and historical evidence.
6. Chat/model memory only as supplementary context.

## Next action

Recover fresh `main`, open PRs/issues, CI, durable state, relevant source/tests, and current user intent before selecting another bounded objective. Fleet Watch may be used as read-only evidence when repository-fleet awareness materially affects that decision.
