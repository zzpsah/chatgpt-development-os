# Autonomous Development Loop v1

## Purpose

The Autonomous Development Loop defines a bounded control loop for continuing authorized engineering work across multiple iterations. It turns the existing DevOS contracts into a repeatable execution cycle without granting unrestricted autonomy.

The loop is **bounded, evidence-driven, checkpointed, and stoppable**.

## Core contract

```text
Objective
  -> State resolution
  -> Plan / orchestrate
  -> Capability check
  -> Authorization check
  -> Execute one bounded iteration
  -> Checkpoint
  -> Verify
  -> Review / security gate when applicable
  -> Persist evidence and state
  -> Decide: CONTINUE | STOP | ESCALATE
  -> next iteration or final report
```

The loop must not skip state resolution, capability checks, authorization, verification, or persistence merely because the previous iteration succeeded.

## Iteration contract

Each iteration has a bounded scope and produces a checkpoint:

```yaml
iteration:
  number: 1
  objective: "specific outcome"
  work_units: []
  capabilities:
    required: []
    available: []
    missing: []
  authorization: NOT_REQUIRED | REQUIRED | ALREADY_GRANTED
  changes: []
  evidence: []
  verification: VERIFIED | PARTIAL | UNVERIFIED | FAILED
  blockers: []
  next: CONTINUE | STOP | ESCALATE
```

An iteration should make the smallest useful progress toward the objective. A bounded iteration is not permission to broaden scope.

## Bounded autonomy

Every autonomous run must have explicit bounds:

- maximum iteration count or another concrete execution budget;
- defined objective and acceptance criteria;
- defined project and working scope;
- no implicit production deployment;
- no implicit destructive, irreversible, security-sensitive, or data-affecting authority;
- stop when required evidence, capability, or authority is unavailable.

If the host cannot enforce a requested bound, the loop must not claim that it can.

## Capability check

Before an action requiring a tool or external system, compare required capabilities with actually available capabilities.

Capability states are:

- **AVAILABLE** — the host can perform the operation now;
- **DELEGATABLE** — another supported tool/host can perform it, and the delegation boundary is explicit;
- **MISSING** — no supported capability is available.

Missing capability is not failure of the underlying project. It is an execution limitation and must be reported honestly.

The loop must never invent tool execution, external-system results, test results, deployment state, or file changes.

## Authorization and approval gates

The loop distinguishes permission from capability.

- Planning does not authorize implementation.
- Verification does not authorize deployment.
- A previous low-risk iteration does not automatically authorize a newly discovered high-risk action.
- Production-impacting, destructive, irreversible, security-sensitive, or data-affecting operations require the applicable explicit approval before execution.
- If approval is required and unavailable, **ESCALATE** or **STOP**; do not continue around the gate.

## Stop / continue / escalate

### CONTINUE

Continue only when:

1. the objective remains valid;
2. required capabilities are available or safely delegated;
3. the next work is within authorized scope;
4. no blocking verification/security condition exists;
5. the execution budget remains;
6. the next iteration has a concrete useful action.

### STOP

Stop when:

- the objective is complete and appropriately verified;
- the iteration budget is exhausted;
- there is no useful authorized next action;
- required capability is missing and no safe delegation exists;
- a failure cannot be safely recovered;
- continuing would require unauthorized scope expansion.

### ESCALATE

Escalate when:

- explicit user approval is required;
- a security-sensitive decision requires human judgment;
- a production/destructive/irreversible/data-affecting action is proposed;
- evidence conflicts materially and cannot be resolved safely;
- a blocker requires information or authority outside the current run.

## Checkpointing and resumability

After every meaningful iteration, persist a checkpoint containing:

- objective and current scope;
- iteration number and execution bound;
- work-unit statuses;
- changes made;
- verification evidence and limitations;
- blockers and unknowns;
- authorization/approval state;
- next recommended action.

Checkpoint data belongs in the project-local durable context where appropriate. Secrets, credentials, session cookies, private keys, and unnecessary sensitive data must never be stored merely for resumability.

A resumed loop must reconstruct state from repository evidence and checkpoints, then re-check source, Git, capability, authorization, and verification status as applicable. It must never blindly replay the previous action.

## Evidence aggregation

The loop aggregates evidence from each work unit and iteration without converting hypotheses into facts.

Use:

- **Observed** — directly established evidence;
- **Likely** — evidence-supported interpretation;
- **Unknown** — not established.

Verification remains:

- **VERIFIED**
- **PARTIAL**
- **UNVERIFIED**
- **FAILED**

The aggregate result cannot be stronger than its material evidence. Failed or unverified dependencies remain visible.

## Failure recovery

On failure:

1. checkpoint the failure;
2. preserve evidence;
3. classify the affected work unit and dependency chain;
4. determine whether a safe bounded retry exists;
5. retry only when useful and authorized;
6. otherwise STOP or ESCALATE.

Do not automatically repeat destructive or irreversible operations.

## Relationship to existing DevOS contracts

The Autonomous Development Loop coordinates existing authorities rather than replacing them:

- Project Router — project identity;
- Human Language Execution Engine — intent and authorization semantics;
- AI State Resolver — current-state reasoning;
- Agent Orchestration — decomposition, roles, dependencies, and handoffs;
- Verification / Test Engine — verification status and evidence;
- Security Gate — security-sensitive review;
- `.ai` context — durable project context;
- source/Git — implementation and change authority.

## Non-goals

P4 does not provide unrestricted autonomous software development, automatic production deployment, permission bypass, fabricated tool results, or correctness without verification.

**Automation records and advances evidence; it does not manufacture authority or certainty.**
