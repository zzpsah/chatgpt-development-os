# DevOS Tasks

## Active
- P17 Step Readiness & Authorization Orchestrator v1 is the active maturity milestone on PR #10 / branch `devos/p17-step-readiness`.
- Revalidate/retarget P17 against P16-closed `main`.
- Preserve exact-step readiness, repository freshness, dependency closure, capability evidence, step-bound authorization, Security Gate evidence, and verification-path requirements.
- Keep P17 non-executing/non-authorizing; `READY` is eligibility only.
- Require a direct verified path: `P15 human request → P16 compiled plan → P17 readiness → P16 compiled-plan controller → P17-aware runtime handoff`.

## Foundation audit
- **P0–P15 Foundation Value Audit is complete and recorded** in `docs/P0-P15-FOUNDATION-VALUE-AUDIT.md`.
- P0–P15 are retained as dependency-bearing foundations; no phase is marked for deletion without consumer/contract evidence.
- The audit regression guard is `tools/test-foundation-value-audit.py`.

## Pending verification
- Fresh applicable CI must pass on the final P17 head after retarget/revalidation against current `main`.
- Do not reuse pre-retarget P17 runs as final closure evidence.

## Planned after P17
- Build the **Production E2E Harness**: natural human request → P15 interpretation → P16 plan → P17 readiness → controller → bounded runtime → verification → persistence → recovery.
- Add failure-injection proof for stale plans, dependency failures, capability absence, authorization mismatch, verification failure, persistence corruption, and connection-layer failures.
- Prove long-running/fresh-AI continuation on a realistic managed project.
- Use observed failures/gaps to drive subsequent hardening instead of adding milestone numbers for their own sake.
- Harden higher-impact remote mutation only after E2E/recovery gates are proven.
- Continue multilingual/contextual language regression evolution without weakening project isolation, constraints, authorization, evidence, Security Gate, or verification boundaries.
- Normalize P0–P8 historical documentation where useful without rewriting Git history.

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

## P16 closure invariant
P16 remains planning-only. Compiler output, plan classification, Operational Intelligence ranking, prior success, or language confidence never grants authority or proves execution. The controller independently revalidates repository state, capability, authorization, Security Gate, and verification conditions before runtime candidacy.
