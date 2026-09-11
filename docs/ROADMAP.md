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

### P2 — Multi-AI Portability
- [ ] Vendor/account-independent project context
- [ ] Adapter contract
- [ ] ChatGPT/Codex adapter documentation
- [ ] Repository-only recovery by another AI

### P2 — Auto-Onboarding
- [ ] Existing-repository onboarding flow
- [ ] Onboarding script/workflow
- [ ] Context validation
- [ ] Preserve existing context; no destructive overwrite
- [ ] GitHub-side versus local automation boundaries

## Cross-cutting

- [ ] `.ai` remains durable project-local memory
- [ ] Git/source remains implementation authority
- [ ] `STATE-INDEX.md` remains deterministic
- [ ] DevOS tooling/workflows gain validation tests
- [x] README and architecture docs synchronized for the Human Language Execution Engine
- [ ] This roadmap and Git/project state do not contradict each other

## Execution rule

Complete the current milestone before advancing to the next milestone. Do not mark work complete without repository evidence and appropriate verification.
