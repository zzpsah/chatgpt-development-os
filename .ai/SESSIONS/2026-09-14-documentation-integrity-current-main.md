# 2026-09-14 — Documentation Integrity current-main recovery

## Context

Legacy PR #2 (`devos/documentation-integrity-v2`) remained open against a stale P12-era repository state. Its broad 56-file branch is not safe to merge into current DevOS because later P13–P17, permission-governance, actionable-hold, onboarding, evidence, and recovery work superseded that tree.

## Recovered requirement

One still-valid requirement from PR #2 was not present on current `main`: the deterministic documentation-at-change boundary expressed as:

`IMPLEMENTED + VERIFIED + DOCUMENTED`

The original `core/documentation-integrity.md` and `tools/verify-documentation-integrity.py` artifacts were absent from current `main`, and the current Contracts workflow did not enforce an equivalent check.

## Current-main bounded implementation

This change restores only that missing capability on top of current `main`:

- `core/documentation-integrity.md` — normative contract;
- `tools/verify-documentation-integrity.py` — deterministic latest-change-boundary verifier;
- `tools/test-documentation-integrity.py` — regression corpus;
- `.github/workflows/verify-devos-contracts.yml` — Contracts CI wiring.

The verifier is intentionally stricter than the legacy version: `core/`, `tools/`, `tests/`, `workflows/`, `rules/`, and `.github/` are material implementation authorities and do not self-satisfy the durable-record requirement merely because a file is Markdown. Durable documentation is limited to `.ai/`, `docs/`, `AGENTS.md`, `CHANGELOG.md`, and `README.md`.

## Safety/evidence boundary

- No numbered phase is created.
- This guard is syntactic/deterministic, not semantic proof of documentation completeness.
- It grants no execution or mutation authority.
- It does not alter P15/P16/P17/controller authorization semantics.
- `production_ready=false` and `live_provider_proven=false` remain unchanged.
- No live/destructive/provider/credential/permission/deployment mutation is performed.

## Legacy PR disposition

PR #2 should be treated as superseded only after this current-main replacement is verified and merged. Its stale branch should not be rebased or merged wholesale.
