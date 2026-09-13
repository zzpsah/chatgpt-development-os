# DevOS Tasks

## How to read this file

This file tracks **work state**, not normative law. Durable principles and authorization/security decisions live in `.ai/DECISIONS.md` and the relevant core contracts. Source tree + Git/PR metadata remain authoritative for exact implementation/integration state.

## Normative references — not task records

- **Core documentation law:** **What is not written was never done.** The normative definition lives in `.ai/DECISIONS.md` and core living-state contracts.
- **Core safety invariants:** maintained in `.ai/DECISIONS.md` and the relevant core contracts; they are referenced here for recovery compatibility rather than interleaved with historical task records.

## Active bounded work

### Priority 1 — AI State Resolver v2
- Unnumbered resolver-hardening objective on current `main`.
- Upgrade the existing P0 documentation contract into a deterministic, read-only claim resolver.
- Preserve P12 ownership of execution-evidence normalization and freshness.
- `observed` requires current P12 execution evidence with citable provenance; durable-state grounding is capped at `likely`.
- Propagate unresolved claim identifiers through P16 as `CLARIFY`; P17 rejects a tampered `PLANNED` envelope that still carries unresolved claims.
- Resolver confidence never grants authorization, execution, mutation, or completion.
- Next action: inspect fresh resolver implementation/docs/tests against current `main`, close any remaining v2 gaps, run fresh exact-head CI, and persist closure evidence if the objective is complete.
- No P18/P19 phase is created for this hardening work.

### Priority 2 — repository-wide closure and continuity pass
- After Resolver v2 closes, perform one bounded consistency pass across `.ai/CURRENT-STATE.md`, `.ai/TASKS.md`, `.ai/DECISIONS.md`, the Master Engineering Map, handoff/bootstrap surfaces, and current open PR/CI state.
- The pass is documentation/state consistency work only unless a concrete implementation defect is discovered.
- Do not create a new numbered phase merely to record closure.

### Future evidence gate — live mutation proof, only if explicitly authorized later
- GitHub App authentication, controller-facing live read proof, CI success, and merged provider-adapter code do **not** authorize mutation.
- If a future objective is to prove live mutation, use a disposable repository/branch/file target rather than production state.
- Start with the lowest-impact reversible mutation, require exact scoped authorization, verify expected resource state before dispatch, perform one bounded operation, then require fresh provider readback before claiming completion.
- Uncertain provider outcomes enter HOLD / READBACK_BEFORE_RETRY; never blind-replay a mutation.
- Production/destructive mutation remains outside this evidence step unless separately and explicitly authorized.

## Completed — GitHub Provider Controller Adapter v1

- PR #35 — `Integrate GitHub App with governed DevOS provider adapter` — merged at `d379277af53155a2695c99b0bdf9682f43bb2d05`.
- Final source head before merge: `a7c4aad059c2b1c31d62356a2b42155f7f3accbe`.
- Added the GitHub provider adapter, controller bridge, proven-auth read path, deterministic regressions, documentation, and dedicated CI.
- The bridge requires the existing P17/controller runtime handoff and the existing remote-permission gate; it does not create a second authorization authority.
- Mutation paths require exact capability/target/authorization scope, use state anchors where applicable, and require fresh provider readback before completion.
- Uncertain mutation outcomes produce HOLD / READBACK_BEFORE_RETRY rather than automatic retry.
- Live repository read through the controller-facing adapter path is proven using the GitHub App installation-token authentication path.
- Post-merge `main` verification on `d379277af53155a2695c99b0bdf9682f43bb2d05` passed: Trust-First Audit #179, GitHub Provider Controller Adapter #16, Remote Resource Permission Governance #25, Development OS Contracts #716, and Full Development OS #638.
- No live mutation was performed; `production_ready=false` remains conservative.

## Completed — GitHub Identity & Token Control Plane v1

