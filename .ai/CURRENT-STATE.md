# Current State

## Current source and authority

- Repository: `zzpsah/chatgpt-development-os`.
- Source tree + current Git/PR/CI metadata are authoritative for exact implementation/integration state; `.ai` records carry durable semantic context.
- **ChatGPT Memory/chat history and any model/account memory are supplementary only and never authoritative project state.**
- The feature branch for the current bounded objective was created from `main` at `aa38761270ac9acdf6af90a4bae64890c766ec91`; `main` then advanced concurrently to `040c7d21b5fac6224ced1bdbfeaa7c3b71b78c78` (`docs: separate active state from historical evidence`).
- `docs/DEVOS-MASTER-ENGINEERING-MAP.md` remains the living architecture index; `docs/DEVOS-ENGINEERING-STAGE-HISTORY.md` is the durable stage-history/navigation ledger added by the current objective.

## Core documentation law

> **What is not written was never done.**

Material engineering work follows:

`OBSERVE → ACT / CHANGE / DECIDE → VERIFY → DOCUMENT → PERSIST IN GIT`

Completion requires `IMPLEMENTED + VERIFIED + DOCUMENTED + DURABLE STATE`.

## Canonical governed path

`Human request → P15 interpretation → P16 plan → P17 readiness → Actionable HOLD / Scoped Approval → controller → bounded runtime → verification → persistence → recovery / continuation`

Interpretation, planning, readiness, provider credentials, prior approvals, recovery state, documentation, CI, or simulated evidence never manufacture permission.

## Active bounded work

### AI State Resolver v2 — explicit cross-claim contradiction handling

- Unnumbered hardening objective; no P18/P19 phase is created.
- Adds optional stable `fact_key` + deterministic JSON `fact_value` identity.
- Claims are compared only when they explicitly share the same valid `fact_key`; statement prose is never semantically paired by guesswork.
- Different canonical values for the same fact make all involved claims `unknown` with `CROSS_CLAIM_CONTRADICTION`, record `contradiction_fact_keys`, and produce resolver `NEEDS_EVIDENCE`.
- Existing unresolved-state propagation remains authoritative: P16 returns `CLARIFY`; P17 fails closed if unknown claims are hidden in a forged `PLANNED` envelope.
- Legacy claims without fact identity remain backward compatible.
- The objective is currently under PR #46 verification and is not complete until exact-final-head CI is green, merged, and durable post-merge state is reconciled.

## Current verified capability state

### Numbered architecture

- P9 through P17 are complete at their recorded evidence levels.
- P11 remains the repository-first recovery/revalidation/cross-AI continuity baseline.
- P12 remains owner of execution-evidence provenance and freshness.
- P15/P16/P17 remain interpretation/planning/readiness layers respectively; none of them independently grants runtime authority.

### AI State Resolver v2 envelope integrity — closed

- PR #44 merged at `a4a3413bb27802ef38a698550807e8fb0102f839`; final source head `71d93755e171da5e83e62b00baa4680a0e929f5e`.
- P16 validates and preserves the full resolver envelope; P17 independently revalidates it and fails closed on hidden uncertainty or changed safety invariants.
- PR #45 merged at `aa38761270ac9acdf6af90a4bae64890c766ec91` to reconcile durable post-#44 state.

### Live GitHub App/provider evidence — proven, scoped

- Live read-only GitHub App runtime authentication is **proven**, not pending. DevOS GitHub App Runtime Auth run `34785659043` succeeded against `zzpsah/chatgpt-development-os`, with non-secret evidence including `status: PASS`, `credential_material: NOT_INCLUDED`, `execution: NONE`, and `mutation: NONE`.
- Live governed GitHub provider mutation through the P17/controller bridge is also **proven on dedicated isolated test resources**:
  - create provider commit `e8235f7864678a27bbf036def806a1624fb66678`;
  - update/reconciliation provider commit `27a3b3cf4f7c8c8511f3c5a8f3283d8a6a883232`;
  - delete provider commit `3f530da3ee1efd4e52baad10fe4e644d4db5d116`, followed by fresh `ABSENT` readback.
- PR #42 merged bounded post-mutation HTTP 404 readback-only retries of 1s, 2s, and 4s. The mutation is never replayed merely because readback is uncertain.
- Provider response is attempt evidence; completion still requires fresh provider readback/reconciliation.

## Current boundaries

- `production_ready = false`.
- Proven provider capability does not authorize arbitrary or production mutation.
- No live repository deletion, branch deletion, force update, production mutation, credential mutation, or permission mutation has been established as an authorized/general DevOS capability by the evidence above.
- Credentials are technical capability only and never DevOS authorization.
- Uncertain mutation is never blindly replayed.
- Historical exact-head evidence remains pinned; later source movement must not silently rewrite what a past run proved.

## Recovery and navigation

### Universal portability invariant

`AI A + Account A → repository → AI B + Account B → correct state recovery → safe continuation`

### Recovery precedence

1. Current source tree + Git/PR/CI metadata.
2. Explicit current user requirements and durable decisions.
3. `.ai/CURRENT-STATE.md`, `.ai/TASKS.md`, and other semantic `.ai` state.
4. Relevant core contracts/tests.
5. `.ai/SESSIONS/` and historical evidence.
6. ChatGPT Memory/chat history only as supplementary context.

### Stable references

- First-contact context: `DEVOS-PROJECT-CONTEXT.md`.
- Historical handoff: `docs/handoff/README.md`.
- Master architecture: `docs/DEVOS-MASTER-ENGINEERING-MAP.md`.
- Engineering stage history: `docs/DEVOS-ENGINEERING-STAGE-HISTORY.md`.
- Resolver contradiction contract: `docs/AI-STATE-RESOLVER-CROSS-CLAIM-CONTRADICTIONS.md`.

## Next action

- Finish exact-head verification for PR #46 and repair any CI compatibility issue without weakening fail-closed semantics.
- If PR #46 is green and mergeable, it may be merged under the user's current time-bounded standing authorization for normal DevOS development/PR/merge work.
- After merge, reconcile `.ai/CURRENT-STATE.md` and `.ai/TASKS.md` so the contradiction objective is marked closed and the active/history separation remains truthful.
- Keep `production_ready = false`; do not create P18/P19 merely for bookkeeping.
