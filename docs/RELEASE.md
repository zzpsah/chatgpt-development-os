# DevOS Release Process

## Release meaning

**Distribution release readiness is not production readiness.**

A DevOS distribution can be engineering-release-ready while `production_ready = false`. The release gate verifies repository identity, version consistency, durable safety boundaries, required documentation, an exact clean Git checkout, and reproducible source packaging. It does not grant deployment authority, enable provider mutation, approve production use, or certify every external runtime.

Canonical version source: `VERSION`.
Canonical release metadata: `config/release-manifest.json`.
Canonical release gate: `python tools/devos.py release-check`.

## Supported baseline

- Python 3.11 or newer for the release CLI/gate.
- Git available for exact-source and clean-worktree verification.
- Repository identity: `zzpsah/chatgpt-development-os`.
- Default entry point: `python tools/devos.py`.

Quick verification:

```bash
python tools/devos.py version
python tools/devos.py release-check
```

The release check exits non-zero when metadata, safety boundaries, Git state, documentation, or required files drift.

## CI release gate

`.github/workflows/verify-release-readiness.yml` performs the release-specific checks on pull requests and manual dispatch. It must pass on the exact release candidate head together with the normal DevOS verification workflows.

The workflow:

1. validates `VERSION`, the release manifest, README markers, security/release documentation, durable production boundaries, and exact Git state;
2. runs the release checker regression corpus;
3. exercises the cross-platform `devos` CLI on Linux and Windows with supported Python versions;
4. builds a source-only ZIP from the exact Git commit with `git archive`;
5. computes a SHA-256 checksum; and
6. uploads the ZIP and checksum as CI artifacts without publishing a GitHub Release or creating a tag.

## Reproducible source artifact

For an exact checked-out release commit:

```bash
VERSION="$(cat VERSION)"
mkdir -p dist
git archive --format=zip --prefix="chatgpt-development-os-${VERSION}/" HEAD -o "dist/chatgpt-development-os-${VERSION}.zip"
sha256sum "dist/chatgpt-development-os-${VERSION}.zip" > "dist/chatgpt-development-os-${VERSION}.zip.sha256"
```

The artifact is source distribution only. Secrets, credentials, local caches, untracked files, and working-tree state are not included by `git archive`.

## Publication boundary

Release-readiness CI does **not** automatically:

- create or move a Git tag;
- create a GitHub Release;
- deploy software;
- alter credentials, secrets, databases, permissions, or production systems;
- upgrade `production_ready`;
- convert runtime declarations into verified integrations; or
- grant approval for a runtime/provider action.

Those remain separate, explicit operations with their own evidence and authorization requirements.

## Managed-project lifecycle support

DevOS `0.21.0` adds Managed Project Lifecycle v1.

A repository selected for DevOS work is not considered managed merely because the provider or filesystem says it exists. The lifecycle must verify repository-local DevOS identity and minimum durable context. If the repository is unmanaged or partial, development continuation remains HOLD until onboarding is explicitly authorized, applied within scope, and fresh readback returns `MANAGED`.

```text
REPOSITORY EXISTS != DEVOS MANAGED
REPOSITORY CREATED != ONBOARDED
REPOSITORY DISCOVERED != SAFE TO CONTINUE
```

Release/distribution readiness of DevOS itself does not authorize onboarding arbitrary external repositories. Local/provider discovery and onboarding still depend on selected project scope, provider capability, and authorization.

## Runtime support statement

The merged runtime profile registry is authoritative for DevOS conformance claims. `reference-local-agent` is only verified for its recorded static contract evidence. `codex`, `claude-code`, and `openhands` remain declaration-only until a separate evidence-backed conformance proof is merged. A familiar runtime name is not capability evidence.

DevOS `0.18.0` introduced challenge-bound conformance evidence intake. It can validate that a candidate packet matches one exact runtime ID, adapter version, Git head, nonce, required capability set, provenance shape, and SHA-256 evidence digests. `EVIDENCE_PACKET_VALID` is not a verified runtime and cannot mutate or promote the registry; separate directly observed invocation evidence, semantic review, durable registry change, and verification remain mandatory.

## Security and integrity

Before publication, the exact candidate must have green applicable CI and no unresolved release-check blocker. Never place secrets, tokens, private keys, cookies, production data, or private school/user documents into release artifacts or repository history. Follow `.github/SECURITY.md` for vulnerability handling.

## Version policy

DevOS uses semantic versioning for distribution metadata. `0.21.0` is a backward-compatible capability increment over the `0.20.0` line, adding managed-project lifecycle enforcement so repository creation/discovery cannot silently bypass onboarding. It preserves all authority, authorization, publication, deployment, and production-readiness boundaries. Remaining `0.x` communicates that production-grade external execution/deployment guarantees are intentionally not claimed.

A new capability that changes the exact source distribution must not silently reuse an already release-ready version identifier; the canonical `VERSION`, release manifest, README, changelog, current production-readiness assessment version, and exact-source CI artifact must move together.

## Release completion evidence

A release candidate is engineering-ready only when:

- `python tools/devos.py release-check` returns `READY` on an exact clean candidate checkout;
- the dedicated release-readiness workflow is green on that same candidate head;
- the normal DevOS security/contracts/integration workflows are green;
- the source ZIP and SHA-256 artifact are generated from that exact head; and
- durable state records the exact verification evidence after merge.

`production_ready = false` remains a deliberate safety boundary unless a separately scoped, evidence-backed objective changes it.
