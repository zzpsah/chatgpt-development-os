# Current State

## Snapshot

- Repository: `zzpsah/chatgpt-development-os`.
- Source tree + Git are authoritative for implementation and exact project state; ChatGPT Memory/chat history are supplementary only.
- P11 Federation & Self-Healing Context remains the repository-first recovery/revalidation/cross-AI continuity baseline.
- P9 through P17 are complete on `main` at their stated evidence levels.
- Universal Project Onboarding + Repository Creation, host-neutral MCP/App `repository.create`, and Current-Source Evidence Refresh are closed at their stated evidence levels.
- **Active unnumbered bounded objective: MCP/App Permission Control Plane + Multi-Project Agent Isolation.**
- No new numbered phase is created or implied.
- DevOS is intended to operate as a long-lived agent across multiple repositories without letting provider write access, API tokens, AI accounts, chats, or model memory become authority.

## Active objective — MCP/App Permission Control Plane

Purpose: connect the host-neutral MCP/App boundary to a provider-independent remote-resource permission control plane so remote operations are authorized per exact project, repository, resource, capability, workflow, impact, and freshness scope.

Governed remote capabilities:
- `repository.create` — HIGH
- `repository.delete` — DESTRUCTIVE
- `branch.create` — LOW by default; higher for protected/default/release/production targets
- `branch.update` — HIGH for canonical/protected/release/production refs
- `branch.force_update` — DESTRUCTIVE
- `branch.delete` — DESTRUCTIVE

Core control flow:

`AI host → MCP/App adapter → P15 → P16 → P17 → Actionable Hold / Scoped Approval → Remote Permission Control Plane → provider adapter → fresh readback → durable evidence`

The MCP/App adapter is an interface, not an authority. Existing `devos.create_repository` remains host-neutral and provider-nonexecuting. The new control-plane gateway adds the missing authorization boundary before provider execution.

Implemented on working branch:
- `tools/devos-mcp-governed-gateway.py`
- `tools/devos-governed-continuation.py`
- `tools/test-devos-mcp-governed-gateway.py`
- `tools/test-devos-governed-continuation.py`
- `docs/DEVOS-MCP-PERMISSION-CONTROL-PLANE.md`
- `.github/workflows/verify-mcp-permission-control-plane.yml`
- expanded `.ai/TASKS.md`

The provider-neutral remote permission policy already defines exact capability separation and consequence disclosure in `core/remote-resource-permission-governance.md`.

## Multi-project agent isolation

A long-lived DevOS agent may manage multiple projects concurrently, but:

`Project A state != Project B state`

`Project A approval != Project B approval`

`Project A credentials/provider binding != Project B credentials/provider binding`

Approval cannot move between repositories, branches, capabilities, or workflows. `continue` can reuse an approval only while the exact approved scope and freshness/security conditions remain valid. A new/high-impact/out-of-scope action becomes an actionable HOLD requiring fresh approval.

## Provider credentials / token boundary

Provider/API tokens are technical capabilities only.

They are never DevOS authorization and must never be copied into `.ai/`, MCP arguments, logs, generated evidence, or model output.

The provider permission set should be minimum necessary for the enabled adapter capabilities. Provider-specific permission names remain adapter concerns and must be verified against the current provider API before live activation.

## Verification boundary

The new control-plane work is currently **IMPLEMENTED but not yet independently VERIFIED to final-head CI**.

No live repository deletion, branch deletion, force update, production mutation, credential mutation, or permission mutation has been performed for this objective.

The dedicated CI gate is expected to prove deterministic policy and integration semantics only. Live-provider proof remains a separate, explicitly bounded sandbox exercise.

## Existing production-readiness boundary

- `production_ready = false`.
- `live_provider_proven = false`.
- Controlled remote mutation remains provider-simulated / contract-level evidence.
- Provider response is attempt evidence, not completion proof.
- Uncertain mutation is not blindly replayed.
- Historical evidence remains pinned and is never silently rewritten.

## Universal portability invariant

`AI A + Account A → repository → AI B + Account B → correct state recovery → safe continuation`

No private AI memory is authoritative project state.
