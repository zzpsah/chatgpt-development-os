# DevOS Tasks

## Active
- Define P14 adaptive verification and self-healing scope from the completed P13 execution-feedback boundary.

## Planned
- Harden higher-impact remote mutation capabilities only with operation-specific authorization, verification, security, and recovery contracts.

## Blocked
- None.

## Completed recently
- P9 Development Task Controller v1 implemented and verified.
- P10 Context Continuity & Recovery v1 completed.
- Durable `.ai` project context established as the cross-chat project memory layer.
- Engineering-relevant chat recovery snapshot persisted.
- Durable context-sync contract verifier added and wired into primary CI.
- Reusable context-sync meaningful-path configuration made effective.
- Context-sync workflow refactored to use the portable `tools/context-sync.py` implementation.
- External project-side caller validated successfully in `zzpsah/automation-suite` on branch `devos-p10-context-sync-test`.
- Verified generated `.ai/STATE-INDEX.md`, `.ai/CURRENT-STATE.md`, and `.ai/CHANGELOG.md` were persisted by the Development OS bot commit `0291fa0fd226e15e87da9e2bb35624cd0f5b887d`.
- Temporary reusable-workflow smoke/debug files removed after isolation.
- P11 versioned project manifest compatibility verifier implemented and verified by fresh CI.
- P11 project identity discovery tool and contract verifier implemented and verified by fresh CI.
- P11 context freshness/integrity checker and contract verifier implemented and verified by fresh CI.
- P11 safe derived-context reconciliation guard and executable cases implemented and verified by fresh CI.
- P11 cross-AI bootstrap/recovery handshake specification and vendor-neutral handoff generator implemented and verified by fresh CI.
- P11 composable stance/style registry, parser, DESI profile, and CI contract added and freshly verified.
- P11 bounded deterministic derived-context self-healer and contract verifier added and freshly verified.
- P11 isolated-Git self-healing execution test added and freshly verified.
- P11 repository-first recovery precedence resolver, verifier, and scenarios added and freshly verified.
- P11 recovery/revalidation and bounded self-healing integrated into the Development Task Controller lifecycle.
- P11 DESI/GOD stance contracts aligned with executable verification semantics.
- P11 fresh-AI repository-only recovery proof passed from repository evidence without account memory.
- P12 Operational Intelligence v1 contract added.
- P12 deterministic task graph construction and dependency readiness analysis implemented with explicit missing-dependency and cycle detection.
- P12 Operational Intelligence executable contract checks wired into DevOS contract CI.
- P12 deterministic dependency-aware prioritization implemented with explicit scoring reasons and bounded operational signals.
- P12 deterministic checkpoint event intelligence implemented with explicit recognized events and safe handling of unknown events.
- P12 Operational Intelligence advisory integration documented in the Development Task Controller without granting authority.
- P12 deterministic failure classification implemented with explicit/status mapping, confidence, and raw-evidence preservation.
- P12 evidence intelligence implemented with provenance/freshness normalization and an explicit execution-evidence boundary.
- P12 Operational Intelligence v3 contract checks added for failure and evidence behavior.
- P12 fresh-repository deterministic recovery proof added to contract CI.
- P12 executable controller decision envelope added locally: OI remains `ADVISORY_ONLY`; controller independently checks scope, repository revalidation, readiness, capability, authorization, and Security Gate state before emitting an `EXECUTION_CANDIDATE`.
- P12 controller/OI/runtime-handoff integration verifier added locally and passed alongside the full local contract suite.
- P12 controller/OI/runtime-handoff integration published in commit `1f544f2f000a8357bf801cb0682c1a0e797997b1`; fresh GitHub Actions workflows 415 and 360 passed.
- Portable host-profile contract published in commit `0abaf5340b412d6f7701f0481a1e32f1e50a3504` with fresh GitHub Actions evidence.
- P13 first slice added locally: the goal-to-next-safe-unit orchestrator returns only `CONTINUE`, `STOP`, or `ESCALATE` and never executes a work unit.
- P13 runtime-outcome feedback added locally: only a verified, evidenced completion unlocks a dependent task for fresh selection.
- P13 durable checkpoint added locally: resume compares Git HEAD and always requires fresh revalidation instead of replaying a saved candidate.
- P13 isolated managed-project proof added locally: template context, real Git, candidate selection, verified runtime outcome, dependency unlock, checkpoint, and stale-head escalation execute end to end.
- P13 managed-project proof published in commit `cee2d894af4c1230240456fa635a31bbd1586248`; fresh GitHub Actions workflows 417 and 362 passed.

## Verification note
P11, P12, and P13 are closed with fresh GitHub Actions evidence. P14 Adaptive Verification & Self-Healing is the next milestone.
