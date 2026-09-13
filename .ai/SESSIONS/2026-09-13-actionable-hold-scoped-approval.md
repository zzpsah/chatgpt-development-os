# Session — 2026-09-13 — Actionable Hold & Scoped Approval

## Objective
Implement the human-language continuation behavior requested by DevOS governance: actionable HOLD responses, scoped full approval reuse, and fresh approval when scope/freshness/impact changes.

## Work completed
- Added `core/actionable-hold-scoped-approval.md` as the normative contract.
- Added side-effect-free `tools/devos-actionable-hold.py` reference engine.
- Added `tools/test-devos-actionable-hold.py` deterministic regression corpus.
- Added `docs/ACTIONABLE-HOLDS-AND-SCOPED-APPROVAL.md` user-facing/AI-facing operational documentation.
- Added `.github/workflows/verify-actionable-hold.yml` isolated CI gate.

## Design decision
`continue` may resume an already-authorized bounded workflow when project, workflow, capability, target, impact ceiling, freshness anchor, and required Security Gate conditions remain valid.

`FULL APPROVAL` means full approval within the explicitly represented scope; it never becomes blanket permission.

Out-of-scope capability/target, higher impact, changed repository freshness, changed Security Gate state, or unproven approval provenance requires an actionable HOLD and fresh approval/evidence.

## Safety
This implementation is read-only/side-effect-free. No repository/provider mutation is performed by the reference engine or tests.

## Verification
The deterministic regression corpus covers same-workflow approval reuse, target/capability/impact violations, repository-head changes, Security Gate changes, missing approval, actionable HOLD structure, and no-blanket-permission semantics.

## Remaining integration work
The next integration slice should wire these semantics into the existing human-language/controller continuation path without creating a competing authorization system. The integration must preserve P15/P16/P17 boundaries and must be covered by end-to-end regression tests.
