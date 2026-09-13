# Semantic Goal-to-Plan Compiler v1

## Status

P16 active design contract. This layer sits immediately after top-level Human Language Interpretation and before bounded task execution.

## Purpose

Convert an already-interpreted human objective into a small, explicit, dependency-aware execution plan that downstream DevOS controllers can inspect, authorize, verify, and execute safely.

Core transformation:

`Canonical intent(s) + constraints + resolved project state + evidence → bounded plan graph + per-step authority class + verification obligations + unresolved ambiguity`

The compiler does not execute work and does not grant authority.

## Position in DevOS

`Human input → Human Language Execution Engine → Project Router / State Resolver → Semantic Goal-to-Plan Compiler → Development Task Controller → bounded workflow/runtime → Verification + Security → durable state`

P16 connects semantic understanding to engineering planning. It must not become a second language interpreter, a hidden executor, or an authorization bypass.

## Required plan envelope

A compiled plan must expose at least:

```yaml
protocol: DEVOS-GOAL-PLAN-v1
objective: null
project: null
steps: []
dependencies: []
constraints: []
assumptions: []
ambiguity: []
authority_requirements: []
verification_requirements: []
decision: PLANNED | CLARIFY | BLOCKED
execution: NONE
```

Each step must have a stable id, bounded objective, dependency list, expected evidence, risk/impact classification, authorization requirement, verification requirement, and stop/escalation condition.

## Planning rules

1. Preserve all interpreted negative constraints and explicit user boundaries.
2. Use repository/source evidence over chat-only assumptions.
3. Decompose only as far as useful for safe execution; avoid artificial micro-task explosion.
4. Represent dependencies explicitly rather than relying on sequence prose.
5. Keep high-impact actions visible and separately gated.
6. Never convert an unresolved material ambiguity into a guessed step.
7. Never infer authorization from plan order, previous success, urgency, or model confidence.
8. Prefer reversible/read-only evidence-gathering steps before mutation when uncertainty is material.
9. Require fresh verification evidence for completion claims.
10. Preserve Security Gate routing for security-sensitive or high-impact steps.

## Authority classes

The compiler may classify a step for downstream gating, but classification is not permission. Minimum classes:

- `READ_ONLY`
- `LOW_IMPACT_MUTATION`
- `HIGH_IMPACT_MUTATION`
- `SECURITY_SENSITIVE`
- `PRODUCTION_OR_DESTRUCTIVE`

Any class requiring stronger authorization remains blocked until the existing authorization/Security Gate contracts are satisfied.

## Evidence and assumptions

Plans distinguish observed evidence from assumptions. Assumptions that can materially alter project, scope, action, or impact must either be verified first or produce `CLARIFY`/`BLOCKED`.

## Verification contract

Every mutating step must declare how success will be verified. A plan with no applicable verification path is not executable and must be `BLOCKED` or revised.

## Acceptance criteria for P16

P16 v1 is complete only when:

1. the compiler contract is integrated into the canonical architecture;
2. an executable reference compiler emits the plan envelope deterministically for a bounded corpus;
3. tests cover single intent, multi-intent dependencies, negative constraints, ambiguity, read-before-write ordering, high-impact authorization classification, and verification requirements;
4. Development Task Controller integration consumes compiled plan steps without granting new authority;
5. CI verifies the contract and reference corpus;
6. fresh CI passes on the final implementation state.

## Safety invariant

> **Planning may reduce ambiguity and organize work; it may never manufacture permission.**
