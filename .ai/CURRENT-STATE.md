# Current State

## Current source and authority

- Repository: `zzpsah/chatgpt-development-os`.
- Current source tree + Git/PR/CI metadata are authoritative for exact implementation/integration state; `.ai` records carry durable semantic context.
- **ChatGPT Memory/chat history and any model/account memory are supplementary only and never authoritative project state.**
- Current bounded objective started from `main` at `2500ddc235ce99dbe45a6cd0537d4b0d2372c4a4`, the merge of post-PR #49 durable-state reconciliation PR #51.
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

### AI State Resolver v2 — detailed contradiction provenance

Fresh post-#51 inspection found no open competing PR. Closed stale/diverged PR #50 contained one useful non-duplicate concept after PR #49 superseded its downstream integrity work: deterministic detailed contradiction provenance.

Current bounded objective on `feat/resolver-detailed-contradiction-provenance`:

- keep PR #46 contradiction semantics and PR #49 P16/P17 independent contradiction recomputation unchanged;
- resolver emits `contradictions` alongside `contradiction_fact_keys`;
- each detail record contains the explicit `fact_key`, sorted involved claim IDs, and sorted canonical conflicting JSON values;
- non-contradictory and blocked-top-level results emit `contradictions: []`;
- P16 independently recomputes the expected detailed provenance from claims and returns `CLARIFY` if the field is forged or inconsistent;
- P17 independently repeats the validation on P16-preserved provenance and returns `BLOCKED` if detailed contradiction provenance is forged or changes after planning;
- the detail is audit evidence only and cannot grant authority, erase uncertainty, select a winning claim, create execution, or make a step READY.

This is an unnumbered observability/integrity hardening objective. No P18/P19 is created.

## Current verified capability state

### Resolver contradiction envelope integrity — merged

- PR #49 — `Harden resolver contradiction envelope integrity` — merged at `58d37ea23d025d7414f0d55fe2ba5ccc42068b8e`.
- Exact final PR head: `3c0711a9803649505d105728e90e1ef90b3d7ce8`.
- P16 independently recomputes explicit same-`fact_key` / canonical-`fact_value` contradiction groups before planning.
- P16 rejects hidden contradictions, inconsistent `CROSS_CLAIM_CONTRADICTION` reasons, and inconsistent `contradiction_fact_keys`.
- P17 independently recomputes contradiction integrity from full resolver provenance retained by P16.
- A post-P16 `fact_value` edit that creates a hidden contradiction is `BLOCKED` even when top-level status/confidence/count metadata remains superficially valid.
- Exact-final-head CI passed all triggered workflows: Development OS Contracts `34810461613`, Development OS `34810461872`, Actionable Hold `34810461632`, Living Engineering Map `34810461677`, Trust-First Audit `34810461612`, GitHub Identity/Token `34810461701`, Current-Source Evidence `34810461718`, MCP Repository Create `34810461678`, and P13 External Managed Project `34810461615`.
- The Contracts workflow completed its full regression suite including P16, P17, resolver, Security Gate, P12, and P14 checks.
- PR #51 reconciled durable state after #49 and merged at `2500ddc235ce99dbe45a6cd0537d4b0d2372c4a4`.
- This hardening creates no authority, authorization, execution, provider mutation, or production-readiness upgrade.

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

- Open a bounded PR for detailed contradiction provenance from the current branch.
- Require exact-final-head applicable CI; repair compatibility failures without weakening claims-based P16/P17 recomputation.
- Merge only under the user's currently applicable bounded DevOS authorization and only when exact-head CI is green and the PR remains mergeable.
- After merge, reconcile durable state so this completed objective is not left active.
- Keep `production_ready = false`; do not invent a new numbered phase solely for bookkeeping.
