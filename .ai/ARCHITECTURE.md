# DevOS Project Architecture

## Core pipeline

`User intent → State + scope resolution → Work decomposition → Capability + authorization → Bounded execution → Checkpoint → Verification → Security → Review → Durable persistence → Evidence-backed outcome`

## Major layers

1. **State Resolver** — reconstructs current project/work state with Observed / Likely / Unknown evidence.
2. **Human Language Execution Engine** — normalizes natural language/Hinglish into canonical engineering intent and workflow.
3. **Verification Engine** — determines applicable checks and reports VERIFIED / PARTIAL / UNVERIFIED / FAILED only from evidence.
4. **Security Gate** — enforces authorization, credential protection, and high-impact/destructive boundaries.
5. **Teaching Engine** — supports do-it, teach-me, and explain modes without weakening engineering rigor.
6. **Multi-AI Portability / Auto-Onboarding** — makes project context recoverable across AI hosts and initializes durable `.ai` context safely.
7. **Agent Orchestration** — decomposes objectives into bounded work units and coordinates roles/dependencies.
8. **Autonomous Development Loop** — executes bounded iterations with checkpoint, verification, persistence, and stop/escalation rules.
9. **Executable Runtime** — executes already-authorized work units through declared capabilities.
10. **Host / External Adapters** — expose filesystem, Git, verification, GitHub and CI capabilities without granting authority.
11. **Runtime–Adapter Bridge** — connects authorized runtime work to bounded provider operations and normalized evidence.
12. **Remote Mutation Controls** — controls provider-backed GitHub file updates with explicit scope, optimistic concurrency, Security Gate, and uncertain-outcome handling.
13. **Development Task Controller (P9)** — integrates the full task lifecycle from request through durable evidence-backed outcome.

## Durable context

`.ai/` is portable project memory. `AGENTS.md` is the project AI entry point. `STATE-INDEX.md` is generated deterministic evidence and is not semantic authority. Source code and Git history remain authoritative for implementation state.

## Safety boundary

Adapters expose capabilities; they do not create authorization. High-impact remote mutations remain separately gated and are not implied by the controlled GitHub file-update capability.
