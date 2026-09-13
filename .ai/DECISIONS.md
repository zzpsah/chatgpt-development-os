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

## P0–P15 foundation value decision

- P0–P15 are not to be treated as disposable historical milestones.
- Current architecture evidence shows that the early foundations supply bootstrap, portable context, evidence/verification, security/authorization, bounded autonomy, runtime, portability, automation/onboarding, controller, recovery, federation, operational intelligence, orchestration, adaptive verification, and human-language entry capabilities consumed by the current system.
- Historical milestone age is not a valid reason for deletion.
- Any future deprecation requires repository evidence showing that no current consumer or normative contract depends on the capability.
- The durable capability ledger is `docs/P0-P15-FOUNDATION-VALUE-AUDIT.md` and must be updated when a foundation capability is consolidated, replaced, or deprecated.

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

## P16 milestone decision

- P16 Semantic Goal-to-Plan Compiler v1 is complete and merged to `main` through PR #9 on merge commit `460a212ebb7600619f396a455ac3e47e5a5c80fa`.
- Final-head verification passed on source head `877833ef0f11d5a869284f9b86407c155125d96f`: contracts run 476, full DevOS run 402, and P13 external managed-project run 11.
- P16 remains planning-only; compiler output never grants authority or execution evidence.

## Post-P17 development strategy

- After P17 closure, development becomes **gap-driven production maturity**, not automatic milestone-number expansion.
- The first maturity gate is a Production E2E Harness proving the complete request-to-recovery path on a managed software project.
- Subsequent gates are failure injection/recovery, long-running fresh-AI continuation, controlled higher-impact remote mutation, and production release readiness.
- Component-level CI success is necessary but is not sufficient evidence of whole-system autonomous development.

## Future persistence rule

- Meaningful future engineering work must be persisted in repository-local `.ai` state rather than relying on chat history.
- Session-level semantic outcomes belong in `.ai/SESSIONS/`.
- Changes to remaining work, intentional choices, or current project state must be reflected in `TASKS.md`, `DECISIONS.md`, or `CURRENT-STATE.md` as applicable.
- Generated `STATE-INDEX.md` remains deterministic evidence only.

## Verification boundary

- Static contract verification proves repository contracts are structurally present; it does not by itself prove semantic AI behavior or application correctness.
- Milestone closure requires fresh applicable verification evidence.
- Higher-impact execution remains separately authorized and verified even when language interpretation is HIGH confidence.
