# Current State

## Snapshot

- Repository: `zzpsah/chatgpt-development-os`.
- Source tree + Git are authoritative for implementation and exact project state; ChatGPT Memory/chat history are supplementary only.
- P11 Federation & Self-Healing Context remains the repository-first recovery/revalidation/cross-AI continuity baseline.
- P12 Operational Intelligence remains the advisory/runtime-observability and durable recovery substrate used by later governed execution paths.
- P9 through P17 are complete on `main` at their stated evidence levels.
- Universal Project Onboarding + Repository Creation, host-neutral MCP/App `repository.create`, Current-Source Evidence Refresh, MCP/App Permission Control Plane + Multi-Project Agent Isolation, and Actionable HOLD + Scoped Approval + Governed Continuation are closed at their stated evidence levels.
- PR #27 merge commit: `2bb8d978113b64ab88d6ba5f8e357fa595162c9c`.
- PR #27 exact-head source: `99a48fea51bd2d9d33860115c0212f7b25ca4ad8`.
- PR #27 exact-head verification passed: Full DevOS 543, Contracts 621, Trust-First 84, MCP Permission Control Plane 3, Remote Resource Permission Governance 4, MCP Repository Create 13, Current-Source Evidence 16.
- PR #23 merge commit: `7c60c3a4a36982ba894e2f30ba9dd98500f98d02`.
- PR #23 exact final source head: `954b094a3832c300d371426d682eac90156cbb04`.
- PR #23 exact-head verification passed: Actionable Hold 16, Contracts 639, Trust-First 102, Full DevOS 561, Current-Source Evidence 31, MCP Repository Create 28.
- No new numbered phase is active or implied by this closure state.

## Core documentation law

> **What is not written was never done.**

For every material AI engineering action, decision, repair, experiment, verification result, evidence change, architecture change, roadmap change, or externally relevant outcome:

`OBSERVE → ACT / CHANGE / DECIDE → VERIFY → DOCUMENT → PERSIST IN GIT`

Completion is `IMPLEMENTED + VERIFIED + DOCUMENTED + DURABLE STATE`. An undocumented material action is unfinished work.

## Canonical governed path

`Human request → P15 interpretation → P16 plan → P17 readiness → Actionable HOLD / Scoped Approval → controller → bounded runtime → verification → persistence → recovery / continuation`

Interpretation, planning, readiness, provider credentials, prior approvals, prior successful runs, recovery checkpoints, continuation packets, and simulated provider evidence never manufacture permission.

## GitHub Identity & Token Control Plane v1 — integration pending PR #33

- Clean-history integration PR: #33, branch `fix/github-identity-token-control-plane-clean`.
- PR #32 reached a fully green, reconciled head but GitHub's PR merge engine reported `mergeable_state: dirty`; PR #33 carries the same final implementation as a clean descendant of current `main` and supersedes #32 as the integration vehicle.
- Exact current PR head is authoritative in Git/PR metadata; this file intentionally does not self-pin the commit that contains itself.
- Added `core/devos-github-identity-token-control-plane.md`, `tools/devos-github-auth.py`, `tools/devos-github-capability-discovery.py`, `tools/devos-github-actions-auth.py`, deterministic regression suites, dedicated CI, hosted runtime workflow, guides, master-map integration, and durable session provenance.
- OAuth callback handling for interactive adapters is freshness-bounded, one-time, constant-time compared, and fail-closed for stale/reused/mismatched state.
- Provider capability discovery is permission-level-aware and repository-scope-aware; `read` cannot satisfy required `write`, and out-of-scope targets cannot become `AVAILABLE`.
- Capability evidence remains `authorization: UNCHANGED`, `execution: NONE`, `mutation: NONE`, and `credential_material: NOT_INCLUDED`.
- Dedicated auth/control-plane CI runs on PRs and relevant pushes to `main`.

## Live GitHub App read-only proof

- Live GitHub App Runtime Auth run 6 / `34785659043` completed successfully on the equivalent verified final PR #32 tree.
- It used masked GitHub Actions secrets, created a GitHub App installation-token authentication context, resolved installation account `zzpsah` and installation ID `161468193`, and read `zzpsah/chatgpt-development-os` successfully.
- Runtime output reported `status: PASS`, `authentication: github_app_installation_token`, `credential_material: NOT_INCLUDED`, `execution: NONE`, and `mutation: NONE`.
- No raw App private key, token, refresh token, JWT signing material, or other credential material was emitted in the inspected workflow log.
- This is live **read-only provider authentication/capability proof**, not live provider mutation proof and not blanket DevOS authorization.

