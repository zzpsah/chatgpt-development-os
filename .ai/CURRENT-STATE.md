# Current State

## Current source and authority

- Repository: `zzpsah/chatgpt-development-os`.
- Current source tree + Git/PR/CI/release-artifact metadata are authoritative for exact implementation/integration state; `.ai` records carry durable semantic context.
- **ChatGPT Memory/chat history and any model/account memory are supplementary only and never authoritative project state.**
- Latest fully merged/reconciled source before the active objective: PR #65 at `b221a240a41426b200a9235eacfa5300042936c0`.
- Active feature branch: `feature/production-readiness-evidence-v2`, created from exact `b221a240a41426b200a9235eacfa5300042936c0`.
- Candidate distribution version on the active branch: `0.19.0`.
- Historical `config/readiness-evidence.json` remains pinned v1 evidence and is not rewritten as current proof.
- Current production-readiness model: `config/production-readiness-v2.json`.

## Core documentation law

> **What is not written was never done.**

Material work follows:

`OBSERVE → ACT / CHANGE / DECIDE → VERIFY → DOCUMENT → PERSIST IN GIT`

Completion requires:

`IMPLEMENTED + VERIFIED + DOCUMENTED + DURABLE STATE`

## Canonical governed path

`Human request → P15 interpretation → state resolution → P16 plan → P17 readiness → Actionable HOLD / Scoped Approval → controller → bounded runtime → verification → evidence/durable-state reconciliation → persistence → recovery / continuation`

Interpretation, planning, readiness, credentials, CI, generated facts, reconciliation metadata, prior approvals, recovery state, documentation, or release status never manufacture permission.

## Active bounded work

### DevOS 0.19.0 Production Readiness Evidence v2

The historical v1 readiness protocol intentionally rejects live/production claims, so it cannot truthfully represent the later bounded live-provider evidence or derive a current production verdict. The active objective introduces a separate v2 current-source assessment rather than relabeling v1 history.

Implemented on the active branch:

- closed ten-criterion production-readiness schema;
- exact blocker derivation;
- current-source / current-live-read / bounded-live / external-required evidence classes;
- fail-closed verifier and adversarial regression corpus;
- Python 3.11/3.12 dedicated CI;
- `devos production-readiness` CLI and `--require-production` mode;
- coherent candidate version `0.19.0` and release-manifest binding;
- current README/changelog/readiness/status documentation.

Pending before this objective can close:

1. exact feature-head CI;
2. expected-head PR merge;
3. fresh merged-main CI;
4. exact-source 0.19.0 artifact + SHA-256 evidence;
5. final durable reconciliation/history update.

No numbered architecture stage is created for this work. Do not invent P18/P19 for bookkeeping.

## Current Production Readiness v2 assessment

Current deterministic verdict: **HOLD**.

`production_ready = false`

### Criteria currently PROVEN at bounded scopes

- `source_integrity` — current source/release machinery.
- `authorization_security` — current governance/security source.
- `deterministic_verification` — current verifier/regression source.
- `provider_read` — bounded current live-read evidence.
- `remote_mutation` — bounded historical live GitHub create/update/delete + readback evidence.

### Required production blockers

- `runtime_direct_conformance` — no production runtime has direct observed conformance durably promoted from declaration-only state.
- `recovery_disaster` — no production backup/storage target with measured restore RPO/RTO evidence.
- `operational_observability` — no production service target, SLO, alert routing, telemetry, or incident-response evidence.
- `deployment_target` — no explicit production target with environment contract, rollout, rollback, and production readback evidence.
- `high_impact_governance` — production-scoped high-impact operations remain separately authorization-gated and unproven.

These are evidence requirements, not authorization to perform the operations.

## Readiness v2 authority boundary

The v2 assessment fixes these independently of its verdict:

- `authority = UNCHANGED`
- `authorization = UNCHANGED`
- `execution = NONE`
- `mutation = NONE`
- `publication_authorized = false`
- `deployment_authorized = false`
- `evidence_can_authorize = false`

Therefore:

- `VALID ASSESSMENT != PRODUCTION READY`
- `PRODUCTION READY != PUBLICATION AUTHORIZATION`
- `PRODUCTION READY != DEPLOYMENT AUTHORIZATION`
- `EVIDENCE != AUTHORIZATION`

