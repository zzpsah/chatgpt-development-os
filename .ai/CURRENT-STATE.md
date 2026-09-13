# Current State

## Snapshot

- Repository: `zzpsah/chatgpt-development-os`.
- Source tree + Git/PR metadata are authoritative for exact implementation/integration state; ChatGPT Memory/chat history are supplementary only.
- Current verified `main` checkpoint at this update: `d379277af53155a2695c99b0bdf9682f43bb2d05`.
- P9 through P17 are complete on `main` at their stated evidence levels.
- P11 Federation & Self-Healing Context remains the repository-first recovery/revalidation/cross-AI continuity baseline.
- P12 Operational Intelligence remains the advisory/runtime-observability and durable recovery substrate used by later governed execution paths.
- GitHub Identity & Token Control Plane v1 and GitHub Provider Controller Adapter v1 are merged on `main` at their stated evidence levels.
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
- Live **read-only GitHub access through the normal controller-facing provider adapter** is also proven.
- Live provider **mutation** is not proven or authorized by either read-only evidence stream.
- No live repository deletion, branch deletion, force update, production mutation, credential mutation, or permission mutation was performed for the GitHub auth/provider-adapter objectives.
- Provider response is attempt evidence, not completion proof; successful mutation would require fresh provider readback.
- Uncertain mutation is not blindly replayed and must enter HOLD / READBACK_BEFORE_RETRY.
- Historical evidence remains pinned and is never silently rewritten.

## Active bounded work

### Priority 1 — AI State Resolver v2

- Unnumbered resolver-hardening objective on current `main`.
- Upgrades the existing P0 contract with a deterministic read-only claim resolver while preserving P12 and P17 authority boundaries.
- `observed` requires current P12 execution evidence with citable provenance; durable-state wording cannot self-upgrade a claim.
- Durable-state claims are capped at `likely`; recovery/handoff boundaries and relevant changed paths remain explicit revalidation reasons.
- Execution-evidence claims inherit P12 freshness and are not normalized again.
- Unresolved claims propagate to P16 as `CLARIFY`; P17 rejects a tampered `PLANNED` envelope that still carries unresolved claim IDs.
- Resolver confidence never grants authorization, execution, mutation, or completion.
- Next action: inspect the current implementation/docs/tests on fresh `main`, close any remaining v2 gaps, run exact-head CI, and persist closure evidence if the objective is complete.

### Priority 2 — repository-wide closure and continuity pass

- After Resolver v2 closes, perform one bounded consistency pass across durable `.ai` state, Master Engineering Map, handoff/bootstrap surfaces, open PR state, and current CI.
- Treat this as closure/continuity work unless a concrete implementation defect is discovered.
- Do not create P18/P19 merely for bookkeeping.

### Future evidence gate — live mutation proof

- Not active by default.
- Authentication, read-only proof, merged adapter code, CI success, or provider capability never substitute for exact mutation authorization.
- If explicitly requested later, use a disposable/sandbox target and the lowest-impact reversible mutation first.
- Require exact authorization, expected resource state/sha where applicable, one bounded provider operation, and fresh provider readback before completion.
- Any uncertain outcome enters HOLD / READBACK_BEFORE_RETRY; never blind-replay a mutation.
- Production/destructive targets remain outside this evidence step unless separately and explicitly authorized.

## Current verified capability state

### GitHub Identity & Token Control Plane v1 — merged

- PR #32 — `Implement GitHub identity and token control plane v1` — merged at `2f1740930116ab520d40d35aaa6dfcb1786a5595`.
- Final merged source head: `216999bef827c9efbe78a026d06486a4765e9602`.
- OAuth callback state is freshness- and reuse-checked; capability discovery is permission-level-aware and repository-scope-aware.
- Credentials remain external; no raw App private key/token/refresh token/JWT signing material is persisted in durable project state.

### Live GitHub App runtime evidence

