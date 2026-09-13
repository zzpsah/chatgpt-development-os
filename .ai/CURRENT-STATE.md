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

## MCP/App Permission Control Plane — CLOSED AT CURRENT EVIDENCE LEVEL

Purpose: connect the host-neutral MCP/App boundary to provider-independent remote-resource permission governance and multi-project agent isolation.

Governed capabilities remain distinct: `repository.create`, `repository.delete`, `branch.create`, `branch.update`, `branch.force_update`, and `branch.delete`.

## Actionable HOLD + Scoped Approval — CLOSED AT CURRENT EVIDENCE LEVEL

- Scoped approval never replaces P17/controller authorization.
- `continue` may reuse approval only when project/workflow/capability/target/impact/freshness/security scope remains valid.
- Stale repository state, changed target/capability, impact escalation, or changed Security Gate requires fresh evaluation.
- Every actionable HOLD should explain status, reason, next action, consequence/impact, required evidence/approval, and valid next choices.

## Multi-project agent isolation

A long-lived DevOS agent may manage multiple projects concurrently, but:

`Project A state != Project B state`

`Project A approval != Project B approval`

`Project A credentials/provider binding != Project B credentials/provider binding`

Approval cannot move between repositories, branches, capabilities, or workflows. A new/high-impact/out-of-scope action becomes an actionable HOLD requiring fresh approval.

## Provider credentials / token boundary

Provider/API tokens are technical capabilities only. They are never DevOS authorization and must never be copied into `.ai/`, MCP arguments, logs, generated evidence, or model output.

## Production-readiness boundary

- `production_ready = false`.
- `live_provider_proven = false`.
- Controlled remote mutation remains provider-simulated / contract-level evidence.
- No live repository deletion, branch deletion, force update, production mutation, credential mutation, or permission mutation was performed for PR #27 or PR #23.
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
Historical evidence snapshots remain dated and do not auto-refresh when source advances. Exact implementation remains authoritative in Git history.

## Next bounded direction

Do not create P18/P19 merely for bookkeeping. Continue with consolidation/evidence-hardening and the next repository-supported bounded objective only after inspecting current `main`, open PRs, CI, and durable task/decision/state records. Any material next action must update the affected durable records before completion.

## Plain Project Context and Recovery Guide v1

- A new unnumbered bounded objective adds `DEVOS-PROJECT-CONTEXT.md` and a host-neutral recovery protocol for fresh external AI chats.
- The guide presents DevOS as ordinary repository context, never as authority over a host's policies, permissions, tools, or safety rules.
- It requires honest unavailable-context reporting and does not claim universal live compatibility.

The Plain Project Context and Recovery Guide is now a core bootstrap requirement: `core/ai-bootstrap-protocol.md` routes fresh chats through it before durable-state recovery, and `core/devos-base-operating-rule.md` requires it before material diagnosis/repair.
