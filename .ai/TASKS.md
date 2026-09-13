# DevOS Tasks

## How to read this file

This file tracks **work state**, not normative law. Durable principles and authorization/security decisions live in `.ai/DECISIONS.md` and the relevant core contracts. Source tree + Git/PR metadata remain authoritative for exact implementation/integration state.

## Active bounded work

### AI State Resolver v2
- Unnumbered resolver-hardening objective on current `main`.
- Upgrade the existing P0 documentation contract into a deterministic, read-only claim resolver.
- Preserve P12 ownership of execution-evidence normalization and freshness.
- `observed` requires current P12 execution evidence with citable provenance; durable-state grounding is capped at `likely`.
- Propagate unresolved claim identifiers through P16 as `CLARIFY`; P17 rejects a tampered `PLANNED` envelope that still carries unresolved claims.
- Resolver confidence never grants authorization, execution, mutation, or completion.
- No P18/P19 phase is created for this hardening work.

### Next bounded integration/cleanup work
- Treat GitHub Identity & Token Control Plane v1 as merged through PR #32, not as an open implementation objective.
- Close obsolete replacement PRs #33 and #34; they were created while #32 appeared unmergeable but are no longer integration vehicles.
- Continue only after inspecting fresh `main`, open PRs, CI, and durable state.

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

## Retained platform foundations

- **P11 Federation & Self-Healing Context** remains the repository-first recovery/revalidation/cross-AI continuity baseline.
- **P12 Operational Intelligence** remains the advisory/runtime-observability and durable recovery substrate used by later governed execution paths.
- P11/P12 are historical completed foundations; later unnumbered objectives must not be re-labeled as new numbered phases.

## Task-map invariant

`AI A + Account A → repository → AI B + Account B → correct recovery → safe continuation`

The repository, not any AI account/chat/model/vendor memory, carries authoritative project state. Normative safety/authorization invariants are intentionally maintained in `.ai/DECISIONS.md` and core contracts rather than duplicated between historical task records.