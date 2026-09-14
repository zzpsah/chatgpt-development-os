# Session — Distribution Release Readiness v1

Date: 2026-09-14

## Objective

Drive DevOS from a verified engineering repository to an engineering **distribution release-ready** state without converting that status into production readiness or deployment authority.

## Trigger

The user explicitly authorized autonomous inspection, modification, testing, debugging, documentation, CI, PR creation/update/merge, and iteration until all achievable release gates are complete.

## Fresh-source observations

At objective start:

- authoritative `main` was `52cb5624c949cfa217bd6dc00bc733f9136268b0` after PR #60 durable reconciliation;
- no open pull requests were present;
- no GitHub Releases were present;
- README still advertised stale `0.12 / P12` version metadata despite P17 and later unnumbered capabilities being merged;
- existing DevOS doctor/health/readiness evidence correctly kept `production_ready = false` and historical evidence pinned;
- no dedicated distribution version source, release manifest, release-specific cross-platform gate, reproducible source artifact/checksum workflow, or public security policy existed.

## Bounded implementation

Branch: `release/devos-0.17.0-readiness`

Added/updated:

- `VERSION` as canonical distribution version (`0.17.0`);
- `config/release-manifest.json` with fail-closed release/publication boundaries;
- `tools/devos.py` as a small shell-free cross-platform dispatcher for version/doctor/health/bootstrap/release-check;
- `tools/devos-release-check.py` to validate version, canonical identity, durable production boundaries, required release files/docs, security markers, changelog, clean Git checkout and exact expected head;
- adversarial release-gate and CLI regression tests;
- `.github/workflows/verify-release-readiness.yml` with Linux/Windows and Python 3.11/3.12 matrix plus exact-commit `git archive` ZIP/SHA-256 artifact generation;
- `docs/RELEASE.md` documenting release semantics, packaging and non-goals;
- `.github/SECURITY.md` for private vulnerability reporting and secret-handling boundaries;
- `CHANGELOG.md` release notes and explicit limitations;
- README rewritten to current P17-complete architecture/recovery/runtime/delivery/release status.

## Version decision

`0.17.0` was selected because the historical README tied `0.12` to P12, while the numbered architecture is now complete through P17. Later resolver/provider/delivery/runtime/reconciliation work remains deliberately unnumbered. Remaining `0.x` status is consistent with the repository's explicit refusal to claim production-grade external execution/deployment guarantees.

## Safety boundaries

This objective does **not**:

- set `production_ready = true`;
- create a Git tag or GitHub Release;
- deploy anything;
- change credentials, secrets, databases or permissions;
- perform destructive actions;
- expand provider/runtime authorization;
- promote Codex, Claude Code or OpenHands from declaration-only to verified runtime integration;
- rewrite historical readiness evidence as current evidence; or
- change public licensing terms.

Release readiness is an engineering distribution claim only and requires exact-head CI plus reproducible artifact evidence.

## Completion rule

The objective is not complete until:

1. dedicated release-readiness CI is green on the exact final feature head;
2. applicable normal DevOS workflows are green on that same head;
3. exact-source ZIP and SHA-256 artifacts are successfully generated;
4. feature PR is merged with expected-head protection;
5. fresh `main` readback verifies merge truth; and
6. durable CURRENT/TASKS/history/reconciliation evidence records the exact release-readiness result.

No recursive documentation-only PR should be created beyond the one bounded post-feature reconciliation needed to leave recoverable durable state.
