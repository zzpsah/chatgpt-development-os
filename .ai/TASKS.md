# DevOS Tasks

## How to read this file

This file tracks **work state**, not normative law. Source tree + current Git/PR/CI metadata remain authoritative for exact implementation/integration state. Durable principles and authorization/security decisions live in `.ai/DECISIONS.md` and the relevant core contracts.

## Normative references — not task records

- **Core documentation law:** **What is not written was never done.**
- Provider credentials/capability never manufacture DevOS authorization.
- `CONTINUE != BLANKET AUTHORIZATION`.
- `READY != EXECUTION`.
- `production_ready = false` unless separately upgraded by evidence and an explicit bounded decision.

## Active bounded work

### AI State Resolver v2 — cross-claim contradiction handling

- Unnumbered hardening objective on PR #46 / branch `feat/resolver-cross-claim-contradictions`.
- Introduce optional explicit fact identity: `fact_key` + deterministic JSON `fact_value`.
- Do not infer fact equivalence from arbitrary statement prose.
- Same valid `fact_key` + different canonical values => all involved claims become `unknown` with `CROSS_CLAIM_CONTRADICTION` and are listed in unresolved state.
- Reuse existing downstream control path: resolver `NEEDS_EVIDENCE` → P16 `CLARIFY`; forged hidden uncertainty → P17 fail-closed.
- Preserve legacy claims that provide neither identity field.
- Preserve P12 ownership of execution-evidence provenance/freshness.
- Preserve authority/authorization/execution/mutation boundaries.
- Verification requires exact-final-head CI; completion additionally requires merge and durable post-merge reconciliation.
- Do not create P18/P19 for this objective.

### Documentation objective included in the same boundary

- `docs/DEVOS-ENGINEERING-STAGE-HISTORY.md` records numbered architecture history P9–P17 and major unnumbered hardening/proof milestones through PR #45.
- The history ledger is navigation/context only; it does not replace current source/Git/CI or durable task/current-state records.
- `docs/AI-STATE-RESOLVER-CROSS-CLAIM-CONTRADICTIONS.md` records the detailed contradiction contract and non-goals.

### Concurrent-state reconciliation

- After this feature branch started from `main` at `aa38761270ac9acdf6af90a4bae64890c766ec91`, `main` advanced to `040c7d21b5fac6224ced1bdbfeaa7c3b71b78c78` with a durable-state simplification.
- That change correctly separated active state from historical evidence, but it accidentally regressed already-proven live GitHub provider evidence and removed an explicit fresh-AI account-memory boundary required by recovery tests.
- PR #46 therefore preserves the active/history separation while restoring truthful live evidence and the explicit `ChatGPT Memory/chat history` supplementary-only boundary.

## Completed — AI State Resolver v2 envelope-integrity hardening

- PR #44 — `Harden AI State Resolver v2 envelope integrity` — merged at `a4a3413bb27802ef38a698550807e8fb0102f839`.
- Exact final PR head: `71d93755e171da5e83e62b00baa4680a0e929f5e`.
- Resolver returns `NEEDS_EVIDENCE` whenever any claim resolves to `unknown`.
- Durable-state revalidation reasons remain explicit for already-`likely` claims.
- P16 validates resolver status/authority/execution/mutation/confidence/unresolved consistency and preserves full validated resolver provenance.
- P17 independently revalidates preserved resolver provenance and fails closed on hidden uncertainty or changed safety invariants.
- Exact final-head CI passed the triggered gates recorded in the PR/session evidence.
- No authority, authorization, execution, provider mutation, production mutation, or production-readiness upgrade was introduced.

## Completed — post-PR #44 durable-state reconciliation

- PR #45 merged at `aa38761270ac9acdf6af90a4bae64890c766ec91`.
- Reconciled `.ai/CURRENT-STATE.md`, `.ai/TASKS.md`, and session provenance after PR #44.

## Completed — GitHub Identity & Token Control Plane v1

- PR #32 merged at `2f1740930116ab520d40d35aaa6dfcb1786a5595`; final source head `216999bef827c9efbe78a026d06486a4765e9602`.
- GitHub App identity binding, short-lived installation-token authentication, scope/permission-aware capability discovery, and hosted-runtime support are implemented.
- Live read-only GitHub App Runtime Auth run `34785659043` succeeded; credential material was not persisted/exposed.

## Completed — governed GitHub provider mutation slice

- PR #35 merged the governed provider/controller adapter path.
- Isolated live create/update/delete evidence is recorded in current/session history.
- PR #42 merged bounded readback-only reconciliation (1s, 2s, 4s) without mutation replay.
- This proves the scoped governed mutation path, not blanket production/destructive authority.

## Completed — other major unnumbered foundations

- Production E2E Harness — PR #11.
- Failure + Recovery Proof — PR #12.
- Multi-Session / Fresh-AI Continuation Proof — PR #13.
- Controlled Remote Mutation Proof — PR #14.
- Production-Readiness Evidence Matrix & Limitations — PR #16.
- Trust-First audit gap closure — PR #17.
- Foundation Health & State Consistency — PR #18.
- Universal Project Onboarding + Repository Creation — PR #19.
- Cross-Host Recovery Friction & Onboarding Proof — PR #20.
- Recovery Friction → Foundation Health/Doctor Integration — PR #21.
- Host-neutral MCP/App `repository.create` adapter — PR #22.
- Actionable HOLD + Scoped Approval + Governed Continuation — PR #23.
- Current-Source Evidence Refresh — PR #24.
- MCP/App Permission Control Plane + Multi-Project Agent Isolation — PR #27.
- GitHub Identity & Token Control Plane v1 — PR #32.
- Governed GitHub provider/controller adapter — PR #35.
- DevOS activation handshake — PR #39.
- GitHub mutation readback reconciliation — PR #42.
- AI State Resolver v2 envelope integrity — PR #44.
- Post-PR #44 durable-state reconciliation — PR #45.

## Retained platform foundations

- P9 through P17 are completed architecture stages at their recorded evidence levels.
- **P11 Federation & Self-Healing Context** remains the repository-first recovery/revalidation/cross-AI continuity baseline.
- **P12 Operational Intelligence** remains the advisory/runtime-observability and evidence provenance/freshness substrate.
- Later unnumbered hardening objectives must not be relabeled as P18/P19 merely for bookkeeping.

## Task-map invariant

`AI A + Account A → repository → AI B + Account B → correct recovery → safe continuation`

The repository, not any AI account/chat/model/vendor memory, carries authoritative project state.
