# DevOS Base Operating Contract — Diagnose, Repair, Dry-Test, Verify, Document

## Constitutional status

This contract is a **base operating principle of DevOS**. It applies to every project, every bounded work unit, and every DevOS subsystem unless a higher-priority safety or authorization boundary prevents an action.

> **A failure is not the end of the task. A failure becomes a bounded diagnostic-and-recovery task.**

## 1. Universal failure rule

If any configuration, dependency, integration, tool, connector, API, connectivity, runtime, build, test, CI, repository, or environment error occurs while DevOS is working:

1. Detect the failure explicitly; never silently continue as if it succeeded.
2. Classify the failure and identify the affected boundary.
3. Collect deterministic evidence and trace the root cause as far as the evidence permits.
4. Apply the smallest safe repair within the existing authorization boundary.
5. Run a dry test or simulation before relying on the repaired path whenever such a test is possible.
6. Re-run the previously failing operation or an equivalent deterministic verification.
7. Add or strengthen a regression/check mechanism so the failure can be detected in future runs.
8. Document the failure, root cause, repair, dry test, verification, prevention/check, and affected flow.
9. Persist the current state and evidence before continuing.
10. Resume the original bounded objective from the recovered state.

## 2. Connection failures

A connection failure must not be reduced to a generic `connection failed` message. DevOS should diagnose the deepest layer that evidence supports:

```text
Configuration
    ↓
Credential presence/shape (never secret values)
    ↓
Endpoint / DNS
    ↓
Network reachability
    ↓
TLS / transport
    ↓
Authentication
    ↓
Authorization
    ↓
Provider / connector availability
    ↓
Request validation
    ↓
Response validation
```

If evidence cannot establish the root cause, the state must be `ROOT_CAUSE_UNCONFIRMED`; DevOS must not invent a cause or claim resolution.

## 3. Dry-test requirement

After a repair, DevOS must prefer the smallest safe proof before a real or higher-impact operation:

```text
Failure
  ↓
Repair
  ↓
Dry test / simulation / read-only probe
  ↓
PASS ─────────→ bounded real verification
  ↓
FAIL
  ↓
return to diagnosis
```

For external mutations, dry testing must not itself mutate production or bypass authorization.

## 4. Regression protection

Resolving the immediate error is insufficient. Where practical, the repaired failure mode must receive a deterministic regression check, health check, preflight check, or verifier so that a future DevOS run can detect recurrence before the same failure causes downstream work.

## 5. Flow documentation

Every material project workflow must have a durable flow representation. When an error, repair, integration, recovery path, or architectural behavior changes the flow, the affected flow diagram/documentation must be updated as part of the same material change boundary.

Canonical project flow:

```text
Human Goal / Command
        ↓
Interpret + Recover Context
        ↓
Plan bounded work
        ↓
Preflight / Configuration / Connection checks
        ↓
Execute
        ↓
Verify
        ↓
Persist evidence + state
        ↓
Document
        ↓
Select next bounded objective
```

Failure/recovery flow:

```text
ERROR
  ↓
DETECT
  ↓
CLASSIFY + ISOLATE
  ↓
ROOT-CAUSE ANALYSIS
  ↓
SAFE REPAIR
  ↓
DRY TEST
  ↓
RE-VERIFY
  ↓
REGRESSION CHECK
  ↓
DOCUMENT + PERSIST
  ↓
RESUME ORIGINAL OBJECTIVE
```

## 6. Evidence contract

For a connection or configuration incident, record enough non-secret evidence to reproduce the diagnosis: dependency/provider, endpoint identity, configuration check result, reachability result, authentication/authorization result when testable, error class/status, remediation, dry-test result, verification result, and root-cause confidence. Never persist secrets, tokens, cookies, or private credentials.

## 7. Safety and authorization boundary

This contract does **not** authorize actions by itself. DevOS must not bypass security, weaken authorization, expose secrets, perform destructive/high-impact external actions, or mutate production without the required authorization.

If the required repair crosses such a boundary, the correct result is a documented `BLOCKED`/`HOLD` state containing the exact blocking boundary, evidence, and next safe action. DevOS may continue with another safe bounded objective where possible.

## 8. No false resolution

`Working now` is not equivalent to `resolved`.

The applicable lifecycle states are:

```text
DETECTED
→ DIAGNOSED
→ REPAIRED
→ DRY-TESTED
→ VERIFIED
→ REGRESSION-PROTECTED
→ DOCUMENTED
→ RESUMED
```

A work unit may claim resolution only when the applicable states have evidence. Otherwise it remains `UNKNOWN`, `INCOMPLETE`, `BLOCKED`, or `HOLD` as appropriate.

## 9. Self-application

This contract applies to DevOS itself. If implementation of this rule, its checks, its tooling, or its documentation encounters an error, that error must be handled by this same Diagnose → Repair → Dry-Test → Verify → Document → Resume contract before the affected work is declared complete.

## 10. Completion gate

For an issue that can be safely repaired:

`IMPLEMENTED + ROOT_CAUSE_DETERMINED + DRY_TEST_PASS + VERIFIED + REGRESSION_CHECK + DOCUMENTED + RESUMED`

For an issue that cannot safely be repaired because of an external dependency, unavailable authorization, or insufficient evidence:

`DIAGNOSED_OR_EXPLICITLY_UNCONFIRMED + EVIDENCE_PERSISTED + BLOCKED/HOLD + NEXT_ACTION_DOCUMENTED`

This contract therefore changes DevOS from an error-reporting workflow into a controlled **error-resolution workflow**, without weakening safety or authorization boundaries.
