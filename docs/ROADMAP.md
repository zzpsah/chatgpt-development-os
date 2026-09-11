# Development OS Roadmap

This is the authoritative high-level implementation order for the Development OS repository. Git history and project-local `.ai` state remain authoritative for actual implementation state.

## Milestones

### P0 — AI State Resolver v1
- [x] Resolver contract and purpose
- [x] Observed / Likely / Unknown evidence model
- [x] Unfinished-work prioritization
- [x] Verification and authorization rules
- [x] `core/ai-state-resolver.md`
- [x] Integrate with resume workflow
- [x] End-to-end verification

### P1 — Human Language Execution Engine
- [x] Normalize natural language into engineering intents
- [x] Map intents to workflows
- [x] Safely combine multiple intents
- [x] Preserve authorization boundaries
- [x] Define verification expectations
- [x] Integrate routing and architecture documentation
- [x] Contract verification harness

### P1 — Verification / Test Engine
- [x] Define verification levels and evidence model
- [x] Detect applicable tests/checks
- [x] Execute or delegate supported checks
- [x] Honest VERIFIED / PARTIAL / UNVERIFIED / FAILED reporting
- [x] Prevent unsupported correctness claims
- [x] Integrate verification workflow and CI contract harness

### P1 — Security Gate
- [x] Define security review stages
- [x] Auth/authz and data-access checks
- [x] Secret/credential protection
- [x] Dependency and configuration checks
- [x] Production/destructive-action gates
- [x] Integrate Security Gate with language, review, and CI workflows
- [x] Contract verification harness and successful CI run

### P2 — Teaching Engine
- [x] Do-it / Teach-me / Explain modes
- [x] Simple mental model before terminology
- [x] Practical infrastructure/operations connections
- [x] Progressive developer growth with full engineering rigor
- [x] Evidence-aware teaching and safe learning boundaries
- [x] Contract verification harness and CI integration
- [x] Integrate teaching behavior with language routing and architecture

### P2 — Multi-AI Portability
- [x] Vendor/account-independent project context
- [x] Adapter contract
- [x] ChatGPT/Codex adapter documentation
- [x] Repository-only recovery by another AI

### P2 — Auto-Onboarding
- [x] Existing-repository onboarding flow
- [x] Onboarding script/workflow
- [x] Context validation
- [x] Preserve existing context; no destructive overwrite
- [x] GitHub-side versus local automation boundaries

### P3 — Agent Orchestration
- [x] Orchestration contract and role coordination
- [x] Work-unit, dependency, and parallelism rules
- [x] Evidence handoff and failure recovery
- [x] Authorization, scope, verification, and security boundaries
- [x] Orchestration workflow
- [x] Verification harness and CI integration

## Cross-cutting

- [x] `.ai` remains durable project-local memory
- [x] Git/source remains implementation authority
- [x] `STATE-INDEX.md` remains deterministic
- [x] DevOS tooling/workflows gain validation tests
- [x] README and architecture docs synchronized for the Human Language Execution Engine
- [x] Teaching Engine architecture and routing synchronized
- [x] Multi-AI portability architecture and documentation synchronized
- [x] Auto-Onboarding architecture, tooling, and validation synchronized
- [x] Agent Orchestration architecture, workflow, and validation synchronized
- [x] This roadmap and Git/project state do not contradict each other

## Execution rule

Complete the current milestone before advancing to the next milestone. Do not mark work complete without repository evidence and appropriate verification.

## Next planned capability

### P4 — Autonomous Development Loop

The next phase will turn the existing contracts into a controlled end-to-end execution loop. It will define how DevOS repeatedly moves from objective → state resolution → planning/orchestration → authorized implementation → verification → review → persistence, while stopping safely when authority, evidence, or required capabilities are missing.

Planned scope:

- [ ] Define autonomous-loop lifecycle and bounded iteration
- [ ] Define stop/continue/escalation conditions
- [ ] Connect orchestration outputs to executable workflow steps
- [ ] Define capability checks and honest delegation when a host lacks tools
- [ ] Define checkpointing and resumability between iterations
- [ ] Define approval gates for high-risk actions
- [ ] Define end-to-end evidence aggregation
- [ ] Build contract verification harness and CI integration

P4 does **not** mean unrestricted autonomous deployment or removal of user authorization. The existing Security Gate, Verification / Test Engine, project-local `.ai` context, and Git/source authority remain in force.
