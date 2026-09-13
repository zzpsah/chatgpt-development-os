# Decisions

## Durable project state authority
- DevOS project-local `.ai` is the portable durable context layer.
- Source tree + Git are authoritative for implementation state and exact changes.
- AI account memory/chat history are supplementary and not project authority.
- `STATE-INDEX.md` is evidence/navigation, not semantic authority.

## Canonical repository identity
- Canonical repository: `zzpsah/chatgpt-development-os`.
- Name-only similarity never overrides exact repository identity evidence.

## P9–P11 continuity decisions
- P9 Development Task Controller remains the governed controller boundary for bounded execution candidacy.
- P10 Context Continuity & Recovery established repository-local continuity independent of chat memory.
- P11 Federation & Self-Healing Context remains the repository-first recovery/revalidation/cross-AI continuity baseline.

## P15–P17 decisions
- P15 Human Language Interpretation is the top-level semantic entry capability and never grants authority.
- P16 planning remains non-executing/non-authorizing.
- P17 `READY` means eligibility only; authority/authorization/execution remain unchanged.

## Production E2E + Failure Recovery closures
- Production E2E Harness closed through PR #11.
- Failure + Recovery Proof closed through PR #12 at `83fd14e4cc696f3cd96778fe7d447db1216c3fc0` after Contracts 503, Full 428, External 24 passed on final head `29c07deed803df430b2f7fd40bf302bb8deac160`.
- No-blind-mutation-replay remains a durable safety invariant.

## Multi-session / fresh-AI continuation decision
- This is a gap-driven maturity gate, not an automatic numbered milestone.
- Repository-local state must be sufficient for a fresh process/AI to recover project identity, active objective, latest safe checkpoint, constraints and verification obligations without chat/account memory.
- Continuation packets preserve facts only and must carry `authority: UNCHANGED`, `authorization: UNCHANGED`, `execution: NONE`.
- Same-head continuation returns `REVALIDATE_REQUIRED`; a saved candidate is never directly executable.
- Changed-head continuation returns `RECOMPILE_REQUIRED`; prior authorization is explicitly non-reusable after repository drift.
- Project identity mismatch, unsupported protocol, packet authority/authorization tampering, packet execution authority, and inherited mutation-replay prohibition all HOLD.
- Authorization/Security Gate evidence does not silently migrate across session, step or repository-head boundaries.
- A fresh process may reconstruct what work remains, but must re-run ordinary P16/P17/controller/runtime/verification gates before execution/completion.

## Two-process proof decision
- The deterministic proof must use separate Python processes so Session B cannot depend on imported in-memory state from Session A.
- Session A communicates only through a persisted continuation packet.
- Session B uses the packet plus current repository evidence and must return revalidation/recompilation semantics, never an execution handoff.

## Real managed-project continuation decision
- `zzpsah/automation-suite` is the real external read-only managed-project proof target.
- Session A may write only bounded local `.ai/EVIDENCE/` continuation artifacts in the ephemeral checkout.
- Session B derives current project identity from Git origin and current head from Git, not from chat memory.
- The proof must preserve unchanged HEAD/origin, zero tracked source diff, evidence-only worktree deltas, and no commit/push.
- External evidence artifact upload is part of the proof provenance.

## Verification boundary
- Earlier successful runs are historical evidence only.
- PR #13 closes only after fresh Contracts, Full DevOS and External Managed Project success on the exact final semantic-state head.
- Higher-impact execution remains separately authorized and Security-Gate controlled.
