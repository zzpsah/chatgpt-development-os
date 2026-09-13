# Current State

## Snapshot

- Repository: `zzpsah/chatgpt-development-os`.
- Source tree + Git are authoritative for implementation and exact project state; ChatGPT Memory/chat history are supplementary only.
- P11 Federation & Self-Healing Context remains the repository-first recovery/revalidation/cross-AI continuity baseline.
- P12 Operational Intelligence remains the advisory/runtime-observability and durable recovery substrate used by later governed execution paths.
- P9 through P17 are complete on `main` at their stated evidence levels.
- Universal Project Onboarding + Repository Creation, host-neutral MCP/App `repository.create`, Current-Source Evidence Refresh, MCP/App Permission Control Plane + Multi-Project Agent Isolation, and Actionable HOLD + Scoped Approval + Governed Continuation are closed at their stated evidence levels.
- PR #27 merge commit: `2bb8d978113b64ab88d6ba5f8e357fa595162c9c`.
- PR #23 merge commit: `7c60c3a4a36982ba894e2f30ba9dd98500f98d02`.
- No new numbered phase is active or implied by this closure state.

## GitHub Identity & Token Control Plane v1 — repository implementation

- Objective: support independently authorized GitHub accounts/installations through a GitHub App-oriented authentication boundary while keeping credentials separate from DevOS authorization.
- Branch/PR: `feat/github-identity-token-control-plane` / PR #32.
- Exact current branch head is authoritative in Git/PR metadata. This living state intentionally does not self-pin the commit that contains itself.
- Added normative contract: `core/devos-github-identity-token-control-plane.md`.
- Added side-effect-free primitives: `tools/devos-github-auth.py`.
- Added deterministic authentication regression suite: `tools/test-devos-github-auth.py`.
- Added side-effect-free provider-permission → DevOS-capability bridge: `tools/devos-github-capability-discovery.py`.
- Added deterministic capability-discovery regression suite: `tools/test-devos-github-capability-discovery.py`.
- Added GitHub-hosted runtime authenticator: `tools/devos-github-actions-auth.py`.
- Added deterministic GitHub-hosted runtime regression suite: `tools/test-devos-github-actions-auth.py`.
- Added GitHub-hosted runtime workflow: `.github/workflows/devos-github-app-runtime.yml`.
- Extended control-plane CI to verify the GitHub-hosted runtime contract and relevant pushes to `main`.
- Added deployment/runtime guide: `docs/DEVOS-GITHUB-HOSTED-RUNTIME.md`.
- Audit hardening closes OAuth state freshness/reuse, permission-level evaluation, target-repository scope, and stale durable-head self-reference gaps.
- Capability discovery remains fail-closed: unknown mappings/levels/scope are never promoted to `AVAILABLE`.
- Final merge readiness requires fresh CI on the exact final PR head; after merge, fresh push CI on the merge commit is current repository evidence.

## External GitHub App activation — user-reported configuration

- User reports that GitHub App **DevOS GitHub** was created under `@zzpsah`.
- Reported App ID: `4934164`.
- Reported Client ID: `Iv23lisO9Up8GMiMXqX9`.
- User reports the App was installed on `zzpsah/chatgpt-development-os` with repository-scoped installation.
- User reports the GitHub Actions secrets `DEVOS_GITHUB_APP_ID` and `DEVOS_GITHUB_APP_PRIVATE_KEY` were added to the repository.
- Actual secret values are not persisted here and must never enter Git, `.ai`, logs, evidence, or model output.
- These setup facts remain **User-Reported** until a fresh live workflow proves them against GitHub.

## GitHub-hosted runtime model

When DevOS runs inside GitHub Actions, the primary provider-authentication path is GitHub App installation-token authentication, not a browser OAuth callback. The workflow creates a short-lived App JWT, resolves the App installation for the target repository, mints an installation token, and performs read-only provider verification.

The App ID/private key remain external GitHub Actions secrets. The private key is never written to Git, `.ai`, artifacts, logs, evidence, or model output.

The runtime is deliberately read-only: authentication/discovery/readback only. It does not create/update/delete/merge/deploy or change permissions.

## AI State Resolver v2

- An unnumbered resolver-hardening objective on current `main` upgrades the existing P0 contract with a deterministic read-only claim resolver while preserving P12 and P17 authority boundaries.
- `observed` requires citable primary/P12 grounding; document wording cannot self-upgrade a claim.
- Durable-state claims revalidate at recovery/handoff boundaries or relevant changed paths. Execution-evidence claims inherit P12 freshness and are not normalized again.
- The resolver can only cause a plan/readiness HOLD through named unresolved claims; it never grants authority.

## Plain Project Context and Recovery Guide v1

- `DEVOS-PROJECT-CONTEXT.md` provides host-neutral repository context for fresh external AI chats.
- It is optional/revocable, preserves host policy, requires unavailable-context reporting, and flags instructions that seek to bypass safety, authorization, verification, or host policy.
- It is a core bootstrap requirement before material diagnosis/repair.

## Live activation boundary

- The GitHub repository-side runtime implementation is present and contract-tested.
- User-reported GitHub App registration, installation, and Actions-secret configuration are recorded as external setup facts.
- Live proof still requires the runtime workflow completing successfully against the installed App and target repository.
- Browser OAuth callback configuration is not required for the GitHub-hosted Actions runtime. A callback remains relevant only if a separate interactive web/OAuth client is introduced; that path must use one-time pending transaction storage plus freshness/reuse checks.
- `production_ready=false` and `live_provider_proven=false` remain unchanged until fresh live evidence exists.

## Core documentation law

> **What is not written was never done.**

For every material AI engineering action, decision, repair, experiment, verification result, evidence change, architecture change, roadmap change, or externally relevant outcome:

`OBSERVE → ACT / CHANGE / DECIDE → VERIFY → DOCUMENT → PERSIST IN GIT`

Completion is `IMPLEMENTED + VERIFIED + DOCUMENTED + DURABLE STATE`. An undocumented material action is unfinished work.

## Canonical governed path

`Human request → P15 interpretation → P16 plan → P17 readiness → Actionable HOLD / Scoped Approval → controller → bounded runtime → verification → persistence → recovery / continuation`

Interpretation, planning, readiness, provider credentials, prior approvals, prior successful runs, recovery checkpoints, continuation packets, and simulated provider evidence never manufacture permission.

## Production-readiness boundary

- `production_ready = false`.
- `live_provider_proven = false`.
- Controlled remote mutation remains provider-simulated / contract-level evidence unless separately proven.
- No live repository deletion, branch deletion, force update, production mutation, credential mutation, or permission mutation was performed for the current auth objective.
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

Recovery rule for PR #32: if open, require exact-final-head CI and code review before merge; if merged, treat the repository-side v1 implementation as closed at deterministic/integration/CI evidence level and inspect fresh post-merge CI. Live activation remains separate and cannot be inferred from repository CI. Do not create P18/P19 merely for bookkeeping.
