# DevOS Tasks

## Active
- GitHub Identity & Token Control Plane v1 integration is pending through clean replacement PR #33 on `fix/github-identity-token-control-plane-clean`.
- PR #32 contains the development history and reached a fully green reconciled head, but GitHub's merge engine reported `mergeable_state: dirty`; do not merge or force-update it. PR #33 is the clean descendant of current `main` carrying the same final implementation.
- Repository implementation includes authentication primitives, capability discovery, GitHub-hosted runtime, audit hardening, deterministic tests, dedicated CI, durable state, and master-map integration.
- AI State Resolver v2 is also an active bounded unnumbered hardening objective on current `main`; PR #33 preserves its P12/P16/P17 semantics and latest documentation alignment.
- Plain Project Context and Recovery Guide v1 remains part of bootstrap/recovery.
- No P18/P19 phase is created merely for these objectives.

## Completed — GitHub Identity & Token Control Plane v1 implementation slice
- Added `tools/devos-github-auth.py` with GitHub App-oriented identity binding, OAuth transaction creation, constant-time state comparison, bounded freshness, one-time callback validation, expiry handling, and secret fingerprinting.
- Added `tools/devos-github-capability-discovery.py` with fail-closed provider-permission → DevOS-capability evaluation.
- Capability mappings are adapter-supplied and permission-level-aware; `read` cannot satisfy a required `write` level.
- Existing-repository capabilities require an explicit target repository within provider-reported repository scope before `AVAILABLE` can be returned.
- Added `tools/devos-github-actions-auth.py` for GitHub App JWT + installation-token authentication from GitHub Actions.
- Added deterministic regression coverage for auth, capability discovery, and GitHub-hosted runtime behavior.
- Added `.github/workflows/devos-github-app-runtime.yml` as a read-only provider-authentication verification workflow.
- Added/extended `.github/workflows/verify-github-auth-control-plane.yml` to test repository implementation on PRs and relevant pushes to `main`.
- Added hosted-runtime and identity/token-control-plane guides, master-map integration, and durable session provenance.
- Durable capability evidence remains `authorization: UNCHANGED`, `execution: NONE`, `mutation: NONE`, and `credential_material: NOT_INCLUDED`.
- No raw credentials, OAuth secrets, App private keys, refresh tokens, JWT signing material, destructive provider action, deployment, permission change, or production mutation is introduced by this repository implementation.

## Completed — live read-only GitHub App authentication proof
- DevOS GitHub App Runtime Auth run 6 / `34785659043` succeeded on the equivalent final implementation tree.
- The live run resolved the configured App installation and target repository, used masked Actions secrets, and returned `status: PASS`.
- Evidence reported `authentication: github_app_installation_token`, `credential_material: NOT_INCLUDED`, `execution: NONE`, and `mutation: NONE`.
- This proves live read-only provider authentication/capability for the repository runtime. It does **not** prove destructive/write mutation or production readiness.

## AI State Resolver v2 — active bounded objective
- Upgrade the existing P0 documentation contract into a deterministic, read-only claim resolver.
- Preserve P12 ownership of execution-evidence normalization and freshness.
- Durable-state claims cannot self-upgrade to `observed`; current P12 execution evidence with citable provenance is required.
- Propagate unresolved claim identifiers through P16 as `CLARIFY` and reject any tampered P17 `PLANNED` envelope that carries unresolved claims.
- This is an unnumbered hardening objective; it does not create P18/P19.

## Plain Project Context and Recovery Guide v1
- Completed on `main`: root guide, core recovery protocol, bootstrap/base-rule integration, and deterministic guardrails.
- It remains an unnumbered portability hardening objective; no P18/P19 was created.

