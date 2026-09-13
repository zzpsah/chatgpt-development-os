# DevOS Universal Project Onboarding Contract v1

## Purpose

Make DevOS portable across **AI vendors, models, accounts, sessions, coding agents, machines, and Git providers** by ensuring every managed project carries its own durable AI-development context.

## Product invariant

> The AI is replaceable. The project's authoritative state and governance are durable.

The target continuation path is:

`AI A + Account A → repository → AI B + Account B → correct recovery → safe continuation`

No AI account, model, chat, vendor memory, or private session may be the authoritative project state.

## Scope

Onboarding supports:

1. **Existing repositories/projects** — add only missing DevOS infrastructure.
2. **New projects** — use the DevOS project template or initializer so standard context exists from the first commit.
3. **Local projects not yet on GitHub** — initialize repository-local DevOS context without requiring a cloud connection.
4. **GitHub repositories** — optionally add the reusable context-sync caller so repository-derived evidence can be synchronized by GitHub Actions after pushes.

## Preservation rule

Onboarding is infrastructure establishment, not permission to overwrite application code or existing semantic project knowledge.

- Existing `.ai/*` files are preserved by default.
- Existing `AGENTS.md` is preserved by default.
- Existing source files are never replaced by onboarding.
- Existing project workflows are never overwritten; the DevOS caller is added only when absent.
- A pre-existing incompatible/canonical identity is reported as `HOLD` rather than silently rewritten.

## Execution model

The portable onboarding command is:

```text
python tools/devos-onboard.py --path <project> [--apply]
```

Default behavior is **plan/inspect only**. `--apply` is required before creating missing infrastructure.

The command must be idempotent:

`onboard(onboard(project)) == onboard(project)`

## Minimum managed context

A successfully onboarded repository has, at minimum:

- `AGENTS.md`
- `.ai/manifest.yaml`
- `.ai/PROJECT.md`
- `.ai/CURRENT-STATE.md`
- `.ai/ARCHITECTURE.md`
- `.ai/DECISIONS.md`
- `.ai/TASKS.md`
- `.ai/CHANGELOG.md`
- `.ai/STATE-INDEX.md`
- `.ai/SESSIONS/session-template.md`

A GitHub-managed repository may additionally receive:

- `.github/workflows/context-sync.yml`

## Evidence boundary

Successful onboarding proves only that the required DevOS infrastructure was established or already present.

It does **not** prove:

- application correctness;
- security correctness;
- deployment correctness;
- test success;
- production readiness;
- authorization to perform project work.

## New-project policy

For future projects, the preferred path is:

`Create project → initialize DevOS context before substantial work → first commit includes context → all AIs can bootstrap from repository evidence.`

The `templates/project` template should remain aligned with the onboarding contract.

## Automatic-onboarding policy

DevOS may provide automation hooks for repositories that an explicit local worker, GitHub App, organization workflow, or similar authorized integration can observe.

DevOS must **not** claim that an ordinary repository can silently modify every future GitHub repository merely because the DevOS repository exists.

Automatic onboarding of arbitrary new remote repositories requires an explicitly installed integration with appropriate permissions and must preserve the same least-privilege and authorization boundaries.

## Cross-AI acceptance

A managed project is portable when a fresh AI can:

1. discover the DevOS bootstrap path;
2. read the durable project state;
3. inspect source/Git before making material claims;
4. distinguish verified evidence from unknowns;
5. recover current work without previous chat memory;
6. preserve authorization boundaries.

## Safety invariants

- `PLAN != EXECUTION`
- `READY != EXECUTION`
- `INTERPRETATION != AUTHORIZATION`
- `OLD APPROVAL != NEW APPROVAL`
- `CHAT MEMORY != SOURCE OF TRUTH`
- onboarding success != feature success
- diagnostics != authorization
- onboarding must fail closed on incompatible identity evidence
