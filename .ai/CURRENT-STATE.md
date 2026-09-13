# Current State

## Snapshot

- Repository: `zzpsah/chatgpt-development-os`.
- Source tree + Git/PR metadata are authoritative for exact implementation/integration state; ChatGPT Memory/chat history are supplementary only.
- Current verified `main` checkpoint at this update: `867f9b3f0e74137691d92b7746b7fe3398403505`.
- P9 through P17 are complete on `main` at their stated evidence levels.
- P11 Federation & Self-Healing Context remains the repository-first recovery/revalidation/cross-AI continuity baseline.
- P12 Operational Intelligence remains the advisory/runtime-observability and durable recovery substrate used by later governed execution paths.
- Universal Project Onboarding + Repository Creation, host-neutral MCP/App `repository.create`, Current-Source Evidence Refresh, MCP/App Permission Control Plane + Multi-Project Agent Isolation, Actionable HOLD + Scoped Approval + Governed Continuation, and GitHub Identity & Token Control Plane v1 are closed at their stated evidence levels.
- PR #35 is the only current open implementation PR and is the next integration priority.
- No new numbered phase is active or implied by the current state.

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
- Live read-only provider access through the controller-facing adapter path has also been proven on PR #35's earlier verified head.
- Live provider **mutation** is not proven or authorized by either form of read-only evidence.
- Controlled remote mutation remains provider-simulated / contract-level evidence unless separately proven through the governed mutation path with fresh readback.
- No live repository deletion, branch deletion, force update, production mutation, credential mutation, or permission mutation was performed for the GitHub auth/provider-adapter objectives.
- Provider response is attempt evidence, not completion proof.
- Uncertain mutation is not blindly replayed.
- Historical evidence remains pinned and is never silently rewritten.

## Active bounded work

### Priority 1 — GitHub Provider Controller Adapter v1 / PR #35

- PR #35 — `Integrate GitHub App with governed DevOS provider adapter` — is open, draft, and mergeable at the time of this update.
- Current PR head: `a7c4aad059c2b1c31d62356a2b42155f7f3accbe`.
- Purpose: connect the proven GitHub App authentication path to the normal P17/controller/remote-permission governed provider path.
- The adapter supports bounded repository/file/branch/PR reads and defines governed mutation operations without creating authorization.
- Deterministic checks and live read-only adapter proof passed on the earlier PR head.
- Fresh comparison against current `main` shows PR #35 is **20 commits ahead and 5 commits behind**; its previous green evidence therefore cannot be treated as final merge evidence.
- Required next action: reconcile PR #35 history-safely onto fresh `main`, preserve the durable-state restructuring and Resolver v2 semantics, re-audit the final diff, rerun exact-final-head CI, and require explicit merge authorization only after the reconciled head is green and mergeable.
- No live mutation should be attempted as part of reconciliation or merge verification.

### Priority 2 — AI State Resolver v2

- Unnumbered resolver-hardening objective on current `main`.
- Upgrades the existing P0 contract with a deterministic read-only claim resolver while preserving P12 and P17 authority boundaries.
- `observed` requires current P12 execution evidence with citable provenance; durable-state wording cannot self-upgrade a claim.
- Durable-state claims are capped at `likely`; recovery/handoff boundaries and relevant changed paths remain explicit revalidation reasons.
- Execution-evidence claims inherit P12 freshness and are not normalized again.
- Unresolved claims propagate to P16 as `CLARIFY`; P17 rejects a tampered `PLANNED` envelope that still carries unresolved claim IDs.
- Resolver confidence never grants authorization, execution, mutation, or completion.
- Continue Resolver v2 hardening after PR #35 integration unless fresh repository evidence shows a dependency requiring the order to change.

### Future evidence gate — live mutation proof

- Not active by default.
- If explicitly requested later, use a disposable/sandbox target and the lowest-impact reversible mutation first.
- Require exact scoped authorization, expected resource state/sha where applicable, one bounded provider operation, and fresh provider readback before completion.
- Any uncertain outcome enters HOLD / READBACK_BEFORE_RETRY; never blind-replay a mutation.
- Production/destructive targets remain outside this evidence step unless separately and explicitly authorized.

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
- This proves live provider authentication/capability for the read-only runtime only; it does not authorize or prove provider mutation or production readiness.

### GitHub provider/controller adapter evidence — PR #35, not yet merged

- Dedicated adapter workflow and companion CI passed on PR head `a7c4aad059c2b1c31d62356a2b42155f7f3accbe`.
- Live repository read through the controller-facing adapter path succeeded using the proven GitHub App authentication helper.
- No live mutation was performed.
- Because PR #35 is currently behind `main`, this evidence is retained as historical branch evidence and must be refreshed after reconciliation before merge.

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
- PR #36 merge commit: `867f9b3f0e74137691d92b7746b7fe3398403505` — durable-state/task-map restructuring.

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

1. Reconcile PR #35 onto fresh `main` without force-pushing or dropping concurrent history.
2. Re-audit provider adapter/controller bridge authorization boundaries, replay/uncertain-result handling, readback requirements, and secret exclusion on the reconciled tree.
3. Run fresh exact-final-head CI and live read-only adapter proof on the reconciled head.
4. If and only if the reconciled PR is green and mergeable, request/apply explicit merge authorization and verify fresh post-merge `main` CI.
5. Resume/close the remaining AI State Resolver v2 hardening objective from fresh `main` evidence.
6. Consider a separate disposable-sandbox live mutation proof only after an explicit new authorization; do not infer it from authentication, CI, or adapter merge success.
7. Do not create P18/P19 merely for bookkeeping; Resolver cross-claim semantic contradiction remains outside v2 scope unless promoted by a future bounded objective.