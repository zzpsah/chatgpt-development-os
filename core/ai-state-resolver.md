# AI State Resolver — v2 Current Contract

> **Reading order:** [v2 deterministic implementation](#v2-deterministic-implementation) is the current executable contract for claim records, grounding, confidence, validation, output, and P15/P16/P17 propagation. The earlier v1 semantic/recovery sections are retained as historical context. If the sections differ, v2 governs.

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

- **Observed** — in resolver v2, only a claim with current P12 execution evidence and citable provenance. A durable record is not sufficient by itself.
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

## v2 deterministic implementation

`tools/ai-state-resolver.py` implements a read-only, deterministic resolver. It accepts claim records plus recovery/handoff events and changed paths; it returns `DEVOS-AI-STATE-RESOLUTION-v2`. It neither reads a provider nor writes repository state.

### Claim record

```yaml
- id: stable-claim-id
  statement: plain-language claim
  state_confidence: observed | likely | unknown
  grounding:
    type: execution_evidence | durable_state | none
    ref: P12-evidence-id or file-path-plus-line
  revalidated_at: ISO-8601 timestamp or null
  revalidate_on: [RECOVERY_BOUNDARY, HANDOFF_BOUNDARY, path-glob]
```

`observed` requires current P12 `execution_evidence` with a non-empty grounding reference. An uncited observed claim is malformed and resolves to `unknown`. A `durable_state` record proves only that an assertion was recorded, so an observed durable-state claim resolves to `likely` even when it has a file/line reference. Duplicate claim identifiers also resolve to `unknown`; conflicts must be surfaced, never silently selected.

`execution_evidence` belongs to P12. The resolver accepts it only by reference and uses P12 freshness: an observed claim based on non-current P12 evidence decays to `likely`. It never re-normalizes the evidence.

`durable_state` is broader semantic project context. It is capped at `likely` until independently supported by current P12 execution evidence. Recovery/handoff boundaries and configured path changes remain explicit reasons to revalidate it. The default revalidation boundaries are recovery and handoff.

### Downstream propagation

P16 may receive a resolver result as `state_resolution`. If it includes unresolved claim IDs, P16 returns `CLARIFY` and preserves the named uncertainty. A `PLANNED` envelope retains resolver provenance. P17 rejects a tampered `PLANNED` envelope that contains unresolved resolver claims. `likely` remains an explicit uncertainty signal; it does not automatically block every plan. This does not change P17 authorization, Security Gate, capability, verification, or runtime gates.

```text
P11 recovery -> resolver v2 -> P16 plan -> P17 readiness -> controller
                     |             |            |
                claims only    no execution  no authorization
```

## v2 non-goals

- No automatic parsing of prose `.ai` files into claims.
- No semantic truth claim from a document merely asserting success.
- No P12 evidence re-normalization.
- No authorization, completion marking, mutation, or execution.
- No cross-claim semantic contradiction resolution. v2 detects duplicate identifiers only; a future bounded objective must define a stable fact identity and contradiction policy before it attempts to reconcile different claims about the same fact.

The reference continuation path (`tools/devos-continuation-path.py`) now calls resolver v2 when its caller supplies `state_claims`, `events`, or `changed_paths`. It returns the resolver result alongside P15/P16/P17 evidence. An unresolved supplied claim yields P16 `CLARIFY` and prevents P17/controller continuation.

### Validation reasons and output

The resolver only preserves or downgrades caller-supplied confidence. It never upgrades a claim. Its deterministic reasons include:

- `CLAIM_ID_OR_STATEMENT_INVALID`
- `STATE_CONFIDENCE_INVALID`
- `GROUNDING_TYPE_INVALID`
- `OBSERVED_CLAIM_GROUNDING_MISSING`
- `DUPLICATE_CLAIM_ID`
- `P12_EXECUTION_EVIDENCE_NOT_CURRENT`
- `DURABLE_STATE_CANNOT_SELF_UPGRADE_TO_OBSERVED`
- `REVALIDATION_BOUNDARY_REACHED`
- `REVALIDATION_PATH_CHANGED`

The result contains the protocol identifier, unchanged authority/authorization, `execution: NONE`, `mutation: NONE`, resolved claims, their reasons, a weakest-confidence summary, and unresolved claim IDs. `RESOLVED` means no claim is unknown; it does not mean a task is authorized, verified, or complete. `NEEDS_EVIDENCE` names unknown claims. `BLOCKED` means the `claims` input itself was invalid.

### Relationship to P12 and the continuation path

P12 owns execution-evidence provenance and freshness. Resolver v2 accepts a P12 reference and its freshness label but does not query Git, read the filesystem, run tests, or calculate P12 freshness itself. In the reference continuation path, callers may supply claims from durable records, session records, or prior evidence:

```text
User request -> P15 interpretation -> State Resolver v2 -> P16 plan -> P17 readiness -> controller
```

The resolver does not select a task or priority. It resolves claim confidence only. P16/controller choose the next bounded work under their existing constraints.
