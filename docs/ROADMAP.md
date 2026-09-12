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
- [x] Implement provider-backed reference operations
- [x] Add external integration end-to-end tests

### P8 — Remote Mutation Controls v1
- [x] Define explicit remote-mutation authorization boundary
- [x] Define target/scope validation and optimistic concurrency requirements
- [x] Define safe retry and uncertain-outcome semantics
- [x] Define Security Gate requirement for controlled remote mutation
- [x] Implement provider-backed GitHub file-update reference operation
- [x] Connect controlled file mutation to the executable runtime bridge
- [x] Add mutation safety tests and CI contract verification
- [ ] Execute a real provider-backed mutation only through an explicitly authorized production/test workflow
- [ ] Add controlled branch mutation
- [ ] Add controlled pull-request mutation
- [ ] Add controlled workflow trigger/mutation
- [ ] Add operation-specific rollback/recovery contracts for higher-impact mutations

### P9 — Development Task Controller v1
- [x] Define end-to-end task lifecycle and task states
- [x] Resolve project, canonical intent, durable state, objective, acceptance criteria, scope, and budget
- [x] Integrate orchestration/work units with capability and authorization checks
- [x] Connect bounded execution, checkpoints, verification, Security Gate, review, and durable persistence
- [x] Define evidence-backed final outcomes and blocker/escalation semantics
- [x] Implement the Development Task Controller
- [x] Add the P9 development task workflow
- [x] Add the P9 contract verifier
- [x] Wire P9 verification into CI
- [x] Verify current repository HEAD through the primary Development OS verification workflows

P9 is implemented and verified. Higher-impact remote mutations from P8 remain separately incomplete.

### P10 — Context Continuity & Recovery v1 — COMPLETE
- [x] Define repository-first continuity and recovery rules
- [x] Preserve an engineering-relevant chat recovery snapshot
- [x] Add durable context-sync contract verification
- [x] Make configurable meaningful-path patterns effective in context-sync
- [x] Wire context-sync verification into primary CI
- [x] Verify the repaired reusable context-sync workflow through an actual project-side caller run
- [x] Verify generated `STATE-INDEX.md` and `CHANGELOG.md` synchronization end-to-end
- [x] Document and validate future-session persistence expectations
- [x] Complete P10 with fresh CI and context-sync evidence

P10 is complete.

### P11 — DevOS Federation & Self-Healing Context v1 — COMPLETE

Goal: make DevOS context portable, self-identifying, recoverable, and resistant to stale/partial context across AI tools, accounts, projects, and connectivity interruptions.

- [x] Define a versioned DevOS project manifest and compatibility contract
- [x] Add automatic project identity/registration discovery
- [x] Add context freshness and integrity checks
- [x] Detect and reconcile stale `.ai` state against Git/source evidence
- [x] Add cross-AI bootstrap/recovery handshake
- [x] Persist AI-session handoff summaries with provenance
- [x] Add safe self-healing for missing derived context files
- [x] Define recovery precedence when ChatGPT memory, `.ai`, Git, and generated indexes disagree
- [x] Add P11 contract verification and CI coverage
- [x] Prove recovery from a fresh AI/account context using repository-only evidence

P11 identity, freshness/integrity, safe derived-state reconciliation, portable bootstrap/handoff, and fresh-context recovery are implemented. P12 is the active milestone.

### P12 — Operational Intelligence — ACTIVE

Goal: add advisory task intelligence and bounded scheduling above the existing controller and execution boundaries without creating a second executor or granting authority.

- [x] Define operational-intelligence graph/readiness model
- [x] Add dependency-aware prioritization and checkpoint signals
- [x] Add failure classification and raw-evidence intelligence
- [x] Add advisory next-action recommendations with `ADVISORY_ONLY` semantics
- [x] Integrate advisory intelligence with independent controller gating
- [x] Add bounded controller-to-runtime handoff v1
- [x] Add bounded Execution Runtime v1
- [x] Add autonomous development loop v2
- [x] Add durable runtime persistence v1
- [x] Add deterministic runtime recovery v1
- [x] Add Scheduler/Worker v1 with exactly one bounded iteration per invocation
- [x] Fail closed on unknown or malformed scheduler recovery state
- [x] Add executable scheduler/recovery proof and CI coverage
- [ ] Verify the hardened Scheduler/Worker v1 through live CI for the current HEAD
- [ ] Continue bounded P12 hardening through operation-specific capabilities

P12 is implemented through Scheduler/Worker v1 fail-closed recovery hardening. Current CI verification remains the acceptance gate. Higher-impact P8 remote mutations remain independently incomplete.

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
- [x] External Integration Adapter connected to the Executable Runtime for read-only GitHub operations
- [x] Remote Mutation Controls connected to the Executable Runtime for controlled GitHub file updates
- [x] Development Task Controller integrated into the runtime/orchestration/verification path
- [x] Durable context continuity work completed as P10
- [x] P11 continuity/federation scope recorded
- [x] P11 identity, integrity, and safe reconciliation gates verified by fresh CI
- [x] P12 runtime persistence and recovery boundaries documented
- [x] P12 Scheduler/Worker recovery hardening documented and tested

## Execution rule

Complete the current milestone before advancing to the next milestone. Do not mark work complete without repository evidence and appropriate verification.

## Current milestone

### P12 — Operational Intelligence — ACTIVE

P12 is active. Scheduler/Worker v1 fail-closed recovery hardening is implemented and documented, but current-HEAD CI evidence is still required before this slice is marked verified. Higher-impact P8 remote mutations remain independently incomplete.
