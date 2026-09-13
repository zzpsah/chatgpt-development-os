# Session — 2026-09-14 — GitHub Capability Discovery Bridge

## Objective
Continue the GitHub Identity & Token Control Plane v1 toward the existing Remote Permission Control Plane without performing live authentication or remote mutation.

## Source inspected
- `core/remote-resource-permission-governance.md`
- `docs/DEVOS-MCP-PERMISSION-CONTROL-PLANE.md`
- `tools/devos-github-auth.py`
- `tools/test-devos-github-auth.py`
- `.ai/CURRENT-STATE.md`
- `.ai/TASKS.md`
- `.ai/DECISIONS.md`
- `docs/DEVOS-GITHUB-IDENTITY-AND-TOKEN-CONTROL-PLANE.md`

## Implemented
- Added `tools/devos-github-capability-discovery.py` as a side-effect-free provider-permission → DevOS-capability evaluation bridge.
- Added `tools/test-devos-github-capability-discovery.py` with deterministic fail-closed scenarios.
- Extended `.github/workflows/verify-github-auth-control-plane.yml` to run both authentication and capability-discovery regressions.
- Updated GitHub authentication/control-plane documentation with the capability discovery boundary.
- Updated `.ai/TASKS.md`, `.ai/CURRENT-STATE.md`, and `.ai/DECISIONS.md` with durable state and safety semantics.

## Design decision
Provider permission mappings are adapter-supplied instead of being permanently hard-coded into generic DevOS logic. This preserves provider-specific accuracy and prevents stale permission names from becoming authorization.

## Evidence boundary
The bridge only emits non-secret capability metadata and explicitly preserves:
- `authorization: UNCHANGED`
- `execution: NONE`
- `mutation: NONE`
- `credential_material: NOT_INCLUDED`

`UNCONFIRMED` is fail-closed and cannot be upgraded to permission through inference.

## Verification
Initial v1 branch CI for source `113508a32eedcd1d42cb0def9438224fe03aeb1b` passed all observed applicable runs, including GitHub Identity and Token Control Plane run 1 (`34781566089`). This continuation adds new capability-discovery code after that source and therefore requires fresh CI on the latest branch head.

## Remaining work
- fresh branch CI after this hardening;
- PR review/integration;
- externally configured GitHub App;
- secure secret storage;
- real OAuth/token exchange;
- live identity/capability discovery;
- explicit disposable live provider verification;
- fresh readback for any live mutation.

No P18/P19 phase is created. No credentials or live mutations were introduced.
