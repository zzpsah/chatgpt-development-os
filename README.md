# ChatGPT Development OS

A repository-first, human-language development operating system for safely continuing software work across AI models, accounts, coding tools, Git providers, and machines.

DevOS defines **how AI develops software** while keeping source, durable project state, authorization, verification, and execution evidence separate.

```text
human request
  → P15 interpretation
  → state resolution
  → P16 bounded plan
  → P17 readiness
  → scoped approval / HOLD
  → bounded runtime
  → verification + readback
  → evidence reconciliation
  → durable repository state
```

Core law:

> **What is not written was never done.**

Material work follows:

`OBSERVE → ACT / CHANGE / DECIDE → VERIFY → DOCUMENT → PERSIST IN GIT`

Completion requires:

`IMPLEMENTED + VERIFIED + DOCUMENTED + DURABLE STATE`

## Quick start

Requirements for the distribution release line:

- Git
- Python 3.11+

From a checked-out repository:

```bash
python tools/devos.py version
python tools/devos.py doctor --root .
python tools/devos.py release-check
python tools/devos.py project-lifecycle --path . --require-managed --json
python tools/devos.py project-fleet --snapshot fleet.json --json
python tools/devos.py project-remediation fleet-assessment.json --json
python tools/devos.py production-readiness --json
```

For a fresh AI or a full project recovery, start with:

1. `AGENTS.md`
2. `.ai/manifest.yaml`
3. `.ai/CURRENT-STATE.md`
4. `.ai/TASKS.md`
5. current source tree + Git/PR/CI evidence

A normal fresh-AI instruction is:

> Open this project, read `AGENTS.md` and `.ai/manifest.yaml`, recover the current project state, revalidate it against current source/Git, and tell me the next safe action.

AI account memory or old chat history is supplementary only; it is never authoritative project state.

## Release status

Current distribution version: **0.23.0**.

```bash
python tools/devos.py version
python tools/devos.py release-check
python tools/devos.py project-lifecycle --path <project> --require-managed --json
python tools/devos.py project-fleet --snapshot <fleet.json> --json
python tools/devos.py project-fleet --github-owner @me --limit 100 --json
python tools/devos.py project-remediation <fleet-assessment.json> --json
python tools/devos.py production-readiness --json
python tools/devos.py production-target-evidence <packet.json> --expected-source-sha <sha> --expected-target-id <target>
```

`0.23.0` adds Project Remediation Planner v1 on top of Managed Project Lifecycle and Project Fleet Watch. Fleet Watch tells DevOS which repositories need attention; the remediation planner turns that observed state into a deterministic priority queue such as restore a regressed managed repository, resolve a management conflict, complete partial onboarding, or onboard a newly accessible repository.

The planner is advisory only: every proposed action still requires P17 readiness and separately scoped explicit authorization. It never mutates a repository or provider by itself.

Permanent project-management invariants:

```text
REPOSITORY EXISTS != DEVOS MANAGED
REPOSITORY CREATED != ONBOARDED
REPOSITORY DISCOVERED != SAFE TO CONTINUE
REPOSITORY ACCESSIBLE != DEVOS MANAGED
FLEET DISCOVERY != ONBOARDING AUTHORIZATION
FLEET ATTENTION != AUTOMATIC MUTATION
REMEDIATION PLAN != AUTHORIZATION
PLAN READY != SAFE TO APPLY
FLEET HEALTHY != APPLICATION VERIFIED
```

The current Production Readiness v2 assessment remains intentionally **HOLD**, not READY, until direct target-specific evidence is actually observed and separately reconciled.

**Distribution release readiness is not production readiness.** A green release gate, managed-project/fleet/remediation verdict, valid readiness assessment, or valid target-evidence packet does not authorize publication, deployment, production mutation, credentials, database changes, permission changes, destructive actions, or unscoped external execution.

See [`docs/RELEASE.md`](docs/RELEASE.md), [`docs/AUTO-ONBOARDING.md`](docs/AUTO-ONBOARDING.md), [`docs/PROJECT-FLEET-WATCH.md`](docs/PROJECT-FLEET-WATCH.md), [`core/managed-project-lifecycle.md`](core/managed-project-lifecycle.md), [`core/project-fleet-watch.md`](core/project-fleet-watch.md), [`core/project-remediation-planner.md`](core/project-remediation-planner.md), [`docs/PRODUCTION-READINESS-EVIDENCE.md`](docs/PRODUCTION-READINESS-EVIDENCE.md), and [`.github/SECURITY.md`](.github/SECURITY.md).

