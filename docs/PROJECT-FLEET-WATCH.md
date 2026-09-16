# Project Fleet Watch

DevOS 0.22.0 adds a read-only fleet view across many repositories so a newly created or newly accessible repository cannot silently remain outside DevOS management awareness.

## Why this exists

Managed Project Lifecycle v1 answers one question for one repository: is this repository durably managed by DevOS?

Project Fleet Watch answers the account/workspace-level question: which repositories are managed, which require onboarding, which have a management conflict, and what changed since the last observation?

## Commands

Assess a deterministic snapshot:

```bash
python tools/devos.py project-fleet --snapshot fleet.json --json
```

Compare current and previous observations:

```bash
python tools/devos.py project-fleet \
  --snapshot current.json \
  --previous previous.json \
  --require-clean \
  --json
```

Perform bounded read-only GitHub discovery:

```bash
GITHUB_TOKEN=... python tools/devos.py project-fleet --github-owner @me --limit 100 --json
```

The token is read from the environment and is never printed or persisted by the tool. `@me` discovery requires a token because it represents authenticated accessible repositories. Named public GitHub users can be inspected through the public read API where available.

## Fleet verdicts

- `HEALTHY` — every active repository is DevOS `MANAGED`.
- `ATTENTION` — at least one active repository requires onboarding.
- `HOLD` — a repository has conflicting/blocked management evidence, or a previously managed repository regressed.
- `EMPTY` — only archived/no active repositories were observed.
- `BLOCKED` — the fleet snapshot itself cannot be trusted/parsed.

Archived repositories are visible but excluded from active fleet cleanliness.

## Drift detection

Supplying `--previous` enables explicit detection of:

- new repositories;
- new unmanaged repositories;
- newly managed repositories;
- removed repositories;
- management regressions;
- newly attention-required repositories.

A managed-to-unmanaged regression forces a fleet `HOLD`.

## Important boundary

Fleet Watch does not auto-onboard anything. It only discovers and classifies. A repository that requires onboarding must still pass Managed Project Lifecycle and its explicit authorization rules.

```text
FLEET DISCOVERY != ONBOARDING AUTHORIZATION
FLEET ATTENTION != AUTOMATIC MUTATION
FLEET HEALTHY != APPLICATION VERIFIED
FLEET HEALTHY != PRODUCTION READY
```

Provider reads are evidence collection only. They do not grant execution authority, mutation permission, deployment authority, publication authority, or production readiness.

## Recommended operational pattern

1. Take a fleet snapshot after repository creation/discovery events or on a scheduled authorized worker.
2. Compare with the previous snapshot.
3. Treat `new_unmanaged` and `management_regressions` as actionable control-plane signals.
4. Onboard only the intended repositories through the existing governed lifecycle.
5. Re-run Fleet Watch and require a clean/managed readback before assuming the fleet is healthy.

An organization-wide or scheduled watcher requires a separately authorized GitHub App/token/worker with appropriate read scope. The public DevOS repository itself does not gain access to arbitrary repositories.
