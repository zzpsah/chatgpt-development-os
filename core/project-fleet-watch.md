# Project Fleet Watch v1

## Purpose

Managed Project Lifecycle v1 closes the state transition for one repository. Project Fleet Watch v1 closes the visibility gap across many repositories: a newly created or newly accessible repository must not silently disappear outside DevOS awareness when an authorized read-capable provider or deterministic fleet snapshot is available.

## Protocols

- Assessment: `DEVOS-PROJECT-FLEET-WATCH-v1`
- Snapshot: `DEVOS-PROJECT-FLEET-SNAPSHOT-v1`

The fleet layer reuses `DEVOS-MANAGED-PROJECT-LIFECYCLE-v1` for every active repository. It does not define a second management authority.

## Core invariants

```text
REPOSITORY ACCESSIBLE != DEVOS MANAGED
FLEET DISCOVERY != ONBOARDING AUTHORIZATION
FLEET ATTENTION != AUTOMATIC MUTATION
FLEET HEALTHY != APPLICATION VERIFIED
FLEET HEALTHY != PRODUCTION READY
```

Project Fleet Watch is read-only. It can discover, classify, compare and report. It cannot onboard a repository, edit project state, deploy, publish, grant credentials, change permissions, mutate databases, or manufacture authorization.

## Fleet states

Each non-archived repository is classified through Managed Project Lifecycle v1:

- `MANAGED` — minimum durable DevOS identity/context is present and consistent.
- `ONBOARDING_REQUIRED` — the repository is un/partially managed; development continuation remains held.
- `HOLD` — management identity/context conflicts or otherwise requires resolution.
- `BLOCKED` — observation/evidence is malformed or cannot be safely classified.

Archived repositories are reported as `ARCHIVED` and excluded from active fleet cleanliness.

Fleet verdicts:

- `HEALTHY` — every active repository is `MANAGED`.
- `ATTENTION` — at least one active repository requires onboarding and none are HOLD/BLOCKED.
- `HOLD` — at least one repository is HOLD/BLOCKED or a previously managed repository regressed.
- `EMPTY` — no active repositories are present.
- `BLOCKED` — the fleet snapshot itself is invalid/unusable.

Only repository-level `MANAGED` status can allow development continuation for that repository. A fleet verdict never broadens authority.

## Drift/watch semantics

When both previous and current valid snapshots are supplied, DevOS computes:

- `new_repositories`
- `removed_repositories`
- `new_unmanaged`
- `newly_managed`
- `management_regressions`
- `newly_attention_required`

A transition from `MANAGED` to any non-managed active state is a management regression and elevates the fleet to `HOLD`.

## Snapshot schema

A deterministic snapshot contains:

```json
{
  "protocol": "DEVOS-PROJECT-FLEET-SNAPSHOT-v1",
  "provider": "github",
  "observed_at": "2026-09-17T00:00:00+00:00",
  "repositories": [
    {
      "repository": "owner/repo",
      "default_branch": "main",
      "observed_head": "40-char-lowercase-git-sha",
      "archived": false,
      "files": ["AGENTS.md", ".ai/manifest.yaml"],
      "manifest": {
        "project_id": "repo",
        "managed_by": "development-os",
        "canonical_repository": "owner/repo",
        "devos_repository": "zzpsah/chatgpt-development-os"
      }
    }
  ]
}
```

Snapshot validation is fail-closed for duplicate repositories, malformed timestamps, invalid Git heads, invalid entry shapes, invalid file lists and malformed manifest evidence.

## GitHub discovery

`tools/devos-project-fleet.py --github-owner ...` provides a bounded read-only GitHub adapter. For `@me`, `GITHUB_TOKEN` is read from the environment and never printed or persisted. The adapter reads repository metadata, branch/head/tree evidence and `.ai/manifest.yaml`; it performs no POST/PATCH/PUT/DELETE request.

Provider capability is still not DevOS authorization. Discovery merely supplies observation evidence.

## CLI

```bash
python tools/devos.py project-fleet --snapshot fleet.json --json
python tools/devos.py project-fleet --snapshot current.json --previous previous.json --require-clean --json
python tools/devos.py project-fleet --github-owner @me --limit 100 --json
```

`--require-clean` fails closed unless every active repository is `MANAGED`.

## Security boundaries

Every assessment fixes:

```text
authority = UNCHANGED
authorization = UNCHANGED
external_mutation = NONE
production_ready = false
publication_authorized = false
deployment_authorized = false
```

A read-only provider execution may be reported as `READ_ONLY_PROVIDER`; this is evidence collection, not mutation authority.

## Acceptance

Project Fleet Watch v1 is accepted only when regression coverage proves:

- all-managed fleet → `HEALTHY`;
- newly discovered unmanaged repository → `ATTENTION` + `new_unmanaged`;
- managed → unmanaged regression → `HOLD`;
- successful onboarding reflected in later snapshot → `newly_managed`;
- conflicting management identity → `HOLD`;
- duplicate/malformed snapshot → `BLOCKED`;
- archived repository does not create false onboarding work;
- read-only GitHub discovery can produce a valid managed snapshot without leaking a token;
- `@me` discovery without credentials fails closed;
- no assessment path mutates a provider or creates authorization.
