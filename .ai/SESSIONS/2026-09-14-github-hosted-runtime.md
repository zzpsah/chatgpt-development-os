# Session — GitHub-hosted DevOS Runtime

Date: 2026-09-14
Objective: adapt DevOS GitHub authentication for a runtime that executes entirely on GitHub.

## Decision
The runtime path is GitHub Actions + GitHub App installation-token authentication. A browser OAuth callback is not required for the GitHub-hosted automation runtime.

## Implementation
- Added `tools/devos-github-actions-auth.py`.
- Added `tools/test-devos-github-actions-auth.py`.
- Added `.github/workflows/devos-github-app-runtime.yml`.
- Extended `.github/workflows/verify-github-auth-control-plane.yml`.
- Added `docs/DEVOS-GITHUB-HOSTED-RUNTIME.md`.
- Updated `.ai/CURRENT-STATE.md`, `.ai/TASKS.md`, and `.ai/DECISIONS.md`.

## Runtime behavior
1. Read `DEVOS_GITHUB_APP_ID` and `DEVOS_GITHUB_APP_PRIVATE_KEY` from GitHub Actions secrets.
2. Create a short-lived RS256 App JWT on the GitHub-hosted runner.
3. Resolve the App installation for the requested `owner/name` repository.
4. Mint a short-lived installation token.
5. Read the target repository metadata with the installation token.
6. Emit only non-secret verification metadata.

No repository mutation is performed by this workflow.

## Security / evidence
- Raw App private key is never committed, printed, artifacted, or persisted as DevOS state.
- Installation token is process-local and not emitted.
- `credential_material: NOT_INCLUDED`.
- `execution: NONE`.
- `mutation: NONE`.
- Provider authentication/capability does not manufacture DevOS authorization.
- P17, Security Gate, remote permission control, and fresh readback remain mandatory for later mutation.

## External activation required
- Create/register the DevOS GitHub App.
- Configure least-privilege permissions.
- Install it on each target repository/account.
- Add Actions secrets `DEVOS_GITHUB_APP_ID` and `DEVOS_GITHUB_APP_PRIVATE_KEY`.
- Run `DevOS GitHub App Runtime` manually against the intended repository.
- Preserve fresh run evidence before claiming live provider proof.

## Unknowns
- App registration/installation may not yet exist.
- Actions secrets may not yet be configured.
- No live-provider smoke run is claimed by this session.

## Next AI
Run fresh branch CI. After the App and Actions secrets are configured, run the manual read-only runtime workflow. Reconcile any authentication/capability failure before considering further integration.
