# Current State

## Current source and authority

- Repository: `zzpsah/chatgpt-development-os`.
- Current source tree + Git/PR/CI metadata are authoritative for exact implementation/integration state; `.ai` records carry durable semantic context.
- **ChatGPT Memory/chat history and any model/account memory are supplementary only and never authoritative project state.**
- Current reconciliation checkpoint is post-PR #52 merge commit `2a5e13ad5a46085dc6949bfbcf325f84e29f9d02`.
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

### P15 bounded multilingual interpretation and gating

- Repository-only hardening objective; no P18/P19 phase is created.
- Preserve Devanagari Hindi Unicode during deterministic interpretation and support a bounded Hindi/Hinglish regression corpus.
- Prove the entire `P15 → P16 → P17` path: language interpretation may select an intent and constraints, but it never grants authority, authorization, or execution.
- High-impact Hindi phrases must remain independently classified and gated by P16/P17; explicit negative constraints must block conflicting plans.
- This does not claim universal Hindi, regional-language, or model-level language coverage.

## Current verified capability state

### AI State Resolver v2 detailed contradiction provenance — merged

- PR #52 — `Add detailed resolver contradiction provenance` — merged at `2a5e13ad5a46085dc6949bfbcf325f84e29f9d02`.
- Exact final source head: `b091ef2058f3c089d3daeafb41ca9fc58568f435`.
- Resolver emits deterministic `contradictions` records alongside `contradiction_fact_keys`.
- Each contradiction record contains the explicit `fact_key`, sorted involved `claim_ids`, and sorted canonical conflicting JSON values.
- Non-contradictory and invalid-top-level claim input produce `contradictions: []`.
- P16 independently recomputes expected detailed contradiction provenance from claims and returns `CLARIFY` when detail is forged or inconsistent.
- P17 independently revalidates the same detail on P16-preserved provenance and returns `BLOCKED` when detail is forged or inconsistent after planning.
- The detailed field is audit evidence only; claims remain the independently recomputed source for contradiction integrity.
- Exact-final-head CI passed all triggered workflows: Development OS `34811362766`, Development OS Contracts `34811362710`, MCP Repository Create `34811362769`, Actionable Hold `34811362786`, P13 External Managed Project `34811362707`, Current-Source Evidence `34811362749`, GitHub Identity/Token `34811362750`, Living Engineering Map `34811362775`, and Trust-First Audit `34811362701`.
- Closed PR #50 remains unmerged; only its non-duplicate detailed-provenance idea was re-evaluated and promoted from fresh `main`.
- No authority, authorization, execution, provider mutation, automatic truth-winner selection, or production-readiness upgrade was introduced.

### Resolver contradiction envelope integrity — merged

- PR #49 — `Harden resolver contradiction envelope integrity` — merged at `58d37ea23d025d7414f0d55fe2ba5ccc42068b8e`.
- Exact final PR head: `3c0711a9803649505d105728e90e1ef90b3d7ce8`.
- P16 independently recomputes explicit same-`fact_key` / canonical-`fact_value` contradiction groups before planning.
- P16 rejects hidden contradictions, inconsistent `CROSS_CLAIM_CONTRADICTION` reasons, and inconsistent `contradiction_fact_keys`.
- P17 independently recomputes contradiction integrity from full resolver provenance retained by P16.
- A post-P16 `fact_value` edit that creates a hidden contradiction is `BLOCKED` even when top-level status/confidence/count metadata remains superficially valid.
- Exact-final-head CI passed all triggered workflows: Development OS Contracts `34810461613`, Development OS `34810461872`, Actionable Hold `34810461632`, Living Engineering Map `34810461677`, Trust-First Audit `34810461612`, GitHub Identity/Token `34810461701`, Current-Source Evidence `34810461718`, MCP Repository Create `34810461678`, and P13 External Managed Project `34810461615`.
- PR #51 reconciled durable state after #49 and merged at `2500ddc235ce99dbe45a6cd0537d4b0d2372c4a4`.

### AI State Resolver v2 cross-claim contradiction handling — merged

- PR #46 — `Add resolver cross-claim contradiction handling` — merged at `36f3001487fb7ce666bb1e7241b539645878101a`.
- Exact final feature head: `490eeebea69a4f4ae44657f5d94edaef35a26db4`.
- Optional explicit `fact_key` + deterministic JSON `fact_value` identity is supported.
- Same valid fact identity with different canonical values makes involved claims `unknown`, adds `CROSS_CLAIM_CONTRADICTION`, records `contradiction_fact_keys`, and produces `NEEDS_EVIDENCE`.
- PR #47 was a concurrent duplicate attempt and was closed without merge.
- PR #48 reconciled durable state after #46 and merged at `7009e8e1b4398462b1a9321bb1e2a38a3c35e478`.

### AI State Resolver v2 envelope integrity — merged

- PR #44 merged at `a4a3413bb27802ef38a698550807e8fb0102f839`; final source head `71d93755e171da5e83e62b00baa4680a0e929f5e`.
- P16 validates and preserves the full resolver envelope; P17 independently revalidates it and fails closed on hidden uncertainty or changed safety invariants.
- PR #45 merged at `aa38761270ac9acdf6af90a4bae64890c766ec91` to reconcile durable post-#44 state.

### Numbered architecture

- P9 through P17 are complete at their recorded evidence levels.
- P11 remains the repository-first recovery/revalidation/cross-AI continuity baseline.
- P12 remains owner of execution-evidence provenance and freshness.
- P15/P16/P17 remain interpretation/planning/readiness layers respectively; none independently grants runtime authority.

### Live GitHub App/provider evidence — proven, scoped

- Live read-only GitHub App runtime authentication is proven by run `34785659043`.
- Live governed GitHub provider mutation through the P17/controller bridge is proven on dedicated isolated test resources using create → update → delete plus fresh readback/reconciliation.
- PR #42 merged bounded post-mutation HTTP 404 readback-only retries; mutation is never replayed merely because readback is uncertain.
- Provider response is attempt evidence; completion still requires fresh readback/reconciliation.

## Current boundaries

- `production_ready = false`.
- Proven provider capability does not authorize arbitrary or production mutation.
- Credentials are technical capability only and never DevOS authorization.
- Uncertain mutation is never blindly replayed.
- Historical exact-head evidence remains pinned and is not silently rewritten when source advances.
- Resolver confidence and contradiction provenance never grant authorization, execution, completion, mutation, or production readiness.
- P12 remains owner of execution-evidence provenance/freshness; P16 remains plan compiler; P17 remains readiness/authorization gate.

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

- Recover fresh `main`, open PRs, CI, durable state, and relevant source before selecting another bounded engineering objective.
- Do not reactivate completed resolver hardening merely to continue development.
- Keep `production_ready = false` unless a separately bounded evidence-backed objective explicitly changes it.
- Do not invent a new numbered phase solely for bookkeeping.
