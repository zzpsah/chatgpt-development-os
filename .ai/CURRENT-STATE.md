# Current State

## Current source and authority

- Repository: `zzpsah/chatgpt-development-os`.
- Current source tree + Git/PR/CI metadata are authoritative for exact implementation/integration state; `.ai` records carry durable semantic context.
- **ChatGPT Memory/chat history and any model/account memory are supplementary only and never authoritative project state.**
- Latest closed release-readiness feature reconciled before this objective is PR #61, `Add DevOS 0.17.0 distribution release readiness`, merged at `ecee10168b43d13430dd71c2e8d85556956f56a6`; source/Git/CI remain authoritative for exact current state.
- Current bounded source objective is **Agent Runtime Conformance Evidence Intake v1** on the DevOS `0.18.0` line. Until exact-head CI, merge, and post-merge reconciliation are observed, this record does not claim that objective closed.
- Canonical distribution version in this source candidate: `0.18.0` from `VERSION`.
- `docs/DEVOS-MASTER-ENGINEERING-MAP.md` is the living architecture index.
- `docs/DEVOS-ENGINEERING-STAGE-HISTORY.md` is the durable milestone ledger.
- `.ai/RECONCILIATION-LEDGER.jsonl` is the machine-readable post-feature reconciliation ledger.

## Core documentation law

> **What is not written was never done.**

Material work follows:

`OBSERVE → ACT / CHANGE / DECIDE → VERIFY → DOCUMENT → PERSIST IN GIT`

Completion requires:

`IMPLEMENTED + VERIFIED + DOCUMENTED + DURABLE STATE`

## Canonical governed path

`Human request → P15 interpretation → state resolution → P16 plan → P17 readiness → Actionable HOLD / Scoped Approval → controller → bounded runtime → verification → evidence/durable-state reconciliation → persistence → recovery / continuation`

Interpretation, planning, readiness, credentials, CI, generated facts, reconciliation metadata, prior approvals, recovery state, documentation, or release status never manufacture permission.

## Active bounded work

- **Agent Runtime Conformance Evidence Intake v1 / DevOS 0.18.0** is the current bounded objective in this source candidate.
- Objective: create deterministic runtime/adapter/Git-head/nonce-bound challenge and candidate-evidence validation so future direct runtime proofs can be reviewed without allowing caller assertions to self-promote runtime capability.
- `EVIDENCE_PACKET_VALID` is intentionally weaker than a verified runtime: `registry_promotion_allowed=false` and `direct_runtime_verified=false` remain mandatory.
- `codex`, `claude-code`, and `openhands` remain declaration-only during this objective.
- Completion requires exact-head feature CI, merge, fresh `main` verification, exact-source 0.18.0 release artifact evidence, and durable post-merge reconciliation.
- Do not create P18/P19 merely for bookkeeping.

## Current release state

### DevOS 0.18.0 Runtime Conformance Evidence Intake v1 — candidate

- Canonical version/manifest/README/changelog/release process are moved together to `0.18.0` in this source candidate to avoid reusing `0.17.0` for a different exact source distribution.
- New contract: `core/agent-runtime-conformance-evidence.md`.
- New deterministic intake tool: `tools/agent-runtime-conformance-evidence.py`.
- New adversarial regression corpus: `tools/test-agent-runtime-conformance-evidence.py`.
- Runtime-profile CI is extended to verify the new corpus and contract markers.
- The release manifest requires the conformance contract/tool/tests and preserves automatic tag/release/deploy as false.
- No vendor runtime is promoted by this source change.
- Exact-head CI/merge/post-merge evidence is not claimed here until actually observed.

### DevOS 0.17.0 Distribution Release Readiness v1 — closed historical baseline

