# DevOS Worker Lifecycle and State-Machine Observability v1

## Purpose

The Worker is the bounded orchestration boundary above the autonomous loop. It must expose deterministic lifecycle state without creating authority, replay permission, or unbounded execution.

## State machine

```text
READY
  ↓
RECOVERING
  ↓
PREFLIGHT
  ↓
DISPATCHED
  ↓
RUNNING
  ↓
VERIFYING
  ↓
PERSISTING
  ↓
COMPLETE
```

Failure/hold exits:

```text
RECOVERING → HOLD_RECOVERY_INVALID
PREFLIGHT  → HOLD_PREFLIGHT_FAILED
DISPATCHED → HOLD_AUTHORIZATION
RUNNING    → FAILED
VERIFYING  → FAILED_VERIFICATION
PERSISTING → HOLD_PERSISTENCE_INVALID
```

## Invariants

1. One worker invocation owns at most one bounded work unit.
2. Every lifecycle transition is explicit and ordered.
3. A terminal `FAILED`, `BLOCKED`, `CANCELLED`, or `HOLD_*` state cannot silently become `RUNNING`.
4. Recovery happens before dispatch and never grants replay permission.
5. Authorization is evaluated by the existing controller/handoff/security gates; the Worker does not create authority.
6. `COMPLETE` requires successful verification and durable persistence of the outcome.
7. Invalid or missing durable state fails closed rather than being guessed.
8. Observability records non-secret state, reason, iteration, and bounded evidence only.
9. The Worker remains `ADVISORY_ONLY` with respect to authorization and production/high-impact mutation.

## Transition record

A deterministic transition record should contain:

- `from`
- `to`
- `reason`
- `iteration`
- `task_id` when available
- `timestamp` when available
- non-secret evidence reference

Secrets, tokens, cookies, credentials, and private keys must never be recorded.

## Worker completion gate

`RECOVERED + PREFLIGHT_PASS + AUTHORIZED_HANDOFF + RUNNING + VERIFIED + PERSISTED + COMPLETE`

Any missing required transition becomes `HOLD`/`FAILED` with evidence and a documented next action.

## Relationship to the Base Operating Contract

Worker failures follow the same bounded recovery lifecycle: detect → classify → diagnose → safe repair → dry-test/read-only proof → re-verify → regression check → document/persist → resume. A Worker state transition never overrides the Base Operating Contract, Security Gate, runtime restrictions, or authorization boundary.
