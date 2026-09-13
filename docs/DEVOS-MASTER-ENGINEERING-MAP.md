# DevOS Master Engineering Map

> Living architecture, history, future flow, semantic model, portability target, and self-evolution rules for the Development OS.

## Core engineering law

> **What is not written was never done.**

This is a permanent DevOS engineering law.

Every material AI engineering action, decision, repair, experiment, verification result, evidence change, architecture change, roadmap change, or externally relevant outcome is unfinished until its durable repository record exists.

```text
OBSERVE
  ↓
ACT / CHANGE / DECIDE
  ↓
VERIFY WHAT ACTUALLY HAPPENED
  ↓
DOCUMENT THE ACTION + EVIDENCE + LIMITATIONS
  ↓
UPDATE DURABLE STATE / ARCHITECTURE
  ↓
PERSIST IN GIT
```

A durable record must let the next AI recover: **WHAT happened, WHY, WHERE, HOW it was verified, WHAT proves it, WHAT remains unknown, and WHAT to do next.** Chat memory, private model memory, temporary tool output, or undocumented local work is not a durable completion record.

Completion is:

```text
IMPLEMENTED + VERIFIED + DOCUMENTED + DURABLE STATE
```

Permanent authority boundaries remain:

```text
INTERPRETATION != AUTHORIZATION
PLAN != EXECUTION
READY != EXECUTION
DOCUMENTATION != AUTHORIZATION
CI PASS != AUTHORIZATION
PROVIDER CREDENTIAL != DEVOS AUTHORIZATION
SIMULATED EVIDENCE != LIVE PROVIDER PROOF
PROVIDER RESPONSE != COMPLETION PROOF
RECOVERY != AUTOMATIC MUTATION REPLAY
```

## Objective

DevOS is a repository-first Development OS for AI-assisted software engineering. It is intended to make engineering context, governance, planning, execution boundaries, verification, recovery, and engineering knowledge portable across AI models/vendors, AI accounts/chats, coding agents/MCP hosts, machines, Git providers, provider adapters, and multiple concurrently managed projects.

```text
AI A + Account A
      ↓
   Repository
      ↓
AI B + Account B
      ↓
Correct state recovery
      ↓
Safe continuation
```

The repository carries project truth. Chat memory is supplementary context, never project authority.

## Verified architecture history

```text
P9  Development Task Controller
P10 Context Continuity & Recovery
P11 Federation & Self-Healing Context
P12 Operational Intelligence
P13 Autonomous Development Orchestration
P14 Adaptive Verification & Self-Healing
P15 Human Language Interpretation v2
P16 Semantic Goal-to-Plan Compiler
P17 Step Readiness & Authorization Orchestrator
```

Later unnumbered hardening/extension work includes Production E2E, Failure + Recovery, Multi-Session/Fresh-AI Continuation, Controlled Remote Mutation, Production-Readiness Evidence, Trust-First Audit, Foundation Health/Doctor, Universal Onboarding + Repository Creation, Recovery Friction/Health, MCP/App repository.create, Current-Source Evidence, MCP/App Permission Control Plane + Multi-Project Isolation, and Actionable HOLD + Scoped Approval + governed continuation.

These labels are architecture history, not an instruction to invent endless numbered phases.

## Current governed flow

```mermaid
flowchart TD
    U[Human request<br/>English / Hinglish / shorthand] --> P15[P15 interpretation]
    P15 --> S[Project + repository state]
    S --> P16[P16 bounded plan]
    P16 --> P17[P17 readiness + authorization]
    P17 --> AH[Actionable HOLD / Scoped Approval]
    AH --> CTRL[Development Task Controller]
    CTRL --> RT[Bounded Runtime]
    RT --> V[Verification + Security Gate]
    V --> D[Durable evidence + state]
    D --> R[Recovery / continuation]
    R --> S
    RT --> RP[Remote Permission Control Plane]
    RP --> PA[Provider / MCP / App adapter]
    PA --> FR[Fresh readback]
    FR --> V
```