- PR #61 merged at `ecee10168b43d13430dd71c2e8d85556956f56a6`; exact verified feature head `b4f46eb7919177e3a0dc19d902401630cd6c12ec`.
- Canonical release metadata at that milestone: `VERSION`, `config/release-manifest.json`, `CHANGELOG.md`, `docs/RELEASE.md`, `.github/SECURITY.md`.
- Cross-platform CLI: `python tools/devos.py`.
- Fail-closed distribution gate: `python tools/devos.py release-check` / `tools/devos-release-check.py`.
- Release CI verified Ubuntu + Windows on Python 3.11 and 3.12, then built an exact Git `git archive` source ZIP, validated the archive, computed SHA-256, and uploaded it as a CI artifact.
- Exact feature-head release workflow: `34822126832` — success; all other triggered feature-head workflows also succeeded.
- Post-merge exact-main release workflow: `34822341533` — success.
- Post-merge exact-main workflow set contained eight triggered workflows and all completed successfully: Isolated Managed Repository Write Proof `34822341488`; GitHub Provider Controller Adapter `34822341489`; Managed Repository Preflight `34822341626`; Development OS Contracts `34822341505`; Development OS `34822341560`; Distribution Release Readiness `34822341533`; Remote Resource Permission Governance `34822341509`; Trust-First Audit `34822341478`.
- Exact merged-source artifact from `ecee10168b43d13430dd71c2e8d85556956f56a6`: artifact `10338323248`, name `devos-source-ecee10168b43d13430dd71c2e8d85556956f56a6`, digest `sha256:4a44fbaa6d9df23afb538afe27b2b38595b3c0aa1632292a43f26b2dea3a2091`, 719498 bytes, not expired when verified.
- Reconciliation record digest: `80154dd84d9e6bd7cdfac0d379a708d25455a9542565feb0edcb117bf6362af6`.
- Semantic status at that exact milestone: **engineering/distribution release-ready**, not production-ready.
- No Git tag, GitHub Release, package-registry publication, or deployment was performed by that objective.
- Public licensing terms were not changed.

## Current verified capability state

### Agent Runtime Profile Registry + Conformance v1 — closed

- PR #59 merged at `d426ccf480e48544e8078ab7b61065ffd6b18f48`; exact verified feature head `447e8fbaee96eb0be22e9a59d75da147dbcbb8ac`.
- `reference-local-agent` is verified only for its recorded static repository-contract conformance.
- `codex`, `claude-code`, and `openhands` remain declaration-only templates and must HOLD until separate direct evidence proves required capabilities.
- Runtime identity never manufactures verified capability.

### Runtime conformance evidence intake — source candidate, not vendor verification

- Challenge identity binds runtime ID, adapter version, exact Git head, nonce, and required capability set with SHA-256.
- Candidate evidence must cover exactly `filesystem.read`, `filesystem.write_scoped`, `git.inspect`, and `verification.run` with provenance and SHA-256 evidence digests.
- Tamper, replay, mismatch, missing/extra capabilities, invalid provenance/digest, or failed required probes fail closed/HOLD.
- A valid packet still cannot self-promote the registry and does not establish direct runtime verification.

### Universal Agent Runtime Adapter v1 — closed

- PR #57 merged at `5d0bdbc0258e898ece21f99937dc4f5b886778a0`.
- A P17 READY step plus exact scoped approval can be compiled into a runtime-neutral SHA-256-bound handoff and returned diff/test/readback evidence is independently validated.
- The adapter is side-effect-free and does not itself invoke a vendor runtime or mutate a repository.

### Safe delivery proof line — closed at recorded scopes

- Local Disposable Delivery Proof v1 proves a temporary local Git delivery path through P15 → P16 → P17 → scoped approval → safe local update → tests/readback → evidence.
- Managed-Repository Delivery v1 Read-Only Preflight binds clean-worktree/head/path evidence and intentionally HOLDs before mutation.
- Isolated Managed-Repository Write Proof v1 proves one scoped file update in a newly created isolated fixture with diff/test/readback/evidence and no commit/push/provider/deployment action.
- These proofs do not imply unrestricted managed-repository or production delivery authority.

### Automated Evidence → Durable State Reconciliation v1 — closed

- PR #54 merged at `e31c2099b5d9ce88ee4a20c225fe70b424dffa3d`.
- Machine-verifiable merge/CI/file/document facts may be normalized deterministically; semantic CURRENT/TASKS/roadmap meaning still requires review.
- Reconciliation metadata cannot create authorization, execution, mutation, completion authority, or production readiness.

