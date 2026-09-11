# DevOS Tasks

## Active
- P12: define Operational Intelligence architecture and first dependency-aware task graph slice.

## Planned
- P12: dependency-aware prioritization and checkpoint intelligence.
- P12: failure classification and evidence collection improvements.
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

## Verification note
P11 completion criteria are satisfied by fresh primary CI run 290 on commit `e701f5fa0a6dce1f0f4ab3ad1cb260de2f55853f` (all jobs successful), plus fresh repository-only recovery, self-healing, recovery-precedence, handoff, and stance verification. P11 is closed. P12 is now the active milestone.