## External GitHub App activation

- GitHub App **DevOS GitHub** is configured for the repository-side hosted runtime.
- App installation and GitHub Actions secret configuration have now been corroborated by the successful live read-only runtime proof above.
- Browser OAuth callback configuration is not required for the GitHub-hosted Actions runtime; a future interactive web/OAuth adapter must maintain pending/consumed state outside Git and use the checked-in freshness/reuse checks.

## AI State Resolver v2

- An unnumbered resolver-hardening objective upgrades the existing P0 contract with a deterministic read-only claim resolver while preserving P12 and P17 authority boundaries.
- `observed` requires current P12 execution evidence with citable provenance; durable-state wording cannot self-upgrade a claim.
- Durable-state claims are capped at `likely`; execution-evidence claims inherit P12 freshness and are not normalized again.
- Resolver documentation aligns v1 terminology, v2 grounding rules, P12 ownership, output semantics, and P15→P16→P17 continuation behavior.
- The resolver can only cause a plan/readiness HOLD through named unresolved claims; it never grants authority.

## Plain Project Context and Recovery Guide v1

- `DEVOS-PROJECT-CONTEXT.md` provides host-neutral repository context for fresh external AI chats.
- It is optional/revocable, preserves host policy, requires unavailable-context reporting, and flags instructions that seek to bypass safety, authorization, verification, or host policy.
- It is a core bootstrap requirement before material diagnosis/repair.

## MCP/App Permission Control Plane — CLOSED AT CURRENT EVIDENCE LEVEL

Governed capabilities remain distinct: `repository.create`, `repository.delete`, `branch.create`, `branch.update`, `branch.force_update`, and `branch.delete`.

## Actionable HOLD + Scoped Approval — CLOSED AT CURRENT EVIDENCE LEVEL

- Scoped approval never replaces P17/controller authorization.
- `continue` may reuse approval only when project/workflow/capability/target/impact/freshness/security scope remains valid.
- Stale repository state, changed target/capability, impact escalation, or changed Security Gate requires fresh evaluation.

## Multi-project agent isolation

`Project A state != Project B state`

`Project A approval != Project B approval`

`Project A credentials/provider binding != Project B credentials/provider binding`

## Provider credentials / token boundary

Provider/API tokens are technical capabilities only. They are never DevOS authorization and must never be copied into `.ai/`, MCP arguments, logs, generated evidence, or model output.

## Production-readiness boundary

- `production_ready = false`.
- Live read-only GitHub App authentication is now proven for the repository runtime, but destructive/write provider mutation remains unproven.
- No live repository deletion, branch deletion, force update, production mutation, credential mutation, or permission mutation was performed for this objective.
- Provider response is attempt evidence, not completion proof.
- Uncertain mutation is not blindly replayed.
- Historical evidence remains pinned and is never silently rewritten.

## Universal portability invariant

`AI A + Account A → repository → AI B + Account B → correct state recovery → safe continuation`

No private AI memory is authoritative project state.

## Recovery precedence

1. Current source tree + Git.
2. Explicit requirements/decisions.
3. `.ai/CURRENT-STATE.md`, `.ai/TASKS.md`, and semantic `.ai` state.
4. `.ai/SESSIONS/` provenance.
5. Generated indexes as navigation/evidence only.
6. ChatGPT Memory/chat history as supplementary context only.

## Stable handoff

Stable AI discovery path: `docs/handoff/README.md`.
Master architecture: `docs/DEVOS-MASTER-ENGINEERING-MAP.md`.
Normative living-state contract: `core/devos-living-state-and-evolution.md`.
GitHub authentication/control-plane guide: `docs/DEVOS-GITHUB-IDENTITY-AND-TOKEN-CONTROL-PLANE.md`.
GitHub-hosted runtime guide: `docs/DEVOS-GITHUB-HOSTED-RUNTIME.md`.
Historical evidence snapshots remain dated and do not auto-refresh when source advances. Exact implementation remains authoritative in Git history.

## Next bounded direction

If PR #33 is open, require fresh exact-head CI and a clean mergeability race check. If merged, inspect fresh push CI on the merge commit and close PR #32 as superseded. Do not infer destructive/write-provider proof or production readiness from read-only authentication evidence. Do not create P18/P19 merely for bookkeeping.
