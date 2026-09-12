# DevOS Failure Resolution Engine v1

## Purpose

The Base Operating Contract defines what DevOS must do when something fails. This document defines the bounded executable decision boundary for that behavior.

## Mandatory lifecycle

```text
FAILURE → DETECT → CLASSIFY + ISOLATE → DIAGNOSE → SAFE REPAIR
       → DRY TEST / READ-ONLY PROBE → RE-VERIFY → REGRESSION CHECK
       → DOCUMENT + PERSIST → RESUME ORIGINAL OBJECTIVE
```

## Rules

1. A failure produces an explicit state; silent success is forbidden.
2. Diagnosis identifies the deepest boundary supported by evidence.
3. Root cause may be `ROOT_CAUSE_UNCONFIRMED`; never invent a cause.
4. Repairs stay inside the existing authorization boundary and are the smallest safe change.
5. Prefer a dry test or read-only probe before higher-impact operations.
6. A failed repair returns to diagnosis rather than silently advancing.
7. Material repaired failures receive a deterministic regression check where practical.
8. Evidence and state are persisted before resuming the original objective.
9. Production/destructive/high-impact mutation remains separately authorization-gated.
10. This engine never grants authority merely because a repair is technically possible.

## Connection diagnosis boundary

```text
CONFIGURATION → CREDENTIAL SHAPE (NO SECRET VALUES) → ENDPOINT / DNS
→ NETWORK REACHABILITY → TLS / TRANSPORT → AUTHENTICATION
→ AUTHORIZATION → PROVIDER / CONNECTOR → REQUEST VALIDATION
→ RESPONSE VALIDATION
```

Only non-secret diagnostic evidence is retained. Credentials, tokens, cookies, and private keys are never persisted.

## State semantics

`DETECTED` = observed; `DIAGNOSED` = evidence-backed boundary; `ROOT_CAUSE_UNCONFIRMED` = insufficient evidence; `REPAIRED` = bounded repair applied; `DRY_TESTED` = safe proof passed; `VERIFIED` = failing path passes; `REGRESSION_PROTECTED` = recurrence guarded; `DOCUMENTED` = durable record updated; `RESUMED` = original objective may continue; `BLOCKED`/`HOLD` = action exceeds authorization or evidence.

## Completion gate

Safe repair: `IMPLEMENTED + ROOT_CAUSE_DETERMINED + DRY_TEST_PASS + VERIFIED + REGRESSION_CHECK + DOCUMENTED + RESUMED`.

Unsafe/unavailable: `EVIDENCE_PERSISTED + BLOCKED/HOLD + NEXT_ACTION_DOCUMENTED`.

This engine does not replace controller authorization, security gates, runtime restrictions, verification, or durable persistence.
