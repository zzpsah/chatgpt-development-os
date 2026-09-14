# Current State

## Snapshot

- Repository: `zzpsah/chatgpt-development-os`.
- Source tree + Git/PR metadata are authoritative for exact implementation/integration state; ChatGPT Memory/chat history are supplementary only.
- Current verified `main` head at this reconciliation checkpoint: `a4a3413bb27802ef38a698550807e8fb0102f839` (merge of PR #44, AI State Resolver v2 envelope-integrity hardening).
- P9 through P17 are complete on `main` at their stated evidence levels.
- P11 Federation & Self-Healing Context remains the repository-first recovery/revalidation/cross-AI continuity baseline.
- P12 Operational Intelligence remains the advisory/runtime-observability and durable recovery substrate used by later governed execution paths.
- Universal Project Onboarding + Repository Creation, host-neutral MCP/App `repository.create`, Current-Source Evidence Refresh, MCP/App Permission Control Plane + Multi-Project Agent Isolation, Actionable HOLD + Scoped Approval + Governed Continuation, GitHub Identity & Token Control Plane v1, governed GitHub provider/controller adapter integration, GitHub mutation readback reconciliation hardening, and AI State Resolver v2 envelope-integrity hardening are closed at their stated evidence levels.
- No new numbered phase is active or implied by the current closure state.

## Durable principles and boundaries

### Core documentation law

> **What is not written was never done.**

Material engineering actions, decisions, repairs, experiments, verification results, evidence changes, architecture changes, roadmap changes, and externally relevant outcomes must follow:

`OBSERVE → ACT / CHANGE / DECIDE → VERIFY → DOCUMENT → PERSIST IN GIT`

Completion requires `IMPLEMENTED + VERIFIED + DOCUMENTED + DURABLE STATE`.

### Canonical governed path

`Human request → P15 interpretation → P16 plan → P17 readiness → Actionable HOLD / Scoped Approval → controller → bounded runtime → verification → persistence → recovery / continuation`

Interpretation, planning, readiness, provider credentials, prior approvals, prior successful runs, recovery checkpoints, continuation packets, documentation, CI, and simulated provider evidence never manufacture permission.

### Production-readiness boundary

- `production_ready = false`.
- Live **read-only GitHub provider authentication** is proven for the DevOS GitHub App runtime.
- Live **GitHub provider mutation through the governed controller bridge is now proven** on a dedicated isolated test branch/resource using create → update → delete with fresh provider evidence and safe reconciliation.
- The live proof is scoped to the governed adapter/controller path and isolated test resources; it does not imply production readiness, destructive authorization, or permission to mutate arbitrary repositories/resources.
- Create/update initially exhibited a short post-write HTTP 404 readback race. The merged PR #42 hardening adds bounded **readback-only** retries (1s, 2s, 4s) without replaying the mutation. Exhausted reconciliation remains `HOLD / READBACK_REQUIRED`.
- No live repository deletion, branch deletion, force update, production mutation, credential mutation, or permission mutation was performed for this GitHub integration objective.
- Provider response is attempt evidence; completion still requires fresh provider readback.
- Uncertain mutation is not blindly replayed.
- Historical evidence remains pinned and is never silently rewritten.

## Active bounded work

- No numbered phase is active.
- AI State Resolver v2 envelope-integrity hardening is closed through PR #44 and must not be treated as active work.
- Any next resolver objective must begin from fresh `main` evidence and be promoted explicitly as a new bounded objective.

## Current verified capability state

### AI State Resolver v2 envelope-integrity hardening — merged

- PR #44 — `Harden AI State Resolver v2 envelope integrity` — merged at `a4a3413bb27802ef38a698550807e8fb0102f839`.
- Exact final PR head: `71d93755e171da5e83e62b00baa4680a0e929f5e`.
- Resolver status now becomes `NEEDS_EVIDENCE` whenever any resolved claim is `unknown`, including a malformed unknown claim without a usable ID.
- Durable-state recovery/handoff/path revalidation reasons remain visible for claims already supplied as `likely`.
- P16 validates resolver protocol, status, authority, authorization, execution, mutation, claim confidence, weakest confidence, summary counts, and unresolved consistency before planning.
- P16 preserves the full validated resolver provenance unchanged in the plan.
- P17 independently revalidates that preserved resolver provenance and fails closed on hidden unknown claims, inconsistent confidence summaries, or changed authority/execution state.
- Exact final-head verification passed all triggered PR gates: Development OS Contracts `34806650522`, Development OS `34806650407`, Current-Source Evidence `34806650590`, Trust-First Audit `34806650421`, MCP Repository Create `34806650443`, Actionable Hold `34806650548`, and P13 External Managed Project `34806650599`.
- This hardening creates no authority, authorization, execution, mutation, or production-readiness upgrade.

### GitHub Identity & Token Control Plane v1 — merged

- PR #32 — `Implement GitHub identity and token control plane v1` — merged at `2f1740930116ab520d40d35aaa6dfcb1786a5595`.
- Final merged source head: `216999bef827c9efbe78a026d06486a4765e9602`.
- Added normative contract: `core/devos-github-identity-token-control-plane.md`.
- Added `tools/devos-github-auth.py` with one-time/fresh OAuth state validation, identity binding, expiry handling, and secret fingerprinting.
- Added `tools/devos-github-capability-discovery.py` with fail-closed, permission-level-aware, repository-scope-aware capability evaluation.
- Added `tools/devos-github-actions-auth.py` plus deterministic hosted-runtime regression coverage.
- Added `.github/workflows/devos-github-app-runtime.yml` and dedicated control-plane verification CI.
- Audit hardening closed stale/reused OAuth state, permission-level, target-repository scope, and stale durable-head self-reference gaps.
- Capability discovery returns no `AVAILABLE` result from unknown mappings, insufficient permission level, or out-of-scope targets.

### Live GitHub App runtime evidence

- DevOS GitHub App Runtime Auth run `34785659043` succeeded against `zzpsah/chatgpt-development-os` on the verified auth implementation tree.
- The runtime authenticated via a GitHub App installation token, resolved the repository installation, and performed read-only repository verification.
- Reported evidence included `status: PASS`, `credential_material: NOT_INCLUDED`, `execution: NONE`, and `mutation: NONE`.
- The inspected workflow log masked secret values and did not expose the App private key or installation token.
- This proves live provider authentication/capability for the read-only runtime; the separate controller-bridge mutation evidence below proves the governed mutation slice.

### Live GitHub Controller Adapter mutation proof

- The normal controller bridge uses the proven App installation-token provider and the exact P17/runtime-handoff gates.
- Dedicated live test branch/resource sequence established:
  - `file.create`: provider commit `e8235f7864678a27bbf036def806a1624fb66678`, returned content SHA `6b08d07761cdaa4ae07bad6d0820239e022d52f6`; immediate adapter readback returned HTTP 404 and safely held for reconciliation.
  - Reconciliation/update: provider commit `27a3b3cf4f7c8c8511f3c5a8f3283d8a6a883232`, resulting content SHA `349c63f9bacf1efc2a9f5409665803d1e970b201`; immediate readback again returned HTTP 404 and safely held.
  - Delete: provider commit `3f530da3ee1efd4e52baad10fe4e644d4db5d116`; fresh readback returned `ABSENT`, producing `COMPLETE / PROVIDER_MUTATION / FRESH_PROVIDER_READBACK` evidence.
- Temporary live PRs #40 and #41 were closed and not merged.
- This evidence proves the governed live provider mutation path without upgrading `production_ready`.

### GitHub mutation readback reconciliation hardening — merged

- PR #42 — `Harden GitHub mutation readback reconciliation` — merged at `0a3ef4a7386e7f94cfa651eef4af75df66cc5933`.
- Final source head: `aed21d1a3e1f0dd2894144296e5b9c845dfb8521`.
- Adds bounded post-mutation HTTP 404 readback-only reconciliation delays of 1s, 2s, and 4s.
- Never replays the mutation as part of reconciliation.
- Keeps 401/auth, validation, and network uncertainty outside this retry path.
- Preserves fail-safe `HOLD / READBACK_REQUIRED` after exhausted reconciliation.
- Records `readback_attempts` in successful completion evidence and includes deterministic regression coverage.

### Plain Project Context and Recovery Guide v1

- `DEVOS-PROJECT-CONTEXT.md` is the plain, host-neutral first-contact recovery context for fresh external AI chats.
- It is optional/revocable, preserves host policy, requires unavailable-context reporting, and flags instructions that seek to bypass safety, authorization, verification, or host policy.
- Fresh-session bootstrap defaults to the plain Project Context Guide; stance codes are optional after orientation.

## External GitHub App configuration record

- GitHub App **DevOS GitHub** is recorded under `@zzpsah`.
- Recorded App ID: `4934164`.
- Recorded Client ID: `Iv23lisO9Up8GMiMXqX9`.
- The App is recorded as installed on `zzpsah/chatgpt-development-os` with repository-scoped installation.
- Repository Actions secrets `DEVOS_GITHUB_APP_ID` and `DEVOS_GITHUB_APP_PRIVATE_KEY` are configured externally; actual secret values are not persisted in Git, `.ai`, logs, evidence, or model output.
- The live runtime evidence above upgrades the prior setup facts from user-reported-only status to observed read-only authentication evidence for the target repository.

## Completed milestone evidence

- PR #27 merge commit: `2bb8d978113b64ab88d6ba5f8e357fa595162c9c` — MCP/App Permission Control Plane + Multi-Project Agent Isolation.
- PR #23 merge commit: `7c60c3a4a36982ba894e2f30ba9dd98500f98d02` — Actionable HOLD + Scoped Approval + Governed Continuation.
- PR #24 merge commit / verified `main`: `a93f9f435ffab5f81ce070f07a0da694757ab6cb` — Current-Source Evidence Refresh.
- PR #32 merge commit: `2f1740930116ab520d40d35aaa6dfcb1786a5595` — GitHub Identity & Token Control Plane v1.
- PR #35 merge commit: `d379277af53155a2695c99b0bdf9682f43bb2d05` — GitHub provider/controller adapter slice and governed bridge.
- PR #42 merge commit: `0a3ef4a7386e7f94cfa651eef4af75df66cc5933` — bounded GitHub mutation readback reconciliation hardening.
- PR #39 merge checkpoint: `8d7ff1cde34c0e5d324b9a30034bbf5cff178cfc` — DevOS activation handshake, merged after PR #42 without changing controller/provider mutation semantics.
- PR #44 merge commit / current reconciliation checkpoint: `a4a3413bb27802ef38a698550807e8fb0102f839` — AI State Resolver v2 envelope-integrity hardening.

Historical exact-head CI remains pinned in task/session records and must not be rewritten merely because later source advances.

## Recovery and navigation

### Universal portability invariant

`AI A + Account A → repository → AI B + Account B → correct state recovery → safe continuation`

No private AI memory is authoritative project state.

### Recovery precedence

1. Current source tree + Git/PR metadata.
2. Explicit requirements/decisions.
3. `.ai/CURRENT-STATE.md`, `.ai/TASKS.md`, and semantic `.ai` state.
4. `.ai/SESSIONS/` provenance.
5. Generated indexes as navigation/evidence only.
6. ChatGPT Memory/chat history as supplementary context only.

### Stable handoff

- Plain project context: `DEVOS-PROJECT-CONTEXT.md`.
- Stable AI discovery path: `docs/handoff/README.md`.
- Master architecture: `docs/DEVOS-MASTER-ENGINEERING-MAP.md`.
- Normative living-state contract: `core/devos-living-state-and-evolution.md`.
- GitHub authentication/control-plane guide: `docs/DEVOS-GITHUB-IDENTITY-AND-TOKEN-CONTROL-PLANE.md`.
- GitHub-hosted runtime guide: `docs/DEVOS-GITHUB-HOSTED-RUNTIME.md`.
- Historical evidence snapshots remain dated and do not auto-refresh when source advances.

## Next bounded direction

- PR #44 AI State Resolver v2 envelope-integrity hardening is closed and merged; do not treat it as active work.
- Do not create P18/P19 merely for bookkeeping.
- Resolver cross-claim semantic contradiction remains explicitly out of current v2 scope. Promote it only as a separate bounded objective after fresh source inspection defines a stable fact identity, contradiction policy, deterministic behavior, downstream propagation rules, and adversarial regression coverage.
- Until such an objective is explicitly promoted, continuation should recover fresh `main`, inspect open PRs/CI/durable state, and avoid inventing a new active milestone.