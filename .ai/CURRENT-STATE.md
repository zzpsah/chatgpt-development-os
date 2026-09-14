# Current State

## Current source and authority

- Repository: `zzpsah/chatgpt-development-os`.
- Current source tree + Git/PR/CI metadata are authoritative for exact implementation/integration state; `.ai` records carry durable semantic context.
- **ChatGPT Memory/chat history and any model/account memory are supplementary only and never authoritative project state.**
- Current bounded follow-up is based on `main` at `7009e8e1b4398462b1a9321bb1e2a38a3c35e478`, the merge of PR #48 post-#46 durable-state reconciliation.
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

### Resolver contradiction envelope-integrity follow-up

PR #46 completed and verified the base structured cross-claim contradiction feature. Post-merge inspection found a narrower defense-in-depth gap at the resolver → P16 → P17 envelope boundaries.

Current bounded hardening:

- P16 independently recomputes explicit same-`fact_key` / canonical-`fact_value` contradiction groups from resolver claim provenance;
- P16 rejects hidden contradictions, inconsistent contradiction reasons, or inconsistent `contradiction_fact_keys` before planning;
- P17 independently recomputes contradiction integrity from the full resolver provenance preserved in a plan;
- changing a previously consistent `fact_value` after P16 so that claims now conflict causes P17 `BLOCKED` even if status/confidence/count metadata remains superficially consistent;
- no free-text/NLP fact pairing or automatic source-precedence winner is introduced.

This is an unnumbered defense-in-depth objective. No P18/P19 is created.

## Current verified capability state

### AI State Resolver v2 cross-claim contradiction handling — merged

- PR #46 — `Add resolver cross-claim contradiction handling` — merged at `36f3001487fb7ce666bb1e7241b539645878101a`.
- Exact final feature head: `490eeebea69a4f4ae44657f5d94edaef35a26db4`.
- Optional explicit `fact_key` + deterministic JSON `fact_value` identity is supported.
- Same valid fact identity with different canonical values makes involved claims `unknown`, adds `CROSS_CLAIM_CONTRADICTION`, records `contradiction_fact_keys`, and produces `NEEDS_EVIDENCE`.
- Legacy claims without fact identity remain backward compatible.
- Exact final-head CI passed: Development OS `34809630956`, Contracts `34809630926`, Current-Source Evidence `34809630993`, Trust-First Audit `34809630947`, Living Engineering Map `34809631004`, GitHub Identity/Token `34809631046`, MCP Repository Create `34809630925`.
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
- Plain Project Context and Recovery Guide v1 remains the default first-contact path.

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
- Resolver confidence never grants authorization, execution, completion, mutation, or production readiness.
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

- Run exact-head applicable CI for the contradiction envelope-integrity follow-up.
- Repair compatibility failures without weakening independent contradiction recomputation.
- Merge under the current standing user authorization only when exact-head CI is green and the PR is mergeable.
- After merge, reconcile durable state so no completed objective remains marked active.
- Keep `production_ready = false`; do not invent a new numbered phase solely to continue development.
