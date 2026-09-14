# Current State

## Current source and authority

- Repository: `zzpsah/chatgpt-development-os`.
- Source tree + current Git/PR/CI metadata are authoritative for exact implementation/integration state; `.ai` records carry durable semantic context.
- **ChatGPT Memory/chat history and any model/account memory are supplementary only and never authoritative project state.**
- Current `main` baseline for this bounded follow-up: `36f3001487fb7ce666bb1e7241b539645878101a` (merge of PR #46, cross-claim contradiction handling).
- `docs/DEVOS-MASTER-ENGINEERING-MAP.md` remains the living architecture index; `docs/DEVOS-ENGINEERING-STAGE-HISTORY.md` is the durable stage-history/navigation ledger.

## Core documentation law

> **What is not written was never done.**

Material engineering work follows:

`OBSERVE → ACT / CHANGE / DECIDE → VERIFY → DOCUMENT → PERSIST IN GIT`

Completion requires `IMPLEMENTED + VERIFIED + DOCUMENTED + DURABLE STATE`.

## Canonical governed path

`Human request → P15 interpretation → P16 plan → P17 readiness → Actionable HOLD / Scoped Approval → controller → bounded runtime → verification → persistence → recovery / continuation`

Interpretation, planning, readiness, provider credentials, prior approvals, recovery state, documentation, CI, or simulated evidence never manufacture permission.

## Active bounded work

### Resolver contradiction envelope-integrity follow-up

PR #46 completed the base structured cross-claim contradiction feature. Fresh post-merge inspection found one narrower defense-in-depth gap: P16/P17 still trusted resolver-produced uncertainty metadata enough that a crafted envelope could theoretically change contradictory claims back to `likely`, clear contradiction/unresolved metadata, or alter a `fact_value` after planning while preserving apparently consistent counts.

This follow-up therefore adds independent contradiction recomputation at both governed boundaries:

- P16 recomputes explicit `fact_key` / canonical `fact_value` groups before planning;
- P16 rejects hidden contradictions, inconsistent `CROSS_CLAIM_CONTRADICTION` reasons, and inconsistent `contradiction_fact_keys`;
- P17 recomputes the same contradiction integrity from full resolver provenance preserved in the plan;
- post-P16 `fact_value` tampering that creates a contradiction is `BLOCKED` even when status/confidence/count metadata is left unchanged;
- no free-text/NLP fact-identity inference is introduced;
- no authority, authorization, execution, mutation, or production-readiness upgrade is introduced.

This is an unnumbered hardening objective. No P18/P19 is created.

## Current verified capability state

### AI State Resolver v2 cross-claim contradiction handling — merged

- PR #46 — `Add resolver cross-claim contradiction handling` — merged into `main` at `36f3001487fb7ce666bb1e7241b539645878101a`.
- Exact final source head: `490eeebea69a4f4ae44657f5d94edaef35a26db4`.
- Explicit `fact_key` + deterministic JSON `fact_value` identity is supported.
- Same valid fact identity with different canonical values makes involved claims `unknown` with `CROSS_CLAIM_CONTRADICTION`, records `contradiction_fact_keys`, and produces `NEEDS_EVIDENCE`.
- Legacy claims without fact identity remain backward compatible.
- Exact-final-head CI passed: Development OS `34809630956`, Contracts `34809630926`, Current-Source Evidence `34809630993`, Trust-First `34809630947`, Living Engineering Map `34809631004`, GitHub Identity/Token `34809631046`, and MCP Repository Create `34809630925`.
- PR #47 was a concurrent duplicate attempt; it was closed as superseded and was not merged.

### AI State Resolver v2 envelope integrity — closed

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
- PR #42 merged bounded post-mutation HTTP 404 readback-only retries of 1s, 2s, and 4s; mutation is never replayed merely because readback is uncertain.
- Provider response is attempt evidence; completion still requires fresh provider readback/reconciliation.

## Current boundaries

- `production_ready = false`.
- Proven provider capability does not authorize arbitrary or production mutation.
- No live repository deletion, branch deletion, force update, production mutation, credential mutation, or permission mutation is established as blanket authority.
- Credentials are technical capability only and never DevOS authorization.
- Uncertain mutation is never blindly replayed.
- Historical exact-head evidence remains pinned; later source movement must not silently rewrite what a past run proved.
- Resolver confidence never grants authorization, execution, completion, mutation, or production readiness.

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

- Verify the contradiction envelope-integrity follow-up on its exact candidate head.
- Repair compatibility regressions without weakening the new fail-closed contradiction checks.
- Merge only after applicable exact-head CI is green and the PR is mergeable under the current standing user authorization.
- After merge, reconcile durable state so this follow-up is no longer active.
- Keep `production_ready = false`; do not create P18/P19 merely for bookkeeping.
