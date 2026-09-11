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

### P4 — Autonomous Development Loop
- [x] Define autonomous-loop lifecycle and bounded iteration
- [x] Define stop/continue/escalation conditions
- [x] Connect orchestration outputs to executable workflow steps
- [x] Define capability checks and honest delegation when a host lacks tools
- [x] Define checkpointing and resumability between iterations
- [x] Define approval gates for high-risk actions
- [x] Define end-to-end evidence aggregation
- [x] Build contract verification harness and CI integration

### P5 — Executable Development Runtime
- [x] Runtime execution contract
- [x] Work-unit execution and capability registry
- [x] Checkpoint and resume contract
- [x] Evidence capture and safety boundaries
- [x] Runtime workflow and verification harness

### P6 — Host Execution Adapters
- [x] Define host adapter contract
- [x] Define capability discovery and honest availability states
- [x] Define scoped filesystem, Git, verification, and GitHub/CI boundaries
- [x] Define normalized execution evidence and failure semantics
- [x] Implement portable reference adapters
- [x] Execute real bounded operations through adapters
- [x] Add adapter integration tests and end-to-end runtime verification

### P7 — External Integration Adapters
- [x] Define external integration contract
- [x] Define GitHub/CI capability and authorization boundaries
- [x] Define actual-response evidence and safe retry semantics
- [x] Add GitHub external adapter profile
- [x] Add contract verification harness and CI integration
- [ ] Implement provider-backed reference operations
- [ ] Add external integration end-to-end tests

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
- [x] Autonomous Development Loop architecture, workflow, and validation synchronized
- [x] Executable Runtime architecture, workflow, and validation synchronized
- [x] Host Adapter architecture and contract synchronized
- [x] Verification Adapter architecture and reference implementation synchronized
- [x] External Integration Adapter architecture and contract synchronized
- [x] This roadmap and Git/project state do not contradict each other

## Execution rule

Complete the current milestone before advancing to the next milestone. Do not mark work complete without repository evidence and appropriate verification.

## Next planned capability

### P7 — External Integration Adapters

P7 adds controlled adapters for remote GitHub/CI operations and other external systems where supported. These adapters must preserve explicit authorization, provider capability discovery, actual-response evidence, bounded retries, and Security Gate enforcement. Remote mutation must never be implied by local repository access.
