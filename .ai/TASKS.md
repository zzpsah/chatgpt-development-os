# DevOS Tasks

## How to read this file

This file tracks **work state**, not normative law. Source tree + current Git/PR/CI metadata are authoritative for exact implementation/integration state. Durable principles and authorization/security decisions live in `.ai/DECISIONS.md` and the relevant core contracts.

## Normative references — not task records

- **Core documentation law:** **What is not written was never done.**
- **Core safety invariants:** provider capability/credentials never manufacture DevOS authorization; `CONTINUE != BLANKET AUTHORIZATION`; `READY != EXECUTION`; `production_ready = false` unless separately upgraded by evidence and an explicit bounded decision.

## Active bounded work

### P15 bounded multilingual interpretation and gating

- Preserve Devanagari Hindi Unicode through the deterministic P15 interpreter.
- Maintain a corpus of bounded Hindi/Hinglish examples with expected interpretation, P16 classification, and P17 outcome.
- Prove high-impact Hindi wording remains authorization-gated and explicit negative constraints block conflicting plans.
- Preserve `INTERPRETATION != AUTHORIZATION`, `PLAN != EXECUTION`, and `READY != EXECUTION`.
- Completion requires local regression, exact-head CI, merge, and durable reconciliation. This does not create P18/P19.
- Do not create P18/P19 merely for bookkeeping.

## Completed — AI State Resolver v2 detailed contradiction provenance

- PR #52 — `Add detailed resolver contradiction provenance` — merged at `2a5e13ad5a46085dc6949bfbcf325f84e29f9d02`.
- Exact final source head: `b091ef2058f3c089d3daeafb41ca9fc58568f435`.
- Resolver emits deterministic `contradictions` records alongside `contradiction_fact_keys`.
- Each contradiction record contains `fact_key`, sorted involved `claim_ids`, and sorted canonical JSON values.
- Non-contradictory and invalid-top-level results emit `contradictions: []`.
- P16 independently recomputes the expected detailed provenance from claims and returns `CLARIFY` when detail is forged/inconsistent.
- P17 independently revalidates the same detail and returns `BLOCKED` when detail is forged/inconsistent after planning.
- Existing post-P16 `fact_value` tamper defense remains intact and claims-based.
- Exact-final-head CI passed: Development OS `34811362766`; Development OS Contracts `34811362710`; MCP Repository Create `34811362769`; Actionable Hold `34811362786`; P13 External Managed Project `34811362707`; Current-Source Evidence `34811362749`; GitHub Identity/Token `34811362750`; Living Engineering Map `34811362775`; Trust-First Audit `34811362701`.
- Closed PR #50 remains unmerged; only its non-duplicate detailed-provenance concept was recovered after fresh comparison against current `main`.
- No authority, authorization, execution, provider mutation, automatic winner selection, production mutation, or production-readiness upgrade was introduced.

## Completed — resolver contradiction envelope integrity

- PR #49 — `Harden resolver contradiction envelope integrity` — merged at `58d37ea23d025d7414f0d55fe2ba5ccc42068b8e`.
- Exact final source head: `3c0711a9803649505d105728e90e1ef90b3d7ce8`.
- P16 independently recomputes explicit same-`fact_key` / canonical-`fact_value` contradictions from resolver claim provenance.
- P16 fails closed on hidden contradictions, inconsistent contradiction reasons, or inconsistent `contradiction_fact_keys`.
- P17 independently recomputes contradiction integrity from the full resolver provenance retained by P16.
- Post-P16 `fact_value` tampering that creates a hidden contradiction is `BLOCKED` even when status/confidence/count metadata remains superficially consistent.
- Adversarial integration coverage proves forged contradiction hiding is rejected by P16 and post-plan fact-value tampering is rejected by P17.
- Exact-final-head CI passed: Development OS Contracts `34810461613`; Development OS `34810461872`; Actionable Hold `34810461632`; Living Engineering Map `34810461677`; Trust-First Audit `34810461612`; GitHub Identity/Token `34810461701`; Current-Source Evidence `34810461718`; MCP Repository Create `34810461678`; P13 External Managed Project `34810461615`.
- PR #51 reconciled post-#49 durable state and merged at `2500ddc235ce99dbe45a6cd0537d4b0d2372c4a4`.

