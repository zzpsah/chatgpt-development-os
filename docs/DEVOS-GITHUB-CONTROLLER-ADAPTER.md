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
  -> GitHub App installation token
  -> one bounded provider operation
  -> fresh provider readback
  -> evidence/persistence
```

The bridge and adapter do not create authorization. GitHub credentials only provide technical provider capability. Remote mutations remain governed by the existing remote-permission control plane.

## Authentication

The adapter uses GitHub App installation-token authentication inside GitHub Actions through:

- `DEVOS_GITHUB_APP_ID`
- `DEVOS_GITHUB_APP_PRIVATE_KEY`

The private key is used only for short-lived JWT signing. It is never emitted as evidence or persisted in the repository.

The adapter first resolves the target repository's App installation and then mints an installation token constrained to that repository. Current GitHub App installation tokens are short-lived; GitHub documents a one-hour lifetime. The adapter does not persist the token and does not rely on token shape/length. citeturn195196search0

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

## Exactly-once and uncertain outcomes

File update/delete requires an `inputs.expected_sha`. This prevents a stale resource from being overwritten or deleted without an explicit state anchor.

For branch operations and pull-request merge, the operation input carries the expected target commit/sha where applicable.

If a mutation request may have been dispatched but the network result is uncertain, the adapter returns `HOLD` with `UNCERTAIN_PROVIDER_RESULT` and instructs `READBACK_BEFORE_RETRY`. It never automatically retries the mutation.

After every successful mutation, the adapter performs a fresh provider readback:

- file mutation → current file SHA/presence;
- branch mutation → current branch ref SHA/presence;
- pull-request merge → current merged/state/merge SHA.

A successful HTTP response without the required readback is never reported as `COMPLETE`.

## Controller bridge

`tools/devos-github-controller-bridge.py` requires an exact `DEVOS-STEP-READINESS-v1` READY envelope plus the controller `EXECUTION_CANDIDATE` envelope. It reuses `tools/devos-runtime-handoff.py` instead of defining a second readiness authority.

The compiled controller step must contain an explicit `provider_operation` object. The bridge does not infer provider operations from free-form objective text.

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

Live read proof remains read-only. A provider mutation requires the normal DevOS authorization/P17/security gates and must be tested separately against an explicitly approved sandbox target.