- PR #32 — `Implement GitHub identity and token control plane v1` — merged at `2f1740930116ab520d40d35aaa6dfcb1786a5595`.
- Final merged source head: `216999bef827c9efbe78a026d06486a4765e9602`.
- Added GitHub App-oriented identity binding, OAuth state freshness/reuse protection, permission-level-aware and repository-scope-aware capability discovery, hosted runtime authentication, deterministic tests, and dedicated CI.
- Live read-only GitHub App Runtime Auth run `34785659043` succeeded against `zzpsah/chatgpt-development-os`; evidence reported `credential_material: NOT_INCLUDED`, `execution: NONE`, and `mutation: NONE`.
- Live authentication/capability proof does **not** authorize or prove live provider mutation, deployment, permission change, or production readiness.
- No raw credentials, OAuth secrets, App private keys, refresh tokens, or JWT signing material are persisted in Git or durable AI state.

## Completed — Plain Project Context and Recovery Guide v1

- Completed on `main`: root guide, core recovery protocol, bootstrap/base-rule integration, deterministic guardrails, and plain-context-first recovery entry.
- It remains an unnumbered portability hardening objective; no P18/P19 phase was created.

## Completed — Actionable HOLD + Scoped Approval + Governed Continuation

- PR #23 — `Integrate actionable holds and scoped approval into governed continuation` — merged at `7c60c3a4a36982ba894e2f30ba9dd98500f98d02`.
- Exact final PR head: `954b094a3832c300d371426d682eac90156cbb04`.
- Exact-head CI passed: Actionable Hold 16 / `34778601254`; Contracts 639 / `34778601256`; Trust-First 102 / `34778601246`; Full DevOS 561 / `34778601273`; Current-Source Evidence 31 / `34778601271`; MCP Repository Create 28 / `34778601263`.
- `continue` reuses approval only when project/workflow/capability/target/impact/freshness/security scope remains valid.
- Scoped approval never replaces P17 or the controller and never grants execution by itself.

## Completed — MCP/App Permission Control Plane + Multi-Project Agent Isolation

- PR #27 — `Integrate MCP/App remote permission control plane` — merged at `2bb8d978113b64ab88d6ba5f8e357fa595162c9c`.
- Provider/API write permission remains technical capability only; it is never DevOS authorization.
- Multi-project isolation keeps state, approval, and provider binding separated per project.

## Completed — Current-Source Evidence Refresh Protocol

- Unnumbered bounded objective merged through PR #24.
- Final source head: `bc400112d0bbaced6ed699a6863bc8dcf91e47c8`.
- Merge commit / verified `main`: `a93f9f435ffab5f81ce070f07a0da694757ab6cb`.
- Adds fresh exact-current-source proof without rewriting historical provenance.

## Earlier completed objectives

- Production E2E Harness — PR #11.
- Failure + Recovery Proof — PR #12.
- Multi-Session / Fresh-AI Continuation Proof — PR #13.
- Controlled Remote Mutation Proof — PR #14.
- Production-Readiness Evidence Matrix & Limitations — PR #16.
- Trust-First audit gap closure / adversarial Security Gate proof — PR #17.
- Foundation Health & State Consistency — PR #18.
- Universal Project Onboarding + Repository Creation — PR #19.
- Cross-Host Recovery Friction & Onboarding Proof — PR #20.
- Recovery Friction → Foundation Health/Doctor Integration — PR #21.
- Host-neutral MCP/App `repository.create` adapter — PR #22.
- Current-Source Evidence Refresh — PR #24.
- MCP/App Permission Control Plane + Multi-Project Agent Isolation — PR #27.
- Actionable HOLD + Scoped Approval + Governed Continuation — PR #23.
- GitHub Identity & Token Control Plane v1 — PR #32.
- GitHub Provider Controller Adapter v1 — PR #35.
- Durable-state/task-map restructuring — PR #36.

## Retained platform foundations

- **P11 Federation & Self-Healing Context** remains the repository-first recovery/revalidation/cross-AI continuity baseline.
- **P12 Operational Intelligence** remains the advisory/runtime-observability and durable recovery substrate used by later governed execution paths.
- P11/P12 are historical completed foundations; later unnumbered objectives must not be re-labeled as new numbered phases.

## Task-map invariant

`AI A + Account A → repository → AI B + Account B → correct recovery → safe continuation`

The repository, not any AI account/chat/model/vendor memory, carries authoritative project state. Normative safety/authorization invariants are intentionally maintained in `.ai/DECISIONS.md` and core contracts rather than duplicated between historical task records.