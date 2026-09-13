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
- P9 Development Task Controller v1 remains the governed controller boundary for bounded execution candidacy.
- P10 Context Continuity & Recovery v1 established repository-local continuity independent of chat memory.
- P11 Federation & Self-Healing Context v1 remains the repository-first recovery/revalidation/cross-AI continuity baseline.

## P15–P17 decisions
- P15 Human Language Interpretation is the top-level semantic entry capability and never grants authority.
- P16 Semantic Goal-to-Plan Compiler is complete; planning remains non-executing/non-authorizing.
- P17 Step Readiness & Authorization Orchestrator is complete; `READY` means eligibility only and preserves unchanged authority/authorization/execution boundaries.

## Production E2E Harness decision
- Production E2E Harness is complete and merged through PR #11 at `1d6031d3578b859a6afe1dca1032287de5beceba`.
- Final source head `4270440533925628a88daa17a6620aa51295319a` passed Contracts 490, Full DevOS 415 and External Managed Project 15.
- The harness composes existing DevOS contracts; it does not create a parallel runtime or permission source.
- READ_ONLY steps may not execute mutation operations.
- Runtime mutation requires exact-step authorization; GitHub remote mutation additionally requires Security Gate PASS.
- Verification remains explicit argv through the bounded verification adapter.
- Persistence is a separate authorized `.ai/` write boundary and does not imply commit/push.

## Failure + Recovery Proof decision
- Failure + Recovery Proof is a gap-driven maturity gate, not an automatic numbered milestone.
- Recovery composes P14 adaptive verification/self-healing, P13 checkpoint/resume, P11 repository-first recovery, and the merged Production E2E Harness rather than creating a second recovery architecture.
- Failure checkpoints preserve observed evidence and the last safe stage; they are evidence, never execution authority.
- Repository drift/stale plans require recompilation and revalidation before retry.
- Replay-safe read-only paths may retry only after the ordinary P15/P16/P17/controller/runtime/verification gates run again.
- Once a mutation operation reaches the runtime adapter, automatic replay is forbidden. The required outcome is `HOLD / MUTATION_REPLAY_FORBIDDEN` pending explicit re-evaluation.
- A preflight-blocked mutation is not treated as an executed mutation; it may be reconsidered only after exact authorization/Security Gate/capability evidence is repaired and revalidated.
- Persisted evidence must itself be readable and structurally valid before a recovery can be accepted.
- Checkpoint authority/authorization tampering is an immediate HOLD.
- Successful recovery must produce fresh verification before completion is claimed.

## High-impact semantic gating decision
- P15's `HIGH_IMPACT_REQUIRES_AUTHORIZATION_CHECK` marker is a gating annotation, not material ambiguity by itself.
- P16 must preserve that annotation while continuing to block genuine unresolved ambiguity.
- This does not grant authorization: high-impact/security steps still carry independent authorization/Security Gate requirements and must pass P17/controller/runtime gates.
- A direct P16 regression permanently covers this P15→P16 boundary.

## Real managed-project recovery proof decision
- `zzpsah/automation-suite` remains the real external managed-project target for read-only recovery proof.
- The proof may write only bounded local `.ai/EVIDENCE/` files in the ephemeral checkout; it may not commit, push, or alter tracked source/history.
- Git porcelain may collapse multiple untracked evidence files into a single `.ai/EVIDENCE/` directory entry. Proof validity therefore depends on explicit evidence-file existence/content, unchanged HEAD/origin, evidence-only worktree status, and zero tracked diff—not on one porcelain line per evidence file.

## Future persistence rule
- Meaningful engineering state must be persisted in repository-local `.ai` state rather than chat history.
- Session outcomes belong in `.ai/SESSIONS/`; active work/decisions/current state belong in `TASKS.md`, `DECISIONS.md`, and `CURRENT-STATE.md`.

## Verification boundary
- Static contracts and earlier successful runs are necessary but insufficient for a new final head.
- PR #12 closure requires fresh applicable Contracts, Full DevOS, and External Managed Project success on the exact final head.
- Higher-impact execution remains separately authorized and Security-Gate controlled.
