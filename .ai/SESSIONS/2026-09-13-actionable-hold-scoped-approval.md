# Session — 2026-09-13 — Actionable Hold & Scoped Approval

## Objective
Implement human-language continuation behavior requested by DevOS governance: actionable HOLD responses, scoped approval reuse, fresh approval when scope/freshness/impact/security changes, and integration through the existing P15 → P16 → P17/controller path.

## Reference layer
- Normative contract: `core/actionable-hold-scoped-approval.md`.
- Side-effect-free reference engine: `tools/devos-actionable-hold.py`.
- Reference regression: `tools/test-devos-actionable-hold.py`.
- Python 3.14 dynamic-import harness fixed by registering the dynamically loaded module in `sys.modules` before `exec_module`; dataclass implementation was not weakened or changed to hide the failure.
- Reference-fix head `4796fff53d5f9b8db5201d94e982a66378cc4630` passed Actionable Hold 2 / `34777843251`, Contracts 622 / `34777843239`, Trust-First 85 / `34777843233`, and Full DevOS 544 / `34777843244`.

## Real continuation-path integration
- Added `tools/devos-continuation-path.py`.
- Added `tools/test-actionable-hold-continuation-integration.py`.
- Updated `.github/workflows/verify-actionable-hold.yml` to run both reference and real-path regressions.
- Integrated path: `P15 human-language interpreter → P16 semantic plan → scoped-approval validation → P17 step readiness → development-task controller`.
- Scoped approval never replaces P17 or the controller. Only a still-valid approval is represented to P17 as exact step-bound `ALREADY_GRANTED` evidence.
- The integration does not execute or mutate repository/provider state; even a controller `EXECUTION_CANDIDATE` leaves `execution: NONE` and `mutation: NONE` in this layer.

## Integration proof
The integration regression covers:
1. `continue` + valid scoped approval → P17 READY/controller continuation without duplicate approval;
2. missing approval → actionable HOLD;
3. stale repository HEAD → approval invalidated;
4. target/capability change → fresh approval;
5. impact escalation → fresh approval;
6. Security Gate change → fresh evaluation;
7. HOLD includes status, reason, next action, consequence/impact, required approval/evidence, options, and natural-language examples.

Actionable Hold CI 6 / `34778139986` first proved the integrated path. The branch was subsequently reconciled non-force with newer `main` work.

## Verified integration checkpoint
Checkpoint source head `2cfd26a1019ae4fa37bf4d9cc96abebcb9ae9bfd` was based on `main` `6107d5d91c6f3eae93fa4e9724b8668b9c0d63a7` and passed:
- Actionable Hold 11 / `34778365304` — success; both reference and real continuation-path regressions passed.
- Contracts 634 / `34778365175` — success.
- Trust-First 97 / `34778365197` — success.
- Full DevOS 556 / `34778365250` — success.
- Additional applicable gates: Current-Source Evidence 26 / `34778365249` and MCP Repository Create 23 / `34778365285` — success.

This is a historical verified checkpoint, not a moving-HEAD claim. The actual PR tip must receive its own fresh exact-head CI before merge readiness is asserted.

## Documentation
- `docs/ACTIONABLE-HOLDS-AND-SCOPED-APPROVAL.md` documents the operational UX and integrated path.
- `docs/ACTIONABLE-HOLD-IMPLEMENTATION-CHECKPOINT.md` records architecture, acceptance cases, and evidence boundary.

## Safety and evidence boundary
- `CONTINUE != BLANKET AUTHORIZATION`.
- `FULL APPROVAL = FULL WITHIN EXPLICIT SCOPE`.
- `INTERPRETATION != AUTHORIZATION`.
- `READY != EXECUTION`.
- stale HEAD, changed target/capability/impact, or changed Security Gate invalidates reuse as applicable.
- No live provider, destructive, production, deployment, credential/secret, permission, or database mutation is performed or claimed.
- PR #23 remains unmerged until separately authorized.