## What DevOS provides

### Repository-first durable project memory

Each managed project can carry portable `.ai` state:

```text
project/
├── AGENTS.md
└── .ai/
    ├── manifest.yaml
    ├── STATE-INDEX.md
    ├── PROJECT.md
    ├── CURRENT-STATE.md
    ├── ARCHITECTURE.md
    ├── DECISIONS.md
    ├── TASKS.md
    ├── CHANGELOG.md
    └── SESSIONS/
```

Recovery precedence is:

1. current source tree + Git/PR/CI metadata;
2. explicit requirements and durable decisions;
3. durable `.ai` state;
4. generated indexes/evidence navigation;
5. AI memory/chat history only as supplementary context.

### Managed project lifecycle

`tools/devos-project-lifecycle.py` is the mandatory boundary between repository discovery/creation and feature development.

For local repositories:

```bash
python tools/devos.py project-lifecycle --path <project> --require-managed --json
```

If onboarding is required, an explicitly authorized local flow can create only missing DevOS infrastructure and immediately re-read the project:

```bash
python tools/devos.py project-lifecycle \
  --path <project> \
  --apply \
  --authorization EXPLICIT \
  --require-managed \
  --json
```

Provider/controller integrations can submit `DEVOS-REPOSITORY-DISCOVERY-SNAPSHOT-v1` readback evidence. Unmanaged, partial, conflicting, or malformed repositories never silently become development-ready. Repository creation itself carries a mandatory `project.onboard` postcondition.

### Project Fleet Watch

`tools/devos-project-fleet.py` extends lifecycle visibility across a repository fleet without creating another authority layer.

Deterministic snapshot assessment:

```bash
python tools/devos.py project-fleet --snapshot fleet.json --json
```

Drift/watch comparison:

```bash
python tools/devos.py project-fleet \
  --snapshot current.json \
  --previous previous.json \
  --require-clean \
  --json
```

Bounded read-only GitHub discovery:

```bash
GITHUB_TOKEN=... python tools/devos.py project-fleet --github-owner @me --limit 100 --json
```

The GitHub token is environment-only and is never printed or persisted by Fleet Watch. The adapter performs reads only. Fleet discovery cannot onboard, edit, deploy, publish, grant credentials, change permissions/databases, or manufacture authorization. `--require-clean` fails closed unless every active repository is `MANAGED`.

### Project Remediation Planner

`tools/devos-project-remediation.py` converts a Fleet Watch assessment into a deterministic, priority-ordered remediation proposal.

```bash
python tools/devos.py project-remediation fleet-assessment.json --json
```

Priority order is:

1. restore a previously managed repository that regressed;
2. resolve management identity/conflict HOLDs;
3. investigate blocked/malformed lifecycle evidence;
4. complete partial onboarding;
5. onboard a newly accessible unmanaged repository.

The planner is strictly read-only. Every emitted action has `requires_explicit_authorization=true`, `safe_apply=false`, and `next_gate=P17_READINESS_AND_SCOPED_APPROVAL`. `--require-clean` can fail closed when any remediation remains, but it still performs no mutation.

### Human-language interpretation and governed planning

- **P15 Human Language Interpretation** turns English/Hindi/Hinglish and bounded informal requests into structured intent without turning language into authorization.
- **AI State Resolver** resolves evidence/provenance and fails closed on unknown or contradictory claims.
- **P16 Semantic Goal-to-Plan Compiler** creates bounded dependency-aware plan candidates.
- **P17 Step Readiness & Authorization Orchestrator** evaluates exact-step readiness, capability, authorization, security, dependencies, verification expectations, and evidence gates.

Invariants:

```text
INTERPRETATION != AUTHORIZATION
PLAN != EXECUTION
READY != EXECUTION
CONTINUE != BLANKET AUTHORIZATION
CI PASS != AUTHORIZATION
DOCUMENTATION != AUTHORIZATION
PROVIDER CREDENTIAL != DEVOS AUTHORIZATION
PROVIDER RESPONSE != COMPLETION PROOF
RECOVERY != AUTOMATIC MUTATION REPLAY
REPOSITORY EXISTS != DEVOS MANAGED
FLEET DISCOVERY != ONBOARDING AUTHORIZATION
REMEDIATION PLAN != AUTHORIZATION
PRODUCTION READY != DEPLOYMENT AUTHORIZATION
VALID TARGET EVIDENCE != PRODUCTION READY
```

