# Project Remediation Planner v1

Project Remediation Planner consumes already-observed Project Fleet Watch evidence and produces a deterministic, priority-ordered remediation proposal.

It exists to answer: **which DevOS-managed-project problem should be handled first, and what exact safe action is required next?**

## Protocol

Input:

`DEVOS-PROJECT-FLEET-WATCH-v1`

Output:

`DEVOS-PROJECT-REMEDIATION-PLAN-v1`

## Priority model

1. `RESTORE_MANAGED_STATE` — priority 100 — a previously managed repository regressed.
2. `RESOLVE_MANAGEMENT_CONFLICT` — priority 95 — lifecycle returned HOLD/conflict.
3. `INVESTIGATE_BLOCKER` — priority 90 — lifecycle evidence is blocked or malformed.
4. `COMPLETE_ONBOARDING` — priority 80 — DevOS context exists but is incomplete.
5. `ONBOARD_PROJECT` — priority 70 — repository is accessible but un-managed.

Ties are deterministic by canonical repository identity.

## Safety boundaries

The planner is read-only. It does not onboard a repository, mutate a provider, grant authorization, deploy, publish, or change production readiness.

```text
REMEDIATION PLAN != AUTHORIZATION
REMEDIATION PRIORITY != EXECUTION ORDER AUTHORIZATION
FLEET ATTENTION != AUTOMATIC MUTATION
PLAN READY != SAFE TO APPLY
```

Every proposed remediation action is emitted with:

```text
requires_explicit_authorization = true
safe_apply = false
next_gate = P17_READINESS_AND_SCOPED_APPROVAL
```

The planner always fixes:

```text
authority = UNCHANGED
authorization = UNCHANGED
execution = NONE
mutation = NONE
provider_mutation = NONE
onboarding_authorized = false
production_ready = false
publication_authorized = false
deployment_authorized = false
```

## Fail-closed behavior

Malformed fleet protocol, duplicate repository identities, unsupported fleet states, malformed drift, or drift referring to unknown repositories returns `BLOCKED` and no actions.

## Completion criterion

The feature is complete only when the planner is deterministic, fail-closed, CLI-accessible, regression-tested on supported Python versions, included in the exact-source distribution, and documented without weakening lifecycle/authorization boundaries.
