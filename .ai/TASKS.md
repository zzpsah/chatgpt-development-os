# DevOS Tasks

## How to read this file

This file tracks **work state**, not normative law. Durable principles and authorization/security decisions live in `.ai/DECISIONS.md` and the relevant core contracts. Source tree + Git/PR metadata remain authoritative for exact implementation/integration state.

## Normative references — not task records

- **Core documentation law:** **What is not written was never done.** The normative definition lives in `.ai/DECISIONS.md` and core living-state contracts.
- **Core safety invariants:** maintained in `.ai/DECISIONS.md` and the relevant core contracts; they are referenced here for recovery compatibility rather than interleaved with historical task records.

## Active bounded work

### Priority 1 — GitHub Provider Controller Adapter v1 / PR #35
- PR #35 — `Integrate GitHub App with governed DevOS provider adapter` — is the current integration priority.
- Purpose: connect the proven GitHub App authentication path to the normal P17/controller/remote-permission governed execution path without creating a new authorization model.
- Current PR head: `a7c4aad059c2b1c31d62356a2b42155f7f3accbe`.
- Current `main` checkpoint at this planning update: `867f9b3f0e74137691d92b7746b7fe3398403505`.
- Git comparison shows PR #35 is **20 commits ahead and 5 commits behind** current `main`; therefore its earlier green exact-head evidence is not sufficient for merge against the current repository state.
- Required next action: reconcile PR #35 with fresh `main` history-safely, preserve the durable-state restructuring and Resolver v2 semantics, re-audit the final diff, and rerun exact-final-head CI including the dedicated adapter workflow, Contracts, Trust-First, Current-Source Evidence, MCP Repository Create, Living Engineering Map where applicable, and Full DevOS.
- Only after the reconciled exact head is green and mergeable should merge authorization be requested/applied.
- The PR has proven live **read-only** GitHub access through the controller-facing adapter path on its earlier head; no live mutation has been performed.
- Any future live mutation proof is a separate objective and requires exact fresh authorization, disposable/sandbox scope, state anchors where applicable, and fresh provider readback. No production/destructive mutation is implied by merging PR #35.

### Priority 2 — AI State Resolver v2
- Unnumbered resolver-hardening objective on current `main`.
- Upgrade the existing P0 documentation contract into a deterministic, read-only claim resolver.
- Preserve P12 ownership of execution-evidence normalization and freshness.
- `observed` requires current P12 execution evidence with citable provenance; durable-state grounding is capped at `likely`.
- Propagate unresolved claim identifiers through P16 as `CLARIFY`; P17 rejects a tampered `PLANNED` envelope that still carries unresolved claims.
- Resolver confidence never grants authorization, execution, mutation, or completion.
- Continue Resolver v2 hardening after PR #35 reconciliation/integration unless a fresh repository review shows a dependency requiring the order to change.
- No P18/P19 phase is created for this hardening work.

### Priority 3 — evidence-gated live mutation proof, only if explicitly authorized later
- Do not treat GitHub App authentication, read-only provider proof, CI success, or merged adapter code as mutation authorization.
- If a future objective is to prove live mutation, use a disposable repository/branch/file target rather than production state.
- Start with the lowest-impact reversible mutation, require exact scoped authorization, verify expected resource state before dispatch, perform one bounded operation, then require fresh provider readback before claiming completion.
- Uncertain provider outcomes enter HOLD / READBACK_BEFORE_RETRY; never blind-replay a mutation.

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