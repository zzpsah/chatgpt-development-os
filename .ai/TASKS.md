# DevOS Tasks

## Active
- P11: verify automatic project identity/registration discovery on fresh CI.
- P11: verify context freshness and integrity checks on fresh CI.
- P11: prove repository-only recovery from a fresh AI/account context.

## Planned
- P11: detect/reconcile stale `.ai` state against Git/source evidence.
- P11: add cross-AI bootstrap/recovery handshake and provenance-aware session handoff.
- P11: add safe self-healing for missing derived context files.
- Harden higher-impact remote mutation capabilities only with operation-specific authorization, verification, security, and recovery contracts.

## Blocked
- None recorded for P10.

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
- Temporary reusable-workflow smoke/debug files removed from DevOS after diagnosis.
- P11 versioned project manifest compatibility verifier implemented and wired into primary verification CI.
- P11 project identity discovery tool and contract verifier implemented.
- P11 context freshness/integrity checker and contract verifier implemented and wired into primary verification CI.

## Verification note
P10 is complete based on fresh primary CI evidence plus a successful external-project reusable-workflow execution and durable context generation. P11 identity discovery and context integrity are implemented but require fresh CI evidence on the latest HEAD before their checklist items are marked verified.
