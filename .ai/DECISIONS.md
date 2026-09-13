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

## Production E2E / recovery / continuation closures
- Production E2E Harness closed through PR #11.
- Failure + Recovery Proof closed through PR #12 at `83fd14e4cc696f3cd96778fe7d447db1216c3fc0`.
- Multi-Session / Fresh-AI Continuation Proof closed through PR #13 at `cd8524b11f923e5e29eeaf445869b6239954ed1f` from final head `99822037a9e24625f2e7c216300c4aabd94e134e`.
- Multi-session final verification: Contracts 518, Full DevOS 443, External Managed Project 31 all succeeded.
- No-blind-mutation-replay remains a durable safety invariant across recovery and session boundaries.

## Multi-session / fresh-AI continuation decisions
- Repository-local state preserves context, not permission.
- Same-head continuation requires fresh revalidation; saved candidates are never directly executable.
- Changed-head continuation requires recompilation/revalidation and prior authorization is not reusable.
- Authorization/Security Gate evidence does not migrate across sessions, steps, or repository heads merely because objective/step identifiers match.
- A fresh process/AI can reconstruct active work from repository evidence only; completion still requires fresh verification.
- Real managed-project proof uses `zzpsah/automation-suite` with no commit/push and evidence-only local writes.

## Controlled higher-impact remote mutation direction
- The next maturity work is gap-driven controlled mutation proof, not an automatic numbered milestone.
- Before executing any proof, audit the existing Remote Mutation Controls and runtime-adapter contracts and use the smallest already-supported operation.
- The first proof must be non-production, tightly scoped, reversible or isolated, and independently verifiable.
- Mutation authority must be bound to the exact current step/work unit and current repository state; a prior approval or matching task id is insufficient.
- Security Gate remains independent wherever the existing impact classification requires it.
- Post-mutation state must be freshly observed and verified before success is claimed.
- If a mutation attempt occurs and later verification fails, Failure + Recovery's `MUTATION_REPLAY_FORBIDDEN` HOLD remains authoritative; automatic replay is not allowed.
- Destructive, production, database, credential/secret, or security-sensitive mutation remains out of scope unless separately and explicitly authorized.

## Production-readiness decision
- Production readiness is an evidence claim, not a phase label.
- It must be supported by a documented matrix of proven paths, unproven paths, authorization boundaries, recovery behavior, real-project evidence, and known limitations.
- Green component tests alone do not prove broad production safety.

## Verification boundary
- Earlier successful runs are historical evidence only for a new head.
- Each maturity gate closes only after fresh applicable verification on the exact final head.
- Higher-impact execution remains separately authorized and Security-Gate controlled.
