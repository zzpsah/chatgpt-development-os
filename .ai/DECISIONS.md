# Decisions

## Durable project state authority

- DevOS project-local `.ai` is the portable durable context layer.
- Source tree + Git are authoritative for implementation state and exact changes.
- AI account memory is supplementary and must not be treated as project authority.
- `STATE-INDEX.md` is an evidence index, not semantic authority.

## Canonical DevOS repository identity

- The canonical `DEVOS` / `Development OS` repository is exactly `zzpsah/chatgpt-development-os`.
- The canonical URL is `https://github.com/zzpsah/chatgpt-development-os`.
- Name-only repository similarity is not identity evidence and must never override the exact canonical owner/repository declared by trusted project context.
- `.ai/manifest.yaml` is the repository-local canonical identity declaration; `projects/registry.md` is the natural-language routing map.
- Observed Git/CI repository evidence is compared with the canonical declaration. A mismatch is surfaced as an identity conflict and blocks silent substitution; it does not authorize changes to either repository.

## P9 milestone status

- P9 Development Task Controller v1 is implemented and integrated into the repository CI contract verification workflow.
- The existence of P9 is established by the Git commits recorded in project state.
- Future work must not restart or re-implement P9 merely because older roadmap text labels an earlier phase as current.

## P10 milestone status

- P10 Context Continuity & Recovery v1 is complete.
- P10 was closed only after fresh primary CI evidence and a real external project-side reusable workflow execution successfully generated durable context files.
- The validated external test project was `zzpsah/automation-suite` on branch `devos-p10-context-sync-test`.
- P10 does not imply completion of higher-impact P8 remote mutations.

## P11 milestone decision

- P11 DevOS Federation & Self-Healing Context v1 is complete.
- P11 makes repository-first project continuity resilient across AI tools/accounts, chat loss, connectivity interruptions, stale generated state, and handoffs.
- P11 prioritizes versioned project identity, compatibility, freshness/integrity detection, safe reconciliation, cross-AI handoff, provenance, and deterministic self-healing.

## P15 milestone decision — Human Language Interpretation

- P15 Human Language Interpretation v2 is a top-level DevOS capability, not a side feature.
- Every ordinary human-originated DevOS request enters through the Human Language Execution Engine before project/workflow selection and bounded technical execution.
- The top-level semantic path is `Human input → Human Language Execution Engine → Project Router / State Resolver → Development Task Controller → bounded workflow/runtime → Verification + Security → durable state`.
- The deterministic v2 interpreter is the minimum executable behavior contract. Richer AI/model-assisted multilingual and contextual interpretation may evolve above it without changing downstream safety contracts.
- P15 supports contextual short commands, English/Hinglish shorthand, referential continuation, compatible multi-intent composition, negative constraints, ambiguity/confidence output, and explicit high-impact authorization escalation.
- `SECURITY_REVIEW` routes through `workflows/security.md` and the Security Gate.
- Interpretation never grants authority. Language confidence, emotional intensity, urgency, prior conversational context, or stance codes cannot independently authorize production, destructive, security-sensitive, deployment, merge, database, credential, or other high-impact operations.
- P15 was merged to `main` through PR #8 on merge commit `770c8b3583515e3c947562854be7a2d2fd34710d` after both feature-branch verification workflows passed on repair commit `0be462dac63501a31221fcd972e0de078657d110`.

## P16 milestone decision — Semantic Goal-to-Plan Compiler

- P16 Semantic Goal-to-Plan Compiler v1 bridges top-level semantic interpretation and the Development Task Controller with an explicit bounded plan graph rather than allowing downstream execution logic to reconstruct intent informally.
- Canonical path becomes `Human input → Human Language Execution Engine → Project Router / State Resolver → Semantic Goal-to-Plan Compiler → Development Task Controller → bounded workflow/runtime → Verification + Security → durable state`.
- The compiler preserves interpreted constraints, project identity, ambiguity, evidence provenance, dependencies, authority requirements, verification requirements, and stop/escalation conditions.
- The compiler emits planning structure only. It returns `execution: NONE`, does not grant authority, and cannot convert a plan into permission.
- High-impact, security-sensitive, production, destructive, deployment, merge, database, credential, and similar operations remain independently authorized and Security-Gate controlled.
- Material ambiguity must produce `CLARIFY` or `BLOCKED` rather than a guessed plan step.
- P16 adds automatic read-before-write ordering for mutating plans when no read-only precondition is already present.
- P16 source implementation is complete on PR #9 final source head `981ac5f02ff3d64ac2caf3f49a9dbe008fbe8b6a`; milestone closure still requires fresh final-head CI success before merge.

## P17 milestone decision — Step Readiness & Authorization Orchestrator

- P17 is intentionally narrower than another generic autonomy layer. Its responsibility is to decide whether one exact compiled P16 plan step is currently eligible to proceed.
- P17 canonical input is `compiled plan step + compilation repository head + current repository head + completed dependencies + capability + step-bound authorization + Security Gate evidence + verification path`.
- P17 outcomes are `READY`, `NEEDS_EVIDENCE`, `NEEDS_APPROVAL`, `BLOCKED`, or `STOP`.
- `READY` is not execution authority. Every P17 outcome preserves `authority: UNCHANGED`, `authorization: UNCHANGED`, and `execution: NONE`.
- Authorization is bound to the exact plan step id. Approval for another step, earlier task, previous session, or lower-impact operation does not satisfy an authorization-required step.
- A repository-head mismatch between planning time and execution-readiness time is treated conservatively as a stale plan and returns `STOP`; v1 does not infer that intervening changes are harmless.
- Security-sensitive, high-impact, production, or destructive steps require explicit Security Gate evidence; a missing gate result is not silently treated as pass.
- P17 is stacked on P16 while P16 final CI remains queued. P17 cannot be merged to `main` before P16 is cleanly verified and merged.
- After P17, roadmap progression should become gap-driven: end-to-end maturity harness, real managed-project proof, and targeted hardening are preferred over adding phases only to increase milestone numbering.

## Future persistence rule

- Meaningful future engineering work must be persisted in repository-local `.ai` state rather than relying on chat history.
- Session-level semantic outcomes belong in `.ai/SESSIONS/`.
- Changes to remaining work, intentional choices, or current project state must be reflected in `TASKS.md`, `DECISIONS.md`, or `CURRENT-STATE.md` as applicable.
- Generated `STATE-INDEX.md` remains deterministic evidence only.

## Verification boundary

- Static contract verification proves repository contracts are structurally present; it does not by itself prove semantic AI behavior or application correctness.
- Milestone closure requires fresh applicable verification evidence.
- Higher-impact execution remains separately authorized and verified even when language interpretation, planning, or readiness confidence is HIGH.
