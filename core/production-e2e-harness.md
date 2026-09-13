# Production E2E Harness

## Status

Active post-P17 maturity gate. This is a whole-system proof boundary, not a new authority layer and not an automatic numbered milestone.

## Purpose

The harness proves that existing DevOS capabilities compose into one governed development path:

`human request → interpretation → plan → readiness → controller → bounded runtime → verification → durable persistence → recovery`

It must reuse existing P15/P16/P17/controller/runtime/verification/adapter contracts rather than create a parallel execution framework.

## Protocol

Reference protocol: `DEVOS-PRODUCTION-E2E-v1`.

A successful result has:

```yaml
protocol: DEVOS-PRODUCTION-E2E-v1
status: COMPLETE
stage: RECOVERY
project: <resolved project>
objective: <interpreted objective>
step_id: <exact compiled step>
repository_head: <fresh observed head>
authority: UNCHANGED
authorization: UNCHANGED
trace:
  interpretation: {}
  plan: {}
  readiness: {}
  controller: {}
  handoff: {}
  runtime: {}
  verification: {}
  persistence: {}
  recovery: {}
```

Any unsatisfied gate returns `status: BLOCKED` at the earliest applicable stage and must not silently continue to later mutation/execution stages.

## Required composition

1. Human input is interpreted through the P15 Human Language Interpreter.
2. Only `INTERPRETED` input with canonical intent may proceed.
3. P16 compiles the interpreted objective into `DEVOS-GOAL-PLAN-v1`.
4. Only a `PLANNED` compiled plan may proceed.
5. P17 evaluates the exact selected step against compilation/current repository head, dependencies, capability, exact-step authorization, Security Gate evidence and verification path.
6. Only `READY` may proceed to the Development Task Controller.
7. The controller independently revalidates compiled-plan integrity and its own scope/repository/capability/authorization/security/verification gates.
8. `build_p17_handoff` must bind the exact READY step to the exact `P16-CONTROLLER-v1` execution candidate.
9. Runtime execution must use only operations supported by the bounded runtime-adapter bridge.
10. Verification must use an explicit argv command through the reference verification adapter; shell interpretation is not introduced by the harness.
11. Durable evidence persistence is an explicit bounded `.ai/` write requiring independent `ALREADY_GRANTED` persistence authorization.
12. Recovery must read the persisted evidence back through the bounded host adapter and prove the evidence protocol is recoverable.

## Runtime semantic binding

The harness strengthens, never weakens, adapter boundaries:

- A `READ_ONLY` compiled step may execute only a bounded read operation.
- A runtime mutation may not be paired with a `READ_ONLY` compiled step.
- Any runtime mutation requires exact-step `ALREADY_GRANTED` authorization even if a lower layer would otherwise classify the semantic step as low impact.
- Remote GitHub mutation additionally requires exact-step Security Gate `PASS`.
- Eligibility authorization and runtime-operation authorization are distinct. A security-sensitive review can require authorization to become READY while its underlying read operation remains `NOT_REQUIRED` at the adapter boundary.
- Runtime operation names outside the explicit E2E allowlist are blocked.

Reference read operations:
- `filesystem.read`
- `git.inspect`
- `github.inspect.repository`
- `github.inspect.commit`
- `github.inspect.workflow_run`

Reference mutation operations:
- `filesystem.write_scoped`
- `github.mutate.file`

## Verification boundary

Runtime success is not completion. The harness requires a fresh `VERIFIED` result from the verification adapter after runtime execution.

A failed, unavailable, blocked or timed-out verification result stops the harness before persistence is accepted as successful E2E evidence.

## Persistence and recovery boundary

The harness persists a compact evidence packet only after runtime success and verification success. The packet records the resolved project/objective, repository head, exact step id, runtime status, verification status and unchanged authority boundaries.

The evidence packet is marked `execution_evidence: true` because it is generated only after observed runtime and verification results. Planning/readiness/controller metadata remain non-execution evidence.

Persistence does not push or deploy anything. Repository synchronization/push remains a separate capability and authorization boundary.

## Failure semantics

The deterministic reference harness must cover at least:

- unresolved/ambiguous interpretation;
- non-PLANNED compilation;
- stale repository head;
- missing dependency/capability;
- missing exact-step authorization;
- missing/failed Security Gate evidence;
- controller or handoff mismatch;
- runtime operation/step impact mismatch;
- unavailable/failed runtime provider operation;
- failed verification;
- missing persistence authorization;
- unrecoverable persisted evidence.

No failure may be converted into success by skipping a downstream gate.

## Managed-project proof

Closure requires more than an isolated unit test. At least one realistic managed-project proof must exercise a safe read-only or explicitly bounded low-impact path using current repository evidence and produce recoverable evidence without production/destructive mutation.

## Safety invariant

> **The E2E harness proves composition; it does not manufacture permission. Every existing authorization, Security Gate, freshness, verification and recovery boundary remains independently enforceable.**
