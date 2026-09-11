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
- [ ] Normalize natural language into engineering intents
- [ ] Map intents to workflows
- [ ] Safely combine multiple intents
- [ ] Preserve authorization boundaries
- [ ] Define verification expectations

### P1 — Verification / Test Engine
- [ ] Define verification levels and evidence model
- [ ] Detect applicable tests/checks
- [ ] Execute or delegate supported checks
- [ ] Honest VERIFIED / PARTIAL / UNVERIFIED / FAILED reporting
- [ ] Prevent unsupported correctness claims

### P1 — Security Gate
- [ ] Define security review stages
- [ ] Auth/authz and data-access checks
- [ ] Secret/credential protection
- [ ] Dependency and configuration checks
- [ ] Production/destructive-action gates

### P2 — Teaching Engine
- [ ] Do-it / Teach-me / Explain modes
- [ ] Simple mental model before terminology
- [ ] Practical infrastructure/operations connections
- [ ] Progressive developer growth with full engineering rigor

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
- [ ] README and architecture docs stay synchronized with implemented behavior
- [ ] This roadmap and Git/project state do not contradict each other

## Execution rule

Complete the current milestone before advancing to the next milestone. Do not mark work complete without repository evidence and appropriate verification.