This is a governed loop. Continuation always re-enters current repository state and current gates. Old plans, approvals, checkpoints, or successful runs never silently manufacture permission.

## Semantic architecture

```mermaid
flowchart LR
    N[Human language<br/>intent + constraints] --> I[P15 interpretation]
    I --> G[Goal]
    G --> P[P16 plan]
    P --> R[P17 readiness]
    R --> A[Exact authorization]
    A --> X[Actual execution evidence]
    X --> V[Verification evidence]
    V --> D[Durable project state]
    D --> C[Continuity / recovery]
    C --> I
    K[Provider credential] -. capability only .-> A
    M[Chat/model memory] -. supplementary only .-> I
```

## Any-account / any-AI / any-platform target

```mermaid
flowchart LR
    A1[AI host / account A] --> H1[Host adapter]
    A2[AI host / account B] --> H2[Host adapter]
    A3[AI host / account C] --> H3[Host adapter]
    H1 --> CORE[DevOS governed core]
    H2 --> CORE
    H3 --> CORE
    CORE --> REPO[Project repository + .ai]
    CORE --> PROVIDER[Git / MCP / App / tool adapters]
    CORE --> CI[CI + verification]
```

A compatible AI should recover source/Git + `.ai`, inspect current HEAD, interpret the request, compile bounded plans, obtain current readiness/authorization, execute only through supported runtime/adapters, verify actual outcomes, persist evidence, and continue from a fresh session without the previous chat.

## Future automated engineering flow

```text
Human objective
  ↓
Bootstrap + identity
  ↓
Repository-first recovery
  ↓
P15 interpretation
  ↓
P16 bounded plan
  ↓
P17 exact-step readiness
  ↓
Scoped approval / Security evidence
  ↓
Controller
  ↓
Bounded runtime + adapters
  ↓
Fresh verification / readback
  ↓
Document action + evidence + limitations
  ↓
Update .ai + state + decisions + session provenance
  ↓
Update master architecture when materially affected
  ↓
Regression + CI
  ↓
CONTINUE | HOLD | STOP | ESCALATE
```

## Every-AI maintenance contract

A new AI is a maintainer, not merely a reader.

```text
READ CURRENT REPO
      ↓
IDENTIFY ACTIVE OBJECTIVE
      ↓
INSPECT SOURCE / CONTRACTS / TESTS / EVIDENCE
      ↓
PERFORM BOUNDED WORK
      ↓
VERIFY ACTUAL OUTCOME
      ↓
DOCUMENT EVERY MATERIAL ACTION
      ↓
UPDATE STATE / TASKS / DECISIONS / SESSION PROVENANCE
      ↓
UPDATE THIS MASTER MAP WHEN MATERIAL
      ↓
CI + INTEGRITY
      ↓
LEAVE FRESH RECOVERABLE STATE
```

An undocumented material action is **unfinished work**, not silently completed history.

## Human Language Interpreter evolution

P15 evolves by evidence-driven experiments using real interaction examples, user corrections, outcome evidence, regression corpora, and adversarial tests.

```mermaid
flowchart TD
    IN[Real human language] --> OBS[Observed input + context]
    OBS --> BASE[Current interpreter]
    BASE --> OUT[Candidate interpretation]
    OUT --> E[Outcome / correction / evidence]
    E --> EXP[Experiment ledger]
    EXP --> HYP[Improvement hypothesis]
    HYP --> REG[Regression + adversarial tests]
    REG --> GATE{Safety + semantic gates}
    GATE -->|PASS| NEW[Versioned interpreter]
    GATE -->|FAIL| DISCARD[Reject / defer]
    NEW --> BASE
```

Experiments record source head, input/context, baseline/candidate outputs, semantic delta, false-positive/false-negative hypotheses, security/authorization analysis, regression evidence, observed result, and `ADOPT | REJECT | DEFER`.