### Autonomous development, runtime, and verification

DevOS includes bounded autonomy rather than unrestricted execution:

- P12 Operational Intelligence — dependency/readiness analysis and advisory prioritization;
- P13 Autonomous Development Orchestration — one evidence-backed next work-unit candidate;
- Development Task Controller — independent task/control gates;
- Autonomous Development Loop — bounded iterate/checkpoint/continue-or-escalate behavior;
- Executable Development Runtime — execution boundary for already-authorized work;
- Verification / Test Engine — evidence-based deterministic/integration/E2E/security verification;
- Security Gate — independent risk/security gating;
- failure recovery and no-blind-replay rules;
- durable reconciliation after verified work.

### Safe software-delivery proof line

The current repository contains bounded proof slices for:

- local disposable Git-repository delivery;
- managed-repository read-only preflight;
- isolated managed-repository safe file update proof;
- governed live GitHub create/update/delete plus readback at its recorded bounded scope;
- exact diff/test/readback evidence;
- runtime-neutral P17 + scoped-approval handoff;
- evidence → durable-state reconciliation.

These proofs do **not** imply general production deployment authority.

### Runtime portability

`tools/agent-runtime-handoff.py` defines a vendor-neutral handoff/result-validation contract.

`config/agent-runtime-profile-registry.json` separates runtime identity from verified capability. A runtime must have evidence-backed required capabilities before it can be exported as a handoff-compatible profile. Vendor names such as Codex, Claude Code, or OpenHands are not treated as verified merely because they are recognized.

`tools/agent-runtime-conformance-evidence.py` creates exact runtime/head/nonce-bound conformance challenges and validates returned candidate evidence packets. `EVIDENCE_PACKET_VALID` still means reviewable candidate evidence only: it does not verify runtime identity, mutate the registry, grant authorization, or make a declaration-only runtime handoff-ready.

### Provider governance

DevOS includes bounded GitHub provider/controller integration, identity/token controls, scope-aware capability discovery, current-state anchors, readback verification, uncertain-mutation reconciliation, managed-project lifecycle classification, read-only fleet observation, and read-only remediation planning. Proven provider capability never becomes blanket authorization.

### Production-readiness assessment and target evidence

`config/production-readiness-v2.json` and `tools/verify-production-readiness-v2.py` provide the current production-readiness contract.

The verifier rejects missing/unknown criteria, fake READY states, concealed blockers, missing evidence references, altered authorization/publication/deployment boundaries, and invalid live-mutation provenance. Normal validation may succeed while the verdict is `HOLD`; `--require-production` fails until every production-required criterion is actually `PROVEN`.

`tools/production-target-evidence.py` is the separate external-evidence intake boundary. It validates one explicit production target, exact source SHA, timezone-aware observation, observer, the exact five external criteria, evidence references/digests/scopes, and unchanged authority boundaries. It performs no production action itself.

```bash
python tools/devos.py production-readiness --json
python tools/devos.py production-readiness --require-production --json
python tools/devos.py production-target-evidence <packet.json> --expected-source-sha <sha> --expected-target-id <target>
```

Readiness or target evidence itself can never authorize publication, deployment, or high-impact execution.

## Multi-AI portability

The acceptance invariant is:

`AI A + Account A → repository → AI B + Account B → correct recovery → safe continuation`

The repository—not a model/vendor/account/chat—is the continuity layer.

See:

- [`docs/MULTI-AI-PORTABILITY.md`](docs/MULTI-AI-PORTABILITY.md)
- [`docs/NEW-AI-ONBOARDING.md`](docs/NEW-AI-ONBOARDING.md)
- [`docs/P11-FEDERATION-SELF-HEALING.md`](docs/P11-FEDERATION-SELF-HEALING.md)
- [`docs/CROSS-AI-HANDSHAKE.md`](docs/CROSS-AI-HANDSHAKE.md)

## Auto-onboarding and context synchronization

Existing repositories can be onboarded without manually creating every context file. Managed Project Lifecycle prevents newly created/discovered repositories from silently bypassing onboarding, Project Fleet Watch adds read-only multi-repository visibility, and Project Remediation Planner prioritizes the exact next governance action without executing it.

