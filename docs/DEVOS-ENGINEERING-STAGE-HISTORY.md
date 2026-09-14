# DevOS Engineering Stage History

> Durable navigation ledger for completed numbered stages and major unnumbered hardening/proof milestones. Source, tests, Git/PR/CI metadata, `.ai/CURRENT-STATE.md`, `.ai/TASKS.md`, `.ai/DECISIONS.md`, reconciliation records, and session evidence remain authoritative.

## Numbered architecture stages

| Stage | Role in DevOS | Durable outcome |
|---|---|---|
| P9 | Development Task Controller | Established bounded task control and governed development-task execution semantics. |
| P10 | Context Continuity & Recovery | Added continuity/recovery foundations so work can resume from repository state rather than private chat memory. |
| P11 | Federation & Self-Healing Context | Established repository-first recovery, cross-AI continuity, host portability, and bounded context self-healing. |
| P12 | Operational Intelligence | Added advisory/runtime observability and execution-evidence provenance/freshness substrate used by later gates. |
| P13 | Autonomous Development Orchestration | Added governed orchestration/checkpoint-resume behavior while preserving authorization boundaries. |
| P14 | Adaptive Verification & Self-Healing | Added adaptive verification and bounded healing with deterministic re-verification. |
| P15 | Human Language Interpretation v2 | Added semantic interpretation of human language without treating language itself as authorization. |
| P16 | Semantic Goal-to-Plan Compiler | Converts interpreted objectives into bounded dependency-aware plans with explicit impacts, verification, and ambiguity handling. |
| P17 | Step Readiness & Authorization Orchestrator | Performs exact-step readiness, capability, authorization, security, dependency, and evidence gating before execution. |

P9–P17 are architecture history. Their completion does **not** imply production readiness, blanket authority, or permission to invent P18/P19 for bookkeeping.

## Major unnumbered hardening and proof milestones