### P15 bounded multilingual interpretation and gating — closed

- Bounded English/Hindi/Hinglish/informal corpus evidence preserves Unicode and proves P15 → P16 → P17 safety behavior for high-impact, negative, and unresolved language cases.
- Coverage is bounded corpus evidence, not universal language competence.

### AI State Resolver v2 hardening — closed sequence

- PR #44: resolver envelope integrity.
- PR #46: structured cross-claim contradiction handling.
- PR #49: independent P16/P17 contradiction recomputation and hidden-tamper rejection.
- PR #52: detailed deterministic contradiction provenance and downstream validation.

### Numbered architecture

- P9 through P17 are complete at their recorded evidence levels.
- P11 remains the repository-first recovery/revalidation/cross-AI continuity baseline.
- P12 remains owner of execution-evidence provenance/freshness.
- P15/P16/P17 remain interpretation/planning/readiness layers respectively; none independently grants runtime authority.

### Live GitHub provider evidence — proven, scoped

- GitHub App read-only runtime authentication and bounded governed create/update/delete proof exist at their recorded evidence heads.
- Provider capability does not authorize arbitrary or production mutation; uncertain mutation is never blindly replayed.

## Current boundaries

- `production_ready = false`.
- `CONTINUE != BLANKET AUTHORIZATION`.
- `INTERPRETATION != AUTHORIZATION`.
- `PLAN != EXECUTION`.
- `READY != EXECUTION`.
- `CI PASS != AUTHORIZATION`.
- `DOCUMENTATION != AUTHORIZATION`.
- `DISTRIBUTION RELEASE READY != PRODUCTION READY`.
- `DISTRIBUTION RELEASE READY != PUBLICATION AUTHORIZATION`.
- `PROVIDER CREDENTIAL != DEVOS AUTHORIZATION`.
- `DECLARED RUNTIME != VERIFIED RUNTIME CAPABILITY`.
- `EVIDENCE_PACKET_VALID != VERIFIED RUNTIME`.
- Machine-generated evidence/factual synchronization never becomes semantic truth by itself.
- Historical exact-head evidence remains pinned and is not silently rewritten when source advances.
- Parallel AI work must revalidate against fresh `main`; stale semantic state must never overwrite newer state.

## Recovery precedence

1. Current source tree + Git/PR/CI/release-artifact metadata.
2. Explicit current user requirements and durable decisions.
3. `.ai/CURRENT-STATE.md`, `.ai/TASKS.md`, `.ai/RECONCILIATION-LEDGER.jsonl`, and other semantic `.ai` state.
4. Relevant core contracts/tests and release manifest.
5. `.ai/SESSIONS/` and historical evidence.
6. ChatGPT Memory/chat history only as supplementary context.

## Stable references

- First-contact context: `DEVOS-PROJECT-CONTEXT.md`.
- Bootstrap: `AGENTS.md` and `.ai/manifest.yaml`.
- Master architecture: `docs/DEVOS-MASTER-ENGINEERING-MAP.md`.
- Engineering history: `docs/DEVOS-ENGINEERING-STAGE-HISTORY.md`.
- Release process: `docs/RELEASE.md`.
- Release manifest: `config/release-manifest.json`.
- Changelog: `CHANGELOG.md`.
- Security policy: `.github/SECURITY.md`.
- Runtime profile registry: `core/agent-runtime-profile-registry.md`.
- Runtime conformance evidence intake: `core/agent-runtime-conformance-evidence.md`.
- Evidence reconciliation: `core/evidence-durable-state-reconciliation.md`.

## Next action

- Verify the 0.18.0 runtime-conformance evidence feature on its exact branch head through applicable CI.
- Merge only if exact-head verification is green and the head/base remain expected.
- After merge, freshly verify `main`, the 0.18.0 exact-source release artifact, and durable state; then reconcile this objective closed.
- Do not promote any vendor runtime merely because a candidate evidence packet validates.
- Actual public publication/tagging or production deployment remains a separate objective and is not implied.
- Keep `production_ready = false` unless a separately scoped evidence-backed objective explicitly changes it.
