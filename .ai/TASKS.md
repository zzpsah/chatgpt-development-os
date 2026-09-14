# DevOS Tasks

## How to read this file

This file tracks **work state**, not normative law. Current source/Git/PR/CI are authoritative for exact implementation state. Durable principles and authorization/security decisions live in `.ai/DECISIONS.md` and core contracts. Historical milestone detail lives in `docs/DEVOS-ENGINEERING-STAGE-HISTORY.md` and `.ai/SESSIONS/`.

## Core safety invariants

- **What is not written was never done.**
- `CONTINUE != BLANKET AUTHORIZATION`.
- `INTERPRETATION != AUTHORIZATION`.
- `PLAN != EXECUTION`.
- `READY != EXECUTION`.
- `CI PASS != AUTHORIZATION`.
- provider credentials/capability never manufacture DevOS authority.
- declared runtime identity never manufactures verified runtime capability.
- distribution release readiness never manufactures production or publication authority.
- `production_ready = false` unless a separately bounded evidence-backed decision changes it.

## Active bounded work

- No feature-development objective remains active after DevOS `0.17.0` Distribution Release Readiness v1 closure.
- The post-PR #61 reconciliation branch is the bounded durable-state closure; no recursive reconciliation PR is required solely to record its own merge SHA.
- Future work must be selected only from fresh `main`, open issues/PRs, CI, durable state, relevant source/tests, and current user intent.
- Do not create P18/P19 merely for bookkeeping.

## Completed — DevOS 0.17.0 Distribution Release Readiness v1

- PR #61 — `Add DevOS 0.17.0 distribution release readiness` — merged at `ecee10168b43d13430dd71c2e8d85556956f56a6`.
- Exact verified feature head: `b4f46eb7919177e3a0dc19d902401630cd6c12ec`.
- Canonical distribution version is `0.17.0` in `VERSION` and `config/release-manifest.json`.
- Adds cross-platform `tools/devos.py`, fail-closed `tools/devos-release-check.py`, release/security docs, changelog, current README, adversarial release tests, and dedicated distribution CI.
- Release CI passes on Ubuntu/Windows with Python 3.11/3.12 and produces an exact Git source ZIP plus SHA-256 checksum without creating a tag, GitHub Release, or deployment.
- Exact feature-head workflows all succeeded: Release Readiness `34822126832`; Development OS `34822126813`; Contracts `34822126730`; Trust-First `34822126734`; Current-Source `34822126644`; Evidence Reconciliation `34822126599`; Runtime Adapter `34822126770`; Runtime Profile Registry `34822126715`; Managed Preflight `34822126677`; Isolated Write Proof `34822126827`; MCP Repository Create `34822126759`.
- Exact merged-source main workflows all succeeded: Isolated Write Proof `34822341488`; Provider Controller Adapter `34822341489`; Managed Preflight `34822341626`; Contracts `34822341505`; Development OS `34822341560`; Release Readiness `34822341533`; Remote Permission Governance `34822341509`; Trust-First `34822341478`.
- Exact merged-source artifact from main `ecee10168b43d13430dd71c2e8d85556956f56a6`: artifact ID `10338323248`; name `devos-source-ecee10168b43d13430dd71c2e8d85556956f56a6`; digest `sha256:4a44fbaa6d9df23afb538afe27b2b38595b3c0aa1632292a43f26b2dea3a2091`; 719498 bytes; not expired when verified.
- Machine reconciliation record digest: `80154dd84d9e6bd7cdfac0d379a708d25455a9542565feb0edcb117bf6362af6`.
- Status is **engineering/distribution release-ready**, not production-ready.
- No tag, GitHub Release, package publication, deployment, credentials/secrets, database, permission, destructive operation, provider-scope expansion, or public-license change was performed.

## Completed — Agent Runtime Profile Registry + Conformance v1

- PR #59 merged at `d426ccf480e48544e8078ab7b61065ffd6b18f48`; exact verified feature head `447e8fbaee96eb0be22e9a59d75da147dbcbb8ac`.
- Required verified capabilities are `filesystem.read`, `filesystem.write_scoped`, `git.inspect`, and `verification.run`.
- `reference-local-agent` is verified only for recorded static conformance; `codex`, `claude-code`, and `openhands` remain `DECLARED` and HOLD without separate evidence.
- Forged VERIFIED state, missing/unknown capabilities, duplicate IDs, revoked profiles, and unregistered runtimes fail closed.

## Completed — Universal Agent Runtime Adapter v1

- PR #57 merged at `5d0bdbc0258e898ece21f99937dc4f5b886778a0`.
- Adds a vendor-neutral P17 READY + exact-approval handoff compiler and independent result validator.
- The adapter is side-effect-free and does not itself invoke a vendor runtime or mutate a managed repository.

## Completed — Safe delivery proof line

- Local Disposable Delivery Proof v1 proves bounded local Git update/test/readback/evidence in a temporary repository.
- Managed-Repository Delivery v1 Read-Only Preflight binds clean worktree/head/path evidence and returns HOLD before mutation.
- Isolated Managed-Repository Write Proof v1 proves one safe scoped file update in a newly created isolated fixture with diff/test/readback/evidence and no commit/push/provider/deploy action.

## Completed — Automated Evidence → Durable State Reconciliation v1

- PR #54 merged at `e31c2099b5d9ce88ee4a20c225fe70b424dffa3d`.
- Machine-verifiable facts can be normalized deterministically; semantic CURRENT/TASKS/roadmap meaning still requires review.
- Reconciliation records remain authority-neutral and `production_ready=false`.

## Completed — P15 bounded multilingual interpretation and gating

- Bounded English/Hindi/Hinglish/informal corpus evidence preserves Unicode and proves P15 → P16 → P17 safety behavior for high-impact, negative, and unresolved language cases.
- Coverage is bounded corpus evidence, not universal language competence or authorization.

## Completed — AI State Resolver v2 hardening sequence

- PR #44 — envelope integrity.
- PR #46 — explicit cross-claim contradiction identity/handling.
- PR #49 — downstream P16/P17 independent contradiction recomputation and tamper defense.
- PR #52 — detailed contradiction provenance and downstream detail validation.

## Retained platform foundations

- P9 through P17 remain completed architecture stages at their recorded evidence levels.
- P11 remains repository-first recovery/revalidation/cross-AI continuity baseline.
- P12 remains evidence provenance/freshness owner.
- P15 remains language interpretation; P16 planning; P17 readiness/authorization.
- GitHub governed provider capability, readback reconciliation, multi-project isolation, Actionable HOLD, current-source evidence, onboarding, recovery, adaptive verification/self-healing, and trust-first auditing remain retained foundations.
- `docs/DEVOS-ENGINEERING-STAGE-HISTORY.md` is the durable navigation ledger for numbered and major unnumbered milestones.
- `docs/DEVOS-MASTER-ENGINEERING-MAP.md` remains the living architecture/future-flow map.

## Current HOLD / limits

- `production_ready = false`.
- Distribution release readiness is not publication or production authorization.
- No public Git tag/GitHub Release/package publication has been created by the release-readiness objective.
- Machine evidence and reconciliation records never grant authorization, execution, completion authority, provider permission, or production readiness.
- A `DECLARED` runtime profile is not a verified integration.
- Historical readiness evidence remains pinned to its source head.
- Uncertain provider mutation is never blindly replayed.
- Parallel AI branches must revalidate against fresh `main` before integration.

## Task-map invariant

`AI A + Account A → repository → AI B + Account B → correct recovery → safe continuation`

The repository, not any AI account/chat/model/vendor memory, carries authoritative project state.
