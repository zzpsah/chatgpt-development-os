# DevOS Tasks

## Core safety invariants

- **What is not written was never done.**
- `PLAN != EXECUTION`
- `READY != EXECUTION`
- `INTERPRETATION != AUTHORIZATION`
- `DOCUMENTATION != AUTHORIZATION`
- `SIMULATED EVIDENCE != LIVE PROVIDER PROOF`
- `CHAT MEMORY != SOURCE OF TRUTH`

## Active bounded work

### AI State Resolver v2 — structured cross-claim contradiction hardening

Objective: deterministically surface incompatible claims about the same explicitly identified fact without introducing NLP guessing, evidence-precedence assumptions, authority, or execution.

Required implementation:

- optional structured `fact_key` + `fact_value` pair on resolver claims;
- canonical JSON comparison for stable deterministic values;
- incomplete structured identity => `unknown` / `FACT_IDENTITY_INCOMPLETE`;
- same `fact_key` + multiple canonical values => every involved claim becomes `unknown` / `CROSS_CLAIM_CONTRADICTION`;
- deterministic contradiction summary in resolver output;
- contradiction IDs propagate to P16 as unresolved state and force `CLARIFY`;
- P16 independently recomputes contradiction consistency;
- P17 independently recomputes contradiction consistency after planning and blocks tampering;
- stale/current disagreement is not silently resolved by precedence;
- no change to P12 freshness ownership or P17 authorization/security/runtime gates.

Verification requirements:

- same fact/same canonical value remains resolved;
- structured objects with different key order do not create false contradictions;
- same fact/different value becomes unresolved;
- stale-vs-current disagreement remains unresolved;
- forged resolver contradiction metadata cannot bypass P16;
- post-P16 fact-value tampering cannot bypass P17;
- exact-head applicable CI must pass before completion is claimed.

## Current HOLD / limits

- `production_ready = false`.
- No arbitrary/destructive/production mutation is authorized merely by resolver work.
- Resolver confidence never grants authorization, execution, mutation, or completion.
- P12 remains owner of execution-evidence provenance and freshness.
- No automatic NLP/prose inference of fact identity.
- No automatic winner selection between contradictory claims.
- No P18/P19 phase is created merely for bookkeeping.

## Closed current foundations

- **AI State Resolver v2 grounding/freshness** — deterministic read-only claim resolution; durable-state grounding capped at `likely`; current P12 execution evidence required for `observed`.
- **Resolver -> P16 -> P17 propagation** — unresolved claims force P16 `CLARIFY`; valid resolver provenance is retained; P17 rejects unresolved/tampered state.
- **AI State Resolver v2 envelope-integrity hardening (PR #44)** — P16/P17 validate full resolver invariants and fail closed on hidden uncertainty or changed authority/execution state.
- **Post-PR #44 durable-state reconciliation (PR #45)** — merged at `aa38761270ac9acdf6af90a4bae64890c766ec91`.
- **Live GitHub App read-only provider proof** — workflow run `34785659043` succeeded.
- **Governed GitHub controller/provider mutation proof** — isolated create/update/delete path proven with fresh readback/reconciliation evidence; this does not imply production readiness.
- **GitHub mutation readback hardening (PR #42)** — bounded readback-only retries without mutation replay.
- **Plain Project Context and Recovery Guide v1** — merged and retained.
- **GitHub Identity & Token Control Plane v1 repository slice** — merged through PR #32.

Detailed resolver-stage history: `docs/AI-STATE-RESOLVER-EVOLUTION.md`.

## Historical evidence index

Detailed historical records remain in Git history, dated `.ai/SESSIONS/` files, `docs/handoff/`, and the master engineering map. They are not active tasks.

- P9 Development Task Controller; P10 Context Continuity & Recovery; P11 Federation & Self-Healing Context; P12 Operational Intelligence; P13 Autonomous Development Orchestration; P14 Adaptive Verification & Self-Healing; P15 Human Language Interpretation; P16 Semantic Goal-to-Plan Compiler; P17 Step Readiness & Authorization Orchestrator.
- Production E2E (PR #11), Failure + Recovery (PR #12), Multi-Session / Fresh-AI (PR #13), Controlled Remote Mutation (PR #14), Production-Readiness Evidence (PR #16), Trust-First Audit (PR #17), Foundation Health (PR #18), Onboarding (PR #19), Recovery Friction (PR #20/#21), repository.create (PR #22), Actionable HOLD (PR #23), Current-Source Evidence (PR #24), MCP/App Permission Control Plane (PR #27), GitHub identity/token control plane (PR #32), governed provider/controller adapter (PR #35), mutation readback hardening (PR #42), resolver envelope integrity (PR #44), and durable-state reconciliation (PR #45).

## Permanent task boundaries

- `CI PASS != AUTHORIZATION`
- `OLD APPROVAL != NEW APPROVAL` when scope, freshness, or security changes
- `RECOVERY != AUTOMATIC MUTATION REPLAY`

For durable principles and authorization decisions, use `.ai/DECISIONS.md` and the relevant core contracts. This file is limited to active work, current holds, and an index of closed evidence.
