# Current State

## Current source and authority

- Repository: `zzpsah/chatgpt-development-os`.
- Current source tree + Git/PR/CI metadata are authoritative for exact implementation/integration state; `.ai` records carry durable semantic context.
- **ChatGPT Memory/chat history and any model/account memory are supplementary only and never authoritative project state.**
- Latest reconciled feature is PR #59 merge commit `d426ccf480e48544e8078ab7b61065ffd6b18f48`; source/Git/CI remain authoritative for exact state.
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

Interpretation, planning, readiness, credentials, CI, generated facts, reconciliation metadata, prior approvals, recovery state, or documentation never manufacture permission.

## Active bounded work

- No bounded engineering objective is active after Agent Runtime Profile Registry + Conformance v1 closure.
- Parallel managed-repository/software-delivery development remains separate work and must always be recovered from fresh source before continuation.
- Future work must be selected from fresh `main`, open PRs, CI, durable state, source gaps, and current user intent. No P18/P19 phase is created for bookkeeping.

## Current verified capability state

### Agent Runtime Profile Registry + Conformance v1 — closed

- PR #59 — `Add agent runtime profile registry v1` — merged at `d426ccf480e48544e8078ab7b61065ffd6b18f48`; exact verified feature head `447e8fbaee96eb0be22e9a59d75da147dbcbb8ac`.
- `config/agent-runtime-profile-registry.json` provides durable runtime identity/conformance state under protocol `DEVOS-AGENT-RUNTIME-PROFILE-REGISTRY-v1`.
- `tools/agent-runtime-profile-registry.py` allows only evidence-backed `VERIFIED` entries to export the existing `DEVOS-AGENT-RUNTIME-PROFILE-v1` handoff shape.
- Required verified capabilities are `filesystem.read`, `filesystem.write_scoped`, `git.inspect`, and `verification.run`; missing or unknown capabilities fail closed.
- `reference-local-agent` is verified only for repository static-contract conformance.
- `codex`, `claude-code`, and `openhands` are declaration-only templates and remain HOLD for handoff until a separate evidence-backed conformance proof is merged.
- Exact feature-head CI passed: Runtime Profile Registry `34818246952`; Agent Runtime Adapter `34818246907`; Current-Source Evidence `34818246910`; MCP Repository Create `34818246875`; Trust-First Audit `34818246940`; Development OS `34818246896`; Contracts `34818246842`; Evidence Durable Reconciliation `34818246846`; Isolated Managed Repository Write Proof `34818246855`; Managed Repository Preflight `34818246913`.
- Structured reconciliation evidence is appended to `.ai/RECONCILIATION-LEDGER.jsonl`; canonical record digest `4a613b466092c9c1e811ab16e6fe8af41dfc08668b74312e8c69b3b9d909d7e1` is pinned in the post-PR #59 session record.
- No vendor integration, agent invocation, repository mutation, provider call, approval grant, deployment, credential, database, permission, destructive action, or production-readiness upgrade was introduced.

### Isolated Managed-Repository Write Proof v1 — closed

- Main feature head `2ef6b6e3df832ca132123b85caa69f7eda67d1f3` proves P15 → P16 → P17 → read-only preflight → exact scoped approval → runtime handoff → one real marker update → fixture test/diff/readback → external evidence packet in a newly created isolated local Git fixture.
- Exact-head CI passed: Development OS `34817906419`; Contracts `34817906429`; Trust-First `34817906466`; Provider Controller `34817906454`; Remote Permission `34817906633`; Managed Preflight `34817906427`; Isolated Write Proof `34817906424`.
- No existing managed repository, provider, commit, push, deployment, production, credential, database, permission, deletion, or destructive operation was used.

### Managed-Repository Delivery v1 — Read-Only Preflight — closed

- Feature head `fda3e3a6db624d69d6d651cd531c537ad579c9cd` adds deterministic clean-worktree/HEAD/path preflight through P15 → P16 → P17.
- It binds an exact approval request and intentionally returns `HOLD` before any target-repository write.
- Exact-head CI passed: Development OS `34817368411`; Contracts `34817368361`; Trust-First `34817368368`; Provider Controller `34817368359`; Remote Permission Governance `34817368403`; Managed Repository Preflight `34817368326`.

### Universal Agent Runtime Adapter v1 — closed

- PR #57 merged at `5d0bdbc0258e898ece21f99937dc4f5b886778a0`; exact verified feature head `da57d48c1ec28eac71eff75b59f9c701e9c9c593`.
- `tools/agent-runtime-handoff.py` compiles P17 READY + exact scoped approval into a SHA-256-bound runtime-neutral handoff and independently validates returned diff/test/readback evidence.
- It is side-effect-free and does not itself invoke a vendor runtime or mutate a repository.

