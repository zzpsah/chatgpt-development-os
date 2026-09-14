# DevOS Tasks

## How to read this file

This file tracks **work state**, not normative law. Current source/Git/PR/CI are authoritative for exact implementation state. Durable principles and authorization/security decisions live in `.ai/DECISIONS.md` and core contracts. Historical milestone detail lives in `docs/DEVOS-ENGINEERING-STAGE-HISTORY.md` and `.ai/SESSIONS/`.

## Core safety invariants

- **What is not written was never done.**
- `CONTINUE != BLANKET AUTHORIZATION`.
- `READY != EXECUTION`.
- `CI PASS != AUTHORIZATION`.
- provider credentials/capability never manufacture DevOS authority.
- declared runtime identity never manufactures verified runtime capability.
- `production_ready = false` unless a separately bounded evidence-backed decision changes it.

## Active bounded work

- No bounded engineering objective is active after Agent Runtime Profile Registry + Conformance v1 closure.
- Concurrent software-delivery/managed-repository work must be rediscovered from fresh source before continuation.
- Choose future work only from fresh `main`, open PRs, current CI, durable state, relevant source/tests, and current user intent. Do not create P18/P19 merely for bookkeeping.

## Completed — Agent Runtime Profile Registry + Conformance v1

- PR #59 — `Add agent runtime profile registry v1` — merged at `d426ccf480e48544e8078ab7b61065ffd6b18f48`.
- Exact verified feature head: `447e8fbaee96eb0be22e9a59d75da147dbcbb8ac`.
- Adds `config/agent-runtime-profile-registry.json`, deterministic validator/exporter `tools/agent-runtime-profile-registry.py`, adversarial regression corpus, normative contract, dedicated CI, and session evidence.
- Required verified capabilities are `filesystem.read`, `filesystem.write_scoped`, `git.inspect`, and `verification.run`.
- `reference-local-agent` is verified only for repository static-contract conformance.
- `codex`, `claude-code`, and `openhands` remain `DECLARED` templates and HOLD for runtime handoff until separate evidence-backed conformance proof exists.
- A forged status change to `VERIFIED` without complete capabilities/evidence fails closed; unknown capabilities, duplicate IDs, missing required capabilities, revoked profiles, and unregistered runtimes also fail closed.
- Exact feature-head successful runs: Runtime Profile Registry `34818246952`; Agent Runtime Adapter `34818246907`; Current-Source Evidence `34818246910`; MCP Repository Create `34818246875`; Trust-First Audit `34818246940`; Development OS `34818246896`; Contracts `34818246842`; Evidence Durable Reconciliation `34818246846`; Isolated Managed Repository Write Proof `34818246855`; Managed Repository Preflight `34818246913`.
- Reconciliation ledger record digest: `4a613b466092c9c1e811ab16e6fe8af41dfc08668b74312e8c69b3b9d909d7e1`.
- No agent invocation, target-repository mutation, provider operation, approval grant, deployment, credential, database, permission, destructive action, or production-readiness upgrade was introduced.

## Completed — Isolated Managed-Repository Write Proof v1

- Main feature head `2ef6b6e3df832ca132123b85caa69f7eda67d1f3` proves one actual file update in a newly created isolated local Git fixture after read-only preflight and exact derived approval.
- Diff, test, final readback, runtime validation, and external evidence packet agree; no commit or push occurs.
- This is not proof of an existing managed-repository write or provider mutation.

## Completed — Managed-Repository Delivery v1 Read-Only Preflight

- Main feature head `fda3e3a6db624d69d6d651cd531c537ad579c9cd` adds deterministic clean-worktree/HEAD/path preflight through P15 → P16 → P17.
- It returns an exact scoped approval request and `HOLD`; external evidence output is forbidden inside the inspected checkout.
- No managed-repository mutation, provider operation, commit, push, deployment, production, credential, database, permission, destructive action, or approval grant was performed.

