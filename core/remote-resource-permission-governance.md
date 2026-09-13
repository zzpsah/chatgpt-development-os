# DevOS Remote Resource Permission Governance v1

## Purpose

Define explicit, provider-independent authorization boundaries for remote repository and branch operations. This contract prevents a connected AI, credential, or provider permission from being treated as blanket authority.

## Capability model

Remote mutations are represented as distinct capabilities:

- `repository.create` — create a new repository/project container; HIGH impact.
- `repository.delete` — delete a repository/project container; DESTRUCTIVE impact.
- `branch.create` — create a branch/ref; LOW or HIGH depending on target policy.
- `branch.update` — move a branch/ref to a specific commit; HIGH when a protected/default/production branch is affected.
- `branch.delete` — delete a branch/ref; HIGH and DESTRUCTIVE for protected/important branches.
- `file.create` / `file.update` / `file.delete` — repository content mutations governed separately.
- `pr.merge` — merge a pull request; HIGH impact.

Provider credentials or API write permission do not authorize any capability by themselves.

## Authorization requirements

For any remote mutation, authorization must bind at minimum:

- exact provider;
- exact owner/namespace;
- exact repository when applicable;
- exact branch/ref or resource when applicable;
- exact capability;
- approved target(s);
- impact ceiling;
- workflow identity;
- project identity;
- freshness/state anchor when relevant;
- authorization identifier/provenance.

`FULL APPROVAL` means full approval only within this explicit scope. It is never blanket permission for all repositories, branches, or operations.

## Repository creation

`repository.create` requires explicit authorization for the exact owner/namespace and repository name. A generic instruction such as `create a project` may be interpreted by P15, but interpretation alone cannot authorize creation.

Consequence disclosure should state that a new remote repository will be created and that provider-side resources may incur ownership, visibility, policy, or operational consequences.

If the active host/provider integration does not expose repository creation, DevOS must return `NEEDS_EXTERNAL_REPO_CREATION` and must not simulate completion.

## Repository deletion

`repository.delete` is DESTRUCTIVE and requires a fresh explicit authorization bound to the exact repository. It must never be inferred from `clean up`, `remove it`, `delete the project`, or a previous repository-create/update approval.

Before deletion, DevOS must disclose the consequence: the repository and its hosted history/settings may become unavailable or subject to provider recovery policies. Where the provider offers reversible/archive alternatives, those may be offered as safer options but must not be executed without appropriate authorization.

A delete operation must not proceed when target identity, ownership, or authorization provenance is uncertain.

## Branch creation

`branch.create` may be lower impact when creating a new non-protected feature branch from an exact source ref/SHA. The authorization must still bind the repository and resulting branch name.

Creating a protected/default/production branch or changing branch policy requires the higher applicable impact classification.

## Branch update

`branch.update` is not equivalent to ordinary local planning. Moving a remote ref changes repository state. For `main`, default, protected, release, or production branches, classify as HIGH or higher according to the project's policy.

Force updates are separately classified as DESTRUCTIVE/HIGH-risk and require a distinct capability/approval. A normal approval for `branch.update` must not authorize a force update.

## Branch deletion

`branch.delete` requires exact repository + branch binding and explicit authorization. Protected/default/production branch deletion must be blocked unless the project policy explicitly allows it and the provider confirms the relevant protection requirements are satisfied.

Branch deletion must never be inferred from repository deletion approval.

## Continue / scoped approval

`continue` may reuse a valid prior approval only when the next operation remains inside the exact previously approved capability, targets, workflow, impact ceiling, freshness, and security conditions.

Examples:

```text
Approval: branch.create on repo X for feature/foo
Next: branch.delete feature/foo
→ fresh approval required
```

```text
Approval: repository.delete for repo X
Next: repository.create repo Y
→ fresh approval required
```

```text
Approval: branch.update on feature/foo
Next: force-update main
→ fresh approval required
```

## Actionable HOLD

When a remote mutation cannot proceed, DevOS must return a human-actionable HOLD containing:

- status;
- exact reason;
- next intended action;
- what will happen;
- consequence/impact;
- exact approval or evidence required;
- valid safe alternatives;
- natural-language examples of what the user may say next.

Unsafe operations must not be presented as immediately executable choices.

## Exactly-once and uncertainty

For provider operations that may have been sent but whose completion is uncertain:

```text
HOLD
→ reconcile/read
→ determine actual state
→ do not blindly replay
```

A timeout, connection loss, or ambiguous provider response never creates permission for a second mutation request.

## Host/provider capability boundary

The host adapter must distinguish:

```text
host tool availability
!=
provider capability
!=
DevOS authorization
!=
P17 readiness
!=
execution
```

A capability unavailable in the current host/provider integration must be surfaced explicitly rather than silently delegated or simulated.

## Safety invariants

- `PLAN != EXECUTION`
- `READY != EXECUTION`
- `INTERPRETATION != AUTHORIZATION`
- `FULL APPROVAL != BLANKET PERMISSION`
- `PROVIDER CREDENTIAL != DEVOS AUTHORIZATION`
- `REPOSITORY DELETE != REPOSITORY CREATE`
- `BRANCH DELETE != BRANCH CREATE`
- `NORMAL BRANCH UPDATE != FORCE UPDATE`
- `PROVIDER RESPONSE != COMPLETION PROOF`
- `UNCERTAIN MUTATION != AUTOMATIC RETRY`
- `CHAT MEMORY != SOURCE OF TRUTH`
