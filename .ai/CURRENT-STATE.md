# Current State

## Snapshot

- Repository: `zzpsah/chatgpt-development-os`.
- Source tree + Git are authoritative for implementation and exact project state; ChatGPT Memory/chat history are supplementary only.
- P11 Federation & Self-Healing Context remains the repository-first recovery/revalidation/cross-AI continuity baseline.
- P9 through P17 are complete on `main`.
- Production E2E Harness, Failure + Recovery Proof, Multi-Session / Fresh-AI Continuation Proof, Controlled Remote Mutation Proof, Trust-First audit gap closure, Production-Readiness Evidence Matrix, Foundation Health & State Consistency, Cross-Host Recovery Friction & Onboarding Proof, and Recovery Friction → Foundation Health/Doctor Integration are closed at their stated evidence levels.
- **Active dependency chain: Universal Project Onboarding + Repository Creation (PR #19), followed by host-neutral MCP/App `repository.create` adapter reconciliation (PR #22).**
- The previously started **Current-Source Evidence Refresh Protocol** remains preserved but paused until PR #19/#22 are stable; it is not discarded and is not independently promoted.
- Product invariant: DevOS is a Development OS for AI across vendors, models, accounts, coding agents, sessions, machines, and Git-provider adapters; no AI account/chat/model/vendor memory is authoritative project state.

## Canonical governed path

`Human request → P15 interpretation → P16 plan → P17 readiness → controller → bounded runtime → verification → persistence → recovery / continuation`

Interpretation, planning, readiness, provider credentials, prior approvals, prior successful runs, recovery checkpoints, continuation packets, and simulated provider evidence never manufacture permission.

## Universal Project Onboarding + Repository Creation — ACTIVE PR #19

PR #19 adds provider-independent universal onboarding and the governed `repository.create` capability while preserving the repository as the durable cross-AI source of truth.

Normative contracts:
- `core/devos-universal-project-onboarding.md`
- `core/devos-universal-onboarding-policy.md`
- `core/devos-repository-creation-capability.md`

Implementation:
- `tools/devos-onboard.py` — cross-platform idempotent onboarding; read-only plan by default; apply creates only missing DevOS infrastructure.
- `tools/test-devos-onboard.py` — preservation/idempotency/new-project/incompatible-framework regression corpus.
- `tools/devos-create-repository.py` — provider-neutral repository creation reference adapter with GitHub REST support, explicit apply/authorization/safety gates, one mutation request maximum per governed attempt, and no completion claim without fresh readback.
- `tools/test-devos-create-repository.py` — deterministic capability/authorization/timeout/no-secret-leak regression corpus.

Repository creation is a separate high-impact remote mutation capability. Provider capability, provider credentials, DevOS authorization, P17 readiness, and execution remain distinct. The built-in ChatGPT GitHub connector does not expose repository creation, so connector use must preserve the capability-unavailable path rather than imply a live create.

PR #22 is stacked on PR #19 and must be reconciled only after PR #19 reaches a fresh exact-head verified state.

## Production-readiness evidence boundary

The v1 readiness ledger remains conservative:
- `production_ready = false`;
- live mutation proof remains false;
- controlled remote mutation remains provider-simulated / contract-level evidence;
- historical evidence stays pinned to the original source/run heads;
- current-source divergence is exposed as `historical_source_drift` and is never silently refreshed.

The persistent known drift remains `tools/test-step-readiness-orchestrator.py`. That historical evidence is still valid only for its pinned source. A current-source claim requires separate new evidence rather than rewriting history.

## Foundation Health & State Consistency — CLOSED

Architecture:

`Source / Git / Tests / CI → devos-audit.py → readiness evidence ledger → recovery-friction evidence → devos-health.py → devos-doctor.py`

Normative contract: `core/foundation-health-state-consistency.md`.
Machine health: `tools/devos-health.py`.
Presentation: `tools/devos-doctor.py`.
Adversarial gate: `tools/test-foundation-health.py`.

Foundation Health final source head: `77a8f6f8d8ce012d872b20343bded2e00c53ed7d`.
PR #18 merge commit: `657ae461c0d6df62ca428d8bdd0404bd241b5c84`.
Post-merge main verification: Trust-First 33 / `34764171968`, Contracts 570 / `34764171939`, Full DevOS 495 / `34764171923`: success.

Health/doctor remain READ_ONLY with authority/authorization unchanged and execution/mutation NONE. WARN/UNKNOWN are never PASS.

## Cross-Host Recovery Friction & Onboarding Proof — CLOSED

Analyzer: `tools/recovery-friction.py`.
Protocol: `DEVOS-RECOVERY-FRICTION-v1`.
Normative contract: `core/cross-host-recovery-friction.md`.

Final source head: `55b3a8e64ecefae6058529ea18c6ca04b80d2860`.
PR #20 merge commit: `4161abf357bbca1e8bb844c7d87f74cfb34b94e6`.
Fresh post-merge main: Trust-First 42 / `34764727276`, Contracts 579 / `34764727340`, Full DevOS 504 / `34764727299`: success.
Closure-state main `9258a5e53be542b6ed246ed5c72155f1521b80e7`: Trust-First 45 / `34764829953`, Contracts 582 / `34764829874`, Full DevOS 507 / `34764829850`: success.

Evidence classification remains `DETERMINISTIC_HOST_PROFILE_SIMULATION`; `real_cross_vendor_account_proven` remains false. Recovery success is distinct from continuation capability. Friction units are transparent issue counts, not readiness/authorization/probability scores.

## Recovery Friction → Foundation Health/Doctor Integration — CLOSED

Final source head: `869a95894dad5feaafcbc286ec1fb0027c8321df`.
PR #21 merge commit: `c3c7597a5b475c7060efc8fb9e6df81f88716e8c`.

Fresh exact-final-head PR verification:
- Trust-First Audit 54 / `34765090674`: success.
- Contracts 591 / `34765090663`: success.
- Full DevOS 516 / `34765090662`: success.

Fresh post-merge `main` verification at `c3c7597a5b475c7060efc8fb9e6df81f88716e8c`:
- Trust-First Audit 55 / `34765164604`: success.
- Contracts 592 / `34765164610`: success.
- Full DevOS 517 / `34765164649`: success.

The integration adds one subordinate `cross_host_recovery` row to Foundation Health by invoking the existing recovery-friction analyzer. `devos-doctor.py` only renders the health-supplied result; it does not independently recompute recovery truth.

Conservative propagation is proven for missing/malformed host profile evidence, stale expected HEAD, critical host capability gaps, canonical identity tampering, and simulated-evidence non-promotion. No live/destructive/provider mutation was performed.

## Paused bounded objective — Current-Source Evidence Refresh Protocol

The known historical-source drift still requires a reviewed way to add **new current-source evidence** without mutating or relabeling historical records. This work is preserved but paused behind the active onboarding/MCP dependency chain.

Requirements remain:
- preserve historical ledger rows and archived provenance unchanged;
- bind current-source evidence to exact source head, test path/digest, observed verification result and CI context;
- prove only the level actually observed;
- never infer live-provider/production proof from deterministic or integrated CI;
- extend the existing readiness evidence system rather than create another truth ledger;
- keep evidence refresh non-authorizing and read-only with respect to project/runtime execution.

## Controlled Remote Mutation evidence boundary

The existing controlled mutation proof remains provider-simulated / contract-level only. Provider mutation response is attempt evidence, not completion proof, and failed/uncertain mutation does not authorize automatic replay.

Still unproven unless separately explicitly authorized and bounded:
- live real-provider DevOS runtime mutation proof;
- branch/PR/workflow/deployment/production mutation;
- database mutation;
- permission/credential/secret mutation;
- destructive mutation.

## Safety invariants

```text
PLAN != EXECUTION
READY != EXECUTION
INTERPRETATION != AUTHORIZATION
OLD APPROVAL != NEW APPROVAL
PROVIDER CREDENTIAL != DEVOS AUTHORIZATION
SIMULATED EVIDENCE != LIVE PROVIDER PROOF
CHAT MEMORY != SOURCE OF TRUTH
PROVIDER RESPONSE != COMPLETION PROOF
RECOVERY != AUTOMATIC MUTATION REPLAY
```

## Universal AI/account portability gate

`AI A + Account A → repository → AI B + Account B → correct state recovery → safe continuation`

A fresh AI must recover authoritative state from repository evidence without the previous AI's hidden memory. Host-specific capabilities remain adapter concerns; authorization rules do not change with vendor/model/account.

## Recovery precedence

1. Current source tree + Git.
2. Explicit requirements/decisions.
3. `.ai/CURRENT-STATE.md`, `.ai/TASKS.md`, and semantic `.ai` state.
4. `.ai/SESSIONS/` provenance.
5. Generated indexes as navigation/evidence only.
6. ChatGPT Memory/chat history as supplementary context only.

## Stable handoff

Stable AI discovery path: `docs/handoff/README.md`.
Historical evidence snapshots remain dated and do not auto-refresh when source advances. Exact implementation remains authoritative in Git history.
