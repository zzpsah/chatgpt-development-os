# DevOS Actionable Holds & Scoped Approval UX

## Why this exists

DevOS is intended to feel simple in natural language while keeping engineering authority explicit and bounded. A user may say `continue`, `ok`, `do it`, or `full approval` without knowing internal commands.

When DevOS cannot proceed safely, it should not leave the user guessing what to say next.

## Actionable HOLD response

For a blocked or paused human-originated operation, DevOS communicates:

```text
STATUS
REASON
NEXT ACTION
WHAT WILL HAPPEN
IMPACT / CONSEQUENCE
APPROVAL OR EVIDENCE REQUIRED
OPTIONS
EXAMPLE WORDING
```

The examples are natural-language guidance, not a hidden command language requirement.

## Scoped full approval

A user may provide explicit approval for a whole bounded workflow rather than approving every internal step individually.

DevOS records approval scope containing project/repository, workflow, capabilities, targets, impact ceiling, repository freshness anchor where applicable, Security Gate state where applicable, and approval identifier/provenance.

`FULL APPROVAL` means full approval within that explicit scope, never unrestricted permission.

## Real continuation flow

The integrated path is:

```text
human "continue"
  -> P15 human-language interpretation
  -> existing active project/workflow objective
  -> P16 semantic plan
  -> validate scoped approval against exact next capability/target/impact/HEAD/Security Gate
  -> P17 step readiness
  -> development-task controller
```

Implementation: `tools/devos-continuation-path.py`.

Regression: `tools/test-actionable-hold-continuation-integration.py`.

The scoped-approval layer does not replace P17. Only after approval reuse is proven valid does it supply step-bound `ALREADY_GRANTED` authorization evidence to the existing P17 evaluator. P17 still independently checks plan validity, exact repository freshness, dependencies, capability, authorization, Security Gate, and verification path.

The development controller still decides whether the step is an `EXECUTION_CANDIDATE`. The continuation integration itself never executes or mutates state.

## Continuation semantics

```text
continue + valid scoped approval + fresh P17/controller gates = continue
continue + missing approval = actionable HOLD
continue + stale HEAD = actionable HOLD
continue + changed target/capability = actionable HOLD
continue + higher impact = actionable HOLD
continue + changed Security Gate state = actionable HOLD / fresh evaluation
```

No repetitive approval prompt is needed while the exact next internal step remains inside the same valid scope.

## When approval is requested again

Fresh approval is required when target/repository/branch/path changes, capability changes, impact increases, production/destructive scope appears, repository freshness changes, Security Gate state changes, material workflow scope changes, approval provenance cannot be recovered, or any new capability lies outside the recorded approval.

## HOLD fields

An actionable HOLD produced by the integrated continuation path carries:

- `status`;
- `reason`;
- `next_action`;
- `consequence` / `impact`;
- `required_approval_or_evidence`;
- `options`;
- `natural_language_examples`;
- validation reasons sufficient to explain which scope/freshness/security condition failed.

Example wording may include:

```text
"approve pr.merge on PR#23->main"
"show me the updated plan"
"run the checks first"
"hold"
```

## Freshness semantics

When an approval is tied to repository state:

```text
approved HEAD = A
current HEAD  = B
```

DevOS must not silently continue with the old approval. It holds and requires inspection/re-plan/re-approval as appropriate.

## Universal AI/account portability

Approval scope must be recoverable as project/provider/workflow evidence rather than existing only in one AI account's private conversation.

```text
AI A + Account A
  -> scoped approval + repository state
  -> repository
  -> AI B + Account B
  -> recover approval scope
  -> continue only if scope is still valid
```

## Security boundary

A provider credential does not replace DevOS approval. A plan does not replace approval. P17 READY does not replace approval. A prior approval for another repository, target, or capability does not replace exact approval.

## Safety invariants

- `PLAN != EXECUTION`
- `READY != EXECUTION`
- `INTERPRETATION != AUTHORIZATION`
- `CONTINUE != BLANKET AUTHORIZATION`
- `FULL APPROVAL = FULL WITHIN EXPLICIT SCOPE`
- `OLD APPROVAL != NEW APPROVAL` when scope/freshness/security changes
- `CHAT MEMORY != SOURCE OF TRUTH`
- `PROVIDER CREDENTIAL != DEVOS AUTHORIZATION`
- `PROVIDER RESPONSE != COMPLETION PROOF`
- `RECOVERY != AUTOMATIC MUTATION REPLAY`

## Verification

Reference regression:

`python tools/test-devos-actionable-hold.py`

Integrated real-path regression:

`python tools/test-actionable-hold-continuation-integration.py`

CI gate: `.github/workflows/verify-actionable-hold.yml`.

No live/destructive/provider mutation is required by either regression.
