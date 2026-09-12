# DevOS Tasks

## Active
- P12: move executable controller integration from advisory decision envelope to bounded execution-runtime handoff while preserving independent capability, authorization, verification, and security gates.
- Portable continuity: validate fresh-checkout bootstrap and repository-only recovery across AI/tool boundaries.

## Planned
- P12: implement bounded work-unit execution handoff from controller candidate to the existing execution runtime.
- P12: collect raw execution evidence and feed verification/security results back into durable task state.
- Harden higher-impact remote mutation capabilities only with operation-specific authorization, verification, security, and recovery contracts.
- Extend portable-memory recovery proof to an isolated fresh checkout path and handoff boundary.

## Blocked
- None.

## Completed recently
- P9 Development Task Controller v1 implemented and verified.
- P10 Context Continuity & Recovery v1 completed.
- Durable `.ai` project context established as the cross-chat project memory layer.
- Engineering-relevant chat recovery snapshot persisted.
- Durable context-sync contract verifier added and wired into primary CI.
- Context-sync workflow refactored to use the portable `tools/context-sync.py` implementation.
- External project-side caller validated successfully in `zzpsah/automation-suite` on branch `devos-p10-context-sync-test`.
- P11 versioned project manifest compatibility verifier implemented and verified by fresh CI.
- P11 project identity discovery tool and contract verifier implemented and verified by fresh CI.
- P11 context freshness/integrity checker and contract verifier implemented and verified by fresh CI.
- P11 safe derived-context reconciliation guard and executable cases implemented and verified by fresh CI.
- P11 cross-AI bootstrap/recovery handshake specification and vendor-neutral handoff generator implemented and verified by fresh CI.
- P11 composable stance/style registry, parser, DESI profile, and CI contract added and freshly verified.
- P11 bounded deterministic derived-context self-healer and contract verifier added and freshly verified.
- P11 repository-first recovery precedence resolver, verifier, and scenarios added and freshly verified.
- P11 recovery/revalidation and bounded self-healing integrated into the Development Task Controller lifecycle.
- P11 fresh-AI repository-only recovery proof passed from repository evidence without account memory.
- P12 Operational Intelligence v1 through v4 implemented and executable contract-verified.
- Documentation-integrity boundary implemented and contract-verified.
- Portable project-memory bootstrap inspector, deterministic proof, documentation, and contract-CI integration implemented in one atomic change set.
- P12 executable verifier repaired for Python 3.14 dynamic-import/dataclass compatibility and live CI verified.
- P12 executable controller bridge v1 implemented with independent gates over OI advisory next-action output; bridge is non-executing and preserves authority boundaries.

## Verification note
P11 is closed. P12 graph/readiness, prioritization/checkpoint, failure/evidence, advisory next-action, and controller-gating slices are repository-backed and live-CI verified. The next target is the bounded handoff from controller candidate to execution runtime; no execution authority is granted by OI.