> **The interpreter may learn better language understanding; it may never learn that language itself grants authority.**

## Self-maintaining knowledge model

Automation may safely update machine-verifiable facts such as Git HEAD, changed files, CI outcomes, timestamps, generated indexes, factual summaries, health diagnostics, and evidence references.

AI/engineering judgment is required for semantic architecture, decisions, requirements, objectives, future plans, interpreter conclusions, and security/authorization meaning. Automation must not infer semantic truth from commit messages alone.

The master map is a living navigation/design layer, not a competing source of truth. Source code, contracts, tests, Git history, evidence records, and explicit decisions remain authoritative underneath it.

## Future goals

- **G1 Universal project recovery:** any AI/account/machine recovers correct state without chat-history dependency.
- **G2 Universal host adapter:** compatible AI hosts use the same semantic/runtime contracts.
- **G3 Provider-neutral remote operations:** provider capability remains separate from DevOS authority.
- **G4 Safe long-running engineering agent:** multi-session work with checkpoints, recovery, scoped continuation, and no-blind-replay.
- **G5 Evidence-native development:** important claims trace to source/tests/CI/runtime evidence or clearly marked simulation.
- **G6 Self-improving P15:** interpretation improves through experiments while authority rules remain invariant.
- **G7 Multi-project isolation:** project state, approval, provider binding, and context never leak across projects.
- **G8 Automated engineering lifecycle:** inspect → plan → implement → verify → document → continue, with human escalation when required.
- **G9 Evidence-based production readiness:** readiness is measured evidence, not prose.
- **G10 Self-maintaining engineering knowledge:** every material AI action is durably recorded and materially updates this map when appropriate.

## Outside automatic authority

Even future highly autonomous DevOS must separately gate destructive deletion, force updates, production deployments, permission/credential/secret changes, destructive database changes, security-policy weakening, account/identity changes, and irreversible external side effects.

More autonomy means better planning, recovery, verification, documentation, and tool coordination — not weaker authorization.

## Fresh-AI continuation protocol

```text
1. Read AGENTS.md.
2. Read .ai/manifest.yaml.
3. Read .ai/CURRENT-STATE.md.
4. Read .ai/TASKS.md.
5. Read .ai/DECISIONS.md.
6. Read this master engineering map.
7. Inspect Git HEAD and working tree.
8. Inspect applicable CI / evidence.
9. Resolve conflicts using repository-first precedence.
10. Identify the active bounded objective.
11. Rebuild the current plan; do not trust stale chat instructions.
12. Work only through governed gates.
13. Verify what actually happened.
14. Document every material action and limitation.
15. Persist durable state and provenance.
16. Update the master map when material architecture/future direction changed.
```

## Maintenance links

- Normative living-state contract: `core/devos-living-state-and-evolution.md`
- P15 experiment ledger: `docs/DEVOS-INTERPRETER-EXPERIMENT-LEDGER.md`
- Fresh-AI discovery: `docs/handoff/README.md`
- Current source/project truth: `.ai/CURRENT-STATE.md`, `.ai/TASKS.md`, `.ai/DECISIONS.md`, Git/source/tests/CI

## Final direction

```text
Vendor-neutral engineering OS
+ portable project memory
+ human-language semantic interface
+ bounded planning
+ exact readiness / authorization
+ controlled execution
+ evidence-first verification
+ multi-project isolation
+ adaptive recovery
+ experiment-driven P15 evolution
+ automatic factual synchronization
+ mandatory durable documentation
+ continuously updated master architecture
+ durable future roadmap
= continuously developable AI engineering platform
```

## Plain first-contact portability

For a fresh AI chat, [DEVOS-PROJECT-CONTEXT.md](../DEVOS-PROJECT-CONTEXT.md) provides a repository-first context and recovery path. It uses normal project-documentation language, asks the host to report accessible evidence and unknowns before material work, and explicitly preserves host policies and authorization boundaries. It is locally tested documentation, not evidence that every external AI host will access or follow it.
