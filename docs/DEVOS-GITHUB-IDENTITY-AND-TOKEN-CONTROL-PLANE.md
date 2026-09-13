# DevOS GitHub Identity & Token Control Plane — Implementation

## Objective

Connect GitHub account authorization to the existing DevOS provider capability and remote-permission boundaries without making a GitHub credential equivalent to DevOS authorization.

## Implemented in v1

- Normative GitHub identity/token contract: `core/devos-github-identity-token-control-plane.md`
- Side-effect-free authentication metadata primitives: `tools/devos-github-auth.py`
- Deterministic authentication regression suite: `tools/test-devos-github-auth.py`
- Side-effect-free capability discovery/evaluation bridge: `tools/devos-github-capability-discovery.py`
- Deterministic capability discovery regression suite: `tools/test-devos-github-capability-discovery.py`
- GitHub-hosted read-only App runtime: `tools/devos-github-actions-auth.py`
- Deterministic hosted-runtime regression suite: `tools/test-devos-github-actions-auth.py`
- Manual read-only hosted runtime workflow: `.github/workflows/devos-github-app-runtime.yml`
- Dedicated verification workflow: `.github/workflows/verify-github-auth-control-plane.yml`
- Durable `.ai` state/decision/session updates
- Master architecture update documenting the identity/token boundary

## GitHub authorization model

GitHub App is the recommended production integration. GitHub documents that GitHub Apps provide fine-grained permissions and can act on behalf of a user; installation access tokens are short-lived and currently expire after one hour. GitHub App user access tokens can expire and be renewed with a refresh token. Exact access remains constrained by GitHub-side permissions and the user's own permissions.

Useful official documentation:

- https://docs.github.com/en/apps/creating-github-apps/registering-a-github-app/choosing-permissions-for-a-github-app
- https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app
- https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app
- https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/token-expiration-and-revocation

## OAuth callback guardrails

The optional interactive OAuth path uses a cryptographically random pending transaction state. Callback validation is deterministic and fail-closed:

- state comparison is constant-time;
- a transaction older than the configured maximum age is rejected;
- an already-consumed/reused transaction is rejected;
- a callback timestamp that predates the transaction is rejected;
- malformed/missing callback code is rejected.

The deployment boundary is responsible for storing pending and consumed transaction state outside Git. A matching state string by itself is not indefinitely reusable authorization evidence.

The GitHub-hosted Actions runtime does not require a browser OAuth callback; it uses GitHub App installation-token authentication instead.

## Capability discovery bridge

Authentication metadata is not itself a DevOS capability. The discovery bridge consumes provider-reported, non-secret permissions and evaluates them against an adapter-supplied mapping for individual DevOS capabilities.

```text
GitHub identity
      ↓
non-secret provider permission metadata + repository scope
      ↓
capability discovery bridge
      ↓
AVAILABLE | UNAVAILABLE | UNCONFIRMED
      ↓
Remote Permission Control Plane
      ↓
P17 exact-step readiness
```

The mapping is intentionally supplied by the provider adapter rather than hard-coded into generic DevOS logic. This prevents stale provider permission assumptions from becoming authorization.

Evaluation is permission-level-aware and scope-aware:

- `read` does not satisfy a required `write` permission;
- unknown permission levels fail closed as `UNCONFIRMED`;
- existing-repository capabilities require an explicit target repository;
- the target repository must be present in provider-reported repository scope before `AVAILABLE` is possible;
- missing mapping/evidence is never inferred into capability.

The discovery bridge is side-effect-free and emits only non-secret metadata:

- provider identity;
- target repository and repository scope;
- provider permission names/levels;
- capability status/reason;
- `authorization: UNCHANGED`;
- `execution: NONE`;
- `mutation: NONE`;
- `credential_material: NOT_INCLUDED`.

`UNCONFIRMED` means the adapter mapping or evidence is insufficient. It must not be upgraded to authorization by inference.

## GitHub-hosted runtime boundary

The repository also contains a GitHub Actions runtime for read-only live authentication proof. It may perform network requests when manually dispatched and externally configured with GitHub Actions secrets.

That runtime:

1. creates a short-lived GitHub App JWT;
2. resolves the App installation for the requested repository;
3. mints a short-lived installation token;
4. reads target-repository metadata;
5. emits redacted, non-secret evidence only.

It does **not** create/update/delete repositories or files, merge PRs, deploy, modify permissions, or persist raw credentials. App ID/private-key material remains in GitHub Actions secret storage and is not committed to DevOS state.

## Activation boundary

Repository implementation and deterministic CI do not by themselves prove live-provider readiness.

For the GitHub-hosted runtime, live proof requires:

1. a registered GitHub App;
2. App installation on the intended target repository/account;
3. `DEVOS_GITHUB_APP_ID` and `DEVOS_GITHUB_APP_PRIVATE_KEY` configured as external GitHub Actions secrets;
4. a successful manual read-only runtime workflow;
5. fresh provider evidence from that run.

A separate interactive web client would additionally require redirect URI/OAuth configuration, secure pending-state storage, OAuth callback/token exchange, and secret/private-key storage outside Git.

Any future live mutation proof remains separately gated by exact DevOS authorization, P17, Security Gate, bounded execution, and fresh readback.

## “Full access” interpretation

DevOS must not seek an unrestricted master token. “Full access” means the maximum capability that GitHub explicitly grants to the selected user/app installation and repository/organization scope, further constrained by DevOS capability authorization, P17 readiness, security gates, and exact operation scope.

## Security invariants

```text
GitHub identity != credential
credential != DevOS authorization
provider capability != DevOS capability
DevOS capability != execution
execution != verification
```

No raw credential is persisted in `.ai/`, logs, evidence, source, MCP arguments, or model output.
