# Session — 2026-09-14 — Living Map Canonicalization

## Objective
Post-merge consistency cleanup after PR #30.

## Findings
- `main` contained both `docs/DEVOS-MASTER-ENGINEERING-MAP.md` and `docs/DEVOS-MASTER-ENGINEERING-MAP-v2.md`, each presenting itself as the DevOS master engineering map.
- `tools/test-devos-living-docs.py` checked required files/markers but did not reject duplicate canonical maps.
- `.github/workflows/verify-living-devos-docs.yml` did not run on pushes to `main`.
- `core/devos-living-state-and-evolution.md` repeated documentation-at-change rules without explicitly delegating to the existing normative `core/documentation-integrity.md` contract.

## Cleanup
- Keep `docs/DEVOS-MASTER-ENGINEERING-MAP.md` as the single canonical master map.
- Remove the redundant `docs/DEVOS-MASTER-ENGINEERING-MAP-v2.md`; Git history preserves its provenance.
- Extend the living-doc verifier so reintroducing the legacy duplicate path fails deterministically.
- Run the living-doc workflow on relevant pushes to `main` as well as pull requests.
- Explicitly subordinate documentation-at-change enforcement in the living-state contract to `core/documentation-integrity.md` while retaining living-architecture/P15 evolution semantics.

## Boundaries
- No new numbered DevOS phase.
- No production/live-provider/destructive/credential/permission/deployment mutation.
- Documentation and CI do not create authorization.
- Existing source/Git/evidence precedence remains unchanged.
