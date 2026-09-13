# DevOS Actionable Hold & Scoped Approval Contract v1

## Purpose

Make conversational continuation predictable without weakening DevOS authorization.

When DevOS cannot safely proceed, it must explain the blocker and present valid next actions. A single explicit approval may cover the bounded workflow it actually authorizes, so the user is not repeatedly asked to approve every internal step.

## Product rule

> **Continue means resume the currently valid bounded workflow; it never silently expands that workflow's authority.**

## Actionable Hold

Whenever DevOS returns `NEEDS_APPROVAL`, `NEEDS_EVIDENCE`, `BLOCKED`, `HOLD`, or `STOP` for a human-originated request, the conversational response should expose, when safe to do so:

1. current status;
2. exact reason for stopping;
3. next intended action;
4. material consequence/impact;
5. required authorization/evidence;
6. one or more valid next choices;
7. natural-language examples the user can say next.

Example shape:

```text
STATUS: NEEDS_APPROVAL
NEXT: Merge PR #19 into main
WILL DO: Merge the verified PR and then run post-merge verification
IMPACT: HIGH — remote branch mutation
APPROVAL NEEDED: merge PR #19 into main for repository X at current HEAD
OPTIONS:
  1. "merge it"
  2. "run checks first"
  3. "show the plan"
  4. "hold"
```

The response must not present an unsafe action as an executable option.

## Scoped Approval

An explicit approval can authorize multiple internal steps when the user clearly approves a bounded workflow.

The approval record must bind, at minimum:

- project/repository identity;
- workflow identity;
- allowed operation/capability set;
- target(s), such as PR/branch/path where relevant;
- repository state reference (exact HEAD or equivalent freshness anchor) when the workflow depends on repository state;
- impact ceiling;
- security-gate requirement/status where applicable;
- issuance time/version identifier.

`FULL APPROVAL` means **full approval within the explicitly represented scope**, not unrestricted permission.

## Continue reuse rule

A `continue`/resume instruction may reuse a valid approval without a repeated prompt when ALL of the following remain true:

1. same project/repository identity;
2. same workflow identity;
3. next operation is within the approved capability/target set;
4. current impact does not exceed the approval ceiling;
5. repository freshness requirements remain satisfied;
6. required Security Gate state remains valid;
7. no new security/authorization condition has appeared;
8. no material scope expansion has occurred.

If all conditions hold, DevOS should continue automatically rather than ask for duplicate approval.

## Approval expansion rule

Fresh approval is required when any of the following occurs:

- new capability outside the approved set;
- new target/repository/branch/path;
- higher impact tier;
- production/destructive scope appears;
- repository state becomes stale relative to approval;
- Security Gate becomes newly required or ceases to be satisfied;
- material interpretation changes the workflow;
- approval provenance/validity cannot be established.

## Authorization boundary

Natural-language interpretation is not authorization.

Examples such as `continue`, `yes`, `ok`, `do it`, `full approval`, urgency, or profanity cannot broaden a previous approval beyond its explicit scope.

## Freshness

Approval is not permanently reusable. If the workflow requires a repository-state binding and the repository changes after approval, DevOS must hold and require re-planning/re-approval as appropriate.

## Persistence

The authoritative approval envelope must be repository/provider/workflow evidence, not only chat memory. The durable representation must contain enough scope metadata for a fresh AI/account to determine whether a prior approval is reusable.

## No approval laundering

The following are not equivalent:

```text
FULL APPROVAL for workflow W
!=
FULL PERMISSION for all repository actions
```

and:

```text
Provider write credential
!=
DevOS approval
```

## Safety invariants

- `PLAN != EXECUTION`
- `READY != EXECUTION`
- `INTERPRETATION != AUTHORIZATION`
- `OLD APPROVAL != NEW APPROVAL` when freshness/scope has changed
- `CONTINUE != BLANKET AUTHORIZATION`
- `FULL APPROVAL = FULL WITHIN EXPLICIT SCOPE`
- `CHAT MEMORY != SOURCE OF TRUTH`
- `PROVIDER RESPONSE != COMPLETION PROOF`
- `RECOVERY != AUTOMATIC MUTATION REPLAY`

## Acceptance

The reference implementation must demonstrate:

- a blocked high-impact step produces actionable choices;
- a scoped full approval permits later internal steps in the same workflow without another approval prompt;
- a new capability/target/impact requires fresh approval;
- a changed repository HEAD invalidates a freshness-bound approval;
- a new AI can recover the approval scope from durable evidence;
- conversational wording never silently expands authority.
