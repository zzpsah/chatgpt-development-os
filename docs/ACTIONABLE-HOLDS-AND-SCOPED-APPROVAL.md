# DevOS Actionable Holds & Scoped Approval UX

## Why this exists

DevOS is intended to feel simple in natural language while keeping engineering authority explicit and bounded. A user may say `continue`, `ok`, `do it`, or `full approval` without knowing internal commands.

When DevOS cannot proceed safely, it should not leave the user guessing what to say next.

## Actionable HOLD response

For a blocked or paused human-originated operation, DevOS should communicate:

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

Example:

```text
STATUS: NEEDS_APPROVAL
NEXT: Merge PR #19 into main
WHAT WILL HAPPEN: The verified PR will be merged and post-merge CI will run.
IMPACT: HIGH — remote branch mutation
APPROVAL NEEDED: PR #19 → main in the current repository state

Choose:
1. "merge it"
2. "run the checks first"
3. "show me the plan"
4. "hold"
```

The examples are natural-language guidance, not a hidden command language requirement.

## Scoped full approval

A user may provide explicit approval for a whole bounded workflow rather than approving every internal step individually.

Example:

```text
Full approval: complete the approved PR #19 merge workflow and all required verification.
```

DevOS records an approval scope containing:

- project/repository;
- workflow;
- capabilities;
- targets;
- impact ceiling;
- repository freshness anchor where applicable;
- Security Gate state where applicable;
- approval identifier/provenance.

Then:

```text
continue
→ recover workflow
→ validate current approval scope
→ execute covered internal step
```

No repetitive approval prompt is needed while the next internal step remains inside the same valid scope.

## When approval is requested again

Fresh approval is required when:

- target repository/branch/path changes;
- capability changes;
- impact tier increases;
- production/destructive scope appears;
- the repository freshness anchor changes;
- the Security Gate condition changes;
- material workflow scope changes;
- approval provenance cannot be recovered;
- a new capability not listed in the original approval is required.

Example:

```text
Existing approval: PR #19 merge
Next action: delete remote branch
→ NEEDS_APPROVAL
```

## Continuation semantics

`continue` is not blanket authorization.

It means:

> Resume the currently valid bounded workflow using existing valid authorization when the next step is covered by that authorization.

Therefore:

```text
continue + valid scoped approval = continue
continue + new/out-of-scope operation = actionable HOLD
```

## Freshness semantics

When an approval is tied to repository state:

```text
approved HEAD = A
current HEAD  = B
```

DevOS must not silently continue with the old approval. It should hold, explain that the state changed, and offer:

- inspect changes;
- re-plan/reconcile;
- re-approve the updated workflow;
- hold.

## Universal AI/account portability

Approval scope must be recoverable as project/provider/workflow evidence rather than existing only in one AI account's private conversation.

The goal remains:

```text
AI A + Account A
  ↓
scoped approval + repository state
  ↓
AI B + Account B
  ↓
recover approval scope
  ↓
continue only if scope is still valid
```

## Security boundary

A provider credential does not replace DevOS approval.

A plan does not replace approval.

P17 READY does not replace approval.

A prior approval for another repository or operation does not replace exact approval.

`FULL APPROVAL` never means unrestricted access.

## Safety invariants

- `PLAN != EXECUTION`
- `READY != EXECUTION`
- `INTERPRETATION != AUTHORIZATION`
- `CONTINUE != BLANKET AUTHORIZATION`
- `FULL APPROVAL = FULL WITHIN EXPLICIT SCOPE`
- `OLD APPROVAL != NEW APPROVAL` when scope/freshness changes
- `CHAT MEMORY != SOURCE OF TRUTH`
- `PROVIDER CREDENTIAL != DEVOS AUTHORIZATION`
- `PROVIDER RESPONSE != COMPLETION PROOF`
- `RECOVERY != AUTOMATIC MUTATION REPLAY`

## Implementation status

Reference semantics are implemented in:

`tools/devos-actionable-hold.py`

Regression corpus:

`tools/test-devos-actionable-hold.py`

The reference engine is side-effect free: it evaluates approval reuse and produces structured actionable-hold data; it does not execute repository/provider mutations.
