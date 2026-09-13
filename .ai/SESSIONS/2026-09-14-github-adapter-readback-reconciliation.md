# Session — 2026-09-14 GitHub Adapter Readback Reconciliation

## Objective
Harden the governed GitHub provider adapter so an observed post-mutation HTTP 404 readback race is reconciled without replaying the remote mutation.

## Starting evidence
- Main source head at start: `581057724595f4d9edf08175a61dd924a9db1813`.
- Live governed controller-path mutation proof already existed on isolated test branches/resources: create and update returned provider commits but their immediate readbacks temporarily returned 404; later reconciliation confirmed the remote state. Delete completed with fresh `ABSENT` readback.
- The normal controller bridge already supplied the proven GitHub App installation-token provider.

## Change
- Branch: `fix/github-adapter-readback-reconciliation`.
- Added bounded readback-only retries for HTTP 404 after a successful mutation.
- Default delays: 1s, 2s, 4s; up to four total readback attempts (initial read plus one after each delay).
- No mutation replay is introduced.
- 401/authentication errors, validation errors, and network uncertainty remain non-retriable by this layer.
- Exhausted reconciliation remains `HOLD / READBACK_REQUIRED` and preserves the provider response for safe reconciliation.
- Delete 404 remains an `ABSENT` success readback.
- Evidence now records `readback_attempts` on successful mutation completion.

## Verification plan
- Deterministic tests cover bounded 404 recovery and prove that 401 does not trigger retry.
- Existing controller-bridge regression remains required.
- PR CI must pass before considering the hardening implementation verified.

## Safety boundary
- No direct `main` mutation was performed for this hardening change.
- No live destructive mutation, production deployment, secret change, permission change, force-update, or merge authorization was created by this work.
- The existing production boundary remains `production_ready=false`.

## Completion rule
The change is complete only when implementation, deterministic/CI verification, documentation, and durable state are all updated on the same governed branch/PR.
