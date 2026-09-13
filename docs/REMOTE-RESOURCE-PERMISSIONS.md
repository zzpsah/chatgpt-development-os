# DevOS Remote Resource Permissions

DevOS treats remote repository and branch mutations as distinct capabilities. A connected AI may have provider write access without having authority to perform a specific DevOS operation.

## Capabilities

| Capability | Default impact | Approval scope |
|---|---|---|
| `repository.create` | HIGH | exact provider + owner + repository + project |
| `repository.delete` | DESTRUCTIVE | exact provider + owner + repository + project |
| `branch.create` | LOW | exact repository + branch + source ref |
| `branch.update` | HIGH | exact repository + branch + target SHA |
| `branch.force_update` | DESTRUCTIVE | exact repository + branch + target SHA + explicit force approval |
| `branch.delete` | DESTRUCTIVE | exact repository + branch |

Default-branch, protected, release, or production targets may require a higher project-specific impact level.

## Permission flow

```text
Human request
  ↓
P15 interpretation
  ↓
P16 plan
  ↓
P17 readiness
  ↓
provider capability discovery
  ↓
exact DevOS authorization
  ↓
Security Gate when applicable
  ↓
bounded execution
  ↓
fresh provider readback
  ↓
VERIFIED / HOLD
```

Provider credentials and connector write access are not DevOS authorization.

## Full approval

`FULL APPROVAL` is reusable only within the exact workflow, capability, target, impact ceiling, freshness, and security scope that was approved. It does not automatically authorize:

- another repository;
- another branch;
- repository deletion after repository creation/update approval;
- branch deletion after branch creation/update approval;
- force-update after ordinary branch update approval;
- production or destructive operations.

## Consequence disclosure

Before a high-impact or destructive remote action, the user-facing hold/approval request must explain what will change and the material consequence.

Examples:

- repository creation creates a new provider-side repository and establishes its initial ownership/visibility state;
- repository deletion can make hosted repository data/history/settings unavailable, subject to provider recovery policy;
- branch update changes the canonical remote ref;
- force-update can rewrite reachable branch history;
- branch deletion removes the named remote branch and may require recovery from another ref or provider retention.

## Uncertainty

After a timeout, connection loss, or ambiguous provider response, DevOS must HOLD and reconcile current state before any new attempt. It must never blind-retry a remote mutation.

## Provider capability unavailability

When the active AI/provider integration does not expose a required capability, DevOS must report the capability limitation (for repository creation, `NEEDS_EXTERNAL_REPO_CREATION`) rather than claim execution.

## Invariants

`PLAN != EXECUTION`

`READY != EXECUTION`

`INTERPRETATION != AUTHORIZATION`

`FULL APPROVAL != BLANKET PERMISSION`

`REPOSITORY DELETE != REPOSITORY CREATE`

`BRANCH DELETE != BRANCH CREATE`

`NORMAL BRANCH UPDATE != FORCE UPDATE`

`PROVIDER CREDENTIAL != DEVOS AUTHORIZATION`

`PROVIDER RESPONSE != COMPLETION PROOF`

`UNCERTAIN MUTATION != AUTOMATIC RETRY`
