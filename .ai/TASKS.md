# DevOS Tasks

## Core safety invariants

- **What is not written was never done.**
- `PLAN != EXECUTION`
- `READY != EXECUTION`
- `INTERPRETATION != AUTHORIZATION`
- `DOCUMENTATION != AUTHORIZATION`
- `SIMULATED EVIDENCE != LIVE PROVIDER PROOF`
- `CHAT MEMORY != SOURCE OF TRUTH`

## Active / next bounded objective

### GitHub App live read-only verification

- Repository-side GitHub Identity & Token Control Plane v1 is merged on `main` through PR #32. Its code, contracts, deterministic tests, and CI workflow are closed at repository evidence level.
- The active evidence gate is a **read-only live GitHub App runtime verification**: authenticate from GitHub Actions, resolve the installed App for `zzpsah/chatgpt-development-os`, mint a short-lived installation token, and read back repository identity.
- Required evidence: fresh workflow result, non-secret identity/capability output, and explicit verification that no mutation occurred.
- User-reported App registration, installation, and Actions secrets are setup claims only until the workflow supplies live provider evidence.
- Do not expose secrets or add credential material to Git, `.ai`, logs, artifacts, or model output.

## Current HOLD / limits

- `production_ready = false`.
- `live_provider_proven = false` until the read-only workflow succeeds with fresh evidence.
- Browser OAuth callback/token exchange is out of scope for the GitHub-hosted runtime path.
- No P18/P19 phase is created merely for bookkeeping.

## Closed current foundations

- **AI State Resolver v2** — merged on `main`; deterministic grounding, P16/P17 propagation, and continuation-path regressions are implemented. Durable-state grounding is capped at `likely`; only current P12 execution evidence can remain `observed`.
- **Plain Project Context and Recovery Guide v1** — merged on `main`; the guide is the default fresh-session entry, and stance codes are optional shorthand after orientation.
- **GitHub Identity & Token Control Plane v1 repository slice** — merged through PR #32; see `core/devos-github-identity-token-control-plane.md`, `docs/DEVOS-GITHUB-IDENTITY-AND-TOKEN-CONTROL-PLANE.md`, and `docs/DEVOS-GITHUB-HOSTED-RUNTIME.md`.

## Historical evidence index

Detailed historical records remain in Git history, dated `.ai/SESSIONS/` files, `docs/handoff/`, and the master engineering map. They are not active tasks.

- P9 Development Task Controller; P10 Context Continuity & Recovery; P11 Federation & Self-Healing Context; P12 Operational Intelligence; P13 Autonomous Development Orchestration; P14 Adaptive Verification & Self-Healing; P15 Human Language Interpretation; P16 Semantic Goal-to-Plan Compiler; P17 Step Readiness & Authorization Orchestrator.
- Production E2E (PR #11), Failure + Recovery (PR #12), Multi-Session / Fresh-AI (PR #13), Controlled Remote Mutation (PR #14), Production-Readiness Evidence (PR #16), Trust-First Audit (PR #17), Foundation Health (PR #18), Onboarding (PR #19), Recovery Friction (PR #20/#21), repository.create (PR #22), Actionable HOLD (PR #23), Current-Source Evidence (PR #24), and MCP/App Permission Control Plane (PR #27).

## Permanent task boundaries

- `CI PASS != AUTHORIZATION`
- `OLD APPROVAL != NEW APPROVAL` when scope, freshness, or security changes
- `RECOVERY != AUTOMATIC MUTATION REPLAY`

For durable principles and authorization decisions, use `.ai/DECISIONS.md` and the relevant core contracts. This file is limited to active work, current holds, and an index of closed evidence.
