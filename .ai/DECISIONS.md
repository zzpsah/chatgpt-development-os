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
- Observed Git/CI repository evidence is compared with the canonical declaration; identity conflicts block silent substitution.

## P0–P15 foundation value decision

- P0–P15 are not disposable historical milestones; they are dependency-bearing foundations of the current architecture.
- Historical milestone age is not a valid reason for deletion.
- Future deprecation requires repository evidence that no current consumer or normative contract depends on the capability.
- Durable capability ledger: `docs/P0-P15-FOUNDATION-VALUE-AUDIT.md`.

## P9–P11 continuity decisions

- P9 Development Task Controller v1 is implemented and must not be restarted because of stale roadmap text.
- P10 Context Continuity & Recovery v1 is complete and established durable repository-local continuity.
- P11 Federation & Self-Healing Context v1 is complete and remains the recovery/federation baseline for all later milestones.

## P15 milestone decision — Human Language Interpretation

- P15 Human Language Interpretation v2 is a top-level DevOS capability, not a side feature.
- Human-originated requests enter through the Human Language Execution Engine before project/workflow selection and bounded execution.
- Interpretation never grants authority. Confidence, urgency, emotional intensity, prior chat context, or stance codes cannot independently authorize high-impact operations.
- P15 merged through PR #8 on merge commit `770c8b3583515e3c947562854be7a2d2fd34710d` after feature verification passed.

## P16 milestone decision — Semantic Goal-to-Plan Compiler

- P16 Semantic Goal-to-Plan Compiler v1 is complete and merged to `main` through PR #9 on merge commit `460a212ebb7600619f396a455ac3e47e5a5c80fa`.
- Final source head `877833ef0f11d5a869284f9b86407c155125d96f` passed contracts run 476, full DevOS run 402, and P13 external managed-project run 11.
- P16 bridges interpretation/state resolution and the Development Task Controller with an explicit bounded plan graph.
- Compiler output preserves project identity, constraints, ambiguity, evidence expectations, dependencies, authority requirements, verification requirements, and stop/escalation conditions.
- P16 is planning-only: `execution: NONE`; planning never grants authority or becomes execution evidence.
- High-impact/security/production/destructive operations remain independently authorized and Security-Gate controlled.

## P17 milestone decision — Step Readiness & Authorization Orchestrator

- P17 is an eligibility boundary for one exact compiled P16 step, not another generic autonomy layer.
- Canonical input is `compiled plan + selected step + compilation/current repository heads + completion evidence + capability + exact-step authorization + Security Gate evidence + verification path`.
- Outcomes are `READY`, `NEEDS_EVIDENCE`, `NEEDS_APPROVAL`, `BLOCKED`, or `STOP`.
- Every outcome preserves `authority: UNCHANGED`, `authorization: UNCHANGED`, and `execution: NONE`.
- `READY` is eligibility only; it is never execution authority or proof of completion.
- Authorization is bound to the exact step id. Approval for another step, earlier task, previous session, or lower-impact operation cannot satisfy a gated step.
- Repository-head drift after planning is conservatively `STOP`; v1 does not infer intervening changes are harmless.
- Security-sensitive/high-impact/production-destructive steps require explicit Security Gate evidence.
- P17 validates plan structure, dependency closure/cycles, completion evidence, capability/auth/security evidence maps, negative constraints, verification metadata, and exact runtime-handoff identity before eligibility.
- P17-aware runtime handoff requires a matching `P16-CONTROLLER-v1` execution candidate plus a matching `DEVOS-STEP-READINESS-v1` READY envelope; legacy P12 candidate alone is insufficient for this path.
- PR #10 must receive fresh final-head verification after reconciliation with current `main` before merge.

## Post-P17 development strategy

- After P17 closure, development becomes **gap-driven production maturity**, not automatic milestone-number expansion.
- First maturity gate: Production E2E Harness proving `human request → interpretation → plan → readiness → controller → bounded runtime → verification → persistence → recovery` on a managed project.
- Subsequent gates: failure injection/recovery, long-running fresh-AI continuation, controlled higher-impact remote mutation, and production release readiness.
- Component-level CI success is necessary but not sufficient evidence of whole-system autonomous development.

## Future persistence rule

- Meaningful engineering work must be persisted in repository-local `.ai` state rather than relying on chat history.
- Session semantic outcomes belong in `.ai/SESSIONS/`.
- Remaining work, intentional choices, and current project state belong in `TASKS.md`, `DECISIONS.md`, or `CURRENT-STATE.md` as applicable.
- Generated `STATE-INDEX.md` remains deterministic evidence only.

## Verification boundary

- Static contract verification proves repository contracts are structurally present; it does not by itself prove semantic AI behavior or application correctness.
- Milestone closure requires fresh applicable verification evidence.
- Higher-impact execution remains separately authorized and verified even when interpretation, planning, or readiness is high confidence.
