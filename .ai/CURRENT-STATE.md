# Current State

## Current source and authority

- Repository: `zzpsah/chatgpt-development-os`.
- Current source tree + Git/PR/CI/release-artifact metadata are authoritative for exact implementation/integration state; `.ai` records carry durable semantic context.
- **ChatGPT Memory/chat history and any model/account memory are supplementary only and never authoritative project state.**
- Freshly reconciled release-ready source milestone: PR #64, `Add runtime conformance evidence intake v1`, merged at `a8f19687c177359bd5f646e10913ebdae0851a53` from exact verified feature head `f59fad07b6f7708cfc79f173625f9ddafa7bc5ae`.
- Canonical distribution version: `0.18.0` from `VERSION`.
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

- No numbered feature milestone is active.
- No unreconciled DevOS `0.18.0` implementation objective remains after PR #64 reconciliation.
- A later objective must start from fresh `main`, current CI/issues/PRs, relevant source/tests, runtime evidence, concurrent AI work, and current user intent.
- Do not create P18/P19 merely for bookkeeping.

## Current release state

### DevOS 0.18.0 Runtime Conformance Evidence Intake v1 — closed / engineering-distribution release-ready

- PR #64 merged at `a8f19687c177359bd5f646e10913ebdae0851a53`; exact verified feature head `f59fad07b6f7708cfc79f173625f9ddafa7bc5ae`.
- Feature-head applicable CI: 13/13 workflow runs completed successfully.
- Post-merge exact-main push workflow set: 10/10 completed successfully.
- Post-merge distribution release workflow `34830436068` completed successfully.
- Release matrix: Ubuntu + Windows × Python 3.11 + 3.12 — all success.
- Exact merged-source artifact: ID `10342221168`; name `devos-source-a8f19687c177359bd5f646e10913ebdae0851a53`; digest `sha256:894e369966e5172c609a6008c5f7086a78622b81b7f2794fa93990a88b09caf7`; size `736925` bytes; not expired when verified.
- Runtime conformance evidence intake binds runtime ID, adapter version, exact Git head, nonce, required capability set, invocation provenance, and SHA-256 evidence digests.
- Tamper, replay, mismatch, malformed provenance/digest, missing/extra capabilities, or failed required probes fail closed/HOLD.
- `EVIDENCE_PACKET_VALID` remains weaker than direct runtime verification: `registry_promotion_allowed=false` and `direct_runtime_verified=false` remain mandatory.
- `codex`, `claude-code`, and `openhands` remain declaration-only; no vendor runtime was promoted.
- Reconciliation record digest: `7c08b334ebfedbf9951b8d384313e92a894c83dbb8283b77c7221fb1ad113a99`.
- Semantic status: **engineering/distribution release-ready**, not production-ready and not publicly published.
- No Git tag, GitHub Release, package-registry publication, deployment, credential/database/permission change, destructive action, runtime invocation, or public-license change was performed by this objective.

### DevOS 0.17.0 Distribution Release Readiness v1 — historical baseline

- PR #61 merged at `ecee10168b43d13430dd71c2e8d85556956f56a6`; exact verified feature head `b4f46eb7919177e3a0dc19d902401630cd6c12ec`.
- This milestone established the canonical release manifest, cross-platform CLI, fail-closed release checker, security/release documentation, cross-platform release CI, and exact-source artifact strategy inherited by 0.18.0.
- Historical exact-source artifact and workflow evidence remain pinned in the reconciliation/session history and are not rewritten when source advances.

## Current verified capability state

### Agent Runtime Profile Registry + Conformance v1 — closed

- PR #59 merged at `d426ccf480e48544e8078ab7b61065ffd6b18f48`; exact verified feature head `447e8fbaee96eb0be22e9a59d75da147dbcbb8ac`.
- `reference-local-agent` is verified only for its recorded static repository-contract conformance.
- `codex`, `claude-code`, and `openhands` remain declaration-only templates and must HOLD until separate direct evidence proves required capabilities.

### Agent Runtime Conformance Evidence Intake v1 — closed

- Contract: `core/agent-runtime-conformance-evidence.md`.
- Deterministic intake: `tools/agent-runtime-conformance-evidence.py`.
- Adversarial corpus: `tools/test-agent-runtime-conformance-evidence.py`.
- A valid candidate packet cannot self-promote the registry and does not establish direct runtime verification.

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

### Numbered architecture

- P9 through P17 are complete at their recorded evidence levels.
- P11 remains the repository-first recovery/revalidation/cross-AI continuity baseline.
- P12 remains owner of execution-evidence provenance/freshness.
- P15/P16/P17 remain interpretation/planning/readiness layers respectively; none independently grants runtime authority.
- AI State Resolver v2 contradiction/envelope hardening remains closed through its recorded PR #44/#46/#49/#52 sequence.

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

- No implementation objective is automatically active after this reconciliation.
- Treat DevOS `0.18.0` at merged source `a8f19687c177359bd5f646e10913ebdae0851a53` as the latest engineering/distribution release-ready milestone unless fresh Git truth has advanced.
- Any future vendor-runtime verification must begin with direct observed evidence; candidate packets alone cannot promote a runtime.
- Actual public publication/tagging or production deployment remains a separate objective and is not implied.
- Keep `production_ready = false` unless a separately scoped evidence-backed objective explicitly changes it.
