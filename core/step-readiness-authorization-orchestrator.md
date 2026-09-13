# Step Readiness & Authorization Orchestrator v1

## Status

P17 active implementation contract.

## Purpose

P17 binds one compiled P16 plan step to fresh repository state, dependency completion, capability, step-specific authorization, Security Gate state, and an applicable verification path before that step may be handed toward execution.

It closes the gap between **"this is the planned next step"** and **"this exact step is currently safe and eligible to proceed"**.

Core transformation:

`Validated compiled P16 plan + exact step + compilation repository head + current repository head + dependency evidence + capability + step authorization + Security Gate + verification path → READY | NEEDS_EVIDENCE | NEEDS_APPROVAL | BLOCKED | STOP`

P17 never executes work and never grants authority.

## Position in DevOS

`Human input → Human Language Execution Engine → Project Router / State Resolver → P16 Semantic Goal-to-Plan Compiler → P17 Step Readiness & Authorization Orchestrator → Development Task Controller → bounded runtime → Verification + Security → durable state`

The Development Task Controller consumes the P16 compiled plan directly. P17 supplies a separate, exact-step readiness decision; the runtime handoff requires the controller decision and P17 readiness envelope to agree on the same step and repository state.

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

1. Only protocol `DEVOS-GOAL-PLAN-v1` with `decision: PLANNED`, `authority: UNCHANGED`, `authorization: UNCHANGED`, and `execution: NONE` can be evaluated.
2. A PLANNED plan must have a resolved project/objective and no material ambiguity.
3. The compiled plan must be structurally valid: non-empty step list, unique non-empty ids/objectives, valid dependencies, allowed impact classes, explicit boolean authorization flags, non-empty expected-evidence declarations, verification paths, and stop/escalation conditions.
4. High-impact, security-sensitive, and production/destructive steps must explicitly declare `authorization_required: true`; inconsistent compiler metadata is invalid.
5. Every dependency reference must identify another step in the same compiled plan. Self-dependencies, unknown dependencies, and dependency cycles are invalid.
6. Explicit negative constraints remain binding at readiness time. A tampered PLANNED envelope that contains a conflicting non-read-only step is invalid.
7. The evaluated step must exist in the validated plan and must not already be marked complete.
8. Compilation and current repository heads must be non-empty fresh evidence. A mismatch returns `STOP`; P17 never guesses that intervening changes are harmless.
9. Completion evidence must name real plan steps and must itself satisfy dependency closure. A downstream step cannot be asserted complete while one of its dependencies is incomplete.
10. Every dependency of the selected step must be complete before `READY`.
11. Capability, authorization, and Security Gate evidence maps must be valid mappings. Missing capability blocks readiness.
12. Authorization is bound to the exact step id. Approval for any other step/task/session does not satisfy an authorization-required step.
13. Security-sensitive/high-impact/production-or-destructive steps require explicit Security Gate evidence. Missing/unknown evidence yields `NEEDS_EVIDENCE`; non-PASS blocks.
14. A non-empty applicable verification requirement must exist before `READY`.
15. Every `READY` gate must be true. `READY` means only eligible for the downstream controller/runtime boundary; it does not mean executed or complete.
16. Every outcome preserves `authority: UNCHANGED`, `authorization: UNCHANGED`, and `execution: NONE`.
17. Readiness and compiled-plan metadata are never execution evidence.

## Status semantics

- `READY` — all P17 gates are satisfied for the exact current step/state; downstream controller/runtime gating is still required.
- `NEEDS_EVIDENCE` — required fresh repository or Security Gate evidence is missing/unknown.
- `NEEDS_APPROVAL` — the exact step requires authorization and no matching step-bound approval exists.
- `BLOCKED` — malformed/inconsistent plan, invalid completion evidence, missing capability, unresolved dependency, failed Security Gate, or another deterministic blocker exists.
- `STOP` — repository state changed after compilation and the plan must be revalidated/recompiled.

## Authorization binding

Authorization input is keyed by step id. Accepted authorization for an authorization-required step is exactly `ALREADY_GRANTED`. A global or prior-task approval does not satisfy P17 unless represented for that exact step id. Readiness classification never upgrades authorization.

## Freshness rule

The compilation repository head is plan provenance. If current repository state differs, P17 returns `STOP`. Revalidation/recompilation is required before the step can be considered again.

## Evidence boundary

Readiness inputs are evidence claims that must come from current repository/runtime/security/capability sources. P17 does not fabricate capability, authorization, Security Gate results, dependency completion, repository freshness, or verification applicability. The emitted selected-step metadata includes `execution_evidence: false`.

## Runtime handoff

`tools/devos-runtime-handoff.py` exposes a P17-aware handoff path. It accepts only:

- a `P16-CONTROLLER-v1` `EXECUTION_CANDIDATE` produced from a compiled plan;
- a `DEVOS-STEP-READINESS-v1` `READY` envelope for `DEVOS-GOAL-PLAN-v1`;
- all controller and readiness gates satisfied;
- unchanged authority/authorization and no claimed execution;
- exact equality of controller task id, controller compiled-step id, readiness step id, and readiness step metadata;
- matching repository heads and matching objective/impact/verification metadata.

A legacy P12 controller candidate by itself is intentionally insufficient for the P17 handoff. The legacy P12 handoff remains supported independently for backward compatibility.

## Verification requirement

P17 closure requires deterministic regression coverage for:

- all readiness status outcomes;
- stale-plan detection;
- exact-step approval isolation;
- malformed/internally inconsistent compiled plans;
- dependency cycles and fake/impossible completion evidence;
- missing/invalid capability, authorization, Security Gate, or verification evidence;
- tampered negative constraints;
- exact controller/readiness step identity at runtime handoff;
- rejection of forged READY gates;
- a direct reference path: `P15 Human Language → P16 compiled plan → P17 readiness → P16 compiled-plan controller → runtime handoff`.

## Safety invariant

> **A plan step becomes eligible only from fresh, structurally consistent, step-bound evidence. Eligibility never manufactures permission or proves execution.**
