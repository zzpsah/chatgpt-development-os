# Project Auto-Onboarding

Development OS can make a repository managed with a small, safe onboarding step. The onboarding system is intentionally **idempotent, repository-local, vendor-neutral, account-neutral, and preservation-first**.

## Core product goal

DevOS is a Development Operating System for AI-assisted software development, not a ChatGPT-only workflow.

The project must remain portable across:

- AI vendors;
- AI models;
- AI accounts;
- coding agents;
- sessions/chats;
- machines;
- Git providers, where adapters exist.

Core continuation invariant:

```text
AI A + Account A
      ↓
 repository-local DevOS state
      ↓
AI B + Account B
      ↓
 correct recovery
      ↓
 safe continuation
```

The repository and its durable records remain authoritative. No AI account, model, chat, vendor memory, or private session is authoritative project state.

## Existing-repository flow

```text
Detect candidate
    ↓
Resolve project root
    ↓
Inspect Git / existing AGENTS.md / .ai/
    ↓
Check DevOS identity compatibility
    ↓
PLAN missing infrastructure (read-only)
    ↓
Explicit onboarding apply
    ↓
Preserve existing semantic context
    ↓
Create only missing DevOS infrastructure
    ↓
Optionally add GitHub context-sync caller when missing
    ↓
Run bootstrap / health validation
    ↓
Commit + push when remote portability is desired
```

## Portable onboarding command

The canonical cross-platform onboarding entrypoint is:

```bash
python tools/devos-onboard.py --path <project>
```

This is **read-only plan mode** by default.

To create missing infrastructure:

```bash
python tools/devos-onboard.py --path <project> --apply
```

Machine-readable output:

```bash
python tools/devos-onboard.py --path <project> --json
```

The existing PowerShell wrapper remains supported for Windows workflows:

```powershell
.\tools\onboard-project.ps1 -Path 'D:\Projects\MyApp'
```

## What onboarding creates

A successfully onboarded project receives, when missing:

```text
AGENTS.md
.ai/manifest.yaml
.ai/PROJECT.md
.ai/CURRENT-STATE.md
.ai/ARCHITECTURE.md
.ai/DECISIONS.md
.ai/TASKS.md
.ai/CHANGELOG.md
.ai/STATE-INDEX.md
.ai/SESSIONS/session-template.md
```

For Git repositories, onboarding may also add:

```text
.github/workflows/context-sync.yml
```

The reusable context synchronizer remains in the DevOS repository and is called by the project repository workflow.

## Preservation rule

Existing project files and existing semantic `.ai/` files are preserved by default.

Onboarding never:

- replaces application source;
- overwrites existing semantic project decisions;
- replaces an existing `AGENTS.md`;
- silently replaces another framework's context;
- claims that generated placeholders describe the actual architecture or requirements.

If an existing manifest identifies another framework as the managed authority, onboarding returns `HOLD` rather than overwriting it.

## Existing projects

For a project that already exists:

1. Run plan mode.
2. Review the paths proposed for creation/preservation.
3. Run `--apply` only when the project is intended to be managed by DevOS.
4. Validate bootstrap/health state.
5. Commit and push the onboarding infrastructure if remote portability is required.

This creates a durable handoff point for future AI sessions/accounts.

## New projects

For new projects, the preferred path is:

```text
Create project
   ↓
DevOS template OR cross-platform initializer
   ↓
First commit includes durable AI context
   ↓
Development begins
```

The `templates/project` template should remain aligned with the onboarding contract. A new project should not depend on an AI conversation to reconstruct its initial context later.

## Automatic onboarding levels

DevOS distinguishes three kinds of automation.

### Local automatic onboarding

A configured local worker may watch explicitly configured project roots and invoke the idempotent onboarding command for new Git repositories/directories.

This is the correct mechanism for projects created or cloned on a user's machine.

### Template automatic onboarding

Projects created from an approved DevOS template can start with the DevOS context already present.

### Remote organization automatic onboarding

An explicitly installed GitHub App, organization workflow, or equivalent authorized integration can onboard newly created repositories that it is permitted to observe and modify.

The public DevOS repository itself does **not** automatically gain permission to modify arbitrary repositories.

This distinction is mandatory for security and truthful capability claims.

## GitHub-side synchronization

Once a project contains the caller workflow, the reusable DevOS workflow can synchronize deterministic repository-derived context after configured pushes/pull requests.

The synchronizer is evidence-oriented and does not replace semantic project understanding.

## Semantic onboarding boundary

The initializer may safely derive basic facts such as:

- directory/project name;
- stable project identifier;
- presence/absence of expected infrastructure;
- Git/non-Git state.

It must not silently invent:

- business requirements;
- architecture;
- product decisions;
- security guarantees;
- deployment correctness;
- test success;
- root causes.

Those require AI-assisted inspection and evidence.

## Health / validation

After onboarding, run the project's DevOS bootstrap/health validation.

Onboarding status and application health are separate claims.

```text
ONBOARDED
!=
APPLICATION VERIFIED
!=
PRODUCTION READY
```

## Security and authorization

Onboarding itself can create files and therefore is a mutation. `--apply` is an explicit operation.

Onboarding must never be used as a route to:

- production mutation;
- database mutation;
- permission changes;
- credential/secret changes;
- destructive operations;
- arbitrary remote execution.

All downstream project work remains subject to normal DevOS planning, readiness, authorization, Security Gate, runtime, and verification controls.

## Universal AI portability requirements

A managed project should be recoverable by a fresh AI with no prior chat memory.

The fresh AI must be able to discover:

1. the DevOS bootstrap entrypoint;
2. project identity;
3. current state;
4. tasks/decisions/architecture;
5. recent evidence/change history;
6. the distinction between verified and unverified claims;
7. the current safe next action.

## Reproducibility and acceptance

The canonical implementation is:

```text
core/devos-universal-project-onboarding.md
tools/devos-onboard.py
tools/test-devos-onboard.py
```

Acceptance requires:

- valid existing project → READY;
- missing infrastructure → CREATE only missing files;
- second onboarding → all preserved/no duplicate creation;
- existing semantic context → unchanged;
- other managed framework identity → HOLD;
- new Git project → caller workflow can be created;
- non-Git project → context can be initialized without silently inventing Git state;
- plan mode → no mutation;
- apply mode → only DevOS infrastructure mutation;
- output → explicitly states authority unchanged;
- regression suite → PASS.

## Safety rules

- Never overwrite existing `.ai` semantic files during onboarding.
- Never overwrite application source during onboarding.
- Never put credentials, tokens, private keys, session cookies, or unnecessary personal/student data into `.ai`.
- Never claim tests passed merely because onboarding succeeded.
- Git history remains authoritative for exact repository changes.
- `.ai` is portable project context, not permission.
- AI account memory is supplementary only.

## Completion criterion

Universal Project Onboarding v1 is complete when the repository provides:

1. a cross-platform idempotent onboarding initializer;
2. deterministic regression coverage;
3. existing-project preservation and conflict HOLD behavior;
4. new-project/template guidance;
5. explicit local/template/remote automation boundaries;
6. a documented universal-AI/account portability contract;
7. bootstrap/health validation integration;
8. no false implication that DevOS can silently modify arbitrary remote repositories.
