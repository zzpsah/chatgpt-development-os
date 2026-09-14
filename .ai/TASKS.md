# DevOS Tasks

## How to read this file

This file tracks **work state**, not normative law. Current source/Git/PR/CI are authoritative for exact implementation state. Durable principles and authorization/security decisions live in `.ai/DECISIONS.md` and core contracts. Historical milestone detail lives in `docs/DEVOS-ENGINEERING-STAGE-HISTORY.md` and `.ai/SESSIONS/`.

## Core safety invariants

- **What is not written was never done.**
- `CONTINUE != BLANKET AUTHORIZATION`.
- `READY != EXECUTION`.
- `CI PASS != AUTHORIZATION`.
- provider credentials/capability never manufacture DevOS authority.
- `production_ready = false` unless a separately bounded evidence-backed decision changes it.

## Active bounded work

- No bounded engineering objective remains active after post-PR #54 reconciliation.
- Select future work only from fresh `main`, open PRs, current CI, durable state, relevant source/tests, and current user intent.
- Do not create P18/P19 merely for bookkeeping.

## Completed — Automated Evidence → Durable State Reconciliation v1

- PR #54 — `Add automated evidence to durable-state reconciliation v1` — merged at `e31c2099b5d9ce88ee4a20c225fe70b424dffa3d`.
- Exact final feature head: `a2da0eaf2a5464d4a716859168bf0ba4d87659a6`.
- Adds `tools/evidence-durable-state-reconciler.py` with protocol `DEVOS-EVIDENCE-DURABLE-RECONCILIATION-v1`.
- Machine-verifiable merge/CI/file/document facts can be normalized deterministically; semantic project state still requires explicit review.
- Fail-closed boundary invariants: `authority=UNCHANGED`, `authorization=UNCHANGED`, `execution=NONE`, `mutation=NONE`, `production_ready=false`.
- Ready output emits a deterministic `DEVOS-DURABLE-RECONCILIATION-RECORD-v1`, canonical digest, and bounded write plan; it does not perform repository/provider writes itself.
- Regression corpus covers unmerged work, failed/stale/missing CI, missing required docs, absent semantic review, forged authority/execution/production readiness, unknown auto-authorization fields, and record/digest tampering.
- Dedicated workflow `.github/workflows/verify-evidence-durable-reconciliation.yml` passed on exact feature head.
- Exact-head successful runs: Development OS `34813287533`; Contracts `34813287564`; Current-Source Evidence `34813287546`; MCP Repository Create `34813287537`; Trust-First Audit `34813287565`; Evidence Durable Reconciliation `34813287654`.
- Machine reconciliation record is persisted in `.ai/RECONCILIATION-LEDGER.jsonl`; digest `3d60ab6d8c9b066a4835cc877b38b636cc136e19e6b18fce1b8e1d79702ebac5` is pinned in `.ai/SESSIONS/2026-09-14-post-pr54-evidence-reconciliation.md`.
- Post-merge semantic review preserves P15 multilingual closure and records that the master map already contains G5/G8/G10 architectural direction; no new numbered phase is required.
- No authority, authorization, provider mutation, deployment, automatic merge policy, next-objective inference, or production-readiness upgrade was introduced.

## Completed — P15 bounded Devanagari Hindi/Hinglish interpretation and gating

- Main commit `001f48e64d3e7e6e32d9befc9bb00899b8868e03` preserves Unicode Hindi and adds bounded multilingual corpus plus P15 → P16 → P17 regression.
- Hindi high-impact deployment remains independently production/destructive and authorization-gated; negative deployment wording blocks conflicting plans; unresolved referents clarify.
- Exact-head successful runs: Development OS `34812860000`; Contracts `34812859861`; Trust-First Audit `34812859744`; Living Engineering Map `34812859740`; GitHub Identity/Token `34812859825`; Provider Controller Adapter `34812859833`; Remote Permission Governance `34812859951`.
- Coverage is bounded deterministic corpus evidence, not universal language competence or authority.

## Completed — AI State Resolver v2 hardening sequence

- PR #44 — envelope integrity.
- PR #46 — explicit cross-claim contradiction identity/handling.
- PR #49 — downstream P16/P17 independent contradiction recomputation and tamper defense.
- PR #52 — detailed contradiction provenance and downstream detail validation.
- Post-feature durable reconciliations and exact heads/CI are recorded in stage history and session records.
- Closed/stale duplicate PRs remain historical provenance only and are never substituted for merged current source.

## Completed — previous-stage documentation ledger

- `docs/DEVOS-ENGINEERING-STAGE-HISTORY.md` is the durable navigation ledger for P9–P17 and major unnumbered milestones.
- `docs/DEVOS-MASTER-ENGINEERING-MAP.md` is the living architecture/future-flow map.
- `core/evidence-durable-state-reconciliation.md` is the normative contract for PR #54 capability.
- `docs/AI-STATE-RESOLVER-CROSS-CLAIM-CONTRADICTIONS.md` is the resolver contradiction contract.

## Retained platform foundations

- P9 through P17 remain completed architecture stages at their recorded evidence levels.
- P11 remains repository-first recovery/revalidation/cross-AI continuity baseline.
- P12 remains evidence provenance/freshness owner.
- P15 remains language interpretation; P16 planning; P17 readiness/authorization.
- GitHub governed provider capability, readback reconciliation, multi-project isolation, Actionable HOLD, current-source evidence, onboarding, recovery, adaptive verification/self-healing, and trust-first auditing remain retained foundations.

## Current HOLD / limits

- `production_ready = false`.
- Machine evidence and reconciliation records never grant authorization, execution, completion authority, or provider permission.
- Semantic CURRENT/TASKS/roadmap changes require review; commit messages are not semantic truth.
- Uncertain provider mutation is never blindly replayed.
- Parallel AI branches must revalidate against fresh `main` before integration.

## Task-map invariant

`AI A + Account A → repository → AI B + Account B → correct recovery → safe continuation`

The repository, not any AI account/chat/model/vendor memory, carries authoritative project state.
