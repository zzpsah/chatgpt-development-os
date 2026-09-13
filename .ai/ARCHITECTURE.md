# DevOS Project Architecture

## Core pipeline

`Human input → Human Language Execution Engine → Project Router / State + scope resolution → P16 Semantic Goal-to-Plan Compiler → Development Task Controller → Work decomposition / Operational Intelligence → Capability + authorization → Bounded execution → Checkpoint → Verification → Security → Review → Durable persistence → Evidence-backed outcome`

Human Language Interpretation is the normative top-level semantic entry point for human-originated DevOS work. It is not a side utility. It converts natural language, Hinglish, shorthand, contextual continuation, corrections, and constraints into a bounded semantic objective before project/workflow selection. It never grants technical authority.

P16 is the explicit planning boundary between resolved semantic intent/state and the Development Task Controller. It converts the resolved objective into a bounded dependency-aware plan with explicit constraints, authority classes, evidence expectations, verification obligations, and stop/escalation conditions. The compiler returns `execution: NONE`, `authority: UNCHANGED`, and `authorization: UNCHANGED`; planning structure is never permission or execution evidence.

## Major layers

1. **Human Language Execution Engine (P15)** — top-level semantic interface; normalizes human language/Hinglish/context into canonical engineering intent, constraints, ambiguity, and safe workflow-routing input without manufacturing authorization.
2. **Project Router + State Resolver** — resolves the authoritative project and reconstructs current project/work state with Observed / Likely / Unknown evidence.
3. **Semantic Goal-to-Plan Compiler (P16)** — transforms resolved intent/objective/state into `DEVOS-GOAL-PLAN-v1`, preserving negative constraints, dependencies, ambiguity, impact/authority classifications, evidence expectations, verification obligations, and stop/escalation conditions without executing or authorizing work.
4. **Development Task Controller (P9)** — consumes only validated `PLANNED` compiler output for the P16 path, preserves compiled boundaries, independently rechecks repository/capability/authorization/security/verification conditions, and integrates the full task lifecycle through durable evidence-backed outcome. Legacy P12 task-inventory input remains supported for compatibility.
5. **Verification Engine** — determines applicable checks and reports VERIFIED / PARTIAL / UNVERIFIED / FAILED only from evidence.
6. **Security Gate** — enforces authorization, credential protection, and high-impact/destructive boundaries; `SECURITY_REVIEW` routes through the dedicated security workflow.
7. **Teaching Engine** — supports do-it, teach-me, and explain modes without weakening engineering rigor.
8. **Multi-AI Portability / Auto-Onboarding** — makes project context recoverable across AI hosts and initializes durable `.ai` context safely.
9. **Agent Orchestration** — decomposes objectives into bounded work units and coordinates roles/dependencies.
10. **Autonomous Development Loop** — executes bounded iterations with checkpoint, verification, persistence, and stop/escalation rules.
11. **Operational Intelligence (P12)** — provides evidence-backed dependency/readiness analysis and advisory next-action signals; it is advisory only and cannot create authority.
12. **Executable Runtime** — executes already-authorized work units through declared capabilities.
13. **Host / External Adapters** — expose filesystem, Git, verification, GitHub and CI capabilities without granting authority.
14. **Runtime–Adapter Bridge** — connects authorized runtime work to bounded provider operations and normalized evidence.
15. **Remote Mutation Controls** — controls provider-backed GitHub file updates with explicit scope, optimistic concurrency, Security Gate, and uncertain-outcome handling.

## P16 executable integration boundary

`tools/development-task-controller.py` accepts either the legacy P12 task inventory or a `compiled_plan` envelope. For the P16 path it must:

- accept only protocol `DEVOS-GOAL-PLAN-v1` with `decision: PLANNED`;
- reject compiler output that changes authority/authorization or claims execution;
- validate bounded step identity, objective, dependency, impact, authorization flag, and verification metadata;
- materialize only compiled plan steps into the controller task graph;
- preserve dependency ordering and completed-step evidence;
- require stronger authorization and Security Gate evidence for compiler-marked high-impact/security/production-destructive steps;
- never treat compiler output as proof of execution;
- return only a non-executing controller decision before runtime handoff.

`CLARIFY` and `BLOCKED` compiler output cannot become executable work merely because Operational Intelligence ranks something highly or prior work succeeded.

## Language evolution boundary

The deterministic v2 interpreter is the minimum executable behavior contract, not the ceiling of DevOS understanding. Future language versions may improve multilingual interpretation, typo tolerance, correction handling, referent resolution, temporal context, intent decomposition, and confidence calibration. Every evolution must preserve project isolation, explicit constraints, authorization, evidence, Security Gate, and verification contracts and must regression-test prior behavior.

## Durable context

`.ai/` is portable project memory. `AGENTS.md` is the project AI entry point. `STATE-INDEX.md` is generated deterministic evidence and is not semantic authority. Source code and Git history remain authoritative for implementation state.

## Safety boundary

Adapters expose capabilities; they do not create authorization. Human-language interpretation and P16 planning also do not create authorization. High-impact remote mutations remain separately gated and are not implied by language confidence, conversational context, stance codes, compiled-plan classification, Operational Intelligence priority, or the controlled GitHub file-update capability.
