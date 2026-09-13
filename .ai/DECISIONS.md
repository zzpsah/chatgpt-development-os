# DevOS Decisions

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