- **Production E2E Harness — PR #11:** established end-to-end governed-path proof infrastructure.
- **Failure + Recovery Proof — PR #12:** demonstrated bounded failure handling and recovery behavior.
- **Multi-Session / Fresh-AI Continuation Proof — PR #13:** proved repository-based continuation across sessions/fresh AI contexts.
- **Controlled Remote Mutation Proof — PR #14:** established controlled remote-mutation evidence under bounded governance.
- **Production-Readiness Evidence Matrix & Limitations — PR #16:** separated measured evidence from prose claims and kept readiness limitations explicit.
- **Trust-First Audit Gap Closure — PR #17:** added adversarial security/trust verification.
- **Foundation Health & State Consistency — PR #18:** added consistency/health checks and adversarial regression coverage.
- **Universal Project Onboarding + Repository Creation — PR #19:** generalized onboarding and repository-creation workflows.
- **Cross-Host Recovery Friction & Onboarding Proof — PR #20:** tested host portability/recovery friction.
- **Recovery Friction → Foundation Health Integration — PR #21:** integrated recovery diagnostics into health/doctor behavior.
- **Host-neutral MCP/App `repository.create` — PR #22:** added provider-neutral repository creation adapter behavior.
- **Actionable HOLD + Scoped Approval + Governed Continuation — PR #23:** made HOLD actionable and approval scope explicit; `CONTINUE != BLANKET AUTHORIZATION`.
- **Current-Source Evidence Refresh — PR #24:** added fresh-current-source verification without rewriting historical evidence.
- **MCP/App Permission Control Plane + Multi-Project Agent Isolation — PR #27:** separated provider capability from DevOS authority and isolated project state/approval/provider context.
- **GitHub Identity & Token Control Plane v1 — PR #32:** established GitHub App identity binding, short-lived credential handling, scope-aware capability discovery, and non-secret durable evidence.
- **Governed GitHub Provider/Controller Adapter — PR #35:** connected P17/controller gating to bounded GitHub provider reads/mutations with expected-state anchors.
- **DevOS Activation Handshake — PR #39:** added context-recovery activation semantics with no permission upgrade.
- **GitHub Mutation Readback Reconciliation — PR #42:** added bounded readback-only retries after provider write races; uncertain mutation is never blindly replayed.
- **AI State Resolver v2 Envelope Integrity — PR #44:** hardened resolver→P16→P17 provenance validation and fail-closed tamper detection.
- **Post-PR #44 Durable-State Reconciliation — PR #45:** synchronized durable state after resolver hardening.
- **AI State Resolver v2 Cross-Claim Contradiction Handling — PR #46:** added explicit structured fact identity and contradiction-to-unknown propagation.
- **Post-PR #46 Durable-State Reconciliation — PR #48:** reconciled current/task state after contradiction handling.
- **Resolver Contradiction Envelope Integrity — PR #49:** added independent P16/P17 contradiction recomputation and tamper rejection.
- **Post-PR #49 Durable-State Reconciliation — PR #51:** marked contradiction envelope-integrity hardening complete and pinned exact-head CI.
- **Resolver Detailed Contradiction Provenance — PR #52:** added deterministic audit-only contradiction detail and independent downstream validation.
- **P15 Bounded Devanagari Hindi/Hinglish Corpus & Gating — main commits `001f48e...` / `07fcc3c...`:** preserved Unicode Hindi input and proved bounded P15 → P16 → P17 gating for high-impact, negative, and unresolved language cases.
- **Automated Evidence → Durable State Reconciliation v1 — PR #54:** added deterministic merge/exact-head-CI/documentation evidence validation, mandatory semantic review for durable CURRENT/TASKS meaning, and tamper-evident reconciliation records. Merged at `e31c2099b5d9ce88ee4a20c225fe70b424dffa3d`; exact verified feature head `a2da0eaf2a5464d4a716859168bf0ba4d87659a6`.
- **Universal Agent Runtime Adapter v1 — PR #57:** added a side-effect-free, vendor-neutral compiler for P17 READY plus exact scoped approval and a validator for runtime-returned diff/test/readback evidence. Merged at `5d0bdbc0258e898ece21f99937dc4f5b886778a0`; exact verified feature head `da57d48c1ec28eac71eff75b59f9c701e9c9c593`.
- **Managed-Repository Delivery v1 Read-Only Preflight — feature head `fda3e3a6db624d69d6d651cd531c537ad579c9cd`:** added exact local Git-head/clean-worktree/path recovery through P15 → P16 → P17 and an intentional HOLD before any managed-repository write.
- **Isolated Managed-Repository Write Proof v1 — feature head `2ef6b6e3df832ca132123b85caa69f7eda67d1f3`:** proved one exact scoped local file update in a newly created isolated Git fixture with test, diff, readback, runtime validation, and external evidence packet; no commit/push/provider/deployment/production action occurred.
- **Agent Runtime Profile Registry + Conformance v1 — PR #59:** added durable protocol `DEVOS-AGENT-RUNTIME-PROFILE-REGISTRY-v1`, evidence-backed runtime profile export, fail-closed declaration/conformance states, and dedicated regression CI. Merged at `d426ccf480e48544e8078ab7b61065ffd6b18f48`; exact verified feature head `447e8fbaee96eb0be22e9a59d75da147dbcbb8ac`. `reference-local-agent` is verified only for static repository contract conformance; `codex`, `claude-code`, and `openhands` remain declaration-only templates until separate evidence-backed proofs exist. Reconciliation record digest: `4a613b466092c9c1e811ab16e6fe8af41dfc08668b74312e8c69b3b9d909d7e1`.
- **DevOS 0.17.0 Distribution Release Readiness v1 — PR #61:** replaced stale `0.12 / P12` distribution metadata with canonical `VERSION=0.17.0`, a release manifest, current README/changelog, public security policy, release process, a shell-free cross-platform CLI, fail-closed release checker, adversarial regression tests, and Linux/Windows Python 3.11/3.12 release CI. PR #61 merged at `ecee10168b43d13430dd71c2e8d85556956f56a6`; exact verified feature head `b4f46eb7919177e3a0dc19d902401630cd6c12ec`. The post-merge main release run `34822341533` rebuilt and verified the exact merged-source distribution artifact `10338323248` (`devos-source-ecee10168b43d13430dd71c2e8d85556956f56a6`, digest `sha256:4a44fbaa6d9df23afb538afe27b2b38595b3c0aa1632292a43f26b2dea3a2091`). This milestone is engineering/distribution release readiness only: no tag, GitHub Release, package publication, deployment, production-readiness upgrade, credential/database/permission/destructive action, runtime-verification promotion, or public-license change occurred. Reconciliation record digest: `80154dd84d9e6bd7cdfac0d379a708d25455a9542565feb0edcb117bf6362af6`.
- **DevOS 0.18.0 Agent Runtime Conformance Evidence Intake v1 — PR #64:** added deterministic runtime/adapter/Git-head/nonce-bound conformance challenges, exact capability evidence validation, provenance/digest/replay/tamper defenses, and fail-closed candidate-evidence semantics without vendor promotion. PR #64 merged at `a8f19687c177359bd5f646e10913ebdae0851a53`; exact verified feature head `f59fad07b6f7708cfc79f173625f9ddafa7bc5ae` passed 13/13 applicable workflows. Post-merge exact-main release run `34830436068` passed Ubuntu/Windows × Python 3.11/3.12 and built artifact `10342221168` (`devos-source-a8f19687c177359bd5f646e10913ebdae0851a53`, digest `sha256:894e369966e5172c609a6008c5f7086a78622b81b7f2794fa93990a88b09caf7`). `EVIDENCE_PACKET_VALID != VERIFIED RUNTIME`; `codex`, `claude-code`, and `openhands` remain declaration-only. This milestone is engineering/distribution release readiness only; `production_ready=false`, publication/deployment authority remains separate. Reconciliation record digest: `7c08b334ebfedbf9951b8d384313e92a894c83dbb8283b77c7221fb1ad113a99`.
- **DevOS 0.19.0 Production Readiness Evidence v2 — PR #66:** replaced the stale historical-only readiness interpretation with a separate current-source `DEVOS-PRODUCTION-READINESS-EVIDENCE-v2` protocol while preserving v1 history. The v2 verifier models exactly ten required criteria, derives blockers deterministically, validates evidence paths/classes, rejects fake READY states and authority-boundary tampering, exposes `devos production-readiness`, and supports fail-closed `--require-production`. PR #66 merged at `8cd731b7b91ca9e67983b6deca8646b38e078e33` from exact verified feature head `f81184975ffbb02a3e58466459e12858fdd8294a`; feature-head applicable CI was 14/14 success. Post-merge exact-main push CI was 11/11 success. Release workflow `34846071713` passed Ubuntu/Windows × Python 3.11/3.12 and built exact-source artifact `10348113380` (`devos-source-8cd731b7b91ca9e67983b6deca8646b38e078e33`, digest `sha256:fd07fcebcaebca703c11787e634940de904e85be5e3115894808b6a7955307f0`). Current deterministic production verdict remains `HOLD`/`production_ready=false` because `runtime_direct_conformance`, `recovery_disaster`, `operational_observability`, `deployment_target`, and `high_impact_governance` still require direct target-specific external evidence. Those HOLD criteria are not authorization to perform high-impact actions merely to make the matrix green. Reconciliation record digest: `8a8ce6db2bccbe211030ab681577736717e978cab8760c074e65faca09c8d49f`.
- **DevOS 0.20.0 Production Target Evidence Intake v1 — PR #68:** added a read-only provider-neutral intake contract for the five external Production Readiness v2 blockers, binding already-observed evidence to an exact production target, exact source SHA, timezone-aware observation, observer, evidence references/digests/scopes, and explicit limitations. All-PASS evidence returns `CANDIDATE_COMPLETE` but still forces `production_ready=false`, `readiness_promotion_allowed=false`, and semantic review before any promotion. PR #68 merged at `b9f4c6023aa4bc12111c713b6b262012ed3e51c4` from exact verified feature head `40957dfaf2965d16dc1159f1fca1aca183a4110c`; feature-head applicable CI was 15/15 success after repairing the fresh-AI P11 context marker. Post-merge exact-main push CI was 12/12 success. Release workflow `34877764342` built exact-source artifact `10361816279` (`devos-source-b9f4c6023aa4bc12111c713b6b262012ed3e51c4`, digest `sha256:94f7b68abea833ff1a9814ca96e1f0ff017b5b75a5df6c1fde852e461d6f03cf`). No production probe/deployment/high-impact operation or readiness promotion occurred. Reconciliation record digest: `c38edd8818a313ed6cd9fdeaa1367e8491ea212db89ae8b00b038c3de3fd5171`.