- DevOS GitHub App Runtime Auth run `34785659043` succeeded against `zzpsah/chatgpt-development-os`.
- The runtime authenticated via a GitHub App installation token, resolved the repository installation, and performed read-only repository verification.
- Evidence reported `status: PASS`, `credential_material: NOT_INCLUDED`, `execution: NONE`, and `mutation: NONE`.
- This proves live provider authentication/capability for the read-only runtime only.

### GitHub Provider Controller Adapter v1 — merged

- PR #35 — `Integrate GitHub App with governed DevOS provider adapter` — merged at `d379277af53155a2695c99b0bdf9682f43bb2d05`.
- Final source head before merge: `a7c4aad059c2b1c31d62356a2b42155f7f3accbe`.
- The controller bridge reuses the existing P17/runtime handoff and remote-permission control plane; it does not create authorization.
- Supported provider operations are bounded; unsupported generic endpoints fail closed.
- Mutation paths retain capability/target scope, expected state anchors where applicable, uncertain-result HOLD behavior, and fresh readback requirements.
- Live repository read through the controller-facing adapter path succeeded using the proven GitHub App authentication helper.
- No live mutation was performed.
- Fresh post-merge verification on `d379277af53155a2695c99b0bdf9682f43bb2d05` passed: Trust-First Audit #179, GitHub Provider Controller Adapter #16, Remote Resource Permission Governance #25, Development OS Contracts #716, and Full Development OS #638.

### Plain Project Context and Recovery Guide v1

- `DEVOS-PROJECT-CONTEXT.md` is the plain, host-neutral first-contact recovery context for fresh external AI chats.
- It preserves host policy and makes unavailable context explicit rather than encouraging inference or bypass.

## External GitHub App configuration record

- GitHub App **DevOS GitHub** is recorded under `@zzpsah`.
- Recorded App ID: `4934164`.
- Recorded Client ID: `Iv23lisO9Up8GMiMXqX9`.
- The App is recorded as installed on `zzpsah/chatgpt-development-os` with repository-scoped installation.
- Repository Actions secrets `DEVOS_GITHUB_APP_ID` and `DEVOS_GITHUB_APP_PRIVATE_KEY` are configured externally; actual secret values are not persisted in Git, `.ai`, logs, evidence, or model output.

## Completed milestone evidence

- PR #23 merge commit: `7c60c3a4a36982ba894e2f30ba9dd98500f98d02` — Actionable HOLD + Scoped Approval + Governed Continuation.
- PR #24 merge commit / verified `main`: `a93f9f435ffab5f81ce070f07a0da694757ab6cb` — Current-Source Evidence Refresh.
- PR #27 merge commit: `2bb8d978113b64ab88d6ba5f8e357fa595162c9c` — MCP/App Permission Control Plane + Multi-Project Agent Isolation.
- PR #32 merge commit: `2f1740930116ab520d40d35aaa6dfcb1786a5595` — GitHub Identity & Token Control Plane v1.
- PR #36 merge commit: `867f9b3f0e74137691d92b7746b7fe3398403505` — durable-state/task-map restructuring.
- PR #35 merge commit: `d379277af53155a2695c99b0bdf9682f43bb2d05` — GitHub Provider Controller Adapter v1.

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
- GitHub controller-adapter guide: `docs/DEVOS-GITHUB-CONTROLLER-ADAPTER.md`.

## Next bounded direction

1. Finish/audit AI State Resolver v2 from fresh `main` evidence and close only the remaining real gaps.
2. Run fresh exact-head verification and persist Resolver v2 closure evidence if complete.
3. Perform one bounded repository-wide continuity/closure pass after Resolver v2.
4. Keep `production_ready=false` unless materially stronger production evidence exists.
5. Treat live mutation proof as a separate optional future objective requiring explicit authorization and a disposable/sandbox target.
6. Do not create P18/P19 merely for bookkeeping; Resolver cross-claim semantic contradiction remains outside v2 scope unless promoted by a future bounded objective.