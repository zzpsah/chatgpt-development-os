# DevOS GitHub Identity & Token Control Plane v1

## Purpose

Provide a provider-specific authentication contract for connecting one or more GitHub accounts to DevOS without turning credentials into DevOS authorization.

This objective implements the authentication/control-plane boundary only. It does not claim live GitHub OAuth/App exchange, token-vault deployment, or production provider mutation until a separately deployed integration is configured and verified.

## Recommended GitHub model

Use a **GitHub App** as the primary DevOS integration and user authorization mechanism. GitHub Apps provide fine-grained permissions, can act on behalf of a user, and installation access tokens are short-lived. A GitHub App installation token expires after one hour. User access tokens created by a GitHub App can be refreshed and expire by default after eight hours. Exact permissions remain limited by what GitHub grants to the user/app/installation.

DevOS therefore supports two authentication modes:

1. `github_app_user` — user authorization for acting on behalf of a GitHub user.
2. `github_app_installation` — installation-scoped provider access for repositories granted to the installation.

A fine-grained PAT may exist as a compatibility adapter in a future implementation, but it is not the preferred control-plane path.

## Authentication lifecycle

```text
User
  ↓
DevOS Connect GitHub
  ↓
GitHub App authorization / installation
  ↓
OAuth callback or installation identity
  ↓
Token exchange / installation token issuance
  ↓
Secret vault boundary
  ↓
Capability discovery
  ↓
Project ↔ GitHub identity binding
  ↓
Remote Permission Control Plane
  ↓
P17 exact-step readiness
  ↓
Provider adapter
  ↓
Fresh GitHub readback
  ↓
Durable non-secret evidence
```

## Security boundaries

The following values are deliberately distinct:

```text
GitHub identity
!= token
!= provider capability
!= DevOS capability
!= DevOS authorization
!= P17 readiness
!= execution
!= verification
```

The raw access token, refresh token, GitHub App private key, OAuth client secret, JWT signing material, or equivalent credential must never be persisted in repository files, `.ai/` state, MCP arguments, logs, CI output, evidence records, or model-visible output.

Only non-secret metadata may be persisted, such as:

- GitHub account login / numeric identity when appropriate;
- app/client identifier (not the secret);
- installation identifier;
- provider owner/namespace;
- repository identifiers permitted by the provider;
- granted permission names/levels;
- token type;
- issued/expiry timestamps;
- credential version/fingerprint that cannot reconstruct the secret;
- revocation/health state.

## OAuth state protection

A web callback must bind to a cryptographically random state value stored outside repository state. The callback is accepted only when the presented state exactly matches the pending transaction using constant-time comparison. A missing, reused, malformed, or mismatched state enters `AUTHORIZATION_HOLD` and cannot produce a token binding.

## Token lifecycle rules

Installation tokens are treated as renewable ephemeral credentials. The adapter must:

- never assume an installation token is permanent;
- honor the provider expiry timestamp;
- mint a fresh token when expired or near expiry;
- never log token material;
- treat `401`/revocation as authentication failure requiring recovery/reauthorization, not as permission to retry blindly;
- keep token use scoped to one project/provider identity binding.

User tokens must likewise be treated as renewable/expiring credentials where GitHub is configured for expiration. Refresh-token material remains inside the secret vault boundary.

## Capability discovery

After authentication, DevOS should query the provider and produce a **non-secret GitHub capability manifest**. The manifest is evidence of provider-side capability, not authorization to act.

Example shape:

```json
{
  "provider": "github",
  "identity": {
    "login": "example",
    "id": 12345
  },
  "auth_mode": "github_app_installation",
  "installation_id": 987654,
  "repositories": ["owner/repo"],
  "permissions": {
    "contents": "write",
    "pull_requests": "write",
    "workflows": "write"
  },
  "expires_at": "2026-09-14T02:30:00Z"
}
```

The actual token must never appear in this manifest.

## Project isolation

Each managed project binds explicitly to one provider identity context:

```text
project_id
+ provider=github
+ account/installation identity
+ repository scope
+ capability manifest fingerprint
```

Project A credentials and provider binding must never be reused for Project B. Approval envelopes remain project-specific.

## DevOS authorization integration

Authentication supplies technical capability only. Remote operations continue through the existing control plane:

```text
GitHub credential
    ↓
provider capability
    ↓
DevOS capability
    ↓
exact authorization
    ↓
P17 readiness
    ↓
controller
    ↓
execution
    ↓
fresh readback
```

The existing invariants remain fixed:

```text
PROVIDER CREDENTIAL != DEVOS AUTHORIZATION
FULL APPROVAL != BLANKET PERMISSION
READY != EXECUTION
PROVIDER RESPONSE != COMPLETION PROOF
UNCERTAIN MUTATION != AUTOMATIC RETRY
```

## GitHub permission strategy

Request the minimum GitHub App permissions required by enabled capabilities. For Git over HTTP, GitHub requires repository `Contents` permission; editing files under `.github/workflows` additionally requires the `Workflows` permission. Exact endpoint permission requirements remain provider-adapter concerns and must be verified against current GitHub API documentation before activation.

DevOS may expose broader capability categories in its adapter, but a capability is usable only when the currently authenticated GitHub identity/app installation actually possesses the corresponding provider permission and repository scope.

## Failure states

The authentication adapter must fail closed with explicit categories:

- `AUTH_CONFIG_INVALID`
- `AUTHORIZATION_PENDING`
- `AUTHORIZATION_HOLD`
- `AUTH_STATE_MISMATCH`
- `AUTH_TOKEN_EXPIRED`
- `AUTH_TOKEN_REVOKED`
- `AUTH_TOKEN_SCOPE_UNKNOWN`
- `GITHUB_IDENTITY_UNCONFIRMED`
- `GITHUB_INSTALLATION_UNCONFIRMED`
- `GITHUB_CAPABILITY_UNCONFIRMED`
- `PROJECT_PROVIDER_BINDING_INVALID`

Authentication failure does not modify DevOS authorization or execute a provider mutation.

## Live activation boundary

The checked-in implementation must remain safe when no GitHub App credentials or secret vault are configured. Live OAuth exchange, JWT signing, installation-token issuance, token storage, and live mutation require a separately deployed provider integration with explicit secret management and fresh verification.