Closed/stale duplicate PRs remain provenance only and are never substituted for merged current source.

## Live GitHub provider evidence milestone

A dedicated isolated branch/resource sequence proved the governed GitHub mutation path:

```text
P16 plan
  ↓
P17 READY
  ↓
controller bridge
  ↓
governed GitHub adapter
  ↓
GitHub App provider
  ↓
fresh readback / reconciliation
```

Observed provider commits include create `e8235f7864678a27bbf036def806a1624fb66678`, update/reconciliation `27a3b3cf4f7c8c8511f3c5a8f3283d8a6a883232`, and delete `3f530da3ee1efd4e52baad10fe4e644d4db5d116` with final ABSENT readback.

This proves the scoped governed mutation path only. It does not authorize arbitrary repository deletion, branch deletion, force updates, production mutation, credentials/permission changes, or destructive external actions. `production_ready = false` remains intentional.

## Architectural invariants accumulated across stages

```text
INTERPRETATION != AUTHORIZATION
PLAN != EXECUTION
READY != EXECUTION
CONTINUE != BLANKET AUTHORIZATION
DOCUMENTATION != AUTHORIZATION
CI PASS != AUTHORIZATION
PROVIDER CREDENTIAL != DEVOS AUTHORIZATION
PROVIDER RESPONSE != COMPLETION PROOF
RECOVERY != AUTOMATIC MUTATION REPLAY
MACHINE FACT != SEMANTIC AUTHORITY
RECONCILIATION READY != REPOSITORY MUTATION
DECLARED RUNTIME != VERIFIED RUNTIME CAPABILITY
EVIDENCE_PACKET_VALID != VERIFIED RUNTIME
DISTRIBUTION RELEASE READY != PRODUCTION READY
DISTRIBUTION RELEASE READY != PUBLICATION AUTHORIZATION
VALID ASSESSMENT != PRODUCTION READY
VALID TARGET EVIDENCE != PRODUCTION READY
PRODUCTION READY != PUBLICATION AUTHORIZATION
PRODUCTION READY != DEPLOYMENT AUTHORIZATION
EVIDENCE != AUTHORIZATION
```

