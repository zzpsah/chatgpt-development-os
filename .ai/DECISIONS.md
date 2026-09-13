# DevOS Decisions

## Universal Project Workflow Discovery Protocol v1
- A DevOS stance is a user-supplied workflow preference, not an instruction that overrides host policy and not evidence that DevOS or a managed project is available.
- `DEVOS-UNIVERSAL-ACTIVATION-v1` must discover a repository-local `AGENTS.md` and `.ai/manifest.yaml` before returning `READY_FOR_BOOTSTRAP`.
- Missing repository evidence returns `DEVOS_NOT_AVAILABLE`; incomplete durable context returns `PROJECT_UNKNOWN`; invalid stance syntax returns `INVALID_INVOCATION`.
- `DEVOS::GOD` grants no authorization, execution evidence, provider access, production authority, mutation permission, or override of a host's instructions.
- The protocol is host-neutral: ChatGPT, Codex, Claude, MCP/App, IDE, and future compatible hosts may call it while repository-local state remains authoritative; no external host is required to recognize it.
- `DEVOS-ACTIVATE.md` is the zero-dependency inter-AI/free-model transport. It may be pasted or linked, but supplies user project guidance only and never becomes repository evidence, authority, or host-policy control.
- A host refusal to enter a special DevOS mode, fetch a link, or treat project text as authority is compatible behavior; DevOS must be requested as optional guidance subject to the host's governing rules.

## Core documentation law
- **What is not written was never done.**
- Every material AI engineering action, decision, repair, experiment, verification result, evidence change, architecture change, roadmap change, or externally relevant outcome must leave a durable repository record.
- Completion requires `IMPLEMENTED + VERIFIED + DOCUMENTED + DURABLE STATE`.
- The durable record must preserve what happened, why, where, how it was verified, supporting evidence, remaining unknowns, and next-AI continuation guidance.
- `docs/DEVOS-MASTER-ENGINEERING-MAP.md` is the living architecture/navigation layer and must be updated when material architecture, capability, evidence-boundary, interpreter, portability, security/authorization, or future-goal semantics change.
- Automation may synchronize machine-observable facts; semantic decisions require evidence-driven AI/engineering judgment.

## MCP/App Permission Control Plane
- Remote provider/API write access is a technical capability, not DevOS authorization.
- MCP/App host adapters must route remote mutation eligibility through the provider-independent DevOS permission control plane.
- Remote capabilities are distinct: repository create/delete, branch create/update/force-update/delete.
- `FULL APPROVAL` is scoped approval, never blanket permission.
- `continue` reuses approval only when project, workflow, capability, target, impact ceiling, freshness, and security conditions remain valid.
- Multi-project operation requires isolated state and approval scope per project/repository.
- Provider credentials/tokens never enter `.ai`, MCP arguments, logs, evidence, or model output.
- Provider mutation response is not completion proof; fresh readback is required.
- Uncertain remote mutation enters HOLD/reconciliation and cannot be blindly replayed.
- Initial control-plane work is side-effect-free; live provider mutation remains a separate explicitly authorized sandbox activity.

## Actionable HOLD + Scoped Approval — closure
- PR #23 is merged at `7c60c3a4a36982ba894e2f30ba9dd98500f98d02`.
- Final source head before merge: `954b094a3832c300d371426d682eac90156cbb04`.
- Scoped approval never replaces P17/controller authorization.
- `continue` may reuse approval only within exact project/workflow/capability/target/impact/freshness/security scope.
- Stale repository state, changed target/capability, impact escalation, or changed Security Gate requires fresh evaluation.
- No live/destructive/provider/production mutation was performed for this objective.

## Current-Source Evidence Refresh — closure
- This was a bounded, unnumbered objective; no P18/P19 phase was created.
- The protocol adds fresh exact-current-source proof without rewriting historical readiness evidence.
- Historical provenance remains pinned; `production_ready=false` and `live_provider_proven=false` remain unchanged.

## Durable project state authority
- DevOS project-local `.ai` is the portable durable context layer.
- Source tree + Git are authoritative for implementation state and exact changes.
- AI account memory/chat history are supplementary and not project authority.
- `STATE-INDEX.md` is evidence/navigation, not semantic authority.
- Universal acceptance invariant: `AI A + Account A → repository → AI B + Account B → correct recovery → safe continuation`.

## P9–P11 continuity decisions
- P9 Development Task Controller remains the governed controller boundary for bounded execution candidacy.
- P10 Context Continuity & Recovery established repository-local continuity independent of chat memory.
- P11 Federation & Self-Healing Context remains the repository-first recovery/revalidation/cross-AI continuity baseline.

## P15–P17 decisions
- P15 Human Language Interpretation is the top-level semantic entry capability and never grants authority.
- P16 planning remains non-executing/non-authorizing.
- P17 `READY` means eligibility only; authority/authorization/execution remain unchanged.
- Higher-impact execution remains separately authorized and Security-Gate controlled.
