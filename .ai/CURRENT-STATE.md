# Current State

## Snapshot

- Repository: `zzpsah/chatgpt-development-os`.
- Source tree + Git/PR metadata are authoritative for exact implementation/integration state; ChatGPT Memory/chat history are supplementary only.
- P9 through P17 are complete on `main` at their stated evidence levels.
- P11 Federation & Self-Healing Context remains the repository-first recovery/revalidation/cross-AI continuity baseline.
- P12 Operational Intelligence remains the advisory/runtime-observability and durable recovery substrate used by later governed execution paths.
- Universal Project Onboarding + Repository Creation, host-neutral MCP/App `repository.create`, Current-Source Evidence Refresh, MCP/App Permission Control Plane + Multi-Project Agent Isolation, Actionable HOLD + Scoped Approval + Governed Continuation, and GitHub Identity & Token Control Plane v1 are closed at their stated evidence levels.
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
- Create/update initially exhibited a short post-write HTTP 404 readback race. The adapter hardening branch adds bounded **readback-only** retries (1s, 2s, 4s) without replaying the mutation. Exhausted reconciliation remains `HOLD / READBACK_REQUIRED`.
- No live repository deletion, branch deletion, force update, production mutation, credential mutation, or permission mutation was performed for this GitHub integration objective.
- Provider response is attempt evidence; completion still requires fresh provider readback.
- Uncertain mutation is not blindly replayed.
- Historical evidence remains pinned and is never silently rewritten.

## Active bounded work

### AI State Resolver v2

- Unnumbered resolver-hardening objective on current `main`.
- Upgrades the existing P0 contract with a deterministic read-only claim resolver while preserving P12 and P17 authority boundaries.
- `observed` requires current P12 execution evidence with citable provenance; durable-state wording cannot self-upgrade a claim.
- Durable-state claims are capped at `likely`; recovery/handoff boundaries and relevant changed paths remain explicit revalidation reasons.
- Execution-evidence claims inherit P12 freshness and are not normalized again.
- Unresolved claims propagate to P16 as `CLARIFY`; P17 rejects a tampered `PLANNED` envelope that still carries unresolved claim IDs.
- Resolver confidence never grants authorization, execution, mutation, or completion.

## Current verified capability state

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
- PR #42 is the current hardening PR for bounded post-mutation readback reconciliation; it is intentionally not merged automatically.

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

- Finish PR #42 verification/review of the GitHub adapter readback reconciliation hardening; do not merge without explicit authorization.
- Continue AI State Resolver v2 hardening only from fresh repository evidence after the current bounded GitHub adapter objective is closed.
- PRs #33 and #34 are closed obsolete replacement branches; PR #32 is the authoritative merged integration history.
- Do not create P18/P19 merely for bookkeeping.
- Resolver cross-claim semantic contradiction remains explicitly out of v2 scope unless promoted by a future bounded objective.
