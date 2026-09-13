# Actionable Hold + Scoped Approval Implementation Checkpoint

## Objective

Implement predictable human-language continuation when DevOS pauses for approval, evidence, security, freshness, or scope reasons, and wire it into the real governed continuation path without creating a competing authorization system.

## Rules

- `continue` resumes a currently valid bounded workflow when its next step remains inside a valid existing approval scope.
- `continue` never expands approval scope.
- `FULL APPROVAL` means full approval within the explicitly represented workflow scope, never blanket permission.
- Out-of-scope capability, target, impact, project, workflow, stale repository state, changed Security Gate state, or unproven approval provenance requires fresh approval/evidence.
- Every actionable hold explains status, reason, next action, consequence/impact, required approval/evidence, valid next choices, and natural-language examples.

## Reference layer

- Reference engine: `tools/devos-actionable-hold.py`
- Reference regression corpus: `tools/test-devos-actionable-hold.py`
- Normative contract: `core/actionable-hold-scoped-approval.md`
- Operational documentation: `docs/ACTIONABLE-HOLDS-AND-SCOPED-APPROVAL.md`

The reference engine remains side-effect-free.

## Real continuation-path integration

Integration entrypoint: `tools/devos-continuation-path.py`.

The integration composes the existing governed path rather than replacing it:

`P15 human-language interpreter -> P16 semantic plan -> scoped-approval validation -> P17 step readiness -> development-task controller`

Scoped approval does not bypass P17. A reusable approval is converted only into step-bound `ALREADY_GRANTED` evidence for the exact P17 step after project, workflow, capability, target, impact ceiling, repository HEAD, and Security Gate state are revalidated.

The controller may return an `EXECUTION_CANDIDATE`; the integration itself still reports `execution: NONE` and `mutation: NONE`.

Integration regression: `tools/test-actionable-hold-continuation-integration.py`.

The regression proves:

1. `continue` + valid scoped approval reaches real P17 READY and the controller without a duplicate approval prompt;
2. missing approval produces actionable HOLD;
3. stale repository HEAD invalidates approval;
4. target or capability change requires fresh approval;
5. impact escalation requires fresh approval;
6. Security Gate state change requires fresh evaluation;
7. HOLD contains status, reason, next action, consequence/impact, required approval/evidence, options, and natural-language examples.

CI: `.github/workflows/verify-actionable-hold.yml` runs both the reference regression and the real-path integration regression.

## Evidence boundary

This objective proves deterministic integration behavior through the repository's real P15/P16/P17/controller modules. It does not claim live-provider execution, production mutation, destructive mutation, deployment, credential/secret mutation, permission mutation, or database mutation.

## Safety

- `INTERPRETATION != AUTHORIZATION`
- `READY != EXECUTION`
- `CONTINUE != BLANKET AUTHORIZATION`
- `FULL APPROVAL = FULL WITHIN EXPLICIT SCOPE`
- `OLD APPROVAL != NEW APPROVAL` when scope/freshness/security changes
- no provider or repository mutation is performed by the continuation integration or its tests.
