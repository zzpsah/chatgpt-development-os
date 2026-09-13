# Session — 2026-09-14 — GitHub Provider Controller Adapter

## Objective

Make the live GitHub App usable by the normal DevOS governed execution path after PR #32, while preserving P17/controller/remote-permission boundaries.

## Implementation

- Added `tools/devos-github-provider-adapter.py`.
- Added `tools/devos-github-controller-bridge.py`.
- Added deterministic tests for both components.
- Added `docs/DEVOS-GITHUB-CONTROLLER-ADAPTER.md`.
- Added `.github/workflows/verify-github-provider-controller-adapter.yml`.

## Authentication model

The adapter uses the configured GitHub App installation-token path. The token is scoped to the resolved target repository and is never persisted or emitted as evidence.

## Execution model

```text
P17 READY + controller EXECUTION_CANDIDATE
    -> runtime handoff validation
    -> explicit provider_operation
    -> remote permission gate
    -> GitHub App installation token
    -> one bounded provider operation
    -> fresh provider readback
```

Read operations remain read-only. Mutations require exact DevOS authorization and capability identity.

## Safety / recovery

- `file.update` / `file.delete` require `expected_sha` state anchors.
- `branch.update` and `branch.force_update` remain distinct capabilities.
- uncertain network results become `HOLD` with `READBACK_BEFORE_RETRY`.
- successful mutations require fresh provider readback before `COMPLETE`.
- unsupported generic capabilities fail closed.
- credential material is never included in output/evidence.

## Verification

Latest adapter CI run `34786493965` / #5 passed both deterministic suites:

- GitHub provider adapter: success
- GitHub controller bridge: success

The live-read job is intentionally limited to push/manual events and was skipped on pull request CI. Fresh live read evidence must be obtained from a post-merge/manual run before claiming the adapter's live read path is independently proven.

## Remaining boundary

No live mutation was performed. No production readiness is inferred from the adapter CI. Merge remains separately authorization-gated.
