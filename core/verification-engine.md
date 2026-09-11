# Verification / Test Engine v1

## Purpose

The Verification / Test Engine is the evidence layer that determines whether completed work has been checked, what checks apply, what actually ran, and what conclusion is justified.

Core rule:

> **No evidence, no VERIFIED claim.**

The engine does not decide whether a change is authorized and does not replace source inspection, security review, or human acceptance. It converts applicable checks and their results into an honest verification status.

## Contract

```text
Request → Intent → State → Change → Applicable checks → Execute/delegate → Evidence → Status → Report → Persist
```

Verification is a separate concern from implementation:

```text
Authorization ≠ Verification
Implementation ≠ Proof of correctness
No failure observed ≠ Test passed
```

## Verification levels

Checks should be selected at the lowest level that meaningfully exercises the changed behavior, then expanded when the change crosses boundaries.

- **STATIC** — syntax, formatting, linting, type checking, schema/config validation, link or contract checks.
- **UNIT** — focused tests of isolated functions/modules/components.
- **INTEGRATION** — interactions between application components, APIs, databases, queues, external adapters, or authentication boundaries.
- **E2E** — user-visible workflows across the system.
- **RUNTIME** — build/startup/smoke/health checks against an executable environment.
- **DEPLOYMENT** — deployment configuration, artifact/build validation, and authorized post-deployment smoke checks.
- **SECURITY** — security-specific checks such as auth/authz, secret scanning, dependency/configuration review, and data-access controls. This level may be required by change type but does not replace the dedicated Security Gate milestone.

A higher level does not automatically prove every lower-level property. Select checks based on the actual risk and changed boundaries.

## Evidence model

Every executed or delegated check should record, where available:

```yaml
check:
  name:
  level: STATIC | UNIT | INTEGRATION | E2E | RUNTIME | DEPLOYMENT | SECURITY
  reason:
  command_or_provider:
  scope:
  result: PASS | FAIL | SKIPPED | NOT_AVAILABLE
  evidence:
  limitations:
  timestamp:
  commit:
```

Evidence is classified as:

- **Observed** — the check actually ran and its result was directly obtained.
- **Likely** — an interpretation of available evidence that still needs confirmation.
- **Unknown** — the check/result is not established.

Do not manufacture command output, test results, coverage, deployment state, or provider responses.

## Detecting applicable checks

Applicability is determined from the requested intent, changed paths, project tooling, configuration, tests, and deployment boundaries.

### Change-to-check guidance

| Change | Typical checks |
|---|---|
| Documentation only | markdown/link/schema checks when available |
| Application code | static + focused unit/integration tests; build/typecheck when applicable |
| Bug fix | regression test for failure + relevant focused checks |
| UI change | static/build + focused component/E2E check when available |
| API change | static + API/unit + integration/contract checks when available |
| Database/schema/migration | migration/schema validation + constraints/RLS/data-access checks + affected app tests |
| Authentication/authorization | security checks + focused auth/authz tests + affected integration tests |
| Dependency/config change | static/build + dependency/config validation + affected tests |
| Deployment/infrastructure | configuration validation + build/deployment checks; runtime smoke only with appropriate authorization |

This is guidance, not an excuse to run every available command. Prefer focused checks first, then broader checks when risk or boundaries justify them.

## Execution and delegation

The engine may:

1. Execute a supported local/repository check when the environment and authorization permit it.
2. Delegate a check to CI, a project tool, or another supported execution environment.
3. Record a check as unavailable when the required tool/environment is absent.
4. Ask for authorization when a verification step could modify production, data, external systems, or other protected state.

Read-only/static/test execution is normally safe when it does not mutate protected systems. Production smoke tests, migrations, destructive tests, paid external services, or data-affecting verification require the applicable authorization gate.

## Status semantics

### VERIFIED

Use only when the checks required for the changed scope and risk have been identified and the available evidence is sufficient, relevant, and passing.

`VERIFIED` does **not** mean mathematically or universally correct. It means the defined verification scope has sufficient passing evidence.

### PARTIAL

Use when meaningful checks passed but one or more relevant checks are missing, unavailable, skipped, or outside the verified scope.

### UNVERIFIED

Use when meaningful verification has not been performed or there is insufficient evidence to support a stronger status.

### FAILED

Use when an applicable check fails, or evidence contradicts the expected result. Do not downgrade a known failure to PARTIAL merely because other checks passed.

## Claim-prevention rules

Never report `VERIFIED` solely because:

- code was written without an editor error;
- the diff looks reasonable;
- a build was not attempted;
- tests exist but were not run;
- no failing test was observed;
- CI was not checked;
- the user or AI believes the change is correct;
- a previous commit passed checks unrelated to the current change;
- a deployment was assumed from a successful source change.

If a required check cannot be performed, explicitly state the limitation and use PARTIAL or UNVERIFIED as appropriate.

## Verification report

A verification result should be structured as:

```yaml
verification:
  status: VERIFIED | PARTIAL | UNVERIFIED | FAILED
  scope:
  checks:
    - name:
      level:
      result:
      evidence:
  missing:
  limitations:
  conclusion:
```

Human-facing reports should answer:

1. What changed or what was being checked?
2. Which checks were applicable?
3. Which checks actually ran?
4. What passed or failed?
5. What remains unverified?
6. What conclusion is justified?

## Integration with DevOS

The Verification / Test Engine sits after implementation and before final persistence/reporting:

```text
Human request
    ↓
Project Router
    ↓
Human Language Execution Engine
    ↓
AI State Resolver
    ↓
Workflow
    ↓
Inspect
    ↓
Authorize
    ↓
Implement
    ↓
Verification / Test Engine
    ↓
VERIFIED / PARTIAL / UNVERIFIED / FAILED
    ↓
Persist + Report
```

The engine should be referenced by feature, bug-fix, review, and resume workflows. The AI State Resolver may consume the resulting verification status, but must not invent it.

## Persistence

Meaningful verification evidence may be summarized in project-local `.ai/CURRENT-STATE.md`, session records, or other project context according to the project rules. Deterministic automation may record repository facts separately.

Do not store secrets, credentials, private keys, session cookies, or unnecessary personal/student data in verification records.

## Safety

- Verification never grants implementation authority.
- Do not mutate production merely to obtain a stronger verification label without explicit authorization.
- Do not expose sensitive test output or credentials.
- Do not claim a check ran when it was only proposed.
- Keep failed evidence visible; do not overwrite it with a later passing check unless the scope and sequence are explicit.
- Prefer reproducible commands and CI evidence over subjective judgment.

## v1 scope

Included:

- Verification levels.
- Evidence model.
- Applicability guidance.
- Supported execution/delegation model.
- VERIFIED/PARTIAL/UNVERIFIED/FAILED semantics.
- Unsupported-claim prevention.
- Verification report contract.
- Integration expectations with DevOS workflows.

Not included yet:

- Universal test-runner implementation for every language/framework.
- Automatic browser/E2E infrastructure.
- Full security-gate implementation.
- Production deployment authority.
- Proof of application correctness beyond the defined verification scope.
