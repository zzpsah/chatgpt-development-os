# DevOS Tasks

## How to read this file

This file tracks **work state**, not normative law. Current source/Git/PR/CI/release-artifact metadata are authoritative for exact implementation state. Durable principles and authorization/security decisions live in `.ai/DECISIONS.md` and core contracts. Historical milestone detail lives in `docs/DEVOS-ENGINEERING-STAGE-HISTORY.md` and `.ai/SESSIONS/`.

## Core safety invariants

- **What is not written was never done.**
- `CONTINUE != BLANKET AUTHORIZATION`.
- `INTERPRETATION != AUTHORIZATION`.
- `PLAN != EXECUTION`.
- `READY != EXECUTION`.
- `CI PASS != AUTHORIZATION`.
- provider credentials/capability never manufacture DevOS authority.
- declared runtime identity never manufactures verified runtime capability.
- a valid runtime conformance evidence packet never self-promotes a registry entry.
- distribution release readiness never manufactures production or publication authority.
- `production_ready = false` unless a separately bounded evidence-backed decision changes it.

## Active bounded work

- No numbered feature milestone is active.
- No unreconciled implementation objective remains for DevOS `0.18.0` after PR #64 durable reconciliation.
- Future work must start from fresh `main`, CI/issues/PRs, source/tests, runtime evidence, concurrent AI work, and current user intent.
- Do not create P18/P19 merely for bookkeeping.

## Completed — DevOS 0.18.0 Agent Runtime Conformance Evidence Intake v1

- [x] Define exact runtime/adapter/Git-head/nonce challenge protocol.
- [x] Bind challenges with canonical SHA-256 identity.
- [x] Validate exactly the required runtime capability evidence set.
- [x] Require invocation provenance shape and SHA-256 evidence digests.
- [x] Fail closed on tamper, mismatch, replay, missing/extra capabilities, malformed provenance, and invalid digests.
- [x] HOLD when a required capability probe reports failure.
- [x] Prevent candidate evidence from self-promoting runtime verification or registry mutation.
- [x] Add adversarial regression corpus and dedicated runtime-profile CI coverage.
- [x] Move distribution metadata coherently to `0.18.0` rather than reuse the 0.17.0 source identity.
- [x] Verify all applicable CI on exact feature head `f59fad07b6f7708cfc79f173625f9ddafa7bc5ae` — 13/13 success.
- [x] Merge PR #64 at `a8f19687c177359bd5f646e10913ebdae0851a53`.
- [x] Verify fresh post-merge `main` — 10/10 exact-SHA push workflows success.
- [x] Verify exact-source 0.18.0 release matrix — Ubuntu + Windows × Python 3.11 + 3.12 success.
- [x] Verify exact-source artifact: ID `10342221168`, digest `sha256:894e369966e5172c609a6008c5f7086a78622b81b7f2794fa93990a88b09caf7`.
- [x] Reconcile merge/CI/artifact evidence into durable state; record digest `7c08b334ebfedbf9951b8d384313e92a894c83dbb8283b77c7221fb1ad113a99`.

No vendor runtime was promoted. `codex`, `claude-code`, and `openhands` remain declaration-only unless a later separately observed direct conformance proof is reviewed and merged. `EVIDENCE_PACKET_VALID != VERIFIED RUNTIME`.

## Completed — DevOS 0.17.0 Distribution Release Readiness v1

- PR #61 merged at `ecee10168b43d13430dd71c2e8d85556956f56a6`; exact verified feature head `b4f46eb7919177e3a0dc19d902401630cd6c12ec`.
- Established canonical `VERSION`, release manifest, current README/changelog, public security policy, release process, cross-platform CLI, fail-closed release checker, adversarial release tests, and Ubuntu/Windows Python 3.11/3.12 distribution CI.
- Exact-source `git archive` ZIP + SHA-256 publication artifact strategy is retained by 0.18.0.
- Historical exact-head workflow/artifact evidence remains pinned in durable session/ledger records.

## Completed — Agent Runtime Profile Registry + Conformance v1

- PR #59 merged at `d426ccf480e48544e8078ab7b61065ffd6b18f48`; exact verified feature head `447e8fbaee96eb0be22e9a59d75da147dbcbb8ac`.
- Required verified capabilities are `filesystem.read`, `filesystem.write_scoped`, `git.inspect`, and `verification.run`.
- `reference-local-agent` is verified only for recorded static conformance; `codex`, `claude-code`, and `openhands` remain `DECLARED` and HOLD without separate direct evidence.
- Forged VERIFIED state, missing/unknown capabilities, duplicate IDs, revoked profiles, and unregistered runtimes fail closed.

## Completed — Universal Agent Runtime Adapter v1

- PR #57 merged at `5d0bdbc0258e898ece21f99937dc4f5b886778a0`.
- Adds a vendor-neutral P17 READY + exact-approval handoff compiler and independent result validator.
- The adapter is side-effect-free and does not itself invoke a vendor runtime or mutate a managed repository.

## Completed — Safe delivery proof line

- Local Disposable Delivery Proof v1 proves bounded local Git update/test/readback/evidence in a temporary repository.
- Managed-Repository Delivery v1 Read-Only Preflight binds clean worktree/head/path evidence and returns HOLD before mutation.
- Isolated Managed-Repository Write Proof v1 proves one safe scoped file update in a newly created isolated fixture with diff/test/readback/evidence and no commit/push/provider/deploy action.

## Completed — Automated Evidence → Durable State Reconciliation v1

- PR #54 merged at `e31c2099b5d9ce88ee4a20c225fe70b424dffa3d`.
- Machine-verifiable facts can be normalized deterministically; semantic CURRENT/TASKS/roadmap meaning still requires review.
- Reconciliation records remain authority-neutral and `production_ready=false`.

## Retained platform foundations

- P9 through P17 remain completed architecture stages at their recorded evidence levels.
- P11 remains repository-first recovery/revalidation/cross-AI continuity baseline.
- P12 remains evidence provenance/freshness owner.
- P15 remains language interpretation; P16 planning; P17 readiness/authorization.
- AI State Resolver v2 envelope/contradiction hardening remains closed through its recorded PR sequence.
- GitHub governed provider capability, readback reconciliation, multi-project isolation, Actionable HOLD, current-source evidence, onboarding, recovery, adaptive verification/self-healing, trust-first auditing, runtime-neutral handoff, runtime-profile registry, and runtime-conformance evidence intake remain retained foundations.
- `docs/DEVOS-ENGINEERING-STAGE-HISTORY.md` is the durable navigation ledger for numbered and major unnumbered milestones.
- `docs/DEVOS-MASTER-ENGINEERING-MAP.md` remains the living architecture/future-flow map.

## Current HOLD / limits

- `production_ready = false`.
- Distribution release readiness is not publication or production authorization.
- No public Git tag/GitHub Release/package publication is created by this reconciliation.
- Machine evidence and reconciliation records never grant authorization, execution, completion authority, provider permission, or production readiness.
- A `DECLARED` runtime profile is not a verified integration.
- `EVIDENCE_PACKET_VALID` is not direct runtime verification and is not registry-promotion authority.
- Historical readiness evidence remains pinned to its source head.
- Uncertain provider mutation is never blindly replayed.
- Parallel AI branches must revalidate against fresh `main` before integration.

## Task-map invariant

`AI A + Account A → repository → AI B + Account B → correct recovery → safe continuation`

The repository, not any AI account/chat/model/vendor memory, carries authoritative project state.
