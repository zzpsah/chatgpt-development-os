# Actionable Hold + Scoped Approval Implementation Checkpoint

## Objective

Implement predictable human-language continuation when DevOS pauses for approval, evidence, security, freshness, or scope reasons.

## Rules

- `continue` resumes a currently valid bounded workflow when its next step remains inside a valid existing approval scope.
- `continue` never expands approval scope.
- `FULL APPROVAL` means full approval within the explicitly represented workflow scope, never blanket permission.
- Out-of-scope capability, target, impact, project, workflow, stale repository state, changed Security Gate state, or unproven approval provenance requires fresh approval/evidence.
- Every actionable hold should explain status, reason, next action, consequence/impact, required approval/evidence, and valid next choices.
- The response should give natural-language examples so users do not need to learn internal commands.

## Implementation

Reference engine: `tools/devos-actionable-hold.py`

Regression corpus: `tools/test-devos-actionable-hold.py`

Normative contract: `core/actionable-hold-scoped-approval.md`

Operational documentation: `docs/ACTIONABLE-HOLDS-AND-SCOPED-APPROVAL.md`

CI: `.github/workflows/verify-actionable-hold.yml`

The reference engine is side-effect-free. Integration into the existing P15/P17/controller continuation path is a subsequent bounded integration task.

## Evidence boundary

This checkpoint establishes deterministic semantics and regression coverage. It does not by itself prove that every existing runtime/controller continuation path has been wired to the new semantics.

## Safety

No provider mutation, repository mutation, production operation, credential/secret change, or authorization escalation is performed by this feature.
