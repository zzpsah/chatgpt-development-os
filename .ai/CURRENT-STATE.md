# Current State

## Current source and authority

- Repository: `zzpsah/chatgpt-development-os`.
- Current source tree + Git/PR/CI metadata are authoritative for exact implementation/integration state; `.ai` records carry durable semantic context.
- **ChatGPT Memory/chat history and any model/account memory are supplementary only and never authoritative project state.**
- Post-PR #46 verified `main` checkpoint: `36f3001487fb7ce666bb1e7241b539645878101a`.
- `docs/DEVOS-MASTER-ENGINEERING-MAP.md` is the living architecture index; `docs/DEVOS-ENGINEERING-STAGE-HISTORY.md` is the durable stage-history/navigation ledger.

## Core documentation law

> **What is not written was never done.**

Material work follows:

`OBSERVE → ACT / CHANGE / DECIDE → VERIFY → DOCUMENT → PERSIST IN GIT`

Completion requires `IMPLEMENTED + VERIFIED + DOCUMENTED + DURABLE STATE`.

## Canonical governed path

`Human request → P15 interpretation → P16 plan → P17 readiness → Actionable HOLD / Scoped Approval → controller → bounded runtime → verification → persistence → recovery / continuation`

Interpretation, planning, readiness, provider credentials, prior approvals, recovery state, documentation, CI, or simulated evidence never manufacture permission.

## Active bounded work

- No numbered phase is active.
- AI State Resolver v2 cross-claim contradiction handling is **closed through PR #46** and must not remain marked active after this reconciliation.
- No next engineering objective is promoted by this record. Future continuation must inspect fresh `main`, open PRs, CI, current durable state, and source gaps before selecting the next bounded objective.
- Do not create P18/P19 merely for bookkeeping.

## Current verified capability state

### Numbered architecture

- P9 through P17 are complete at their recorded evidence levels.
- P11 remains the repository-first recovery/revalidation/cross-AI continuity baseline.
- P12 remains owner of execution-evidence provenance and freshness.
- P15/P16/P17 remain interpretation/planning/readiness layers respectively; none independently grants runtime authority.

### AI State Resolver v2 — cross-claim contradiction handling — merged

- PR #46 — `Add resolver cross-claim contradiction handling` — merged at `36f3001487fb7ce666bb1e7241b539645878101a`.
- Exact final feature head: `490eeebea69a4f4ae44657f5d94edaef35a26db4`.
- Optional explicit `fact_key` + deterministic JSON `fact_value` identity is supported.
- Claims are compared only when they explicitly share the same valid `fact_key`; arbitrary statement prose is not semantically paired by guesswork.
- Same fact + different canonical values makes all involved otherwise-resolved claims `unknown`, adds `CROSS_CLAIM_CONTRADICTION`, records `contradiction_fact_keys`, and produces `NEEDS_EVIDENCE`.
- Existing downstream path remains authoritative: resolver `NEEDS_EVIDENCE` → P16 `CLARIFY`; P17 fails closed if unknown claims are hidden in a forged `PLANNED` envelope.
- Legacy claims without fact identity remain backward compatible.
- Exact final-head CI passed all triggered gates: Development OS `34809630956`, Contracts `34809630926`, Current-Source Evidence `34809630993`, Trust-First Audit `34809630947`, Living Engineering Map `34809631004`, GitHub Identity/Token Control Plane `34809631046`, and MCP Repository Create `34809630925`.
- PR #46 also reconciled the concurrent `040c7d21...` compact active/history rewrite without discarding unrelated changes, restoring the explicit account-memory boundary and already-proven live provider evidence.

### AI State Resolver v2 envelope integrity — merged

- PR #44 merged at `a4a3413bb27802ef38a698550807e8fb0102f839`; final source head `71d93755e171da5e83e62b00baa4680a0e929f5e`.
- P16 validates and preserves the full resolver envelope; P17 independently revalidates it and fails closed on hidden uncertainty or changed safety invariants.
- PR #45 merged at `aa38761270ac9acdf6af90a4bae64890c766ec91` to reconcile durable post-#44 state.

### Live GitHub App/provider evidence — proven, scoped

- Live read-only GitHub App runtime authentication is **proven**, not pending. DevOS GitHub App Runtime Auth run `34785659043` succeeded against `zzpsah/chatgpt-development-os` with non-secret evidence including `status: PASS`, `credential_material: NOT_INCLUDED`, `execution: NONE`, and `mutation: NONE`.
- Live governed GitHub provider mutation through the P17/controller bridge is **proven on dedicated isolated test resources**:
  - create provider commit `e8235f7864678a27bbf036def806a1624fb66678`;
  - update/reconciliation provider commit `27a3b3cf4f7c8c8511f3c5a8f3283d8a6a883232`;
  - delete provider commit `3f530da3ee1efd4e52baad10fe4e644d4db5d116`, followed by fresh `ABSENT` readback.
- PR #42 merged bounded post-mutation HTTP 404 readback-only retries of 1s, 2s, and 4s. The mutation is never replayed merely because readback is uncertain.
- Provider response is attempt evidence; completion still requires fresh provider readback/reconciliation.

## Current boundaries

- `production_ready = false`.
- Proven provider capability does not authorize arbitrary or production mutation.
- No live repository deletion, branch deletion, force update, production mutation, credential mutation, or permission mutation has been established as general authorized capability by the evidence above.
- Credentials are technical capability only and never DevOS authorization.
- Uncertain mutation is never blindly replayed.
- Historical exact-head evidence remains pinned and is not silently rewritten when source advances.

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

- Complete this post-PR #46 durable-state reconciliation with exact-head CI and merge.
- After reconciliation merge, recover fresh `main` before promoting any next bounded objective.
- Keep `production_ready = false`; do not invent a new numbered phase solely to continue development.
