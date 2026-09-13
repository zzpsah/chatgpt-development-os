# Step Readiness & Authorization Orchestrator v1

## Status

P17 active implementation contract.

## Purpose

P17 binds one compiled P16 plan step to fresh repository state, dependency completion, capability, step-specific authorization, Security Gate state, and an applicable verification path before that step may be handed toward execution.

It closes the gap between **"this is the planned next step"** and **"this exact step is currently safe and eligible to proceed"**.

Core transformation:

`Compiled P16 plan + compilation repository head + current repository head + completed dependencies + capability + step authorization + Security Gate + verification path → READY | NEEDS_EVIDENCE | NEEDS_APPROVAL | BLOCKED | STOP`

P17 never executes work and never grants authority.

## Position in DevOS

`Human input → Human Language Execution Engine → Project Router / State Resolver → P16 Semantic Goal-to-Plan Compiler → P17 Step Readiness & Authorization Orchestrator → Development Task Controller → bounded runtime → Verification + Security → durable state`

## Readiness envelope

```yaml
protocol: DEVOS-STEP-READINESS-v1
plan_protocol: DEVOS-GOAL-PLAN-v1
step_id: null
status: READY | NEEDS_EVIDENCE | NEEDS_APPROVAL | BLOCKED | STOP
repository_head: null
compiled_repository_head: null
gates:
  plan: false
  freshness: false
  dependencies: false
  capability: false
  authorization: false
  security: false
  verification: false
reasons: []
authority: UNCHANGED
authorization: UNCHANGED
execution: NONE
```

## Required invariants

1. Only a P16 plan with `decision: PLANNED` can be evaluated for readiness.
2. The evaluated step must exist in the compiled plan.
3. A repository-head mismatch between compilation and execution time produces `STOP` with stale-plan evidence; the plan must be recompiled/revalidated rather than silently reused.
4. Every declared dependency must be complete before the step can be `READY`.
5. Missing capability is `BLOCKED`; a capability declaration is evidence input, not permission.
6. Step-specific authorization is required only when the compiled step declares `authorization_required: true`, but approval must be bound to that exact step id. Approval for another step never leaks.
7. Security-sensitive/high-impact/production-or-destructive steps require an explicit Security Gate result. `FAIL` blocks; missing/unknown gate evidence produces `NEEDS_EVIDENCE`.
8. A non-empty applicable verification requirement must exist before a step can be `READY`.
9. `READY` still means only eligible for the existing controller/runtime path; it does not mean executed or completed.
10. P17 must preserve `authority: UNCHANGED`, `authorization: UNCHANGED`, and `execution: NONE` for every outcome.

## Status semantics

- `READY` — all P17 gates are satisfied for the exact current step/state; downstream controller/runtime gating is still required.
- `NEEDS_EVIDENCE` — required fresh state/security/verification evidence is missing or unknown.
- `NEEDS_APPROVAL` — the exact step requires authorization and no matching step-bound approval exists.
- `BLOCKED` — capability missing, dependency unresolved, Security Gate failed, step/plan invalid, or another deterministic blocker exists.
- `STOP` — the compiled plan is stale because material repository state changed after compilation.

## Authorization binding

Authorization input is keyed by step id. Accepted authorization for an authorization-required step is exactly `ALREADY_GRANTED`. A global or prior-task approval does not satisfy P17 unless it is explicitly represented for the same step id.

## Freshness rule

The compiler's repository head is treated as plan provenance. If current repository head differs, P17 does not attempt to infer whether the change is harmless. It returns `STOP` and requires revalidation/recompilation. This is intentionally conservative for v1.

## Acceptance criteria

P17 v1 is complete only when:

1. an executable deterministic readiness evaluator exists;
2. tests cover ready read-only work, dependency blocking, missing capability, step-bound approval, approval non-leakage, Security Gate missing/fail/pass, missing verification path, invalid/non-planned plan, and stale-plan stopping;
3. Development Task Controller/runtime handoff integration refuses to consume non-`READY` P17 state;
4. an end-to-end reference test demonstrates `P16 plan → P17 readiness → controller/runtime handoff boundary` without manufacturing authority or execution evidence;
5. CI verifies the P17 corpus and end-to-end integration;
6. fresh CI passes on the final implementation state.

## Safety invariant

> **A plan step may be correct and still not be ready. Readiness must be recomputed from fresh evidence for that exact step and state.**
