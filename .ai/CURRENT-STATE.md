# Current State

## Snapshot

- Repository: `zzpsah/chatgpt-development-os`.
- Source tree + Git are authoritative for implementation and exact project state; ChatGPT Memory/chat history are supplementary only.
- P11 Federation & Self-Healing Context remains the repository-first recovery/revalidation/cross-AI continuity baseline.
- P9 through P17 are complete on `main`.
- Production E2E Harness, Failure + Recovery Proof, Multi-Session / Fresh-AI Continuation Proof, Controlled Remote Mutation Proof, Trust-First audit gap closure, Production-Readiness Evidence Matrix, and Foundation Health & State Consistency are closed at their stated evidence levels.
- **Active bounded objective: Cross-Host Recovery Friction & Onboarding Proof.** This is unnumbered; no P18/P19 phase is created.
- Product invariant: DevOS is a Development OS for AI across vendors, models, accounts, coding agents, sessions, machines, and Git-provider adapters; no AI account/chat/model/vendor memory is authoritative project state.

## Canonical governed path

`Human request → P15 interpretation → P16 plan → P17 readiness → controller → bounded runtime → verification → persistence → recovery / continuation`

Interpretation, planning, readiness, provider credentials, prior approvals, prior successful runs, recovery checkpoints, continuation packets, and simulated provider evidence never manufacture permission.

## PR #16 readiness-evidence closure

PR #16 final source head: `6c509d6f65b22666f121dfe86604faae72c08f8c`.
Merge commit on `main`: `b8e31ae76201b32e4617ef6044b29ef285004f54`.

Fresh post-merge `main` verification at `b8e31ae76201b32e4617ef6044b29ef285004f54`:
- Trust-First Audit 23 / `34762783110`: success.
- Contracts 560 / `34762783133`: success.
- Full DevOS 485 / `34762783132`: success.
- External Managed Project has no push trigger for this merge and therefore has no fabricated post-merge run.

The v1 readiness ledger remains conservative:
- `production_ready = false`;
- live mutation proof remains false;
- controlled remote mutation remains provider-simulated / contract-level evidence;
- historical evidence remains pinned to original source/run heads;
- current-source changes are exposed as `historical_source_drift`, never silently re-pointed.

## Foundation Health & State Consistency — CLOSED

Normative contract: `core/foundation-health-state-consistency.md`.
Authoritative audit input: `tools/devos-audit.py`.
Machine-readable evidence input: `config/readiness-evidence.json` via `tools/verify-readiness-evidence.py`.
Machine-derived health: `tools/devos-health.py`.
Human presentation: `tools/devos-doctor.py`.
Adversarial regression gate: `tools/test-foundation-health.py`.

Architecture:

`Source / Git / Tests / CI → devos-audit.py → readiness evidence ledger → machine-derived status → devos-doctor.py`

This is not a second truth system. `devos-doctor.py` remains a read-only presentation/diagnostic layer over the Trust-First audit and readiness evidence system.

Foundation Health final source head: `77a8f6f8d8ce012d872b20343bded2e00c53ed7d`.
PR #18 merge commit: `657ae461c0d6df62ca428d8bdd0404bd241b5c84`.

Fresh exact-final-head PR verification:
- Trust-First Audit 29 / `34763332363`: success.
- Contracts 566 / `34763332344`: success.
- Full DevOS 491 / `34763332347`: success.

Fresh post-merge `main` verification at `657ae461c0d6df62ca428d8bdd0404bd241b5c84`:
- Trust-First Audit 33 / `34764171968`: success.
- Contracts 570 / `34764171939`: success.
- Full DevOS 495 / `34764171923`: success.

The health layer conservatively surfaces historical source drift instead of rewriting it. At closure, `tools/test-step-readiness-orchestrator.py` remains historical-source drift in the readiness ledger; this is WARN, not PASS promotion and not evidence refresh.

All health/doctor output preserves:
- `mode: READ_ONLY`;
- `authority: UNCHANGED`;
- `authorization: UNCHANGED`;
- `execution: NONE`;
- `mutation: NONE`.

Conservative outcomes remain `PASS`, `WARN`, `UNKNOWN`, `FAIL`, and `BLOCKED`. `WARN` and `UNKNOWN` are never treated as `PASS`.

## Active bounded objective — Cross-Host Recovery Friction & Onboarding Proof

Existing capabilities already prove repository-only recovery contracts, Multi-AI portability contracts, host profiles, auto-onboarding contracts, and fresh-AI recovery source presence. The remaining gap is **measurable adoption/recovery friction** rather than another portability prose contract.

Goal:
- measure whether a fresh host can recover canonical repository identity, current state, active work, decisions, safety boundaries, and continuation entrypoints from repository evidence only;
- quantify missing/ambiguous recovery inputs instead of calling them success;
- compare host-profile capability gaps without changing authorization rules;
- produce machine-readable deterministic evidence suitable for CI and later doctor presentation;
- keep the entire objective READ_ONLY and repository-local.

This objective must not claim that a simulated host profile proves a real independent AI vendor/account trial. Cross-vendor/account claims remain UNKNOWN unless separately observed.

## Foundation Bootstrap Hardening

Normative contract: `core/devos-bootstrap-contract.md`.
Bootstrap checker: `tools/devos-bootstrap.py`.
Regression coverage: `tools/test-devos-bootstrap.py`.

The bootstrap checker is deterministic and read-only. A bootstrap PASS is structural evidence only; it does not grant authorization, prove feature correctness, or claim production readiness.

## Controlled Remote Mutation evidence boundary

The existing controlled mutation proof is provider-simulated / contract-level proof only. Normal GitHub repository edits used to develop DevOS are development actions through connected tooling and are not treated as DevOS runtime mutation-proof evidence.

Still unproven or unavailable unless separately explicitly authorized and bounded:
- live real-provider DevOS runtime mutation proof;
- branch/pull-request/workflow mutation through the governed runtime;
- deployment/production mutation;
- database mutation;
- permission/credential/secret mutation;
- destructive mutation.

Provider mutation response is attempt evidence, not completion proof. Failed/uncertain mutation does not authorize automatic replay.

## Safety invariants

```text
PLAN != EXECUTION
READY != EXECUTION
INTERPRETATION != AUTHORIZATION
OLD APPROVAL != NEW APPROVAL
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
The historical handoff evidence snapshot is intentionally dated and does not auto-refresh when source advances. Exact implementation remains authoritative in Git history.
