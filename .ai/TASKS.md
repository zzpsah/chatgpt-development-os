# DevOS Tasks

## How to read this file

This file tracks **work state**, not normative law. Source tree + current Git/PR/CI metadata are authoritative for exact implementation/integration state. Durable principles and authorization/security decisions live in `.ai/DECISIONS.md` and the relevant core contracts.

## Normative references — not task records

- **Core documentation law:** **What is not written was never done.**
- **Core safety invariants:** provider capability/credentials never manufacture DevOS authorization; `CONTINUE != BLANKET AUTHORIZATION`; `READY != EXECUTION`; `production_ready = false` unless separately upgraded by evidence and an explicit bounded decision.

## Active bounded work

### Resolver contradiction envelope-integrity follow-up

PR #46 closed the base cross-claim contradiction feature. The active narrow follow-up is defense in depth against a crafted/tampered resolver envelope.

Required behavior:

- P16 independently recomputes explicit same-`fact_key` / canonical-`fact_value` contradiction groups from preserved claims;
- a forged resolver envelope cannot turn contradictory claims back to `likely`, clear `contradiction_fact_keys`, and claim `RESOLVED`;
- P16 verifies contradiction reasons and contradiction summary consistency before allowing a plan;
- P17 independently recomputes contradiction integrity from P16-preserved provenance;
- changing one `fact_value` after P16 to create a contradiction must make P17 fail closed even if status/confidence/count metadata remains superficially valid;
- legacy claims without explicit fact identity remain backward compatible;
- no NLP/prose fact pairing, automatic winner selection, authority change, or execution is introduced.

Verification requirements:

- forged contradiction-hidden envelope => P16 `CLARIFY`;
- valid same-value fact group => P16 `PLANNED`;
- post-plan one-value tamper => P17 `BLOCKED` with hidden-contradiction evidence;
- existing P16/P17/resolver regression suites remain green;
- exact-final-head applicable CI passes before completion is claimed.

## Recently completed

### PR #46 — AI State Resolver v2 cross-claim contradiction handling

- Merged at `36f3001487fb7ce666bb1e7241b539645878101a`.
- Exact final source head: `490eeebea69a4f4ae44657f5d94edaef35a26db4`.
- Optional explicit `fact_key` + deterministic JSON `fact_value` identity added.
- Same fact + different canonical values => involved claims `unknown` + `CROSS_CLAIM_CONTRADICTION`, resolver `NEEDS_EVIDENCE`, and P16 `CLARIFY` through the unresolved-state path.
- Exact-final-head CI passed: Development OS `34809630956`, Contracts `34809630926`, Current-Source Evidence `34809630993`, Trust-First `34809630947`, Living Engineering Map `34809631004`, GitHub Identity/Token `34809631046`, MCP Repository Create `34809630925`.
- `docs/AI-STATE-RESOLVER-CROSS-CLAIM-CONTRADICTIONS.md` records the current contradiction contract.
- `docs/DEVOS-ENGINEERING-STAGE-HISTORY.md` records P9–P17 and major unnumbered milestones through the resolver evolution.
- PR #47 was a concurrent duplicate attempt and was closed without merge after #46 became authoritative.

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

## Current HOLD / limits

- `production_ready = false`.
- Resolver confidence never grants authorization, execution, mutation, or completion.
- P12 retains execution-evidence provenance/freshness ownership; P16 retains planning; P17 retains readiness/authorization.
- No production/deployment/credential/permission/destructive authority is introduced by this follow-up.

## Task-map invariant

`AI A + Account A → repository → AI B + Account B → correct recovery → safe continuation`

The repository, not any AI account/chat/model/vendor memory, carries authoritative project state.
