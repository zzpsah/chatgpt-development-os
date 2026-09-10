# AI State Resolver v1

## Purpose

AI State Resolver is the semantic layer between deterministic repository evidence and development execution.

Automation records facts. The AI determines what those facts mean for the user's current request.

The resolver answers:

> Given the user's request and the recovered project evidence, what is the current situation, what remains unfinished, and what should happen next?

It does not replace source inspection, tests, security review, or project-local decisions.

## Inputs

The resolver should consider, in this order where applicable:

1. Current user request and explicit authorization.
2. Project selected by Project Router.
3. `AGENTS.md`.
4. `.ai/manifest.yaml`.
5. `.ai/STATE-INDEX.md` for generated repository facts.
6. `.ai/PROJECT.md` for project purpose, scope, technology, and constraints.
7. `.ai/CURRENT-STATE.md` for verified semantic state.
8. `.ai/TASKS.md` for active, planned, blocked, and recently completed work.
9. `.ai/DECISIONS.md` for durable project decisions.
10. `.ai/ARCHITECTURE.md` when architecture affects the decision.
11. Recent `.ai/CHANGELOG.md` and session records.
12. Actual source, tests, configuration, deployment files, and Git history when needed to validate the evidence.

Chat/account memory is supplementary only and is never the authoritative project state.

## Output

A resolver result should contain:

```yaml
project:
objective:
facts:
  observed: []
  likely: []
  unknown: []
work:
  active: []
  blocked: []
  planned: []
verification:
  status: VERIFIED | PARTIAL | UNVERIFIED | FAILED
  evidence: []
candidates:
  - action:
    reason:
    evidence: []
    risk: LOW | MEDIUM | HIGH
recommended:
  action:
  reason:
  authorization: NOT_REQUIRED | REQUIRED | ALREADY_GRANTED
  confidence: HIGH | MEDIUM | LOW
```

The exact representation may change as the execution engine develops; the semantic fields are the v1 contract.

## Resolution rules

### 1. Resolve the project first

Never determine a next development action before the correct project is resolved. If multiple projects are plausible and the choice could change the result, ask for clarification.

### 2. Separate fact from meaning

Use these evidence levels:

- **Observed** — directly verified from repository files, Git, tests, or durable project context.
- **Likely** — an evidence-supported interpretation that still needs confirmation.
- **Unknown** — not established by available evidence.

Do not turn a likely interpretation into a fact merely because it sounds reasonable.

### 3. Treat generated state as evidence, not truth

`STATE-INDEX.md` is deterministic repository evidence. It can identify commits, changed paths, task counts, context health, and recent activity, but it does not know business intent, architecture rationale, root cause, correctness, or the true next task.

### 4. Prefer authoritative sources by question

- Repository facts → actual repository/Git evidence.
- Project intent and constraints → `.ai/PROJECT.md` and user instructions.
- Durable decisions → `.ai/DECISIONS.md`.
- Work status → `.ai/CURRENT-STATE.md`, `.ai/TASKS.md`, sessions, then repository evidence.
- Current intent → the user's current request.

When sources conflict, surface the conflict instead of silently choosing a convenient interpretation.

### 5. Do not infer correctness from silence

No recorded error does not mean the system works. No failing test does not mean tests were run. No known security issue does not mean the system is secure.

Verification status must be based on actual evidence.

### 6. Build candidate next actions from evidence

Every candidate action should have a reason and evidence basis. Do not invent requirements, architecture, bugs, or priorities.

### 7. Select unfinished work by priority

Unless the user explicitly requests something else, consider unfinished work in this order:

1. Active blockers, recovery, security, or data-loss risks.
2. Work explicitly requested by the user in the current request.
3. Active unfinished task already in progress.
4. A clearly documented planned task.
5. Maintenance or optional improvement.

A planned item must not outrank an explicit current request.

### 8. Respect authorization boundaries

Continuation authorizes normal development work when the intended action is clear. Destructive, production-impacting, security-sensitive, irreversible, or data-affecting actions require explicit authorization unless the project workflow already grants that authority safely.

### 9. Verification is part of the recommendation

For implementation actions, the recommended next action should include the appropriate verification step or identify why verification is currently unavailable.

### 10. Source inspection remains mandatory for important work

The resolver may identify the likely next task, but important implementation decisions must be validated against the actual source, configuration, tests, and Git state before changes are made.

## Resume behavior

For a request such as `bhai continue`:

```text
User request
    ↓
Project Router
    ↓
Durable project context
    ↓
AI State Resolver
    ↓
Observed / Likely / Unknown
    ↓
Active / Blocked / Planned work
    ↓
Verification status
    ↓
Candidate next actions
    ↓
Priority + risk + authorization
    ↓
Recommended next action
    ↓
Inspect source → Implement → Verify → Persist
```

The resolver must not simply return the last edited file as the next task. Last activity is evidence, not necessarily unfinished intent.

## Safety

- Never guess the project when multiple plausible projects exist.
- Never expose secrets, tokens, passwords, private keys, session cookies, or unnecessary personal/student data.
- Never convert emotional language into destructive authority.
- Never claim tests, security review, deployment, or correctness without evidence.
- Never silently overwrite project-local semantic state because generated state looks different.
- Preserve the distinction between recommendation and execution.

## v1 scope

Included:

- Semantic state reconstruction.
- Evidence classification.
- Unfinished-work identification.
- Candidate next-action generation.
- Priority and risk handling.
- Verification-state handling.
- Authorization awareness.
- Structured resolver output.

Not included yet:

- Autonomous multi-step execution.
- Automatic root-cause inference without source inspection.
- Automatic test generation/execution.
- Full security gate.
- Cross-project dependency reasoning.
- Automatic onboarding of arbitrary repositories.

Those belong to later Development OS milestones.
