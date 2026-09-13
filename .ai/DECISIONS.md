# Decisions

## Durable project state authority
- DevOS project-local `.ai` is the portable durable context layer.
- Source tree + Git are authoritative for implementation state and exact changes.
- AI account memory is supplementary and not project authority.
- `STATE-INDEX.md` is evidence/navigation, not semantic authority.

## Canonical repository identity
- Canonical repository: `zzpsah/chatgpt-development-os`.
- Name-only similarity never overrides exact repository identity evidence.

## Foundation value decision
- P0–P15 are dependency-bearing foundations; age alone is not a reason for deletion.
- Capability ledger: `docs/P0-P15-FOUNDATION-VALUE-AUDIT.md`.

## P9–P11 continuity decisions
- P9 Development Task Controller v1 is complete and remains the governed controller boundary for bounded execution candidacy.
- P10 Context Continuity & Recovery v1 is complete and established repository-local continuity independent of chat memory.
- P11 Federation & Self-Healing Context v1 is complete and remains the repository-first recovery/revalidation/cross-AI continuity baseline.

## P15–P17 decisions
- P15 Human Language Interpretation is the top-level semantic entry capability and never grants authority.
- P16 Semantic Goal-to-Plan Compiler is complete; planning remains non-executing/non-authorizing.
- P17 Step Readiness & Authorization Orchestrator is complete; `READY` means eligibility only and preserves unchanged authority/authorization/execution boundaries.

## Production E2E Harness decision
- Production E2E Harness is complete and merged through PR #11 at `1d6031d3578b859a6afe1dca1032287de5beceba`.
- Final source head `4270440533925628a88daa17a6620aa51295319a` passed Contracts 490, Full DevOS 415 and External Managed Project 15.
- The harness proves composition of existing DevOS contracts; it does not create a parallel runtime or new permission source.
- READ_ONLY steps may not execute mutation operations.
- Runtime mutation requires exact-step authorization; GitHub remote mutation additionally requires Security Gate PASS.
- Verification remains explicit argv through the bounded verification adapter.
- Persistence is a separate authorized `.ai/` write boundary and does not imply commit/push.
- Real managed-project proof uses `zzpsah/automation-suite` read-only and performs no remote mutation.

## Failure + Recovery Proof decision
- Post-E2E work advances to Failure + Recovery Proof as a gap-driven maturity gate, not an automatic numbered milestone.
- Recovery must compose existing P14 adaptive verification/self-healing, P13 checkpoint/resume, P11 repository-first recovery and the merged Production E2E Harness rather than create a second recovery architecture.
- Required failure classes include repository drift/stale plan, dependency/capability failure, exact-step authorization mismatch, Security Gate failure, runtime/provider failure, verification failure, persistence failure/corruption, recovery readback failure and ambiguous resume state.
- Recovery must preserve the last safe checkpoint and observed failure evidence.
- Resume requires fresh repository, dependency, capability, authorization, Security Gate and verification revalidation as applicable.
- An uncertain or failed mutation must never be blindly replayed.
- Deterministic repair is allowed only within existing authority and only where the recovery contract explicitly permits it; otherwise the correct outcome is HOLD/escalation.
- Successful recovery must produce fresh verification before completion is claimed.

## Future persistence rule
- Meaningful engineering state must be persisted in repository-local `.ai` state rather than chat history.
- Session outcomes belong in `.ai/SESSIONS/`; active work/decisions/current state belong in `TASKS.md`, `DECISIONS.md`, and `CURRENT-STATE.md`.

## Verification boundary
- Static contracts and earlier successful runs are necessary but insufficient for a new final head.
- Closure requires fresh applicable verification evidence.
- Higher-impact execution remains separately authorized and Security-Gate controlled.