## Completed — Actionable HOLD + Scoped Approval + Governed Continuation
- PR #23 — `Integrate actionable holds and scoped approval into governed continuation` — merged at `7c60c3a4a36982ba894e2f30ba9dd98500f98d02`.
- Exact final PR head: `954b094a3832c300d371426d682eac90156cbb04`.
- Exact-head CI passed: Actionable Hold 16 / `34778601254`; Contracts 639 / `34778601256`; Trust-First 102 / `34778601246`; Full DevOS 561 / `34778601273`; Current-Source Evidence 31 / `34778601271`; MCP Repository Create 28 / `34778601263`.
- `continue` reuses approval only when project/workflow/capability/target/impact/freshness/security scope remains valid.
- Missing approval, stale HEAD, changed target/capability, impact escalation, or changed Security Gate produces HOLD/fresh-evaluation behavior.
- Scoped approval never replaces P17 or the controller and never grants execution by itself.
- No live/destructive/provider/production mutation was performed.

## Core documentation law
- **What is not written was never done.**
- Every material AI engineering action, decision, repair, experiment, verification result, evidence change, architecture change, roadmap change, or externally relevant outcome must leave a durable repository record.
- Completion requires `IMPLEMENTED + VERIFIED + DOCUMENTED + DURABLE STATE`.
- Undocumented material work is unfinished work, even when code or CI exists.

## Completed — MCP/App Permission Control Plane + Multi-Project Agent Isolation
- PR #27 — `Integrate MCP/App remote permission control plane` — merged at `2bb8d978113b64ab88d6ba5f8e357fa595162c9c`.
- Exact PR head verified before merge: `99a48fea51bd2d9d33860115c0212f7b25ca4ad8`.
- Exact-head verification passed: Full DevOS 543, Contracts 621, Trust-First 84, MCP Permission Control Plane 3, Remote Resource Permission Governance 4, MCP Repository Create 13, Current-Source Evidence 16.
- The control plane governs `repository.create`, `repository.delete`, `branch.create`, `branch.update`, `branch.force_update`, and `branch.delete` with exact project/repository/resource/workflow/impact/freshness scope.
- Provider/API write permission remains technical capability only; it is never DevOS authorization.
- `FULL APPROVAL` remains scoped, not blanket permission.
- Multi-project isolation keeps state, approval, and provider binding separated per project.
- No live/destructive/production provider mutation was performed for PR #27.

## Current-Source Evidence Refresh Protocol — completed
- Unnumbered bounded objective; merged through PR #24.
- Final source head: `bc400112d0bbaced6ed699a6863bc8dcf91e47c8`.
- Merge commit / verified `main`: `a93f9f435ffab5f81ce070f07a0da694757ab6cb`.
- Final PR evidence and post-merge verification were recorded without rewriting historical provenance.

## Completed recently
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

## Platform foundations retained in the durable task map
- **P11 Federation & Self-Healing Context** remains the repository-first recovery/revalidation/cross-AI continuity baseline.
- **P12 Operational Intelligence** remains the advisory/runtime-observability and durable recovery substrate used by later governed execution paths.
- P11/P12 are historical completed foundations; later unnumbered objectives must not be re-labeled as new numbered phases.

## Universal portability invariant
`AI A + Account A → repository → AI B + Account B → correct recovery → safe continuation`

The repository, not any AI account/chat/model/vendor memory, carries authoritative project state.

## Core safety invariants
- `WHAT IS NOT WRITTEN = NOT DONE`
- `PLAN != EXECUTION`
- `READY != EXECUTION`
- `INTERPRETATION != AUTHORIZATION`
- `DOCUMENTATION != AUTHORIZATION`
- `CI PASS != AUTHORIZATION`
- `OLD APPROVAL != NEW APPROVAL` when scope/freshness/security changes
- `FULL APPROVAL != BLANKET PERMISSION`
- `PROVIDER CREDENTIAL != DEVOS AUTHORIZATION`
- `SIMULATED EVIDENCE != LIVE PROVIDER PROOF`
- `CHAT MEMORY != SOURCE OF TRUTH`
- `PROVIDER RESPONSE != COMPLETION PROOF`
- `RECOVERY != AUTOMATIC MUTATION REPLAY`
- `REPOSITORY DELETE != REPOSITORY CREATE`
- `BRANCH DELETE != BRANCH CREATE`
- `NORMAL BRANCH UPDATE != FORCE UPDATE`
