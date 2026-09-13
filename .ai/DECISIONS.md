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

## Production E2E Harness closure
- PR #11 merged at `1d6031d3578b859a6afe1dca1032287de5beceba` after Contracts 490, Full 415, External 15 passed on final head `4270440533925628a88daa17a6620aa51295319a`.
- The harness composes existing DevOS contracts and does not create a parallel runtime or permission source.

## Failure + Recovery Proof closure
- PR #12 merged at `83fd14e4cc696f3cd96778fe7d447db1216c3fc0` from final head `29c07deed803df430b2f7fd40bf302bb8deac160`.
- Final verification: Contracts 503, Full DevOS 428, External Managed Project 24 all succeeded.
- Recovery checkpoints preserve evidence and last-safe state but never become execution authority.
- Repository drift requires recompilation/revalidation before retry.
- Replay-safe read-only paths may retry only after ordinary gates re-run.
- Once a mutation reaches the runtime adapter, automatic replay is forbidden: `HOLD / MUTATION_REPLAY_FORBIDDEN`.
- Checkpoint authority/authorization tampering and invalid/corrupt persisted evidence fail closed.
- Real `zzpsah/automation-suite` proof confirmed failure → checkpoint → capability repair → verified read-only resume with unchanged HEAD/origin, zero tracked source diff, and no commit/push.

## High-impact semantic gating decision
- `HIGH_IMPACT_REQUIRES_AUTHORIZATION_CHECK` is a gating annotation, not material ambiguity by itself.
- Genuine unresolved ambiguity still blocks.
- The annotation never grants permission; downstream authorization/Security Gate checks remain mandatory.

## Multi-session / fresh-AI continuation decision
- The next maturity gate is long-running multi-session / fresh-AI continuation, not an automatic numbered milestone.
- Repository-local state must be sufficient for a fresh process/AI to recover project identity, active objective, latest safe checkpoint, and required next validation without relying on chat memory.
- Saved candidates must never be replayed as authority. Same-head continuation requires fresh revalidation; changed-head continuation must stop/escalate/recompile.
- Authorization and Security Gate evidence must remain exact-step/session scoped and must not leak across continuation boundaries.
- Fresh verification is required before resumed work can be declared complete.
- The proof should compose existing P10/P11/P13/P14/P17/E2E/recovery primitives rather than create a second persistence or execution architecture.

## Verification boundary
- Earlier successful runs are necessary historical evidence but never final evidence for a new head.
- Each maturity gate closes only after fresh applicable verification on the exact final head.
- Higher-impact execution remains separately authorized and Security-Gate controlled.