Material work follows:

```text
OBSERVE → ACT / CHANGE / DECIDE → VERIFY → DOCUMENT → PERSIST IN GIT
```

Completion requires:

```text
IMPLEMENTED + VERIFIED + DOCUMENTED + DURABLE STATE
```

## Current evolution direction

The completed line now includes P9–P17, language-safe interpretation, resolver/provider hardening, evidence-first durable reconciliation, runtime-neutral handoff validation, isolated and managed-repository bounded delivery proofs, evidence-backed runtime profile conformance, DevOS `0.17.0` distribution-release foundations, DevOS `0.18.0` runtime-conformance evidence intake, DevOS `0.19.0` current-source Production Readiness Evidence v2, and DevOS `0.20.0` target-bound external Production Target Evidence Intake v1.

The repo-side 0.20.0 objective is complete while production readiness remains deterministically HOLD on five explicit external evidence criteria. Public publication and production deployment remain separate authorization-gated objectives. Runtime portability and production readiness must continue through direct target-specific evidence, one bounded proof at a time. A familiar vendor/runtime name, external reputation, release status, or caller-supplied capability declaration is not sufficient to mark an integration verified or authorize execution.

No new objective is automatically promoted by this history record. Future development must recover fresh `main`, open issues/PRs, CI, durable state, relevant source/tests, concurrent AI work, and current user intent first.

## Recovery use

A fresh maintainer should use this file as history/navigation only, then recover current truth in this order:

1. source tree + Git/PR/CI/release-artifact metadata;
2. `.ai/CURRENT-STATE.md`, `.ai/TASKS.md`, and `.ai/RECONCILIATION-LEDGER.jsonl`;
3. relevant core contracts/tests/release manifest;
4. `.ai/DECISIONS.md` and session provenance;
5. this historical ledger for architectural context.