## Completed — AI State Resolver v2 cross-claim contradiction handling

- PR #46 — `Add resolver cross-claim contradiction handling` — merged at `36f3001487fb7ce666bb1e7241b539645878101a`.
- Exact final feature head: `490eeebea69a4f4ae44657f5d94edaef35a26db4`.
- Adds optional explicit `fact_key` + deterministic JSON `fact_value` identity while preserving legacy claims with neither field.
- Same valid `fact_key` + different canonical values => involved claims become `unknown` with `CROSS_CLAIM_CONTRADICTION`; resolver status becomes `NEEDS_EVIDENCE` and records `contradiction_fact_keys`.
- Arbitrary statement prose is not semantically paired by guesswork and no automatic winner is selected.
- P16 uses the unresolved-state path and returns `CLARIFY`; P17 fails closed if unknown contradiction claims are hidden in a forged planned envelope.
- Exact final-head CI passed: Development OS `34809630956`; Contracts `34809630926`; Current-Source `34809630993`; Trust-First `34809630947`; Living Engineering Map `34809631004`; GitHub Identity/Token `34809631046`; MCP Repository Create `34809630925`.
- PR #47 was a concurrent duplicate attempt and was closed without merge after #46 became authoritative.
- PR #48 reconciled post-#46 durable state and merged at `7009e8e1b4398462b1a9321bb1e2a38a3c35e478`.

## Completed — previous-stage documentation ledger

- `docs/DEVOS-ENGINEERING-STAGE-HISTORY.md` documents numbered architecture stages P9–P17 and major unnumbered proof/hardening milestones through PR #52.
- The ledger is navigation/history only; current source, Git/PR/CI, `.ai/CURRENT-STATE.md`, `.ai/TASKS.md`, core contracts, tests, and decisions remain authoritative.
- `docs/AI-STATE-RESOLVER-CROSS-CLAIM-CONTRADICTIONS.md` records the contradiction contract, downstream envelope-integrity defenses, detailed contradiction provenance, and non-goals.

## Completed — first-contact acknowledgement hardening

- Main commit `f07c7c5a4afd4fd25c0da5b1ed7ee88733168baa` hardened the Plain Project Context and Recovery Guide first-contact signal.
- Fresh sessions use the host-neutral acknowledgement `DevOS context recovered` / `DevOS context not verified` instead of requesting or implying a host mode.

## Completed — AI State Resolver v2 envelope integrity

- PR #44 merged at `a4a3413bb27802ef38a698550807e8fb0102f839`; exact final source head `71d93755e171da5e83e62b00baa4680a0e929f5e`.
- P16 validates/preserves the full resolver envelope; P17 independently revalidates it and fails closed on hidden uncertainty or changed safety invariants.
- PR #45 merged at `aa38761270ac9acdf6af90a4bae64890c766ec91` to reconcile post-#44 durable state.

## Completed — GitHub governed provider slice

- GitHub Identity & Token Control Plane v1 — PR #32.
- Governed provider/controller adapter — PR #35.
- DevOS activation handshake historical milestone — PR #39; current first-contact wording was later hardened by `f07c7c5...`.
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

## Current HOLD / limits

- `production_ready = false`.
- Resolver confidence and contradiction provenance never grant authorization, execution, mutation, or completion.
- P12 retains execution-evidence provenance/freshness ownership; P16 retains planning; P17 retains readiness/authorization.
- No production/deployment/credential/permission/destructive authority was introduced by the resolver hardening sequence.

## Task-map invariant

`AI A + Account A → repository → AI B + Account B → correct recovery → safe continuation`

The repository, not any AI account/chat/model/vendor memory, carries authoritative project state.
