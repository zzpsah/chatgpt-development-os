# DevOS GitHub Controller Adapter v1

## Purpose

This adapter is the provider execution boundary that turns an already-authorized DevOS controller/P17 handoff into a bounded GitHub operation.

The governed path is:

```text
P15 interpretation
  -> P16 plan
  -> P17 READY
  -> controller EXECUTION_CANDIDATE
  -> runtime handoff
  -> GitHub controller bridge
  -> remote permission gate
  -> proven GitHub App installation token
  -> one bounded provider operation
  -> bounded fresh-provider readback/reconciliation
  -> evidence/persistence
```

The bridge and adapter do not create authorization. GitHub credentials only provide technical provider capability. Remote mutations remain governed by the existing remote-permission control plane.

## Authentication

The controller bridge uses the repository-proven GitHub App authentication implementation in `tools/devos-github-actions-auth.py` to obtain the installation token, then injects that token into the provider adapter.

Required GitHub Actions secrets:

- `DEVOS_GITHUB_APP_ID`
- `DEVOS_GITHUB_APP_PRIVATE_KEY`

The private key is used only for short-lived JWT signing. It is never emitted as evidence or persisted in the repository.

The controller bridge deliberately reuses the known-good authentication/token implementation rather than duplicating an unproven provider-auth path. The adapter does not persist the installation token and does not include credential material in evidence.

## Read operations

Supported provider reads:

- `repository.get`
- `file.get`
- `branch.get`
- `pr.get`

A read returns `FRESH_PROVIDER_READ` evidence and never changes authorization or remote state.

## Governed mutations

Supported first-slice mutations:

- `file.create`
- `file.update`
- `file.delete`
- `branch.create`
- `branch.update`
- `branch.force_update`
- `branch.delete`
- `pr.merge`

Each mutation must use the existing DevOS capability name as its `capability` and `action`. This prevents a mismatched operation from silently receiving a different authorization scope.

Before the provider request, the adapter calls `tools/devos-remote-permission-check.py`. An exact authorization is required for every mutation. The authorization must match provider, owner, repository, resource, capability, workflow, project, impact ceiling, freshness, and authorization provenance.

`branch.force_update` stays distinct from `branch.update`; `file.delete` remains higher impact than ordinary file create/update; `pr.merge` remains HIGH impact.

## Exactly-once, uncertain outcomes, and readback reconciliation

File update/delete requires an `inputs.expected_sha`. This prevents a stale resource from being overwritten or deleted without an explicit state anchor.

For branch operations and pull-request merge, the operation input carries the expected target commit/sha where applicable.

If a mutation request may have been dispatched but the network result is uncertain, the adapter returns `HOLD` with `UNCERTAIN_PROVIDER_RESULT` and instructs `READBACK_BEFORE_RETRY`. It never automatically retries the mutation.

After every successful mutation, the adapter performs a fresh provider readback:

- file mutation → current file SHA/presence;
- branch mutation → current branch ref SHA/presence;
- pull-request merge → current merged/state/merge SHA.

GitHub content reads can briefly lag the mutation response. To handle that observed eventual-consistency window without replaying the mutation, the adapter now performs a bounded retry of the **readback only** when the readback specifically fails with HTTP 404. The default delays are 1s, 2s, and 4s, allowing up to four readback attempts total (the initial read plus one attempt after each delay). Authentication failures, validation errors, network uncertainty, and other failures are not converted into automatic retries.

When a post-mutation readback becomes available within the bounded window, the result is `COMPLETE` with `FRESH_PROVIDER_READBACK` plus `readback_attempts`. When the bounded window is exhausted, the adapter remains fail-safe and returns `HOLD` with `READBACK_REQUIRED` and the original provider response for reconciliation. No mutation replay occurs.

For deletion, a fresh 404 is interpreted as `ABSENT`, so delete completion still uses provider evidence rather than assuming the mutation succeeded from the write response alone.

## Controller bridge

`tools/devos-github-controller-bridge.py` requires an exact `DEVOS-STEP-READINESS-v1` READY envelope plus the controller `EXECUTION_CANDIDATE` envelope. It reuses `tools/devos-runtime-handoff.py` instead of defining a second readiness authority.

The compiled controller step must contain an explicit `provider_operation` object. The bridge does not infer provider operations from free-form objective text.

The bridge supplies the proven GitHub App token provider to the adapter, so the normal governed controller path uses the same authentication path already proven by the runtime smoke test.

## Security boundary

The adapter never stores or prints:

- App private key;
- App JWT;
- installation token;
- OAuth client secret;
- refresh token.

Returned evidence explicitly reports `credential_material: NOT_INCLUDED`.

## Current non-goals

This first adapter slice does not expose arbitrary GitHub API endpoints, organization administration, secret-management operations, deployments, or repository deletion/creation through the generic controller bridge. Unsupported operations fail closed rather than being silently delegated.

## Verification

Deterministic checks:

- `tools/test-devos-github-provider-adapter.py`
- `tools/test-devos-github-controller-bridge.py`

The deterministic adapter regression suite now covers:

- read-only success;
- missing authorization;
- repository-scope mismatch;
- capability/action mismatch;
- bounded 404 readback reconciliation;
- no retry for a 401 readback failure.

Fresh live controller-path mutation evidence has now established the normal governed write path against a dedicated isolated test branch/resource:

- `file.create` through controller bridge: provider commit returned; immediate readback hit 404; external reconciliation confirmed the file and SHA;
- `file.update` through controller bridge: provider commit returned; immediate readback hit 404; subsequent reconciliation confirmed the updated SHA;
- `file.delete` through controller bridge: provider commit returned and the adapter obtained fresh `ABSENT` readback;
- temporary live-test PRs were closed and were not merged.

This proves live provider mutation through the governed controller path, while `production_ready` remains `false` and no production/destructive authorization is implied. The readback hardening closes the remaining known normal-path race without changing authority boundaries.
