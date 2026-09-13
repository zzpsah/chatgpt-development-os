# DevOS Project Architecture

## Core pipeline

`Human input → Human Language Execution Engine → Project Router / State + scope resolution → Work decomposition → Capability + authorization → Bounded execution → Checkpoint → Verification → Security → Review → Durable persistence → Evidence-backed outcome`

Human Language Interpretation is the normative top-level semantic entry point for human-originated DevOS work. It is not a side utility. It converts natural language, Hinglish, shorthand, contextual continuation, corrections, and constraints into a bounded semantic objective before project/workflow selection. It never grants technical authority.

## Major layers

1. **Human Language Execution Engine (P15)** — top-level semantic interface; normalizes human language/Hinglish/context into canonical engineering intent, constraints, ambiguity, and safe workflow-routing input without manufacturing authorization.
2. **Project Router + State Resolver** — resolves the authoritative project and reconstructs current project/work state with Observed / Likely / Unknown evidence.
3. **Development Task Controller (P9)** — integrates the full task lifecycle from interpreted request through durable evidence-backed outcome.
4. **Verification Engine** — determines applicable checks and reports VERIFIED / PARTIAL / UNVERIFIED / FAILED only from evidence.
5. **Security Gate** — enforces authorization, credential protection, and high-impact/destructive boundaries; `SECURITY_REVIEW` routes through the dedicated security workflow.
6. **Teaching Engine** — supports do-it, teach-me, and explain modes without weakening engineering rigor.
7. **Multi-AI Portability / Auto-Onboarding** — makes project context recoverable across AI hosts and initializes durable `.ai` context safely.
8. **Agent Orchestration** — decomposes objectives into bounded work units and coordinates roles/dependencies.
9. **Autonomous Development Loop** — executes bounded iterations with checkpoint, verification, persistence, and stop/escalation rules.
10. **Executable Runtime** — executes already-authorized work units through declared capabilities.
11. **Host / External Adapters** — expose filesystem, Git, verification, GitHub and CI capabilities without granting authority.
12. **Runtime–Adapter Bridge** — connects authorized runtime work to bounded provider operations and normalized evidence.
13. **Remote Mutation Controls** — controls provider-backed GitHub file updates with explicit scope, optimistic concurrency, Security Gate, and uncertain-outcome handling.

## Language evolution boundary

The deterministic v2 interpreter is the minimum executable behavior contract, not the ceiling of DevOS understanding. Future language versions may improve multilingual interpretation, typo tolerance, correction handling, referent resolution, temporal context, intent decomposition, and confidence calibration. Every evolution must preserve project isolation, explicit constraints, authorization, evidence, Security Gate, and verification contracts and must regression-test prior behavior.

## Durable context

`.ai/` is portable project memory. `AGENTS.md` is the project AI entry point. `STATE-INDEX.md` is generated deterministic evidence and is not semantic authority. Source code and Git history remain authoritative for implementation state.

## Safety boundary

Adapters expose capabilities; they do not create authorization. Human-language interpretation also does not create authorization. High-impact remote mutations remain separately gated and are not implied by language confidence, conversational context, stance codes, or the controlled GitHub file-update capability.
