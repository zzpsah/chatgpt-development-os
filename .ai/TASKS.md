# DevOS Tasks

## How to read this file

This file tracks **work state**, not normative law. Source tree + current Git/PR/CI metadata are authoritative for exact implementation/integration state. Durable principles and authorization/security decisions live in `.ai/DECISIONS.md` and the relevant core contracts.

## Normative references — not task records

- **Core documentation law:** **What is not written was never done.**
- **Core safety invariants:** provider capability/credentials never manufacture DevOS authorization; `CONTINUE != BLANKET AUTHORIZATION`; `READY != EXECUTION`; `production_ready = false` unless separately upgraded by evidence and an explicit bounded decision.

## Active bounded work

### AI State Resolver v2 — cross-claim contradiction handling

- Unnumbered hardening objective on PR #46 / branch `feat/resolver-cross-claim-contradictions`.
- Optional explicit fact identity: `fact_key` + deterministic JSON `fact_value`.
- No arbitrary statement-prose equivalence inference.
- Same valid `fact_key` + different canonical values => involved claims become `unknown` with `CROSS_CLAIM_CONTRADICTION` and resolver `NEEDS_EVIDENCE`.
- Existing downstream control path remains authoritative: P16 `CLARIFY`; forged hidden uncertainty => P17 fail-closed.
- Legacy claims with neither fact-identity field remain backward compatible.
- P12 retains execution-evidence provenance/freshness ownership; P16 retains planning; P17 retains readiness/authorization.
- Exact-final-head CI is required before merge; completion additionally requires post-merge durable-state reconciliation.
- Do not create P18/P19 merely for this unnumbered hardening objective.

### Documentation in the same boundary

- `docs/DEVOS-ENGINEERING-STAGE-HISTORY.md` records P9–P17 architecture history and major unnumbered milestones through PR #45.
- `docs/AI-STATE-RESOLVER-CROSS-CLAIM-CONTRADICTIONS.md` records the contradiction contract and non-goals.
- History/navigation docs never replace current source, Git/CI, `.ai/CURRENT-STATE.md`, `.ai/TASKS.md`, core contracts, or tests.

### Concurrent-main reconciliation

- Feature work started from `main` at `aa38761270ac9acdf6af90a4bae64890c766ec91`; `main` then advanced to `040c7d21b5fac6224ced1bdbfeaa7c3b71b78c78` with a compact active/history-state rewrite.
- The compact active/history intent is preserved.
- The feature branch restores the explicit ChatGPT Memory/chat-history supplementary-only recovery boundary and already-proven live GitHub provider evidence that the concurrent rewrite accidentally regressed.
- Current `main` was incorporated through a non-force two-parent merge commit; unrelated concurrent changes are preserved.

## Recently completed

### PR #45 — post-PR #44 durable-state reconciliation

- Merged at `aa38761270ac9acdf6af90a4bae64890c766ec91`.
- Synchronized durable state after PR #44.

### PR #44 — AI State Resolver v2 envelope integrity

- Merged at `a4a3413bb27802ef38a698550807e8fb0102f839`; final source head `71d93755e171da5e83e62b00baa4680a0e929f5e`.
- P16 validates/preserves the full resolver envelope; P17 independently revalidates it and fails closed on hidden uncertainty or changed safety invariants.
- No authority, execution, provider mutation, or production-readiness upgrade was introduced.

### GitHub governed provider slice

- GitHub Identity & Token Control Plane v1 — PR #32.
- Governed provider/controller adapter — PR #35.
- DevOS activation handshake — PR #39.
- GitHub mutation readback reconciliation — PR #42.
- Live read-only App run `34785659043` succeeded without exposing credential material.
- Isolated governed create/update/delete provider evidence is durable; this does not imply blanket production/destructive authority.

## Earlier completed unnumbered objectives

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
- Host-neutral MCP/App `repository.create` — PR #22.
- Actionable HOLD + Scoped Approval + Governed Continuation — PR #23.
- Current-Source Evidence Refresh — PR #24.
- MCP/App Permission Control Plane + Multi-Project Agent Isolation — PR #27.

## Retained platform foundations

- P9 through P17 are completed architecture stages at their recorded evidence levels.
- P11 remains the repository-first recovery/revalidation/cross-AI continuity baseline.
- P12 remains the advisory/runtime-observability and evidence provenance/freshness substrate.
- Later unnumbered hardening objectives must not be relabeled as P18/P19 merely for bookkeeping.

## Task-map invariant

`AI A + Account A → repository → AI B + Account B → correct recovery → safe continuation`

The repository, not any AI account/chat/model/vendor memory, carries authoritative project state.
