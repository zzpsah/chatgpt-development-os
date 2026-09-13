# Session — 2026-09-14 — GitHub Identity & Token Control Plane v1

## Objective
Implement a repository-native GitHub authentication/control-plane boundary so DevOS can connect independently authorized GitHub accounts without turning credentials into DevOS authorization.

## Source inspected
- `core/remote-resource-permission-governance.md`
- `docs/DEVOS-MCP-PERMISSION-CONTROL-PLANE.md`
- `.ai/DECISIONS.md`
- `.ai/CURRENT-STATE.md`
- `.ai/TASKS.md`
- `docs/DEVOS-MASTER-ENGINEERING-MAP.md`

## Implemented
- GitHub App-focused identity/token control-plane contract.
- OAuth state-generation and constant-time callback-state validation.
- Project-scoped GitHub identity binding.
- Installation/user authentication mode distinction.
- Non-secret capability manifest normalization.
- Token expiry/skew evaluation.
- Secret fingerprinting for evidence without persisting secret material.
- Deterministic regression tests.
- Dedicated GitHub-auth CI gate.

## Safety boundary
No GitHub App client secret, private key, access token, refresh token, JWT signing key, live OAuth exchange, token vault, or live provider mutation was introduced. The implementation is side-effect-free until an external deployment supplies secure provider credentials and a secret-management boundary.

## External evidence
GitHub's current documentation states that GitHub Apps provide fine-grained permissions; installation access tokens expire after one hour; GitHub App user access tokens can expire and be refreshed; Git/HTTP access requires the applicable repository `Contents` permission, and workflow-file access requires `Workflows` where applicable.

## Verification
Pending branch CI. Local deterministic verification must report `DevOS GitHub auth checks: PASS (10 assertions)` once run.

## Remaining work
- register/configure the production DevOS GitHub App;
- deploy OAuth callback and secure secret storage;
- perform a separately authorized disposable live authentication/read test;
- connect capability discovery and token issuance to the production provider adapter;
- prove fresh readback for any live mutation in an explicit sandbox.

No P18/P19 phase is created by this objective.
