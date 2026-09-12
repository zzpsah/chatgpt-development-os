# Current State

## Snapshot

- Repository: `zzpsah/chatgpt-development-os`
- Branch: `main`
- Current state is established from Git/source evidence; this file is a durable recovery summary, not a replacement for source inspection.
- P9 Development Task Controller v1 is complete.
- P10 Context Continuity & Recovery v1 is complete.
- P11 DevOS Federation & Self-Healing Context v1 is complete.
- P12 Operational Intelligence is the active milestone.

## Implemented architecture

The repository contains the DevOS architecture through P12 foundations:

1. AI State Resolver
2. Human Language Execution Engine
3. Verification / Test Engine
4. Security Gate
5. Teaching Engine
6. Multi-AI Portability
7. Auto-Onboarding
8. Agent Orchestration
9. Autonomous Development Loop
10. Executable Development Runtime
11. Host Execution Adapters
12. External Integration Adapters
13. Runtime–Adapter Execution Bridge
14. Remote Mutation Controls
15. Development Task Controller (P9)
16. Context Continuity & Recovery (P10)
17. DevOS Federation & Self-Healing Context (P11)
18. Composable stance + communication-style layer (`DEVOS::<STANCE>::<STYLE>`)
19. Deterministic derived-context self-healing layer
20. Repository-first recovery precedence resolver
21. P11 recovery/revalidation and bounded self-healing integrated into the task lifecycle
22. P12 Operational Intelligence: task graph, readiness, prioritization, checkpoints, failure/evidence intelligence, and advisory next-action boundary

## P12 status

P12 graph/readiness, prioritization/checkpoint, failure/evidence, and advisory next-action slices are repository-backed. The operational-intelligence contract uses `ADVISORY_ONLY`; Operational Intelligence does not authorize execution, mutation, deployment, publication, or security bypass. The contract explicitly documents dependency-aware prioritization.

A fresh CI run on the latest P12 contract fix exposed a Python 3.14 compatibility failure in the executable verifier's dynamic module loading: `dataclass` inspection could not resolve `cls.__module__` because the dynamically imported module was not registered in `sys.modules`. The verifier fix registers the module before `exec_module`; this is an executable-verifier compatibility repair, not an authority change. Live CI verification remains required before claiming P12 contract green.

## Portable project memory

The repository is the durable project-memory boundary. A fresh AI/tool must recover from `AGENTS.md`, `.ai/manifest.yaml`, and the `.ai` context before resolving source/Git state. `tools/devos-bootstrap.py` is the deterministic non-executing bootstrap inspector, and `tools/test-devos-bootstrap.py` proves deterministic discovery on the repository path. The contract CI runs this proof.

Portable memory is context, not authority: it does not authorize execution, mutation, deployment, publication, or security bypass.

## Recovery precedence

1. Source tree + Git for exact implementation state.
2. Explicit requirements/decisions for intentional project state.
3. Durable `.ai` state for project context and handoff.
4. Generated indexes for navigation/evidence only.
5. AI account memory/chat history as supplementary context and never as authoritative repository evidence.

## Self-healing boundary

Only deterministic derived artifacts are eligible for automated recreation: `STATE-INDEX.md`, `CHANGELOG.md`, and `PROJECT-IDENTITY.json`. Semantic project files such as `PROJECT.md`, `DECISIONS.md`, `TASKS.md`, `CURRENT-STATE.md`, and `ARCHITECTURE.md` are outside the self-healing write boundary.

## Durable future-work rule

Future meaningful engineering work, decisions, blockers, verification evidence, and recovery notes must be persisted in the repository-local `.ai` context. Use `.ai/SESSIONS/` for session-level semantic records and update `TASKS.md`, `DECISIONS.md`, and `CURRENT-STATE.md` when durable project state changes. Chat history is not the authoritative recovery layer.

## Authority

For implementation state use source tree + Git. For intentional decisions use `DECISIONS.md`. For remaining work use `TASKS.md` plus current evidence. `STATE-INDEX.md` is deterministic evidence indexing only. ChatGPT memory and old conversations are supplementary.
