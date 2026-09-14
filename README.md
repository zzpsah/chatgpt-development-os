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

Current distribution version: **0.18.0**.

```bash
python tools/devos.py version
python tools/devos.py release-check
```

`0.18.0` extends the P17-complete distribution line with challenge-bound Agent Runtime Conformance Evidence Intake v1. Candidate runtime evidence can now be bound to an exact runtime/head/nonce and validated fail-closed without allowing the evidence packet to self-promote a runtime registry entry.

**Distribution release readiness is not production readiness.** `production_ready = false` remains deliberate. A green release gate does not authorize deployment, production mutation, credentials, database changes, permission changes, destructive actions, or unscoped external execution.

See [`docs/RELEASE.md`](docs/RELEASE.md) for the exact-source ZIP/checksum process and release boundaries, and [`.github/SECURITY.md`](.github/SECURITY.md) for vulnerability reporting.

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
- exact diff/test/readback evidence;
- runtime-neutral P17 + scoped-approval handoff;
- evidence → durable-state reconciliation.

These proofs do **not** imply general production deployment authority.

### Runtime portability

`tools/agent-runtime-handoff.py` defines a vendor-neutral handoff/result-validation contract.

`config/agent-runtime-profile-registry.json` separates runtime identity from verified capability. A runtime must have evidence-backed required capabilities before it can be exported as a handoff-compatible profile. Vendor names such as Codex, Claude Code, or OpenHands are not treated as verified merely because they are recognized.

`tools/agent-runtime-conformance-evidence.py` creates exact runtime/head/nonce-bound conformance challenges and validates returned candidate evidence packets. `EVIDENCE_PACKET_VALID` still means reviewable candidate evidence only: it does not verify runtime identity, mutate the registry, grant authorization, or make a declaration-only runtime handoff-ready.

### Provider governance

DevOS includes bounded GitHub provider/controller integration, identity/token controls, scope-aware capability discovery, current-state anchors, readback verification, and uncertain-mutation reconciliation. Proven provider capability never becomes blanket authorization.

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

Existing repositories can be onboarded without manually creating every context file. The project also includes GitHub-side context synchronization and Windows project-watcher helpers.

Examples:

```powershell
.\tools\onboard-project.ps1 -Path 'D:\Projects\MyApp' -DryRun
.\tools\onboard-project.ps1 -Path 'D:\Projects\MyApp'
```

Portable Python onboarding/recovery tools are also available under `tools/`.

See [`docs/AUTO-ONBOARDING.md`](docs/AUTO-ONBOARDING.md).

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

- `config/readiness-evidence.json`
- `.ai/RECONCILIATION-LEDGER.jsonl`
- [`docs/PRODUCTION-READINESS-EVIDENCE.md`](docs/PRODUCTION-READINESS-EVIDENCE.md)
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
- Keep `production_ready = false` unless a separately bounded evidence-backed objective explicitly changes it.

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

**0.18.0** — P17-complete distribution line plus challenge-bound runtime conformance evidence intake. Runtime evidence remains candidate evidence until separate direct observation, semantic review, durable registry change, and verification are completed.
