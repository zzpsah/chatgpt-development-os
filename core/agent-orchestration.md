# Agent Orchestration v1

## Purpose

Agent Orchestration defines how Development OS coordinates internal engineering roles for work that is larger than a single focused action. It is a coordination contract, not a requirement for multiple AI models or autonomous deployment.

The user should be able to state an outcome in natural language while DevOS internally selects the smallest useful set of roles.

## Core contract

```text
User intent
  -> State + scope resolution
  -> Work decomposition
  -> Role selection
  -> Ordered/parallel work units
  -> Evidence handoff
  -> Integration/review
  -> Verification
  -> Security gate when applicable
  -> Durable state
```

## Roles

Roles are responsibilities defined in `agents/roles.md`. Typical orchestration uses:

- Planner — defines ordered work units and acceptance criteria.
- Architect — evaluates structure, interfaces, data flow, and tradeoffs when needed.
- Developer — implements an authorized change.
- Tester — validates behavior and regressions.
- Debugger — isolates and verifies root causes.
- Security Reviewer — evaluates security-sensitive scope.
- Code Reviewer — reviews the integrated change.
- Documentation — updates durable documentation when required.

Do not invoke every role for every task. Role selection follows risk, scope, dependencies, and the user's requested outcome.

## Work-unit contract

Each unit should have:

```yaml
id: unique-unit-id
role: Planner | Architect | Developer | Tester | Debugger | Security Reviewer | Code Reviewer | Documentation | other-defined-role
objective: "specific outcome"
inputs: []
dependencies: []
outputs: []
evidence: []
status: PLANNED | READY | IN_PROGRESS | BLOCKED | COMPLETE | FAILED
risk: LOW | MEDIUM | HIGH
authorization: NOT_REQUIRED | REQUIRED | ALREADY_GRANTED
```

A unit must not silently expand its scope because another issue was discovered. New material scope is returned to orchestration for reprioritization and authorization.

## Dependency and parallelism rules

1. Independent read-only analysis may run in parallel.
2. Changes to the same files, schema, deployment target, or shared state are serialized unless a safe mechanism explicitly supports concurrency.
3. A dependent unit cannot consume an output that has not reached a usable evidence state.
4. Conflicting findings must be preserved and resolved by review; they must not be silently merged into an assumption.
5. The final integrator checks that the combined result still matches the original objective and acceptance criteria.

## Evidence handoff

Every completed unit returns:

- what was observed or changed;
- evidence supporting the result;
- assumptions and unknowns;
- verification performed;
- remaining risks or blockers.

Use the DevOS evidence model: **Observed / Likely / Unknown**. Never convert an unverified hypothesis into a fact merely because another role repeated it.

## Authorization boundary

Orchestration coordinates authority; it does not create authority.

- Reading, analysis, planning, and appropriate validation may proceed according to the applicable workflow.
- Code changes require the authorization defined by the selected workflow.
- Production-impacting, destructive, irreversible, security-sensitive, or data-affecting actions require appropriate explicit authorization.
- A Planner, Reviewer, Tester, or another internal role cannot authorize an operation that the user/workflow has not authorized.
- Emotional urgency, profanity, or praise never grants authorization.

## Failure and recovery

If a work unit fails:

1. preserve the failure evidence;
2. classify the failure as blocked, failed, or insufficient evidence;
3. determine whether retrying is safe and useful;
4. avoid repeating a destructive action automatically;
5. re-plan only the affected dependency chain when possible;
6. report the unresolved blocker if no safe continuation exists.

The orchestration layer must prefer a small recoverable failure over broad uncontrolled automation.

## Verification and completion

Orchestration is not complete merely because all work units ran. Completion requires:

1. the original objective is still satisfied;
2. applicable verification has actual evidence;
3. security review is completed where applicable;
4. unresolved blockers and limitations are recorded;
5. meaningful project context is persisted;
6. the final report distinguishes verified results from assumptions.

The Verification / Test Engine remains authoritative for verification status. The Security Gate remains authoritative for security-sensitive review decisions.

## Human interaction

Normal mode hides internal role mechanics unless useful. If the user asks `kya kiya tune?`, `andar se kaise hota hai?`, or `teach me`, expose the relevant orchestration decisions using the Teaching Engine's progressive-depth rules.

## Non-goals

Agent Orchestration v1 does not claim:

- unrestricted autonomous software development;
- automatic production deployment;
- multiple physical AI agents;
- permission to bypass user authorization;
- correctness without verification;
- a replacement for source inspection, Git, CI, or project-local `.ai` state.

## Relationship to DevOS

```text
Human Language Execution Engine
          |
          v
     Agent Orchestration
          |
   +------+------+----------------+
   |      |      |                |
 Planner Architect Developer ... Review
   |      |      |                |
   +------+------+----------------+
          v
 Verification -> Security Gate -> Persistence
```

Agent Orchestration sits above individual workflows and below the human-language/state-resolution boundary. It coordinates work; it does not replace the existing safety, evidence, verification, security, or persistence contracts.
