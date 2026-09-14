# Session — Managed-Repository Delivery v1 Read-Only Preflight

Date: 2026-09-14

## Objective

Create a managed-repository bridge that uses P15 → P16 → P17 and exact Git evidence to produce a scoped approval request, but stops before any target-repository write.

## Implementation

- `tools/managed-repository-preflight.py` inspects only an existing local Git checkout.
- It requires a clean worktree, exact HEAD, safe explicit paths, P15 interpreted objective, and a P16 read-then-low-impact-change plan.
- It evaluates the read step with P17, elevates the proposed managed-repository change to explicit approval requirement, and verifies P17 returns `NEEDS_APPROVAL`.
- It produces `DEVOS-MANAGED-REPOSITORY-APPROVAL-REQUEST-v1` and a canonical evidence ID, then returns `HOLD`.
- Optional evidence output is prohibited inside the inspected repository; the tool never edits the target checkout, runs tests, calls providers, commits, or pushes.

## Verification plan

The regression corpus creates a temporary Git fixture and proves a clean preflight creates exact-head, exact-path approval evidence while leaving file contents and Git status unchanged. It also proves external-only evidence output, dirty-worktree hold, and path-traversal hold.

## Boundaries

- `authority = UNCHANGED`
- `authorization = UNCHANGED`
- `execution = NONE`
- `mutation = NONE`
- `production_ready = false`
- No provider, deployment, production, credential, secret, database, permission, deletion, commit, push, or destructive action.

## CI repair

The first exact-main CI run exposed two documentation-contract gaps: the dedicated workflow expected the literal external-evidence reason code, and the follow-up CI workflow change lacked a same-boundary durable record. Both are repaired before rerunning exact-head CI.

## Closure

- Feature head `fda3e3a6db624d69d6d651cd531c537ad579c9cd` passed exact-head CI: Development OS `34817368411`; Contracts `34817368361`; Trust-First `34817368368`; Provider Controller `34817368359`; Remote Permission Governance `34817368403`; Managed Repository Preflight `34817368326`.
- The dedicated preflight workflow now runs on pull requests and pushes to `main`; the contracts workflow also executes its regression corpus.
- Durable state, decisions, and task records were reconciled after verification. No managed-repository mutation is part of this objective.
