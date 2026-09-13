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

## P15 decision — Human Language Interpretation
- P15 is the top-level semantic entry capability for ordinary human-originated DevOS work.
- Interpretation never grants authority.

## P16 decision — Semantic Goal-to-Plan Compiler
- P16 is complete and merged through PR #9 at `460a212ebb7600619f396a455ac3e47e5a5c80fa`.
- Final source head `877833ef0f11d5a869284f9b86407c155125d96f` passed Contracts 476, Full 402, External 11.
- P16 remains planning-only; compiler output never grants authority or execution evidence.

## P17 decision — Step Readiness & Authorization Orchestrator
- P17 is complete and merged through PR #10 at `2f29ac1de367fb270c00d73b2ca44405ce09fc00`.
- Final reconciled source head `8011783962d6dddd33bcc50049c8aa4a8748cc52` passed Contracts 483, Full 408, External 12.
- P17 decides eligibility for one exact compiled P16 step using fresh repository state, dependency completion, capability, exact-step authorization, Security Gate evidence, and verification-path presence.
- Outcomes are `READY`, `NEEDS_EVIDENCE`, `NEEDS_APPROVAL`, `BLOCKED`, or `STOP`.
- Every outcome preserves `authority: UNCHANGED`, `authorization: UNCHANGED`, `execution: NONE`.
- `READY` is eligibility only; it is not execution authority or proof of completion.
- Approval never leaks between steps/tasks/sessions; stale repository state conservatively produces `STOP`.
- P17-aware runtime handoff requires exact identity and metadata agreement between readiness and a `P16-CONTROLLER-v1` execution candidate.

## Production E2E Harness decision
- Post-P17 work is gap-driven production maturity, not automatic milestone-number expansion.
- The first active gate is a Production E2E Harness proving: `human request → interpretation → plan → readiness → controller → bounded runtime → verification → persistence → recovery`.
- The harness must compose existing DevOS contracts rather than create a parallel execution path.
- Component-level green CI is necessary but insufficient; closure requires whole-path evidence plus a realistic managed-project proof.
- Failure injection must demonstrate safe non-progress or recovery for stale plans, dependency/capability failures, authorization mismatch, Security Gate failure, verification failure, persistence corruption, and provider/connection failure.

## Future persistence rule
- Meaningful engineering state must be persisted in repository-local `.ai` state rather than chat history.
- Session outcomes belong in `.ai/SESSIONS/`; current work and intentional choices belong in `TASKS.md`, `DECISIONS.md`, and `CURRENT-STATE.md`.

## Verification boundary
- Static contract checks do not by themselves prove application correctness or production safety.
- Closure requires fresh applicable verification evidence.
- Higher-impact execution remains separately authorized and Security-Gate controlled.