Examples:

```powershell
.\tools\onboard-project.ps1 -Path 'D:\Projects\MyApp' -DryRun
.\tools\onboard-project.ps1 -Path 'D:\Projects\MyApp'
```

Portable Python onboarding/recovery tools are also available under `tools/`.

See [`docs/AUTO-ONBOARDING.md`](docs/AUTO-ONBOARDING.md) and [`docs/PROJECT-FLEET-WATCH.md`](docs/PROJECT-FLEET-WATCH.md).

## Health and doctor

Machine-derived foundation health is implemented in `tools/devos-health.py`. Human-readable read-only presentation is provided by:

```bash
python tools/devos.py doctor --root .
```

Doctor/health output never upgrades evidence, creates authorization, or converts historical evidence into current proof. WARN and UNKNOWN are not PASS.

## Evidence and durable reconciliation

DevOS distinguishes historical evidence from current-source evidence. Old evidence is pinned to its original source head rather than silently rewritten when source changes.

After feature completion, the Evidence → Durable State Reconciliation path can normalize machine-verifiable facts while requiring semantic review for architecture/roadmap/current-state meaning.

Important references:

- `config/readiness-evidence.json` — historical v1 snapshot
- `config/production-readiness-v2.json` — current production-readiness assessment
- `core/managed-project-lifecycle.md` — repository-management lifecycle gate
- `core/project-fleet-watch.md` — read-only multi-repository management visibility
- `core/project-remediation-planner.md` — deterministic read-only fleet remediation planning
- `core/production-target-evidence-intake.md` — target-bound external evidence intake
- `.ai/RECONCILIATION-LEDGER.jsonl`
- [`docs/PRODUCTION-READINESS-EVIDENCE.md`](docs/PRODUCTION-READINESS-EVIDENCE.md)
- [`core/production-readiness-evidence-v2.md`](core/production-readiness-evidence-v2.md)
- [`core/evidence-durable-state-reconciliation.md`](core/evidence-durable-state-reconciliation.md)

## Architecture and history

- Living architecture: [`docs/DEVOS-MASTER-ENGINEERING-MAP.md`](docs/DEVOS-MASTER-ENGINEERING-MAP.md)
- Completed numbered/unnumbered milestones: [`docs/DEVOS-ENGINEERING-STAGE-HISTORY.md`](docs/DEVOS-ENGINEERING-STAGE-HISTORY.md)
- General architecture: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)
- AI handoff / independent verification: [`docs/handoff/README.md`](docs/handoff/README.md)

P9 through P17 are completed architecture stages at their recorded evidence levels. Later hardening/proof work is deliberately unnumbered; new P18/P19 labels are not created merely for bookkeeping.

## Security

- Never commit secrets, tokens, passwords, private keys, cookies, or private user/school documents.
- Preserve existing behavior unless a change is intentional and verified.
- Treat production, database, permission, destructive, and security-sensitive changes as high impact.
- Keep approvals scoped to the exact project/workflow/capability/target/state they cover.
- Prefer exact expected-state anchors and fresh readback after mutation.
- Never blindly replay an uncertain mutation.
- Never claim tests, deployment, provider results, or completion without actual evidence.
- Never continue DevOS feature development on a repository whose managed-project lifecycle is not verified.
- Never treat fleet discovery or a remediation plan as onboarding authorization or provider mutation permission.
- Keep `production_ready = false` until the v2 production-readiness criteria are all directly evidenced and independently verified.

See [`.github/SECURITY.md`](.github/SECURITY.md).

## Repository structure

```text
chatgpt-development-os/
├── README.md
├── VERSION
├── AGENTS.md
├── .ai/
├── .github/workflows/
├── adapters/
├── agents/
├── automation/
├── config/
├── core/
├── docs/
├── memory/
├── project-context-spec/
├── projects/
├── rules/
├── templates/
├── tools/
└── workflows/
```

## Version

**0.23.0** — P17-complete distribution line plus managed-project lifecycle enforcement, read-only Project Fleet Watch v1, and deterministic Project Remediation Planner v1, alongside blocker-exact Production Readiness Evidence v2 and target-bound external Production Target Evidence Intake v1. Fleet problems can now be surfaced and priority-ordered without manufacturing onboarding, provider mutation, execution, deployment, publication, or production authority.
