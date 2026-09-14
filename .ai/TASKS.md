# DevOS Tasks

## How to read this file

This file tracks **work state**, not normative law. Current source/Git/PR/CI are authoritative for exact implementation state. Durable principles and authorization/security decisions live in `.ai/DECISIONS.md` and core contracts. Historical milestone detail lives in `docs/DEVOS-ENGINEERING-STAGE-HISTORY.md`, `.ai/RECONCILIATION-LEDGER.jsonl`, and `.ai/SESSIONS/`.

## Core safety invariants

- **What is not written was never done.**
- `CONTINUE != BLANKET AUTHORIZATION`.
- `READY != EXECUTION`.
- `CI PASS != AUTHORIZATION`.
- provider/runtime credentials and capability never manufacture DevOS authority.
- runtime completion claims require independent evidence validation.
- `production_ready = false` unless a separately bounded evidence-backed decision changes it.

## Active bounded work

- No bounded engineering objective remains active after post-PR #57 reconciliation.
- Select future work only from fresh `main`, open PRs, current CI, durable state, relevant source/tests, and current user intent.
- Do not create P18/P19 merely for bookkeeping.

## Completed — Universal Agent Runtime Adapter v1

- PR #57 — `Add universal agent runtime adapter v1` — merged at `5d0bdbc0258e898ece21f99937dc4f5b886778a0`.
- Exact final feature head: `da57d48c1ec28eac71eff75b59f9c701e9c9c593`.
- Adds side-effect-free `tools/agent-runtime-handoff.py`, normative `core/agent-runtime-adapter.md`, generic runtime profile, adversarial tests, and dedicated CI.
- Handoff requires P17 READY/gates/head evidence, exact scoped approval, available local runtime capabilities, safe relative target paths, and only `file.create` / `file.update` operation classes in v1.
- Canonical SHA-256 `handoff_id` detects handoff tampering.
- Runtime `COMPLETED` becomes `VERIFIED_RUNTIME_RESULT` only when touched files, observed diff, passing tests, final readback, runtime identity, repository head, and prohibited-operation evidence agree with the approved handoff.
- Exact-head successful runs: Development OS `34816332421`; Contracts `34816332435`; Current-Source Evidence `34816332392`; MCP Repository Create `34816332425`; Trust-First `34816332380`; Evidence Durable Reconciliation `34816332373`; Agent Runtime Adapter `34816332410`.
- PR #56 was closed without merge after concurrent main advancement; PR #57 is authoritative.
- Runtime Adapter v1 performs no filesystem mutation, command execution, provider call, deployment, or automatic approval and makes no vendor-specific integration claim.
- PR #57 reconciliation record is appended to `.ai/RECONCILIATION-LEDGER.jsonl`; digest `3885b140ce1c81c387ed6dad7a9ceb8183e275717540d5b5711269f1a6a95374` is pinned in the post-merge session.

## Completed — Local Disposable Delivery Proof v1

- Main commit `1f735fa11e19b9852ce9210338bc0907ab0b5b1c`; closure commit `284def759c6532bc80701dcfaff5446d5e315ac4`.
- Proves P15 → P16 → P17 → exact local scoped approval → controller/runtime handoff → disposable-repository file update → local test/readback → evidence packet → fresh recovery.
- Exact-head successful runs: Development OS `34816057996`; Contracts `34816057880`; Trust-First `34816057979`; Living Engineering Map `34816057867`; GitHub Identity/Token `34816057874`; Provider Controller Adapter `34816057869`; Remote Permission Governance `34816057885`.
- Scope excludes commit/push, managed-repository/provider operations, deployment, production, credentials, database, permissions, destructive actions, and general automated-delivery authority.
- Runtime Adapter v1 is complementary and is not retroactively claimed as part of this proof.

## Completed — Automated Evidence → Durable State Reconciliation v1

- PR #54 merged at `e31c2099b5d9ce88ee4a20c225fe70b424dffa3d`; post-merge reconciliation PR #55 merged at `ec77c2efed145fe2c419fba365aad33a6f10990e`.
- Machine-verifiable merge/CI/file/document facts can be normalized deterministically; semantic CURRENT/TASKS/roadmap/authority meaning still requires review.
- Reconciliation records are tamper-evident and do not grant authority, execution, provider permission, or production readiness.

## Completed — P15 multilingual and AI State Resolver hardening

- P15 bounded Devanagari Hindi/Hinglish corpus and P15 → P16 → P17 safety regression remain completed at recorded evidence levels.
- Resolver sequence: PR #44 envelope integrity; PR #46 structured cross-claim contradiction handling; PR #49 downstream independent contradiction recomputation; PR #52 detailed contradiction provenance.
- Closed/stale duplicate PRs remain provenance only and never replace merged current source.

## Completed — previous-stage documentation ledger

- `docs/DEVOS-ENGINEERING-STAGE-HISTORY.md` tracks P9–P17 and major unnumbered milestones.
- `docs/DEVOS-MASTER-ENGINEERING-MAP.md` is the living architecture/future-flow map.
- `core/agent-runtime-adapter.md` is the normative Runtime Adapter v1 contract.
- `core/local-disposable-delivery-proof.md` is the local disposable delivery proof contract.
- `core/evidence-durable-state-reconciliation.md` is the evidence reconciliation contract.

## Retained platform foundations

- P9 through P17 remain completed architecture stages at their recorded evidence levels.
- P11 remains repository-first recovery/revalidation/cross-AI continuity baseline.
- P12 remains evidence provenance/freshness owner.
- P15 remains language interpretation; P16 planning; P17 readiness/authorization.
- Existing controller/runtime handoff, GitHub governed provider capability, readback reconciliation, multi-project isolation, Actionable HOLD, current-source evidence, onboarding, recovery, adaptive verification/self-healing, and trust-first auditing remain retained foundations.

## Current HOLD / limits

- `production_ready = false`.
- Runtime profile/capability is not approval.
- Runtime result is evidence, not authority.
- Universal Agent Runtime Adapter v1 does not prove a vendor-specific Codex/Claude/OpenHands/Gemini integration.
- Local Disposable Delivery Proof v1 remains local/disposable only.
- No production/deployment/credential/database/permission/destructive authority was introduced.
- Semantic CURRENT/TASKS/roadmap changes require review; commit messages are not semantic truth.
- Uncertain provider mutation is never blindly replayed.
- Parallel AI branches must revalidate against fresh `main` before integration.

## Task-map invariant

`AI A + Account A → repository → AI B + Account B → correct recovery → safe continuation`

The repository, not any AI account/chat/model/vendor memory, carries authoritative project state.
