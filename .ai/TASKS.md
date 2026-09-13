# DevOS Tasks

## Active
- No numbered phase is active from PR #27 closure.
- Continue with consolidation, evidence hardening, and the next repository-supported bounded objective only after inspecting current `main`, open PRs, CI, and durable project state.
- Do not create P18/P19 merely for bookkeeping.

## Completed — MCP/App Permission Control Plane + Multi-Project Agent Isolation
- PR #27 — `Integrate MCP/App remote permission control plane` — merged at `2bb8d978113b64ab88d6ba5f8e357fa595162c9c`.
- Exact PR head verified before merge: `99a48fea51bd2d9d33860115c0212f7b25ca4ad8`.
- Exact-head verification passed: Full DevOS 543, Contracts 621, Trust-First 84, MCP Permission Control Plane 3, Remote Resource Permission Governance 4, MCP Repository Create 13, Current-Source Evidence 16.
- The control plane governs `repository.create`, `repository.delete`, `branch.create`, `branch.update`, `branch.force_update`, and `branch.delete` with exact project/repository/resource/workflow/impact/freshness scope.
- Provider/API write permission remains technical capability only; it is never DevOS authorization.
- `FULL APPROVAL` remains scoped, not blanket permission.
- `continue` may reuse an approval only when exact project/workflow/capability/target/impact/freshness/security scope remains valid.
- Multi-project isolation keeps state, approval, and provider binding separated per project.
- No live/destructive/production provider mutation was performed for PR #27.

## Current-Source Evidence Refresh Protocol — completed
- Unnumbered bounded objective; merged through PR #24.
- Final source head: `bc400112d0bbaced6ed699a6863bc8dcf91e47c8`.
- Merge commit / verified `main`: `a93f9f435ffab5f81ce070f07a0da694757ab6cb`.
- Final PR evidence and post-merge verification were recorded without rewriting historical provenance.

## Completed recently
- Production E2E Harness — PR #11.
- Failure + Recovery Proof — PR #12.
- Multi-Session / Fresh-AI Continuation Proof — PR #13.
- Controlled Remote Mutation Proof — PR #14.
- Production-Readiness Evidence Matrix & Limitations — PR #16.
- Trust-First audit gap closure / adversarial Security Gate proof — PR #17.
- Foundation Health & State Consistency — PR #18.
- Universal Project Onboarding + Repository Creation — PR #19.
- Cross-Host Recovery Friction & Onboarding Proof — PR #20.
- Recovery Friction → Foundation Health/Doctor Integration — PR #21.
- Host-neutral MCP/App `repository.create` adapter — PR #22.
- Current-Source Evidence Refresh — PR #24.
- MCP/App Permission Control Plane + Multi-Project Agent Isolation — PR #27.

## Platform foundations retained in the durable task map
- **P11 Federation & Self-Healing Context** remains the repository-first recovery/revalidation/cross-AI continuity baseline.
- **P12 Operational Intelligence** remains the advisory/runtime-observability and durable recovery substrate used by later governed execution paths.
- P11/P12 are historical completed foundations; later unnumbered objectives must not be re-labeled as new numbered phases.

## Universal portability invariant
`AI A + Account A → repository → AI B + Account B → correct state recovery → safe continuation`

The repository, not any AI account/chat/model/vendor memory, carries authoritative project state.

## Core safety invariants
- `PLAN != EXECUTION`
- `READY != EXECUTION`
- `INTERPRETATION != AUTHORIZATION`
- `OLD APPROVAL != NEW APPROVAL` when scope/freshness/security changes
- `FULL APPROVAL != BLANKET PERMISSION`
- `PROVIDER CREDENTIAL != DEVOS AUTHORIZATION`
- `SIMULATED EVIDENCE != LIVE PROVIDER PROOF`
- `CHAT MEMORY != SOURCE OF TRUTH`
- `PROVIDER RESPONSE != COMPLETION PROOF`
- `RECOVERY != AUTOMATIC MUTATION REPLAY`
- `REPOSITORY DELETE != REPOSITORY CREATE`
- `BRANCH DELETE != BRANCH CREATE`
- `NORMAL BRANCH UPDATE != FORCE UPDATE`