## Completed — Universal Agent Runtime Adapter v1

- PR #57 merged at `5d0bdbc0258e898ece21f99937dc4f5b886778a0`; exact verified feature head `da57d48c1ec28eac71eff75b59f9c701e9c9c593`.
- Adds a vendor-neutral P17 READY + exact-approval handoff compiler and result validator.
- Validation binds repository head, scope, runtime profile, targets, allowed operations, diff/test/readback evidence, and permanent safety boundaries.
- The adapter is side-effect-free and does not itself wire a vendor runtime or mutate a managed repository.

## Completed — Local Disposable Delivery Proof v1

- Main commit `1f735fa11e19b9852ce9210338bc0907ab0b5b1c` proves P15 → P16 → P17 → scoped approval → local update → test/readback → durable evidence → fresh recovery in a temporary Git repository.
- The proof excludes commit/push/provider/deployment/production/credential/database/permission/destructive operations.

## Completed — Automated Evidence → Durable State Reconciliation v1

- PR #54 merged at `e31c2099b5d9ce88ee4a20c225fe70b424dffa3d`; exact feature head `a2da0eaf2a5464d4a716859168bf0ba4d87659a6`.
- Machine-verifiable facts can be normalized deterministically; semantic CURRENT/TASKS/roadmap meaning still requires review.
- Reconciliation records remain authority-neutral and `production_ready=false`.

## Completed — P15 bounded Devanagari Hindi/Hinglish interpretation and gating

- Main commit `001f48e64d3e7e6e32d9befc9bb00899b8868e03` preserves Unicode Hindi and adds bounded multilingual corpus plus P15 → P16 → P17 regression.
- High-impact Hindi remains independently production/destructive and authorization-gated; negative deployment wording blocks conflicting plans; unresolved referents clarify.

## Completed — AI State Resolver v2 hardening sequence

- PR #44 — envelope integrity.
- PR #46 — explicit cross-claim contradiction identity/handling.
- PR #49 — downstream P16/P17 independent contradiction recomputation and tamper defense.
- PR #52 — detailed contradiction provenance and downstream detail validation.
- Closed/stale duplicate PRs remain historical provenance only and are never substituted for merged current source.

## Completed — previous-stage documentation ledger

- `docs/DEVOS-ENGINEERING-STAGE-HISTORY.md` is the durable navigation ledger for P9–P17 and major unnumbered milestones.
- `docs/DEVOS-MASTER-ENGINEERING-MAP.md` is the living architecture/future-flow map.
- `core/agent-runtime-profile-registry.md` is the runtime declaration/conformance contract.
- `core/evidence-durable-state-reconciliation.md` is the evidence-to-durable-state contract.
- `docs/AI-STATE-RESOLVER-CROSS-CLAIM-CONTRADICTIONS.md` is the resolver contradiction contract.

## Retained platform foundations

- P9 through P17 remain completed architecture stages at their recorded evidence levels.
- P11 remains repository-first recovery/revalidation/cross-AI continuity baseline.
- P12 remains evidence provenance/freshness owner.
- P15 remains language interpretation; P16 planning; P17 readiness/authorization.
- GitHub governed provider capability, readback reconciliation, multi-project isolation, Actionable HOLD, current-source evidence, onboarding, recovery, adaptive verification/self-healing, and trust-first auditing remain retained foundations.

## Current HOLD / limits

- `production_ready = false`.
- Machine evidence and reconciliation records never grant authorization, execution, completion authority, or provider permission.
- A `DECLARED` runtime profile is not a verified integration.
- Semantic CURRENT/TASKS/roadmap changes require review; commit messages are not semantic truth.
- Uncertain provider mutation is never blindly replayed.
- Parallel AI branches must revalidate against fresh `main` before integration.

## Task-map invariant

`AI A + Account A → repository → AI B + Account B → correct recovery → safe continuation`

The repository, not any AI account/chat/model/vendor memory, carries authoritative project state.
