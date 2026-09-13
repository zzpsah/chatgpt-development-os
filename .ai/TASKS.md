# DevOS Tasks

## Active
- **Production E2E Harness** is the active gap-driven maturity gate on PR #11 / branch `devos/production-e2e-harness`.
- Implementation and real managed-project proof are source-complete; take fresh final-head verification after the semantic-state/session commit.
- Prove final governed path: `human request → P15 interpretation → P16 plan → P17 readiness → controller → bounded runtime → verification → persistence → recovery`.
- Preserve exact project identity, repository freshness, exact-step authorization, Security Gate, capability, evidence provenance, verification and recovery boundaries.

## Implemented
- `core/production-e2e-harness.md` normative contract.
- `tools/production-e2e-harness.py` executable `DEVOS-PRODUCTION-E2E-v1` reference harness.
- `tools/test-production-e2e-harness.py` isolated regression corpus.
- `tools/verify-production-e2e-managed-project.py` real managed-project proof.
- Contracts workflow executes the isolated harness regression.
- External managed-project workflow checks out `zzpsah/automation-suite`, runs the read-only harness proof, and uploads the evidence packet as an artifact.
- Runtime semantic binding blocks READ_ONLY→mutation mismatch and requires exact-step authorization for all mutation operations.
- GitHub remote mutation additionally requires exact-step Security Gate PASS.
- Explicit argv verification is required after runtime success.
- `.ai/` evidence persistence requires independent authorization and is recovered by bounded readback.

## Evidence already observed
- Contracts run 488 / `34751659378`: success, including `Verify Production E2E Harness`.
- External Managed Project run 13 / `34751659403`: success, including the real `automation-suite` Production E2E proof.
- Evidence artifact id `10316730199`, digest `sha256:bea3ec2c742be2a57d7f09066802dd31731b2b863dbb96c7c149a7085a42f7eb`.
- The proof performs no remote mutation, commit or push to `automation-suite`; only an explicitly authorized local `.ai/EVIDENCE/` packet is created in the ephemeral checkout.

## Pending verification
- The semantic-state/session commit will create a new final candidate head. Require fresh applicable final-head verification before merge.
- Required final closure evidence: Contracts success, Full DevOS success, External Managed Project success, PR mergeable.
- Do not reuse earlier head runs as final closure evidence after the head changes.

## Planned after E2E Harness
- **Failure + Recovery Proof**: inject bounded failures and prove diagnose/repair/re-verify/persist/resume or safe HOLD.
- Long-running multi-session/fresh-AI continuation.
- Controlled higher-impact remote mutation, operation by operation.
- Production-readiness evidence and documented limitations.

## Completed baseline
- P9 Development Task Controller v1.
- P10 Context Continuity & Recovery v1.
- P11 Federation & Self-Healing Context v1.
- P12 Operational Intelligence.
- P13 Autonomous Development Orchestration.
- P14 Adaptive Verification & Self-Healing v1.
- P15 Human Language Interpretation v2.
- P16 Semantic Goal-to-Plan Compiler v1.
- P17 Step Readiness & Authorization Orchestrator v1.

## Safety invariant
The Production E2E Harness proves composition; it never manufactures permission. Runtime mutation, production/destructive work, remote mutation, persistence and verification remain independently bounded and evidence-backed.