## Latest completed release-ready milestone

### DevOS 0.18.0 Runtime Conformance Evidence Intake v1 — closed

- PR #64 merged at `a8f19687c177359bd5f646e10913ebdae0851a53` from exact feature head `f59fad07b6f7708cfc79f173625f9ddafa7bc5ae`.
- PR #65 durable reconciliation merged at `b221a240a41426b200a9235eacfa5300042936c0`.
- PR #65 post-merge exact-source release workflow `34842611047` succeeded.
- Exact-source artifact after PR #65: ID `10346418633`; digest `sha256:61e8bc4a4b20c326d2286fc619d202265b9bdd3edbf3feddc70316249cd010f6`.
- No vendor runtime was promoted and no public release/deployment was performed.

## Current verified capability state

### Agent Runtime Profile Registry + Conformance v1 — closed

- `reference-local-agent` is verified only for recorded static repository-contract conformance.
- `codex`, `claude-code`, and `openhands` remain declaration-only templates until separate direct evidence is observed and durably promoted.
- `EVIDENCE_PACKET_VALID != VERIFIED RUNTIME` remains enforced.

### Universal Agent Runtime Adapter v1 — closed

A P17 READY step plus exact scoped approval can be compiled into a runtime-neutral SHA-256-bound handoff and returned diff/test/readback evidence can be independently validated. The adapter itself does not invoke a vendor runtime or create authority.

### Safe delivery proof line — closed at recorded scopes

- Local disposable delivery proof.
- Managed-repository read-only preflight.
- Isolated managed-repository scoped write proof.
- Governed live GitHub file create/update/delete proof with readback at the recorded scope.

These do not imply unrestricted production delivery authority.

### Numbered architecture

- P9 through P17 remain complete at their recorded evidence levels.
- P11 remains repository-first recovery/cross-AI continuity baseline.
- P12 remains evidence provenance/freshness owner.
- P15/P16/P17 remain interpretation/planning/readiness layers respectively; none independently grants runtime authority.
- AI State Resolver v2 contradiction/envelope hardening remains closed through its recorded sequence.

## Current boundaries

- `production_ready = false` while any required v2 criterion remains HOLD.
- `CONTINUE != BLANKET AUTHORIZATION`.
- `INTERPRETATION != AUTHORIZATION`.
- `PLAN != EXECUTION`.
- `READY != EXECUTION`.
- `CI PASS != AUTHORIZATION`.
- `DOCUMENTATION != AUTHORIZATION`.
- `DISTRIBUTION RELEASE READY != PRODUCTION READY`.
- `DISTRIBUTION RELEASE READY != PUBLICATION AUTHORIZATION`.
- `PROVIDER CREDENTIAL != DEVOS AUTHORIZATION`.
- `DECLARED RUNTIME != VERIFIED RUNTIME CAPABILITY`.
- `EVIDENCE_PACKET_VALID != VERIFIED RUNTIME`.
- Historical exact-head evidence remains pinned rather than silently rewritten.
- Uncertain provider mutation is never blindly replayed.
- Parallel AI work must revalidate against fresh `main` before integration.

## Recovery precedence

1. Current source tree + Git/PR/CI/release-artifact metadata.
2. Explicit current user requirements and durable decisions.
3. `.ai/CURRENT-STATE.md`, `.ai/TASKS.md`, `.ai/RECONCILIATION-LEDGER.jsonl`.
4. Relevant core contracts/tests/configuration.
5. `.ai/SESSIONS/` and historical evidence.
6. ChatGPT Memory/chat history only as supplementary context.

## Stable references

- `AGENTS.md`
- `.ai/manifest.yaml`
- `docs/DEVOS-MASTER-ENGINEERING-MAP.md`
- `docs/DEVOS-ENGINEERING-STAGE-HISTORY.md`
- `docs/PRODUCTION-READINESS-EVIDENCE.md`
- `core/production-readiness-evidence-v2.md`
- `config/production-readiness-v2.json`
- `docs/RELEASE.md`
- `.github/SECURITY.md`

## Next action

Verify the exact active feature head. Fix all CI failures without weakening safety semantics. Merge only through an exact expected-head guard after all applicable CI is green. Then verify exact merged-main CI/artifact evidence and perform final durable reconciliation.
