# DevOS Tasks

## Active
- **Remote Resource Permission Control Plane integration** is the active unnumbered bounded objective.
- It exists because DevOS is intended to operate as a long-lived agent across multiple repositories, and provider/API write access must not be treated as blanket authority.
- The control plane governs `repository.create`, `repository.delete`, `branch.create`, `branch.update`, `branch.force_update`, and `branch.delete` with exact project/repository/resource/workflow/impact/freshness scope.
- The MCP/App host adapter must route remote mutation eligibility through this control plane before provider execution.
- `continue` may reuse a valid scoped approval; a new repository/branch/capability/impact/freshness/security scope requires a new approval and actionable HOLD.
- API tokens/credentials are provider capabilities only; they are never DevOS authorization and must remain outside `.ai/`, MCP arguments, logs, and model output.
- This objective is unnumbered; do not create P18/P19 for bookkeeping.
- No live/destructive/production provider mutation is required for closure; deterministic and integrated evidence must remain distinct from live-provider proof.

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
