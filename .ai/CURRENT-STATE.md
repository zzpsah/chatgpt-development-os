# Current State

## Snapshot

- Repository: `zzpsah/chatgpt-development-os`.
- Source tree + Git are authoritative for implementation and exact project state; ChatGPT Memory/chat history are supplementary only.
- P11 Federation & Self-Healing Context remains the repository-first recovery/revalidation/cross-AI continuity baseline.
- P12 Operational Intelligence remains the advisory/runtime-observability and durable recovery substrate used by later governed execution paths.
- P9 through P17 are complete on `main` at their stated evidence levels.
- Universal Project Onboarding + Repository Creation, host-neutral MCP/App `repository.create`, Current-Source Evidence Refresh, and MCP/App Permission Control Plane + Multi-Project Agent Isolation are closed at their stated evidence levels.
- PR #27 merge commit: `2bb8d978113b64ab88d6ba5f8e357fa595162c9c`.
- PR #27 exact-head source: `99a48fea51bd2d9d33860115c0212f7b25ca4ad8`.
- PR #27 exact-head verification passed: Full DevOS 543, Contracts 621, Trust-First 84, MCP Permission Control Plane 3, Remote Resource Permission Governance 4, MCP Repository Create 13, Current-Source Evidence 16.
- No new numbered phase is active or implied by this closure state.

## Canonical governed path

`Human request → P15 interpretation → P16 plan → P17 readiness → controller → bounded runtime → verification → persistence → recovery / continuation`

Interpretation, planning, readiness, provider credentials, prior approvals, prior successful runs, recovery checkpoints, continuation packets, and simulated provider evidence never manufacture permission.

## MCP/App Permission Control Plane — CLOSED AT CURRENT EVIDENCE LEVEL

Purpose: connect the host-neutral MCP/App boundary to provider-independent remote-resource permission governance and multi-project agent isolation.

Governed capabilities remain distinct: `repository.create`, `repository.delete`, `branch.create`, `branch.update`, `branch.force_update`, and `branch.delete`.

Core control flow:

`AI host → MCP/App adapter → P15 → P16 → P17 → Actionable Hold / Scoped Approval → Remote Permission Control Plane → provider adapter → fresh readback → durable evidence`

The MCP/App adapter is an interface, not an authority. Provider/API write permission is technical capability only and is never DevOS authorization.

Preserved safety boundaries:
- `FULL APPROVAL != BLANKET PERMISSION`
- `PROVIDER CREDENTIAL != DEVOS AUTHORIZATION`
- `REPOSITORY DELETE != REPOSITORY CREATE`
- `BRANCH DELETE != BRANCH CREATE`
- `NORMAL BRANCH UPDATE != FORCE UPDATE`
- `PROVIDER RESPONSE != COMPLETION PROOF`
- `UNCERTAIN MUTATION != AUTOMATIC RETRY`

## Multi-project agent isolation

A long-lived DevOS agent may manage multiple projects concurrently, but:

`Project A state != Project B state`

`Project A approval != Project B approval`

`Project A credentials/provider binding != Project B credentials/provider binding`

Approval cannot move between repositories, branches, capabilities, or workflows. `continue` may reuse an approval only while the exact approved scope and freshness/security conditions remain valid. A new/high-impact/out-of-scope action becomes an actionable HOLD requiring fresh approval.

## Provider credentials / token boundary

Provider/API tokens are technical capabilities only. They are never DevOS authorization and must never be copied into `.ai/`, MCP arguments, logs, generated evidence, or model output.

Provider-specific permission names remain adapter concerns and must be verified against the current provider API before live activation.

## Production-readiness boundary

- `production_ready = false`.
- `live_provider_proven = false`.
- Controlled remote mutation remains provider-simulated / contract-level evidence.
- No live repository deletion, branch deletion, force update, production mutation, credential mutation, or permission mutation was performed for PR #27.
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
Historical evidence snapshots remain dated and do not auto-refresh when source advances. Exact implementation remains authoritative in Git history.

## Next bounded direction

Do not create P18/P19 merely for bookkeeping. Continue with consolidation/evidence-hardening and the next repository-supported bounded objective only after inspecting current `main`, open PRs, CI, and durable task state.
