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
- a valid runtime conformance evidence packet never self-promotes a registry entry.
- distribution release readiness never manufactures production or publication authority.
- `production_ready = false` unless a separately bounded evidence-backed decision changes it.

## Active bounded work

### Agent Runtime Conformance Evidence Intake v1 / DevOS 0.18.0

- [x] Define exact runtime/adapter/Git-head/nonce challenge protocol.
- [x] Bind challenges with canonical SHA-256 identity.
- [x] Validate exactly the required runtime capability evidence set.
- [x] Require invocation provenance shape and SHA-256 evidence digests.
- [x] Fail closed on tamper, mismatch, replay, missing/extra capabilities, malformed provenance, and invalid digests.
- [x] HOLD when a required capability probe reports failure.
- [x] Prevent candidate evidence from self-promoting runtime verification or registry mutation.
- [x] Add adversarial regression corpus and dedicated runtime-profile CI coverage.
- [x] Move distribution metadata coherently to `0.18.0` rather than reuse the release-ready `0.17.0` source identity.
- [ ] Verify all applicable CI on the exact feature head.
- [ ] Merge through expected-head protection.
- [ ] Verify fresh post-merge `main`, exact-source 0.18.0 artifact, and triggered CI.
- [ ] Reconcile exact merge/CI/artifact evidence into durable state and close the objective.

No vendor runtime is promoted by this task. `codex`, `claude-code`, and `openhands` remain declaration-only unless a later separately observed direct conformance proof is reviewed and merged.

Do not create P18/P19 merely for bookkeeping.

## Completed — DevOS 0.17.0 Distribution Release Readiness v1

- PR #61 — `Add DevOS 0.17.0 distribution release readiness` — merged at `ecee10168b43d13430dd71c2e8d85556956f56a6`.
- Exact verified feature head: `b4f46eb7919177e3a0dc19d902401630cd6c12ec`.
- Canonical distribution version at that milestone is `0.17.0` in `VERSION` and `config/release-manifest.json`.
- Added cross-platform `tools/devos.py`, fail-closed `tools/devos-release-check.py`, release/security docs, changelog, current README, adversarial release tests, and dedicated distribution CI.
- Release CI passed on Ubuntu/Windows with Python 3.11/3.12 and produced an exact Git source ZIP plus SHA-256 checksum without creating a tag, GitHub Release, or deployment.
- Exact feature-head workflows all succeeded: Release Readiness `34822126832`; Development OS `34822126813`; Contracts `34822126730`; Trust-First `34822126734`; Current-Source `34822126644`; Evidence Reconciliation `34822126599`; Runtime Adapter `34822126770`; Runtime Profile Registry `34822126715`; Managed Preflight `34822126677`; Isolated Write Proof `34822126827`; MCP Repository Create `34822126759`.
- Exact merged-source main workflows all succeeded: Isolated Write Proof `34822341488`; Provider Controller Adapter `34822341489`; Managed Preflight `34822341626`; Contracts `34822341505`; Development OS `34822341560`; Distribution Release Readiness `34822341533`; Remote Permission Governance `34822341509`; Trust-First Audit `34822341478`.
- Exact merged-source artifact from main `ecee10168b43d13430dd71c2e8d85556956f56a6`: artifact ID `10338323248`; name `devos-source-ecee10168b43d13430dd71c2e8d85556956f56a6`; digest `sha256:4a44fbaa6d9df23afb538afe27b2b38595b3c0aa1632292a43f26b2dea3a2091`; 719498 bytes; not expired when verified.
- Machine reconciliation record digest: `80154dd84d9e6bd7cdfac0d379a708d25455a9542565feb0edcb117bf6362af6`.
- Status at that exact source milestone is **engineering/distribution release-ready**, not production-ready.
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
- GitHub governed provider capability, readback reconciliation, multi-project isolation, Actionable HOLD, current-source evidence, onboarding, recovery, adaptive verification/self-healing, trust-first auditing, runtime-neutral handoff, and runtime-profile registry remain retained foundations.
- `docs/DEVOS-ENGINEERING-STAGE-HISTORY.md` is the durable navigation ledger for numbered and major unnumbered milestones.
- `docs/DEVOS-MASTER-ENGINEERING-MAP.md` remains the living architecture/future-flow map.

## Current HOLD / limits

- `production_ready = false`.
- Distribution release readiness is not publication or production authorization.
- No public Git tag/GitHub Release/package publication is created by this objective.
- Machine evidence and reconciliation records never grant authorization, execution, completion authority, provider permission, or production readiness.
- A `DECLARED` runtime profile is not a verified integration.
- `EVIDENCE_PACKET_VALID` is not direct runtime verification and is not registry-promotion authority.
- Historical readiness evidence remains pinned to its source head.
- Uncertain provider mutation is never blindly replayed.
- Parallel AI branches must revalidate against fresh `main` before integration.

## Task-map invariant

`AI A + Account A → repository → AI B + Account B → correct recovery → safe continuation`

The repository, not any AI account/chat/model/vendor memory, carries authoritative project state.
