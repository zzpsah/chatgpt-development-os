# Managed Project Lifecycle v1

## Purpose

DevOS must not lose control of a project merely because a repository was created or discovered outside the exact onboarding step.

Protocol: `DEVOS-MANAGED-PROJECT-LIFECYCLE-v1`.

Core invariant:

> **A repository is not a DevOS-managed project until repository-local management identity and minimum durable context are verified.**

Therefore:

```text
REPOSITORY EXISTS != DEVOS MANAGED
REPOSITORY CREATED != ONBOARDED
REPOSITORY DISCOVERED != SAFE TO CONTINUE
```

## Lifecycle

Every repository entering a DevOS development flow must pass:

```text
CREATE or DISCOVER
      ↓
FRESH REPOSITORY READBACK
      ↓
MANAGED PROJECT LIFECYCLE CHECK
      ↓
MANAGED ?
  ├─ YES → recover durable state → continue
  ├─ NO  → onboarding required → verify readback → continue only if MANAGED
  └─ CONFLICT → HOLD
```

The lifecycle check applies to repositories created by DevOS and repositories discovered later through a provider, local workspace, GitHub App, connector, or other authorized inventory source.

## Managed state

`MANAGED` requires all of the following:

- `AGENTS.md` exists;
- `.ai/manifest.yaml` exists;
- the manifest declares `managed_by: development-os`;
- manifest repository identity does not conflict with the observed repository;
- manifest DevOS authority does not conflict with `zzpsah/chatgpt-development-os`;
- a `project_id` exists;
- the minimum portable DevOS context files created by `tools/devos-onboard.py` exist.

Only `MANAGED` sets:

```text
development_continuation_allowed = true
```

## Unmanaged and partial repositories

A repository with no DevOS manifest is `UNMANAGED` and returns `ONBOARDING_REQUIRED`.

A repository with a compatible DevOS manifest but missing required durable context is `PARTIAL` and also returns `ONBOARDING_REQUIRED`.

Both states force:

```text
development_continuation_allowed = false
```

The next action is onboarding, not feature development.

## Conflict state

If `managed_by`, canonical repository identity, or DevOS authority conflicts with observed evidence, the lifecycle returns `HOLD`.

DevOS must never overwrite another management framework or silently repair an identity conflict.

## Local enforcement

```bash
python tools/devos.py project-lifecycle --path <project> --require-managed --json
```

Read-only classification is the default.

Authorized local onboarding:

```bash
python tools/devos.py project-lifecycle \
  --path <project> \
  --apply \
  --authorization EXPLICIT \
  --require-managed \
  --json
```

Apply mode delegates to the preservation-first universal onboarding implementation and then performs a fresh managed-state readback. An onboarding mutation that does not verify as `MANAGED` returns HOLD.

## Provider / remote enforcement

A provider/controller can supply a read-only snapshot using protocol:

`DEVOS-REPOSITORY-DISCOVERY-SNAPSHOT-v1`

The snapshot binds:

- repository identity;
- default branch;
- observed Git head when available;
- observed file paths;
- parsed DevOS manifest or null.

Example:

```json
{
  "protocol": "DEVOS-REPOSITORY-DISCOVERY-SNAPSHOT-v1",
  "repository": "owner/project",
  "default_branch": "main",
  "observed_head": "0123456789012345678901234567890123456789",
  "files": ["README.md"],
  "manifest": null
}
```

Run:

```bash
python tools/devos.py project-lifecycle --snapshot snapshot.json --require-managed --json
```

Remote snapshot evaluation is read-only. The repository-side tool does not manufacture remote provider mutation capability. A governed provider onboarding path must perform any remote writes and then provide fresh readback.

## Repository creation postcondition

`repository.create` is not complete as a managed-project lifecycle merely because provider creation succeeded.

Every repository creation plan/result carries the postcondition:

```text
managed_project_required = true
development_continuation_allowed = false
required_next_capability = project.onboard
```

After fresh repository readback, the lifecycle check must verify `MANAGED` before the first development action.

## Discovery rule

Any accessible repository selected as a DevOS project must be checked even when DevOS did not create it.

A discovery source may be a configured local root, connected provider inventory, GitHub App installation, connector, or explicit repository selection. Discovery itself grants no mutation authority.

## Permanent boundaries

```text
authority = UNCHANGED
authorization = UNCHANGED
production_ready = false
```

- onboarding mutation still requires explicit authorization or an already-authorized enclosing workflow;
- provider capability is not authorization;
- an unmanaged repository cannot silently continue development;
- onboarding does not prove the application correct;
- onboarding does not authorize deployment, credentials, databases, permissions, destructive operations, or production changes;
- uncertain mutation is never blindly replayed.

## Acceptance

Managed Project Lifecycle v1 is complete when:

- local unmanaged projects are detected;
- provider snapshots classify unmanaged, partial, managed, conflict, and malformed states deterministically;
- local apply requires explicit authorization;
- successful apply is followed by fresh managed-state readback;
- second apply is idempotent;
- repository creation advertises onboarding as a mandatory postcondition;
- the DevOS CLI exposes the lifecycle gate;
- CI proves development continuation is true only for `MANAGED`;
- durable documentation records the lifecycle invariant.
