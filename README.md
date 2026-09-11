# ChatGPT Development OS

A portable, human-language development operating system for working across projects, AI accounts, AI coding tools, and machines.

## Core idea

The Development OS defines **how AI develops software**. Each project owns its own durable `.ai` memory. The project must not depend on ChatGPT Memory, a particular AI account, or a particular GitHub account.

**Understand → Inspect → Plan → Implement → Verify → Review → Security → Document → Persist**

Not every request requires every stage; the workflow scales to the task.

## P12 Operational Intelligence

P12 adds a deterministic, evidence-backed **decision-support layer** to the Development Task Controller. It reads the current task inventory and exposes dependency readiness, advisory prioritization, and checkpoint signals.

```text
Repository + durable .ai state
          ↓
      Task inventory
          ↓
   Dependency graph
          ↓
 Readiness / blockers
          ↓
 Priority + checkpoint signals
          ↓
 Evidence-backed next action
```

The first P12 implementation slices provide:

- explicit dependency graph validation, including missing references and cycles;
- `READY`, `WAITING`, `BLOCKED`, `UNAUTHORIZED`, and `COMPLETE` readiness states;
- deterministic priority scoring using explicit priority plus bounded dependency, status, age, deadline, and effort signals;
- transparent scoring reasons rather than silent reprioritization;
- checkpoint signals for repository changes, work-unit outcomes, blocked transitions, authorization changes, verification/security results, and session/handoff boundaries;
- safe handling of unknown checkpoint events without guessing.

Operational Intelligence is **advisory**. It cannot grant authorization, bypass Security Gate, fabricate execution evidence, or turn a recommendation into an action. The existing Controller, Runtime, Verification Engine, Security Gate, and P11 recovery contracts remain authoritative.

See [`core/operational-intelligence.md`](core/operational-intelligence.md) and [`tools/operational-intelligence.py`](tools/operational-intelligence.py).

## Portable project memory

Every managed software project should contain:

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

This makes project context portable between ChatGPT, Codex, Claude, Gemini, Cursor, other AI tools, GitHub accounts, Git providers, and local machines.

## P11 Federation & Self-Healing Context

P11 makes project continuity resilient to AI-account changes, lost chats, stale generated files, and cross-AI handoffs.

```text
AI / Account / Chat
        ↓
Bootstrap + Project Identity
        ↓
Repository-First Recovery
        ↓
Freshness / Integrity Check
        ↓
Safe Reconciliation / Bounded Self-Healing
        ↓
Current State
        ↓
Provenance-Aware AI Handoff
```

Recovery precedence is explicit:

1. **Source tree + Git** — exact implementation state.
2. **Requirements + decisions** — intentional project state.
3. **Durable `.ai` state** — project context and handoff.
4. **Generated indexes** — navigation/evidence only.
5. **AI memory/chat history** — supplementary, never authoritative.

P11 self-healing can recreate only deterministic derived context. It must never silently overwrite semantic requirements, decisions, task state, or architecture. Ambiguous or semantic conflicts escalate for review.

P11 also defines composable operating codes such as `DEVOS::GOD::DESI`: execution stance and communication style are separate layers, and neither layer changes authorization, security, or verification requirements.

The P11 recovery/revalidation and self-healing rules are integrated into the Development Task Controller lifecycle, so task resumption revalidates repository state rather than blindly trusting an old handoff or replaying actions.

See [`docs/P11-FEDERATION-SELF-HEALING.md`](docs/P11-FEDERATION-SELF-HEALING.md), [`docs/DEVOS-STANCE-CODES.md`](docs/DEVOS-STANCE-CODES.md), and [`core/development-task-controller.md`](core/development-task-controller.md).

## Automatic context synchronization

The Development OS supports automatic GitHub-side `.ai/` synchronization:

- `.github/workflows/context-sync.yml` — reusable workflow that records repository changes in `.ai/CHANGELOG.md` and updates `.ai/CURRENT-STATE.md` for meaningful application changes.
- `templates/project/.github/workflows/devos-context-sync.yml` — ready-to-copy caller workflow for managed projects.
- `templates/project/.ai/CHANGELOG.md` — portable change-record template.
- `tools/init-project.ps1` — idempotent initializer for an existing local project.
- `tools/onboard-project.ps1` — safe existing-repository onboarding wrapper with dry-run support.
- `tools/check-project.ps1` — context health check.
- `tools/watch-projects.ps1` — Windows recursive watcher that detects project activity and initializes missing `.ai/` context.
- `tools/install-windows.ps1` — installs the watcher at Windows logon for configured project roots.

The automatic GitHub sync records verified repository facts. It does **not** invent architecture or decisions from a commit. AI agents remain responsible for updating semantic context such as architecture, decisions, requirements, and task state after meaningful work.

## Auto-Onboarding

Existing repositories can be brought under Development OS management without manually creating every context file.

```powershell
.\tools\onboard-project.ps1 -Path 'D:\Projects\MyApp'
```

Use `-DryRun` to preview the operation. Onboarding preserves existing `.ai` files and existing project files, creates only missing context/integration infrastructure, and does not modify application source. After onboarding, commit and push the generated files so GitHub-side synchronization can begin.

Full design and automation boundaries: [`docs/AUTO-ONBOARDING.md`](docs/AUTO-ONBOARDING.md).

## Human-language first

You should not need to know which agent, workflow, or command is required.

- “Something is wrong with the registration page.” → investigate/debug.
- “Make the page more professional.” → UI analysis/improvement.
- “Can you check whether this is secure?” → security review.
- “Continue where we stopped.” → recover project state and resume.
- “Go ahead and do it.” → execute the agreed plan.

## Agent Orchestration

For larger work, DevOS can coordinate internal engineering responsibilities rather than treating the whole job as one undifferentiated task.

```text
User objective
    ↓
State + scope resolution
    ↓
Work decomposition
    ↓
Role selection
    ↓
Ordered / safe parallel work units
    ↓
Evidence handoff
    ↓
Integration + review
    ↓
Verification + Security Gate
    ↓
Durable project state
```

Orchestration selects only the roles needed for the work, respects dependencies, prevents conflicting shared-state operations from running concurrently, preserves failed/blocked units, and never creates authorization. It does not claim unrestricted autonomy or automatic production deployment.

See [`core/agent-orchestration.md`](core/agent-orchestration.md) and [`workflows/orchestration.md`](workflows/orchestration.md).

## Autonomous Development Loop

P4 adds a controlled execution loop on top of the existing DevOS contracts:

```text
Objective
  ↓
State resolution
  ↓
Plan / orchestrate
  ↓
Capability + authorization check
  ↓
Bounded iteration
  ↓
Checkpoint + verification
  ↓
Review / Security Gate
  ↓
Persist evidence + state
  ↓
CONTINUE / STOP / ESCALATE
```

Each iteration has an execution bound, concrete scope, capability state, authorization state, evidence, verification result, and checkpoint. A resumed loop re-checks current repository state rather than blindly replaying actions. Missing capabilities may be explicitly delegated, but tool execution and external results are never simulated. High-risk, destructive, irreversible, production-impacting, security-sensitive, and data-affecting actions still require the applicable approval.

P4 is **bounded autonomy**, not unrestricted autonomous deployment or permission bypass.

See [`core/autonomous-development-loop.md`](core/autonomous-development-loop.md) and [`workflows/autonomous-loop.md`](workflows/autonomous-loop.md).

## Executable Development Runtime

P5 adds the controlled execution boundary beneath the autonomous loop. The runtime receives an already-authorized work unit, checks capabilities and approval requirements, creates pre/post checkpoints, performs only the bounded action through a supported host/tool adapter, captures actual execution evidence, invokes applicable verification, and returns a factual outcome.

