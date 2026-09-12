# DevOS Tasks

## Active
- Portable AI host profiles: add a vendor-neutral machine-readable capability declaration and contract verifier so any AI host can state its actual capability boundary without inventing support.

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

## Verification note
P11 and P12 are closed with fresh GitHub Actions evidence. Portable host-profile conformance is the active cross-AI portability improvement.
