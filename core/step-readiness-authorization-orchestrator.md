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

1. Only a P16 plan with `decision: PLANNED` and protocol `DEVOS-GOAL-PLAN-v1` can be evaluated for readiness.
2. The compiled plan must be structurally valid before any readiness gate can pass: non-empty step list, unique non-empty step ids, non-empty objectives, valid dependency lists, allowed impact classes, and explicit boolean authorization flags.
3. Every dependency reference must identify another step in the same compiled plan. Self-dependencies and unknown dependency ids are invalid.
4. The evaluated step must exist in the validated compiled plan.
5. A repository-head mismatch between compilation and execution time produces `STOP` with stale-plan evidence; the plan must be recompiled/revalidated rather than silently reused.
6. Every declared dependency must be complete before the step can be `READY`. Completion evidence naming ids that do not exist in the plan is invalid and blocks readiness.
7. Missing capability is `BLOCKED`; a capability declaration is evidence input, not permission.
8. Step-specific authorization is required only when the compiled step declares `authorization_required: true`, but approval must be bound to that exact step id. Approval for another step never leaks.
9. Security-sensitive/high-impact/production-or-destructive steps require an explicit Security Gate result. `FAIL` blocks; missing/unknown gate evidence produces `NEEDS_EVIDENCE`.
10. A non-empty applicable verification requirement must exist before a step can be `READY`.
11. `READY` still means only eligible for the existing controller/runtime path; it does not mean executed or completed.
12. P17 must preserve `authority: UNCHANGED`, `authorization: UNCHANGED`, and `execution: NONE` for every outcome.

## Status semantics

- `READY` — all P17 gates are satisfied for the exact current step/state; downstream controller/runtime gating is still required.
- `NEEDS_EVIDENCE` — required fresh state/security/verification evidence is missing or unknown.
- `NEEDS_APPROVAL` — the exact step requires authorization and no matching step-bound approval exists.
- `BLOCKED` — malformed plan structure, capability missing, dependency unresolved/invalid, Security Gate failed, step/plan invalid, or another deterministic blocker exists.
- `STOP` — the compiled plan is stale because material repository state changed after compilation.

## Authorization binding

Authorization input is keyed by step id. Accepted authorization for an authorization-required step is exactly `ALREADY_GRANTED`. A global or prior-task approval does not satisfy P17 unless it is explicitly represented for the same step id.

## Freshness rule

The compiler's repository head is treated as plan provenance. If current repository state differs, P17 conservatively stops the plan instead of trying to infer that the intervening changes are harmless. A new/revalidated plan is required.

## Evidence boundary

Readiness inputs are evidence claims that must come from current repository/runtime/security/capability sources. P17 does not fabricate capability, authorization, Security Gate results, dependency completion, repository freshness, or verification applicability.

## Runtime handoff

`tools/devos-runtime-handoff.py` exposes a P17-aware handoff path. It accepts only a controller `EXECUTION_CANDIDATE` paired with a `DEVOS-STEP-READINESS-v1` envelope whose status is `READY`, whose step id matches the controller task id, and whose repository head matches the controller repository head. This additional boundary does not remove the legacy P12 integration path and does not execute the work unit itself.

## Verification requirement

P17 closure requires deterministic regression tests for readiness outcomes, stale-plan detection, exact-step approval isolation, malformed compiled plans, invalid/fake dependency evidence, missing capability, Security Gate evidence, verification-path presence, and a reference end-to-end path from P15 human-language interpretation through P16 planning and P17 readiness into controller/runtime handoff.

## Safety invariant

> **A plan step becomes eligible only from fresh, step-bound evidence. Eligibility never manufactures permission or proves execution.**
