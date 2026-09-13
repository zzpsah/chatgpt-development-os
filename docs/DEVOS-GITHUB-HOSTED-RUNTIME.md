# DevOS GitHub-Hosted Runtime

## Purpose

When DevOS itself is executed from GitHub, the primary authentication path is the **GitHub App installation-token flow inside GitHub Actions**. A web OAuth callback is not required for the automation runtime.

This is the GitHub-native deployment shape for DevOS:

```text
GitHub repository
  -> GitHub Actions runner
  -> DevOS GitHub App authentication
  -> installation token (short-lived)
  -> provider capability discovery
  -> DevOS permission control plane
  -> P17 readiness/security gates
  -> bounded operation
  -> fresh readback + evidence
```

## Why there is no callback URL in this mode

A callback URL belongs to the GitHub App web application OAuth flow, where a browser is redirected back to an application endpoint after authorization. GitHub documents a separate installation-token flow for GitHub Apps that uses an App JWT and an installation access token.

DevOS does not need a browser callback when the runtime is already executing inside GitHub Actions. The workflow resolves the App installation for the requested repository, mints a short-lived installation token, and performs a read-only provider check. No OAuth client secret is required by this installation-token path.

## GitHub App requirements

Create one GitHub App for DevOS and enable the minimum repository permissions required by the current DevOS capability map. Install the App on the target repositories/accounts that DevOS is allowed to control.

Store the following as **GitHub Actions secrets** in the DevOS runtime repository:

```text
DEVOS_GITHUB_APP_ID
DEVOS_GITHUB_APP_PRIVATE_KEY
```

The App private key is never written to the repository, `.ai` state, CI artifacts, logs, or evidence.

## Runtime workflow

Workflow:

```text
.github/workflows/devos-github-app-runtime.yml
```

Trigger it from **Actions → DevOS GitHub App Runtime → Run workflow** and provide a target repository in `owner/name` form.

The workflow only performs:

1. App JWT creation.
2. Installation lookup for the target repository.
3. Installation access-token minting.
4. Read-only repository verification.
5. Redacted capability/identity metadata output.

The workflow does **not** create, update, delete, merge, deploy, change permissions, or modify repository contents.

## Security model

- GitHub-hosted runner is execution environment, not DevOS authorization.
- GitHub App installation permission is provider capability, not DevOS approval.
- Installation token is short-lived and held only in memory by the runner process.
- Raw credentials are never persisted as durable DevOS evidence.
- P17 remains the gate before any bounded mutation.
- Uncertain provider state must reconcile/read before any retry.
- `credential_material: NOT_INCLUDED` remains mandatory in durable evidence.

## Multi-account behavior

The same DevOS GitHub App can be installed on multiple GitHub accounts or organizations. Each target repository must be reachable through an installation that grants the required provider permissions. The workflow selects the installation by the requested repository, so DevOS does not assume that the runtime repository and the target repository are the same.

The phrase **full access** means the maximum capability explicitly granted by the GitHub App installation and target account, further constrained by DevOS capability mapping, exact scoped authorization, P17 readiness, security gates, and the requested operation. It never means a hidden universal GitHub administrator token.

## Activation boundary

The GitHub repository-side implementation is complete, but live authentication remains dependent on external GitHub configuration:

```text
GitHub App registered        -> user action
App permissions configured   -> user action
App installed on target     -> user action
Actions secrets configured  -> user action
Workflow run                 -> GitHub execution
```

No production/live provider proof should be claimed until the workflow has completed successfully against an actually installed App and target repository.
