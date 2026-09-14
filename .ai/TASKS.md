# DevOS Tasks

## How to read this file

This file tracks **work state**, not normative law. Durable principles and authorization/security decisions live in `.ai/DECISIONS.md` and the relevant core contracts. Source tree + Git/PR metadata remain authoritative for exact implementation/integration state.

## Normative references — not task records

- **Core documentation law:** **What is not written was never done.** The normative definition lives in `.ai/DECISIONS.md` and core living-state contracts.
- **Core safety invariants:** maintained in `.ai/DECISIONS.md` and the relevant core contracts; they are referenced here for recovery compatibility rather than interleaved with historical task records.

## Active bounded work

- No numbered phase or resolver implementation objective is active at this reconciliation checkpoint.
- AI State Resolver v2 envelope-integrity hardening is completed and merged through PR #44.
- Any next resolver work must be promoted as a separate bounded objective from fresh `main` evidence.

### Next bounded integration/cleanup work

- Treat GitHub Identity & Token Control Plane v1 as merged through PR #32, not as an open implementation objective.
- Treat GitHub mutation readback reconciliation as merged through PR #42, not as active work.
- Treat AI State Resolver v2 envelope-integrity hardening as merged through PR #44, not as active work.
- PRs #33 and #34 are obsolete replacement PRs and have been closed.
- Continue only after inspecting fresh `main`, open PRs, CI, and durable state.
- Resolver cross-claim semantic contradiction remains out of current v2 scope unless explicitly promoted as a new bounded objective with a stable fact identity and deterministic contradiction policy.
- Do not create P18/P19 merely for bookkeeping.

## Completed — AI State Resolver v2 envelope-integrity hardening

- PR #44 — `Harden AI State Resolver v2 envelope integrity` — merged at `a4a3413bb27802ef38a698550807e8fb0102f839`.
- Exact final PR head: `71d93755e171da5e83e62b00baa4680a0e929f5e`.
- Resolver now returns `NEEDS_EVIDENCE` whenever any claim resolves to `unknown`, including malformed unknown claims without usable IDs.
- Durable-state revalidation reasons remain explicit for already-`likely` claims.
- P16 validates resolver protocol/status/authority/execution/mutation/confidence/unresolved consistency before planning and retains full validated resolver provenance unchanged.
- P17 independently revalidates the preserved resolver envelope and fails closed on hidden uncertainty or changed resolver safety invariants.
- Exact final-head CI passed all triggered gates: Contracts `34806650522`; Full DevOS `34806650407`; Current-Source `34806650590`; Trust-First `34806650421`; MCP Repository Create `34806650443`; Actionable Hold `34806650548`; P13 External Managed Project `34806650599`.
- No authority, authorization, execution, provider mutation, production mutation, or production-readiness upgrade was introduced.

## Completed — GitHub Identity & Token Control Plane v1

- PR #32 — `Implement GitHub identity and token control plane v1` — merged at `2f1740930116ab520d40d35aaa6dfcb1786a5595`.
- Final merged source head: `216999bef827c9efbe78a026d06486a4765e9602`.
- Added `tools/devos-github-auth.py` with GitHub App-oriented identity binding, OAuth transaction creation, constant-time state comparison, one-time/fresh callback validation, expiry handling, and secret fingerprinting.
- Added `tools/devos-github-capability-discovery.py` with fail-closed provider-permission → DevOS-capability evaluation.
- Capability mappings are adapter-supplied and permission-level-aware; `read` cannot satisfy required `write`.
- Existing-repository capabilities require an explicit target repository within provider-reported repository scope before `AVAILABLE` can be returned.
- Added `tools/devos-github-actions-auth.py` for GitHub App JWT + installation-token authentication from GitHub Actions.
- Added deterministic regression coverage and dedicated CI for auth, capability discovery, and hosted runtime behavior.
- Added `.github/workflows/devos-github-app-runtime.yml` as a read-only live provider-authentication verification workflow.
- Live read-only GitHub App Runtime Auth run `34785659043` succeeded against `zzpsah/chatgpt-development-os`; evidence reported `credential_material: NOT_INCLUDED`, `execution: NONE`, and `mutation: NONE`.
- Live authentication/capability proof does **not** authorize deployment, permission change, destructive mutation, or production readiness.
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
- No live/destructive/provider/production mutation was performed.

## Completed — MCP/App Permission Control Plane + Multi-Project Agent Isolation

- PR #27 — `Integrate MCP/App remote permission control plane` — merged at `2bb8d978113b64ab88d6ba5f8e357fa595162c9c`.
- Exact PR head verified before merge: `99a48fea51bd2d9d33860115c0212f7b25ca4ad8`.
- Exact-head verification passed: Full DevOS 543, Contracts 621, Trust-First 84, MCP Permission Control Plane 3, Remote Resource Permission Governance 4, MCP Repository Create 13, Current-Source Evidence 16.
- Governs `repository.create`, `repository.delete`, `branch.create`, `branch.update`, `branch.force_update`, and `branch.delete` with exact project/repository/resource/workflow/impact/freshness scope.
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
- GitHub mutation readback reconciliation hardening — PR #42.
- AI State Resolver v2 envelope-integrity hardening — PR #44.

## Retained platform foundations

- **P11 Federation & Self-Healing Context** remains the repository-first recovery/revalidation/cross-AI continuity baseline.
- **P12 Operational Intelligence** remains the advisory/runtime-observability and durable recovery substrate used by later governed execution paths.
- P11/P12 are historical completed foundations; later unnumbered objectives must not be re-labeled as new numbered phases.

## Task-map invariant

`AI A + Account A → repository → AI B + Account B → correct recovery → safe continuation`

The repository, not any AI account/chat/model/vendor memory, carries authoritative project state. Normative safety/authorization invariants are intentionally maintained in `.ai/DECISIONS.md` and core contracts rather than duplicated between historical task records.