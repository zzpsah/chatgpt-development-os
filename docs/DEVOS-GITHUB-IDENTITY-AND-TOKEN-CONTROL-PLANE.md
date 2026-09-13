# DevOS GitHub Identity & Token Control Plane — Implementation

## Objective

Connect GitHub account authorization to the existing DevOS provider capability and remote-permission boundaries without making a GitHub credential equivalent to DevOS authorization.

## Implemented in v1

- Normative GitHub identity/token contract: `core/devos-github-identity-token-control-plane.md`
- Side-effect-free authentication primitives: `tools/devos-github-auth.py`
- Deterministic regression suite: `tools/test-devos-github-auth.py`
- Dedicated verification workflow: `.github/workflows/verify-github-auth-control-plane.yml`
- Durable `.ai` state/decision/session updates
- Master architecture update documenting the new identity/token boundary

## GitHub authorization model

GitHub App is the recommended production integration. GitHub documents that GitHub Apps provide fine-grained permissions and can act on behalf of a user; installation access tokens are short-lived and currently expire after one hour. GitHub App user access tokens can expire and be renewed with a refresh token. Exact access remains constrained by GitHub-side permissions and the user's own permissions.

Useful official documentation:

- https://docs.github.com/en/apps/creating-github-apps/registering-a-github-app/choosing-permissions-for-a-github-app
- https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app
- https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app
- https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/token-expiration-and-revocation

## Production activation boundary

The repository implementation is intentionally side-effect-free. It does not contain client secrets, GitHub App private keys, refresh tokens, access tokens, or live network exchange logic.

A deployed DevOS service still needs:

1. a registered GitHub App;
2. explicit redirect URI(s) / OAuth configuration;
3. secret/private-key storage outside Git;
4. OAuth callback handling using the anti-CSRF state contract;
5. GitHub user/installation token exchange;
6. capability discovery from the authenticated identity;
7. project-scoped identity binding;
8. integration with the existing Remote Permission Control Plane and P17;
9. fresh provider readback for any live mutation proof.

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
