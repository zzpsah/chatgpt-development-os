# DevOS Tasks

## Active
- **P17 Step Readiness & Authorization Orchestrator v1** is the active maturity milestone on PR #10 / branch `devos/p17-step-readiness`.
- PR #10 is retargeted to current `main`; reconcile final branch state without losing mainline foundation-audit/roadmap/P16-closure work.
- Preserve exact-step readiness, repository freshness, dependency closure, capability evidence, step-bound authorization, Security Gate evidence, verification-path requirements, and non-execution semantics.
- Keep P17 non-executing/non-authorizing: `READY` is eligibility only.
- Require a direct verified path: `P15 human request → P16 compiled plan → P17 readiness → P16 compiled-plan controller → P17-aware runtime handoff`.

## P17 implementation completed
- exact P16 step bound to compilation/current repository heads;
- stale plan → `STOP`;
- strict plan structure and semantic-integrity validation;
- dependency cycle and dependency-closure validation;
- fake/unknown/impossible completion-evidence rejection;
- capability evidence validation;
- exact-step approval isolation with no approval leakage;
- explicit Security Gate evidence for security/high-impact/destructive steps;
- verification-path requirement;
- negative-constraint tamper rejection;
- all READY gates required true;
- readiness metadata explicitly not execution evidence;
- P17 runtime handoff requires `P16-CONTROLLER-v1`, exact controller/readiness step identity, matching repository/step metadata, and all controller/readiness gates;
- legacy P12 controller candidate is insufficient for P17-aware handoff while legacy P12 handoff remains separately backward compatible;
- direct end-to-end proof with no manual task reconstruction.

## Foundation audit
- P0–P15 Foundation Value Audit is complete in `docs/P0-P15-FOUNDATION-VALUE-AUDIT.md`.
- P0–P15 are retained as dependency-bearing foundations; deprecation requires consumer/contract evidence.
- Regression guard: `tools/test-foundation-value-audit.py`.

## Pending verification
- Fresh applicable CI must pass on the final reconciled P17 head after current-main synchronization.
- Do not reuse pre-retarget/pre-reconciliation P17 runs as closure evidence.
- If CI fails, repair only the demonstrated defect and require a newer fresh final-head run.

## Planned after P17
- Build the **Production E2E Harness**: natural human request → P15 interpretation → P16 plan → P17 readiness → controller → bounded runtime → verification → persistence → recovery.
- Add failure-injection proof for stale plans, dependency failures, capability absence, authorization mismatch, Security Gate failure, verification failure, persistence corruption, and connection/provider failures.
- Prove long-running/fresh-AI continuation on a realistic managed project.
- Use observed failures/gaps to drive hardening rather than adding milestone numbers for their own sake.
- Harden higher-impact remote mutation only after E2E/recovery gates are proven.
- Continue multilingual/contextual language regression evolution without weakening project isolation, constraints, authorization, evidence, Security Gate, or verification boundaries.

## Completed recently
- P9 Development Task Controller v1.
- P10 Context Continuity & Recovery v1.
- P11 Federation & Self-Healing Context v1.
- P12 Operational Intelligence.
- P13 Autonomous Development Orchestration.
- P14 Adaptive Verification & Self-Healing v1.
- P15 Human Language Interpretation v2 merged through PR #8.
- **P16 Semantic Goal-to-Plan Compiler v1 merged through PR #9 on merge commit `460a212ebb7600619f396a455ac3e47e5a5c80fa`.**
- P0–P15 foundation-value audit and regression guard.

## P16 final verification evidence
- Final source head: `877833ef0f11d5a869284f9b86407c155125d96f`.
- Contracts run 476 / `34750716230`: success.
- Full DevOS run 402 / `34750716222`: success.
- P13 External Managed Project run 11 / `34750716234`: success.

## Safety invariant
P16 planning and P17 readiness never grant authority or prove execution. Runtime candidacy remains independently gated by current repository state, capability, exact authorization, Security Gate, and applicable verification.
