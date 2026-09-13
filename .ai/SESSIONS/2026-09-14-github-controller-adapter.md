# Session — 2026-09-14 — GitHub Provider Controller Adapter

## Objective

Make the live GitHub App usable by the normal DevOS governed execution path after PR #32, while preserving P17/controller/remote-permission boundaries.

## Implementation

- Added `tools/devos-github-provider-adapter.py`.
- Added `tools/devos-github-controller-bridge.py`.
- Added `tools/devos-github-proven-auth-read.py` for live proof using the already-proven App authentication path.
- Added deterministic tests for the adapter and controller bridge.
- Added `docs/DEVOS-GITHUB-CONTROLLER-ADAPTER.md`.
- Added `.github/workflows/verify-github-provider-controller-adapter.yml`.

## Authentication model

The controller bridge obtains the GitHub App installation token through the repository-proven `tools/devos-github-actions-auth.py` authentication path and injects that token into the provider adapter. The App installation in the current deployment is repository-scoped. Credentials are external GitHub Actions secrets and are never persisted or emitted as evidence.

An early adapter attempt used the newer `repository_ids` installation-token request variant and consistently produced `401 Bad credentials` in the adapter read path. The existing DevOS App authentication helper continued to pass. The controller path was therefore changed to reuse the known-good authentication/token acquisition implementation rather than duplicating an unproven auth path.

## Execution model

```text
P17 READY + controller EXECUTION_CANDIDATE
    -> runtime handoff validation
    -> explicit provider_operation
    -> remote permission gate
    -> proven GitHub App installation token
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

Fresh exact-head adapter workflow `34786868890` / #13 passed:

- GitHub provider adapter deterministic regression: success
- GitHub controller bridge deterministic regression: success
- baseline live GitHub App authentication: success
- live repository read through the governed adapter with the proven App auth path: success

Fresh companion CI observed on the same final head:

- Trust-First Audit `34786868845` / #176: success
- Current-Source Evidence `34786868828` / #74: success
- MCP Repository Create `34786868831` / #71: success
- Development OS Contracts `34786868825` / #713: success
- Development OS `34786868830` / #635: success

No live mutation was performed.

## Remaining boundary

PR #35 remains separate from `main` and requires explicit merge authorization. Live GitHub read/provider capability is now proven through the normal controller-facing bridge path; live mutation remains authorization- and readback-gated and was not executed.
