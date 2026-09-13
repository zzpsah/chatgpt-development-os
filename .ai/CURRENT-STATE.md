# Current State

## Snapshot

- Repository: `zzpsah/chatgpt-development-os`.
- Source tree + Git are authoritative for implementation and exact project state; ChatGPT Memory/chat history are supplementary only.
- P11 Federation & Self-Healing Context remains the repository-first recovery/revalidation/cross-AI continuity baseline.
- P9 through P17 are complete on `main`.
- Production E2E Harness, Failure + Recovery Proof, Multi-Session / Fresh-AI Continuation Proof, Controlled Remote Mutation Proof, Trust-First audit gap closure, Production-Readiness Evidence Matrix, Foundation Health & State Consistency, Cross-Host Recovery Friction & Onboarding Proof, Recovery Friction → Foundation Health/Doctor Integration, Universal Project Onboarding + Repository Creation, host-neutral MCP/App `repository.create`, and Current-Source Evidence Refresh are closed at their stated evidence levels.
- Universal Project Onboarding + Repository Creation merged through PR #19.
- Host-neutral MCP/App `repository.create` adapter merged through PR #22.
- Current-Source Evidence Refresh merged through PR #24.
- Current verified `main`: `a93f9f435ffab5f81ce070f07a0da694757ab6cb`.
- Fresh post-merge verification at that head: Trust-First 72 / `34774013758`, Contracts 609 / `34774013791`, Full DevOS 531 / `34774013827` — success.
- No new numbered phase is active or implied by this closure state.
- Product invariant: DevOS is a Development OS for AI across vendors, models, accounts, coding agents, sessions, machines, and Git-provider adapters; no AI account/chat/model/vendor memory is authoritative project state.

## Canonical governed path

`Human request → P15 interpretation → P16 plan → P17 readiness → controller → bounded runtime → verification → persistence → recovery / continuation`

Interpretation, planning, readiness, provider credentials, prior approvals, prior successful runs, recovery checkpoints, continuation packets, and simulated provider evidence never manufacture permission.

## Universal onboarding / repository creation — CLOSED AT CURRENT EVIDENCE LEVEL

PR #19 added provider-independent universal onboarding and governed `repository.create` semantics.
PR #22 added the host-neutral MCP/App boundary over that capability.

Preserved distinctions:

```text
ChatGPT connector capability
!= provider capability
!= DevOS authorization
!= P17 readiness
!= execution
```

The built-in ChatGPT GitHub connector does not expose repository creation. The capability-unavailable path therefore remains `NEEDS_EXTERNAL_REPO_CREATION`; no live ChatGPT repository creation is claimed.

Repository creation remains a high-impact remote mutation. Provider credentials are not DevOS authorization. A provider response is attempt evidence, not completion proof. Uncertain mutation is not blindly replayed.

No live repository creation, production mutation, destructive mutation, credential/secret mutation, permission mutation, or deployment mutation was performed for this evidence.

## Current-Source Evidence Refresh — CLOSED

Purpose: add fresh proof for exact current source without rewriting historical readiness evidence.

Architecture:

`current source + exact HEAD + ledger-declared test + SHA-256 + observed result → current-source-evidence.py → ephemeral validated packet → Foundation Health → DevOS Doctor`

Implementation:

- `tools/current-source-evidence.py`
- `tools/test-current-source-evidence.py`
- `tools/test-current-source-health-integration.py`
- `.github/workflows/verify-current-source-evidence.yml`
- `core/current-source-evidence.md`
- `docs/CURRENT-SOURCE-EVIDENCE.md`
- optional packet consumption in `tools/devos-health.py`
- presentation in `tools/devos-doctor.py`

Protocol: `DEVOS-CURRENT-SOURCE-EVIDENCE-v1`.

The packet binds:
- exact Git `source_head`;
- ledger-declared capability, level and test path;
- SHA-256 of current test bytes;
- observed exit code;
- local or current CI execution context.

Current-source evidence is ephemeral and additive. It never mutates or relabels historical rows in `config/readiness-evidence.json`.

Rule:

`CURRENT_EVIDENCE_ADDS_PROOF_BUT_NEVER_REWRITES_HISTORICAL_PROVENANCE`

Historical `source_head`, run IDs, archive digest, and `freshness: historical` remain pinned.

Foundation Health validates an optional packet but never executes its test. Historical drift remains visible as WARN even when an exact current packet proves the drifted test at the current head. Doctor only renders the Health result.

PR #24 final source head: `bc400112d0bbaced6ed699a6863bc8dcf91e47c8`.
Final exact-head PR verification:
- Current-Source Evidence 12 / `34773566913`: success.
- Trust-First Audit 71 / `34773566958`: success.
- Contracts 608 / `34773566914`: success.
- Full DevOS 530 / `34773566926`: success.
- MCP Repository Create 9 / `34773566919`: success where path-applicable.

PR #24 merge commit: `a93f9f435ffab5f81ce070f07a0da694757ab6cb`.
Fresh post-merge `main` verification:
- Trust-First Audit 72 / `34774013758`: success.
- Contracts 609 / `34774013791`: success.
- Full DevOS 531 / `34774013827`: success.

The dedicated Current-Source Evidence workflow does not have a `main` push trigger, so no fabricated post-merge dedicated run is claimed.

## Production-readiness evidence boundary

The readiness ledger remains conservative:
- `production_ready = false`;
- live mutation proof remains false;
- current-source packets require `live_provider_proven = false`;
- controlled remote mutation remains provider-simulated / contract-level evidence;
- historical evidence stays pinned to original source/run heads;
- source divergence remains `historical_source_drift` and is never silently refreshed.

The known historical drift includes `tools/test-step-readiness-orchestrator.py`. A valid current packet may add exact current proof for that test, but the historical row remains historical and visible.

## Foundation Health & State Consistency

Authoritative composition remains:

`Source / Git / Tests / CI → devos-audit.py → readiness evidence ledger → subordinate evidence inputs → devos-health.py → devos-doctor.py`

`devos-health.py` is a machine-derived composition layer, not a competing truth source.
`devos-doctor.py` is presentation-only.

Health/Doctor remain READ_ONLY with:
- authority `UNCHANGED`;
- authorization `UNCHANGED`;
- execution `NONE`;
- mutation `NONE`.

WARN/UNKNOWN are never PASS.
Malformed/tampered current-source packets are BLOCKED; a requested missing packet is UNKNOWN.

## Cross-host recovery boundary

Cross-host recovery/friction evidence remains deterministic host-profile simulation unless separate real cross-vendor/account evidence is obtained.

`real_cross_vendor_account_proven=false` remains conservative.

Universal portability invariant:

`AI A + Account A → repository → AI B + Account B → correct state recovery → safe continuation`

## Controlled Remote Mutation evidence boundary

Controlled mutation evidence remains provider-simulated / contract-level only. Provider mutation response is attempt evidence, not completion proof, and failed/uncertain mutation does not authorize automatic replay.

Still unproven unless separately explicitly authorized and bounded:
- live real-provider DevOS runtime mutation proof;
- branch/PR/workflow/deployment/production mutation proof as a product capability;
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