### Local Disposable Delivery Proof v1 — closed

- Main commit `1f735fa11e19b9852ce9210338bc0907ab0b5b1c` proves temporary local Git delivery through P15 → P16 → P17 → exact scoped approval → local update → test/readback → evidence persistence → fresh recovery.
- It excludes commit/push/provider/deployment/production/credential/database/permission/destructive operations.

### Automated Evidence → Durable State Reconciliation v1 — closed

- PR #54 merged at `e31c2099b5d9ce88ee4a20c225fe70b424dffa3d`; exact feature head `a2da0eaf2a5464d4a716859168bf0ba4d87659a6`.
- Machine-verifiable merge/CI/file/document facts may be normalized deterministically; semantic CURRENT/TASKS/roadmap meaning still requires review.
- `READY_FOR_DURABLE_RECONCILIATION` is not execution authorization.

### P15 bounded Devanagari Hindi/Hinglish interpretation and gating — closed

- Main commit `001f48e64d3e7e6e32d9befc9bb00899b8868e03` preserves Unicode Hindi input and adds bounded multilingual corpus coverage plus P15 → P16 → P17 safety regression.
- High-impact Hindi remains independently classified/approval-gated; negative deployment wording blocks conflicting plans; unresolved referents clarify.

### AI State Resolver v2 contradiction hardening — merged sequence

- PR #44: resolver envelope integrity.
- PR #46: explicit cross-claim contradiction identity/handling.
- PR #49: independent P16/P17 contradiction recomputation and hidden-tamper rejection.
- PR #52: deterministic detailed contradiction provenance with independent downstream validation.
- Resolver confidence/provenance never grants authorization, execution, mutation, completion, or production readiness.

### Numbered architecture

- P9 through P17 are complete at their recorded evidence levels.
- P11 remains the repository-first recovery/revalidation/cross-AI continuity baseline.
- P12 remains owner of execution-evidence provenance/freshness.
- P15/P16/P17 remain interpretation/planning/readiness layers respectively; none independently grants runtime authority.

### Live GitHub provider evidence — proven, scoped

- GitHub App read-only runtime authentication is proven by run `34785659043`.
- Governed GitHub mutation through P17/controller/provider path is proven on isolated create → update → delete resources with fresh readback/reconciliation.
- Proven provider capability does not authorize arbitrary or production mutation.

## Current boundaries

- `production_ready = false`.
- `CONTINUE != BLANKET AUTHORIZATION`.
- `READY != EXECUTION`.
- `CI PASS != AUTHORIZATION`.
- `DOCUMENTATION != AUTHORIZATION`.
- `PROVIDER CREDENTIAL != DEVOS AUTHORIZATION`.
- `DECLARED RUNTIME != VERIFIED RUNTIME CAPABILITY`.
- Machine-generated evidence/factual synchronization never becomes semantic truth by itself.
- Historical exact-head evidence is pinned and is not silently rewritten when source advances.
- Parallel AI work must revalidate against fresh `main`; stale semantic state must never overwrite newer state.

## Recovery precedence

1. Current source tree + Git/PR/CI metadata.
2. Explicit current user requirements and durable decisions.
3. `.ai/CURRENT-STATE.md`, `.ai/TASKS.md`, `.ai/RECONCILIATION-LEDGER.jsonl`, and other semantic `.ai` state.
4. Relevant core contracts/tests.
5. `.ai/SESSIONS/` and historical evidence.
6. ChatGPT Memory/chat history only as supplementary context.

## Stable references

- First-contact context: `DEVOS-PROJECT-CONTEXT.md`.
- Historical handoff: `docs/handoff/README.md`.
- Master architecture: `docs/DEVOS-MASTER-ENGINEERING-MAP.md`.
- Engineering stage history: `docs/DEVOS-ENGINEERING-STAGE-HISTORY.md`.
- Runtime profile registry contract: `core/agent-runtime-profile-registry.md`.
- Runtime handoff contract: `tools/agent-runtime-handoff.py`.
- Evidence reconciliation contract: `core/evidence-durable-state-reconciliation.md`.
- Resolver contradiction contract: `docs/AI-STATE-RESOLVER-CROSS-CLAIM-CONTRADICTIONS.md`.

## Next action

- Recover fresh `main`, open PRs, CI, durable state, and concurrent delivery work before selecting the next bounded objective.
- Vendor runtime conformance must be promoted one runtime at a time with direct evidence; declaration-only templates must not be upgraded by assumption.
- Keep `production_ready = false` unless a separately bounded evidence-backed objective explicitly changes it.
