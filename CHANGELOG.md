# Changelog

All notable DevOS distribution changes are summarized here. Exact implementation truth remains in source/Git/PR/CI and durable `.ai` records; this file is release navigation, not execution authority.

## 0.22.0 — 2026-09-17

Project Fleet Watch v1 release line.

### Added / completed

- `tools/devos-project-fleet.py` for read-only multi-repository DevOS management visibility.
- `DEVOS-PROJECT-FLEET-SNAPSHOT-v1` deterministic snapshot format.
- Fleet verdicts: `HEALTHY`, `ATTENTION`, `HOLD`, `EMPTY`, and `BLOCKED`.
- Per-repository classification delegates to Managed Project Lifecycle v1 rather than inventing a second authority model.
- Previous/current snapshot drift detection for `new_repositories`, `new_unmanaged`, `newly_managed`, `removed_repositories`, `management_regressions`, and `newly_attention_required`.
- Managed-to-unmanaged regression forces fleet `HOLD`.
- Bounded read-only GitHub discovery for authenticated accessible repositories through `--github-owner @me` and environment-only `GITHUB_TOKEN`.
- `devos project-fleet` CLI dispatch plus `--require-clean` fail-closed mode.
- Dedicated Python 3.11/3.12 Fleet Watch CI and adversarial regression corpus.

### Security / integrity invariants

- `REPOSITORY ACCESSIBLE != DEVOS MANAGED`.
- `FLEET DISCOVERY != ONBOARDING AUTHORIZATION`.
- `FLEET ATTENTION != AUTOMATIC MUTATION`.
- `FLEET HEALTHY != APPLICATION VERIFIED`.
- `FLEET HEALTHY != PRODUCTION READY`.
- `external_mutation = NONE`.
- `production_ready = false` remains unchanged.

### Known limitations

- Fleet Watch is an observation/control-plane feature; it does not auto-onboard repositories.
- Account/organization-wide discovery requires a separately authorized provider token, GitHub App, connector, or worker with sufficient read scope.
- A `HEALTHY` fleet proves management context only; it does not prove application correctness, deployment readiness, runtime conformance, or production readiness.
- GitHub live discovery is bounded by provider visibility, rate limits, and the configured repository cap.

## 0.21.0 — 2026-09-15

Managed Project Lifecycle v1 release line.

### Added / completed

- `tools/devos-project-lifecycle.py` for deterministic local/provider-observed managed-project classification.
- `DEVOS-REPOSITORY-DISCOVERY-SNAPSHOT-v1` read-only provider evidence format.
- Explicit `MANAGED`, `ONBOARDING_REQUIRED`, `HOLD`, and `BLOCKED` lifecycle states.
- Development continuation is permitted only after `MANAGED` readback.
- Local detect → authorized onboarding → fresh managed-state readback flow.
- Repository creation now carries a mandatory `project.onboard` postcondition and keeps development continuation on HOLD after provider creation/readback until management is verified.
- `devos project-lifecycle` CLI dispatch and dedicated Python 3.11/3.12 CI.
- Auto-onboarding documentation updated so externally created/discovered repositories cannot silently bypass DevOS context.

### Security / integrity invariants

- `REPOSITORY EXISTS != DEVOS MANAGED`.
- `REPOSITORY CREATED != ONBOARDED`.
- `REPOSITORY DISCOVERED != SAFE TO CONTINUE`.
- `ONBOARDING != APPLICATION VERIFIED`.
- `PROVIDER CAPABILITY != AUTHORIZATION`.
- `CI PASS != AUTHORIZATION`.
- `production_ready = false` remains unchanged.

### Known limitations

- Remote provider snapshots are read-only evidence; remote onboarding writes still require a governed provider/controller path with sufficient capability and authorization.
- DevOS cannot silently enumerate or mutate every repository on a user/organization account without a configured connector, GitHub App, local worker, or other authorized discovery source.
- Management verification proves durable DevOS context/identity only; it does not prove application correctness, deployment readiness, or production readiness.

## 0.20.0 — 2026-09-14

Production Target Evidence Intake v1 release line.

### Added / completed

- `tools/production-target-evidence.py` for deterministic validation of target-bound external production evidence.
- Exact source-SHA, production-target-ID, timestamp, observer, criterion, evidence-reference, scope, and SHA-256 binding.
- Closed coverage of the five external Production Readiness v2 blockers: runtime direct conformance, recovery/disaster, operational observability, deployment target, and high-impact governance.
- `PASS | FAIL | UNOBSERVED` criterion states with fail-closed schema and evidence requirements.
- `CANDIDATE_COMPLETE` verdict when all five criteria carry valid target-bound PASS evidence, while still forcing `production_ready=false` and `readiness_promotion_allowed=false`.
- Adversarial regression corpus covering source/target mismatch, missing/duplicate/unknown criteria, missing evidence, invalid digests/timestamps, and altered authority boundaries.
- Dedicated Python 3.11/3.12 CI and `devos production-target-evidence` CLI dispatch.

### Security / integrity invariants

- `VALID TARGET EVIDENCE != PRODUCTION READY`.
- `VALID TARGET EVIDENCE != AUTHORIZATION`.
- `VALID TARGET EVIDENCE != DEPLOYMENT AUTHORIZATION`.
- `EVIDENCE != AUTHORIZATION`.
- `PLAN != EXECUTION`.
- `READY != EXECUTION`.
- `CI PASS != AUTHORIZATION`.

### Known limitations

- This intake validates evidence that already exists; it does not run production probes or operations.
- A complete packet requires separate semantic review and durable Production Readiness v2 reconciliation before any readiness criterion may change.
- Production deployment, destructive restore testing, credential/permission/database mutation, and other high-impact operations remain separately gated and are not authorized by this release line.
- `production_ready=false` remains correct until direct target-specific evidence is both valid and separately reconciled.

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
