# DevOS Tasks

## How to read this file

This file tracks **work state**, not normative law. Source tree + current Git/PR/CI metadata are authoritative for exact implementation/integration state. Durable principles and authorization/security decisions live in `.ai/DECISIONS.md` and the relevant core contracts.

## Normative references — not task records

- **Core documentation law:** **What is not written was never done.**
- **Core safety invariants:** provider capability/credentials never manufacture DevOS authorization; `CONTINUE != BLANKET AUTHORIZATION`; `READY != EXECUTION`; `production_ready = false` unless separately upgraded by evidence and an explicit bounded decision.

## Active bounded work

### AI State Resolver v2 — downstream contradiction integrity

- Unnumbered defense-in-depth objective on `fix/resolver-downstream-contradiction-integrity`.
- Keep PR #46 resolver contradiction behavior; do not duplicate/rewrite the completed feature.
- Add detailed deterministic contradiction provenance for downstream validation while keeping `contradiction_fact_keys`.
- P16 recomputes structured contradictions from preserved claims and returns `CLARIFY` if contradiction metadata/confidence was forged.
- P17 recomputes again at readiness and blocks post-P16 `fact_value` tampering with `PLAN_STATE_RESOLUTION_HIDDEN_CONTRADICTION`.
- Existing authority, authorization, P12 freshness ownership, Security Gate, provider, and production boundaries remain unchanged.
- Exact-final-head CI + merge + post-merge durable reconciliation are required for completion.
- Closed PR #47 is provenance for the narrow gap only; its duplicate/stale broad branch is not merged.
- No P18/P19 bookkeeping phase.

## Completed — AI State Resolver v2 cross-claim contradiction handling

- PR #46 — `Add resolver cross-claim contradiction handling` — merged at `36f3001487fb7ce666bb1e7241b539645878101a`.
- Exact final feature head: `490eeebea69a4f4ae44657f5d94edaef35a26db4`.
- Adds optional explicit `fact_key` + deterministic JSON `fact_value` identity while preserving legacy claims with neither field.
- Same valid `fact_key` + different canonical values => involved claims become `unknown` with `CROSS_CLAIM_CONTRADICTION`; resolver status becomes `NEEDS_EVIDENCE` and records `contradiction_fact_keys`.
- Arbitrary statement prose is not semantically paired by guesswork and no automatic winner is selected.
- P16 reuses the existing unresolved-state path and returns `CLARIFY`; P17 fails closed if unknown contradiction claims are hidden in a forged planned envelope.
- Exact final-head CI passed: Development OS `34809630956`; Contracts `34809630926`; Current-Source `34809630993`; Trust-First `34809630947`; Living Engineering Map `34809631004`; GitHub Identity/Token `34809631046`; MCP Repository Create `34809630925`.
- PR #48 merged at `7009e8e1b4398462b1a9321bb1e2a38a3c35e478` to close durable state.

## Completed — previous-stage documentation ledger

- `docs/DEVOS-ENGINEERING-STAGE-HISTORY.md` documents numbered architecture stages P9–P17 and major unnumbered proof/hardening milestones.
- The ledger is navigation/history only; current source, Git/PR/CI, `.ai/CURRENT-STATE.md`, `.ai/TASKS.md`, core contracts, tests, and decisions remain authoritative.
- `docs/AI-STATE-RESOLVER-CROSS-CLAIM-CONTRADICTIONS.md` records the bounded contradiction contract and non-goals.

## Completed — first-contact acknowledgement hardening

- Main commit `f07c7c5a4afd4fd25c0da5b1ed7ee88733168baa` hardened the Plain Project Context and Recovery Guide first-contact signal.
- Fresh sessions use host-neutral `DevOS context recovered` / `DevOS context not verified` acknowledgement instead of requesting or implying a host mode.
- The acknowledgement reports recovered context only; it does not create authority, permissions, or changed host behavior.

## Completed — AI State Resolver v2 envelope integrity

- PR #44 merged at `a4a3413bb27802ef38a698550807e8fb0102f839`; exact final source head `71d93755e171da5e83e62b00baa4680a0e929f5e`.
- P16 validates/preserves the full resolver envelope; P17 independently revalidates it and fails closed on hidden uncertainty or changed safety invariants.
- PR #45 merged at `aa38761270ac9acdf6af90a4bae64890c766ec91` to reconcile post-#44 durable state.

## Completed — GitHub governed provider slice

- GitHub Identity & Token Control Plane v1 — PR #32.
- Governed provider/controller adapter — PR #35.
- DevOS activation handshake historical milestone — PR #39; current first-contact wording was later hardened to host-neutral context-recovery acknowledgement by `f07c7c5...`.
- GitHub mutation readback reconciliation — PR #42.
- Live read-only App run `34785659043` succeeded without exposing credential material.
- Isolated governed create/update/delete provider evidence is durable; this proves the scoped path, not blanket production/destructive authority.

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