```text
Authorized work unit
      ↓
Capability check
      ↓
Authorization / Security Gate
      ↓
Pre-action checkpoint
      ↓
Execute bounded action
      ↓
Capture actual evidence
      ↓
Post-action checkpoint
      ↓
Verification
      ↓
Persist + return outcome
```

The runtime separates **AI decision from execution evidence**. A plan is not proof that an action happened. Missing capabilities are reported or explicitly delegated; they are never simulated. Resume compares current repository state with the checkpoint and never blindly replays an uncertain action.

See [`core/execution-runtime.md`](core/execution-runtime.md) and [`workflows/execution-runtime.md`](workflows/execution-runtime.md).

## Verification / Test Engine

The Verification / Test Engine makes verification an evidence-based stage rather than an assumption. It:

- selects applicable checks from the changed scope and project tooling;
- supports static, unit, integration, E2E, runtime, deployment, and security verification levels;
- executes supported checks or delegates them to CI/project tooling;
- records actual evidence and limitations;
- reports `VERIFIED`, `PARTIAL`, `UNVERIFIED`, or `FAILED` honestly;
- prevents claims such as “tests passed” when tests were not actually run.

See [`core/verification-engine.md`](core/verification-engine.md) and [`workflows/verification.md`](workflows/verification.md).

## Multi-AI portability

The project repository is the durable continuity layer. A new AI should not need the previous chat history or account memory to recover the project.

The portable adapter contract defines the minimum capabilities for a compatible AI: bootstrap project context, inspect source/Git, route human intent, resolve evidence and unfinished work, execute authorized workflows, verify with evidence, and persist meaningful state.

Host-specific capabilities belong in `adapters/`. The adapter is an integration boundary, not a second project-memory system.

See [`adapters/adapter-contract.md`](adapters/adapter-contract.md) and [`docs/MULTI-AI-PORTABILITY.md`](docs/MULTI-AI-PORTABILITY.md).

## Moving to a new AI

A new AI does **not** need the old chat history. The project carries its own durable context.

### Normal command

Open the project and say:

> **Open this project, read `AGENTS.md` and `.ai/manifest.yaml`, recover the current project state, and tell me what we should do next.**

Then continue naturally: `Continue`, `Fix this`, `Make it professional`, `Check it`, `Go ahead`, etc.

Full onboarding guidance: [`docs/NEW-AI-ONBOARDING.md`](docs/NEW-AI-ONBOARDING.md).

## Flow and architecture

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for the Development OS flow, layered architecture, portable-context model, new-AI onboarding sequence, agent orchestration, autonomous development loop, executable runtime, and automation boundaries.

## Architecture

- **Development OS** — reusable methodology, workflows, roles, rules, and adapters.
- **Project `.ai`** — authoritative portable project context.
- **Source code** — actual implementation.
- **Git history** — durable change history when version control is used.
- **AI account memory** — optional personal/contextual assistance, never the sole project memory.
- **GitHub/Supabase/local workers** — infrastructure used when appropriate.

## Safety

- Never commit secrets, tokens, passwords, private keys, or session cookies.
- Preserve existing behavior unless a change is intentional.
- Treat production/database/destructive changes as high-risk.
- Verify assumptions before changing important systems.
- Prefer small, reviewable changes.
- Test and report verification evidence before declaring work complete.
- Keep project-specific knowledge separate from global rules.
- Do not watch entire drives by default; configure dedicated project roots.
- Autonomous looping must remain bounded and must stop or escalate when authority, capability, evidence, or security conditions require it.
- The executable runtime must not claim execution or external results without actual host evidence.

## Repository structure

```text
chatgpt-development-os/
├── README.md
├── AGENTS.md
├── core/
├── agents/
├── workflows/
├── rules/
├── project-context-spec/
├── templates/
├── tools/
├── projects/
├── memory/
├── adapters/
├── docs/
└── .github/workflows/
```

## Version

0.12 — P12 Operational Intelligence: deterministic dependency graph/readiness, advisory prioritization, checkpoint intelligence, and Development Task Controller integration.
