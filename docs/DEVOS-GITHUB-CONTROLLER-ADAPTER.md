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
  -> fresh provider readback
  -> evidence/persistence
```

The bridge and adapter do not create authorization. GitHub credentials only provide technical provider capability. Remote mutations remain governed by the existing remote-permission control plane.

## Authentication

The controller bridge uses the repository-proven GitHub App authentication implementation in `tools/devos-github-actions-auth.py` to obtain the installation token, then injects that token into the provider adapter.

Required GitHub Actions secrets:

- `DEVOS_GITHUB_APP_ID`
- `DEVOS_GITHUB_APP_PRIVATE_KEY`

The private key is used only for short-lived JWT signing. It is never emitted as evidence or persisted in the repository.

The current App installation is configured to the target repository. The adapter does not persist the installation token and does not include credential material in evidence. GitHub documents installation tokens as short-lived, expiring after one hour. citeturn195196search0

An early attempt to use the `repository_ids` installation-token request variant through the new adapter path returned `401 Bad credentials`, while the existing proven runtime helper continued to authenticate successfully. The controller bridge therefore deliberately reuses the known-good authentication/token implementation rather than duplicating an unproven provider-auth path.

## Read operations

Supported provider reads:

- `repository.get`
- `file.get`
- `branch.get`
- `pr.get`

A read returns `FRESH_PROVIDER_READ` evidence and never changes authorization or remote state.

`tools/devos-github-proven-auth-read.py` supplies the same proven App token provider to the adapter for live read verification.

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

Fresh exact-head live proof on the final PR head established:

- baseline App authentication: PASS;
- repository read through the adapter using the proven App auth provider: PASS;
- deterministic adapter and controller-bridge checks: PASS.

Live mutation remains unexecuted. Any remote mutation still requires the normal DevOS authorization/P17/Security Gate conditions and fresh provider readback.
