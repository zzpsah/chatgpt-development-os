# P14 Adaptive Verification & Self-Healing v1

## Purpose

P14 connects the existing Verification/Test Engine, Failure Resolution Engine, P13 execution feedback, and P11 deterministic derived-context self-healing into one bounded policy layer.

The objective is not unrestricted autonomous repair. The objective is to make verification depth responsive to change risk and to permit self-healing only where DevOS can prove that the repair is deterministic, bounded, reversible through Git, and already inside an established write boundary.

## Contract

```text
changed scope + boundaries + risk
  -> required verification levels
  -> fresh observed evidence
  -> VERIFIED | PARTIAL | UNVERIFIED | FAILED
  -> on failure: bounded healing policy
  -> AUTO_ELIGIBLE | PROPOSE_ONLY | HOLD | NO_HEAL
  -> re-verify before any success claim
```

`tools/adaptive-verification.py` is deterministic and non-executing. It never grants authority and always returns `authority: UNCHANGED` and `execution: NONE`.

## Adaptive verification

The policy always starts with STATIC verification. It adds levels only when evidence from changed paths, crossed boundaries, or declared risk justifies them:

- source-code changes add UNIT;
- API/database/auth/queue/external integration boundaries add INTEGRATION;
- UI/user-flow boundaries add E2E;
- runtime/service boundaries add RUNTIME;
- deployment/infrastructure boundaries add DEPLOYMENT;
- auth/authz/secrets/security boundaries add SECURITY;
- HIGH risk requires INTEGRATION;
- CRITICAL risk additionally requires RUNTIME and SECURITY.

A PASS counts only when it is observed and fresh. Missing or stale required evidence prevents VERIFIED. An explicit required-level failure yields FAILED even when other checks pass.

## Healing boundary

Automatic healing eligibility is intentionally narrower than general repair capability.

### AUTO_ELIGIBLE

Only deterministic derived DevOS context already protected by the P11 self-healing contract:

- `.ai/STATE-INDEX.md`
- `.ai/CHANGELOG.md`
- `.ai/PROJECT-IDENTITY.json`

The policy may identify `tools/self-heal-derived-context.py` as the only allowed implementation path. Eligibility is still bounded by a finite attempt budget and must be followed by fresh verification.

### PROPOSE_ONLY

The following are never auto-executed merely because P14 detected a failure:

- application/source code;
- semantic `.ai` state such as `CURRENT-STATE.md`, `TASKS.md`, `DECISIONS.md`, `PROJECT.md`, or `ARCHITECTURE.md`;
- configuration;
- database or migration changes;
- deployment/infrastructure changes;
- security/authentication changes.

These remain subject to normal controller scope, authorization, Security Gate, runtime, review, and verification contracts.

### HOLD

P14 holds when the repair budget is exhausted or the proposed repair is outside the safe allowlist.

## Repair budget

Every adaptive repair attempt has explicit `attempts` and `max_attempts`. Reaching the budget is terminal for that bounded loop and yields HOLD; the system must not retry indefinitely or silently widen scope.

## Completion semantics

A healing action does not itself establish success. After any repair, fresh applicable evidence must be gathered and the adaptive verifier must return VERIFIED before the original objective can resume.

## Safety invariants

1. Verification does not grant mutation authority.
2. P14 does not widen P11's deterministic self-healing write boundary.
3. Semantic and higher-impact repair is proposal-only until normal gates authorize it.
4. Stale evidence cannot prove the current state.
5. Failed evidence remains visible until fresh evidence supersedes it explicitly.
6. Attempt budgets prevent unbounded repair loops.
7. Production, destructive, credential, database, deployment, and security mutations remain separately gated.
