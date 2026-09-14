# Changelog

All notable DevOS distribution changes are summarized here. Exact implementation truth remains in source/Git/PR/CI and durable `.ai` records; this file is release navigation, not execution authority.

## 0.19.0 — 2026-09-14

Current-source production-readiness evidence v2 release line.

### Added / completed

- `config/production-readiness-v2.json` with an explicit closed set of ten production-required criteria.
- `tools/verify-production-readiness-v2.py` with exact schema, evidence-path, blocker, verdict, version, and authorization-boundary validation.
- `tools/test-production-readiness-v2.py` adversarial corpus covering fake READY states, concealed blockers, duplicate/missing criteria, missing evidence, version mismatch, altered authority boundaries, and invalid evidence classes.
- Dedicated Python 3.11/3.12 production-readiness CI.
- `devos production-readiness` CLI dispatch and `--require-production` fail-closed mode.
- Current readiness documentation that distinguishes source/live evidence already proved from production-only evidence that still requires direct external observation.
- Coherent 0.19.0 release identity so the new readiness gate is not silently attached to the already verified 0.18.0 source artifact.

### Evidence improvements

- Current-source integrity, authorization/security gating, deterministic verification, bounded current provider reads, and the recorded governed GitHub create/update/delete proof can be represented as `PROVEN` at their exact scopes.
- Production-only gaps are no longer hidden behind a generic false flag; they are deterministic blocker IDs.
- `production_blockers` must exactly equal all required criteria still in `HOLD`.
- A future all-PROVEN evidence set can produce `READY`, but readiness still cannot create publication, deployment, execution, or mutation authority.

### Security / integrity invariants

- `VALID ASSESSMENT != PRODUCTION READY`.
- `PRODUCTION READY != PUBLICATION AUTHORIZATION`.
- `PRODUCTION READY != DEPLOYMENT AUTHORIZATION`.
- `EVIDENCE != AUTHORIZATION`.
- `INTERPRETATION != AUTHORIZATION`.
- `PLAN != EXECUTION`.
- `READY != EXECUTION`.
- `CONTINUE != BLANKET AUTHORIZATION`.
- `CI PASS != AUTHORIZATION`.
- `PROVIDER CREDENTIAL != DEVOS AUTHORIZATION`.
- `RECOVERY != AUTOMATIC MUTATION REPLAY`.

### Known limitations

- `production_ready = false` remains evidence-driven because five production-required criteria still HOLD: direct production-runtime conformance, production backup/restore RPO/RTO, production observability/SLO/incident routing, an explicit deployment target with rollout/rollback/readback proof, and production-scoped high-impact governance.
- Public tagging/GitHub Release/package publication and deployment remain separate objectives and are not authorized by this release line.
- A historical bounded live mutation proof is not arbitrary production mutation authority.
- Production-only external evidence must be directly observed and durably reconciled before any blocker can be promoted to PROVEN.

## 0.18.0 — 2026-09-14

Runtime conformance evidence intake release line.

### Added / completed

- `tools/agent-runtime-conformance-evidence.py` with exact runtime/adapter/Git-head/nonce challenge binding.
- Candidate evidence validation for the required runtime capabilities: `filesystem.read`, `filesystem.write_scoped`, `git.inspect`, and `verification.run`.
- SHA-256 challenge integrity and per-capability evidence-digest validation.
- Fail-closed rejection of runtime/head/nonce mismatch, replay, malformed provenance, missing/extra capabilities, invalid digests, and tampered challenge data.
- Explicit `HOLD` when a required capability probe reports failure.
- Dedicated adversarial regression corpus and runtime-profile CI integration.
- Release manifest now requires the conformance contract/tool/tests in the exact-source distribution.

### Security / integrity invariants

- `EVIDENCE_PACKET_VALID != VERIFIED runtime`.
- `EVIDENCE_PACKET_VALID != registry mutation`.
- `INTERPRETATION != AUTHORIZATION`.
- `PLAN != EXECUTION`.
- `READY != EXECUTION`.
- `CONTINUE != BLANKET AUTHORIZATION`.
- `CI PASS != AUTHORIZATION`.
- `PROVIDER CREDENTIAL != DEVOS AUTHORIZATION`.
- `PROVIDER RESPONSE != COMPLETION PROOF`.
- `RECOVERY != AUTOMATIC MUTATION REPLAY`.

### Known limitations

- `production_ready = false` remains intentional.
- A challenge-bound packet is candidate evidence only; `registry_promotion_allowed=false` and `direct_runtime_verified=false` remain mandatory verdict fields.
- Codex, Claude Code and OpenHands remain declaration-only until separate direct runtime invocation evidence is actually observed, semantically reviewed, durably merged into the registry, and verified.
- The evidence-intake tool does not invoke a vendor runtime, mutate Git/the registry, deploy, access credentials, alter databases/permissions, or perform destructive actions.
- Distribution release readiness does not authorize public tagging/GitHub Release publication or production deployment.

## 0.17.0 — 2026-09-14

First release-ready P17-complete distribution line.

### Added / completed

- Repository-first recovery and cross-AI continuity through P11 foundations.
- P12 Operational Intelligence and evidence-backed advisory prioritization.
- P13 bounded autonomous development orchestration.
- P15 human-language interpretation with bounded English, Hindi, Hinglish and informal/local regression corpus.
- P16 semantic goal-to-plan compilation with explicit impacts, dependencies and verification requirements.
- P17 exact-step readiness/authorization/security gating.
- AI State Resolver v2 contradiction identity, fail-closed contradiction handling, downstream tamper defense and detailed contradiction provenance.
- Actionable HOLD, scoped approval, governed continuation, current-source evidence refresh and durable documentation integrity.
- GitHub identity/token control plane, governed provider/controller adapter and mutation readback reconciliation.
- Local disposable delivery proof and isolated managed-repository safe-write proof with exact approval, diff, test and readback evidence.
- Universal Agent Runtime Adapter v1 with SHA-256-bound runtime-neutral handoff/result validation.
- Agent Runtime Profile Registry + Conformance v1 separating runtime names from evidence-backed capability claims.
- Automated Evidence → Durable State Reconciliation v1 and machine-readable reconciliation ledger.
- Distribution release manifest, cross-platform `tools/devos.py` CLI, fail-closed release checker, security policy and reproducible exact-source ZIP/SHA-256 CI artifact.

### Security / integrity invariants

- `INTERPRETATION != AUTHORIZATION`
- `PLAN != EXECUTION`
- `READY != EXECUTION`
- `CONTINUE != BLANKET AUTHORIZATION`
- `CI PASS != AUTHORIZATION`
- `PROVIDER CREDENTIAL != DEVOS AUTHORIZATION`
- `PROVIDER RESPONSE != COMPLETION PROOF`
- `RECOVERY != AUTOMATIC MUTATION REPLAY`

### Known limitations

- `production_ready = false` remains intentional.
- Distribution release readiness does not authorize deployment, production mutation, database/permission changes, credentials/secrets operations or destructive actions.
- Historical readiness evidence remains pinned to its original source heads; current-source claims require fresh evidence rather than rewriting history.
- Codex, Claude Code and OpenHands registry entries remain declaration-only until separate conformance evidence is merged.
- No automatic Git tag, GitHub Release or deployment is created by the release-readiness workflow.
- Public licensing terms are not changed by this engineering release-readiness work.

## Earlier development line

The previous README version marker was `0.12`, corresponding to the P12 Operational Intelligence milestone. P13–P17 and subsequent unnumbered hardening/proof milestones are preserved in `docs/DEVOS-ENGINEERING-STAGE-HISTORY.md` and `.ai/SESSIONS/`.
