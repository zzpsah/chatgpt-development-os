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

## Mandatory managed-project lifecycle gate

Repository existence is not enough. Every repository selected for DevOS work must pass the Managed Project Lifecycle v1 gate before feature development continues.

```text
CREATE or DISCOVER repository
            ↓
fresh repository readback
            ↓
python tools/devos.py project-lifecycle ... --require-managed
            ↓
MANAGED ?
  ├─ YES → recover state → continue
  ├─ NO  → onboard → fresh readback → re-check
  └─ CONFLICT → HOLD
```

Permanent rule:

```text
REPOSITORY EXISTS != DEVOS MANAGED
REPOSITORY CREATED != ONBOARDED
REPOSITORY DISCOVERED != SAFE TO CONTINUE
```

An unmanaged or partially managed repository sets `development_continuation_allowed = false`. This closes the lifecycle gap where a repository could be created or discovered but never receive durable DevOS state.

Read-only local check:

```bash
python tools/devos.py project-lifecycle --path <project> --require-managed --json
```

Authorized local onboarding + managed readback:

```bash
python tools/devos.py project-lifecycle \
  --path <project> \
  --apply \
  --authorization EXPLICIT \
  --require-managed \
  --json
```

Provider/controller integrations can supply `DEVOS-REPOSITORY-DISCOVERY-SNAPSHOT-v1` evidence to the same lifecycle tool. Remote snapshots are read-only; provider writes require a separately governed onboarding path.

## Existing-repository flow

```text
Detect candidate
    ↓
Resolve project root / repository identity
    ↓
Managed Project Lifecycle check
    ↓
Inspect Git / existing AGENTS.md / .ai/
    ↓
Check DevOS identity compatibility
    ↓
PLAN missing infrastructure (read-only)
    ↓
Explicit onboarding apply when required
    ↓
Preserve existing semantic context
    ↓
Create only missing DevOS infrastructure
    ↓
Fresh managed-state readback
    ↓
MANAGED verified
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

The Managed Project Lifecycle tool wraps this onboarding path for enforced detect → onboard → readback behavior.

The existing PowerShell wrapper remains supported for Windows workflows.

## Repository creation capability

For new remote repositories, DevOS defines an explicit provider-dependent capability:

`repository.create`

Reference implementation:

```bash
python tools/devos-create-repository.py --owner @me --name <name>
```

The default is **plan-only**. A live creation attempt requires all of the following:

```bash
python tools/devos-create-repository.py \
  --owner @me \
  --name <name> \
  --authorization EXPLICIT \
  --apply
```

and the local safety gate:

```text
DEVOS_ALLOW_REPO_CREATE=1
```

A GitHub token is read from `GITHUB_TOKEN`; credentials are never printed or persisted by the tool.

The implementation supports the authenticated GitHub user with `--owner @me` and GitHub organizations by explicit owner name. It performs one provider create request and returns `ATTEMPTED`, `NEEDS_READBACK`, `HOLD`, or `BLOCKED`; it does not call an operation `VERIFIED` merely because the provider returned success. Fresh provider readback is required for a verified completion claim.

Every repository-creation plan/result also carries this mandatory lifecycle postcondition:

```text
managed_project_required = true
required_next_capability = project.onboard
development_continuation_allowed = false
```

The first development action remains HOLD until fresh readback plus Managed Project Lifecycle verification returns `MANAGED`.

### Important connector limitation

The ChatGPT GitHub connector may expose branch/file/commit/PR write operations without exposing repository creation. When the selected AI/provider does not expose `repository.create`, DevOS must return a capability-unavailable outcome such as:

`NEEDS_EXTERNAL_REPO_CREATION`

The workflow then becomes:

```text
Create repository outside current provider capability
            ↓
Discover the new repository
            ↓
Managed Project Lifecycle check
            ↓
Universal DevOS onboarding if required
            ↓
Fresh readback
            ↓
MANAGED verification
            ↓
first development action
```

Never claim that a repository was created when the provider capability was unavailable. Never continue development merely because an externally created repository was discovered.

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

## Preservation rule

Existing project files and existing semantic `.ai/` files are preserved by default. Onboarding never replaces application source, overwrites existing semantic decisions, replaces another framework's context, or silently claims generated placeholders describe the actual architecture.

If an existing manifest identifies another framework as the managed authority, onboarding returns `HOLD` rather than overwriting it.

## New-project flow

The preferred fully governed flow is:

```text
Human goal
   ↓
P15 interpretation
   ↓
P16 plan
   ↓
P17 exact repository.create readiness
   ↓
explicit authorization + provider capability
   ↓
repository.create (one request)
   ↓
fresh provider verification
   ↓
Managed Project Lifecycle check
   ↓
DevOS onboarding if required
   ↓
fresh managed-state readback
   ↓
MANAGED
   ↓
context recovery / verification
   ↓
first development action
```

Repository creation does **not** authorize application development, production deployment, database mutation, credential changes, or other high-impact actions.

## Existing projects

For a project that already exists:

1. Run the Managed Project Lifecycle read-only check.
2. If `MANAGED`, recover durable state before work.
3. If `ONBOARDING_REQUIRED`, review the proposed onboarding scope.
4. Run `--apply --authorization EXPLICIT` only when the project is intended to be managed by DevOS.
5. Require fresh readback to return `MANAGED`.
6. Validate bootstrap/health state.
7. Commit and push onboarding infrastructure if remote portability is required.

## Automatic onboarding levels

DevOS distinguishes:

### Local automatic onboarding
A configured local worker may discover projects under explicitly configured roots and invoke the lifecycle gate plus idempotent onboarding within its authorized scope.

### Template automatic onboarding
Approved DevOS templates can start with the durable context already present and should verify `MANAGED` before development.

### Remote organization automatic onboarding
An explicitly installed GitHub App, organization workflow, or equivalent authorized integration can discover/create repositories, run the lifecycle check, onboard repositories within its granted scope, and verify fresh managed readback.

The public DevOS repository itself does **not** grant permission to modify arbitrary repositories.

## GitHub-side versus local automation

GitHub-side automation can validate repository-local DevOS context and synchronize repository-derived evidence after pushes and pull requests. It cannot silently observe or mutate a developer's local machine.

A configured local worker may discover projects only under explicitly configured roots and invoke idempotent onboarding within its granted host capabilities. Organization-wide automatic onboarding requires a separately installed GitHub App, organization workflow, or equivalent authorized integration.

Neither local nor GitHub-side automation creates DevOS authorization. Provider capability, provider credentials, P17 readiness, and exact user authorization remain separate controls.

## Context generation boundary

The initializer may derive basic repository facts such as project name, project identifier, infrastructure presence, and Git/non-Git state. It must not invent business requirements, architecture, product decisions, security guarantees, deployment correctness, test success, or root causes. Semantic understanding requires repository inspection and evidence.

## Health / validation

After onboarding, run the project's DevOS bootstrap/health validation.

```text
ONBOARDED
!=
MANAGED READBACK VERIFIED
!=
APPLICATION VERIFIED
!=
PRODUCTION READY
```

## Security and authorization

Repository creation and onboarding are mutations and remain separate capability/authorization decisions.

All downstream work remains subject to normal DevOS planning, readiness, authorization, Security Gate, runtime, and verification controls.

Failure or uncertain provider response must lead to reconciliation/readback, never blind replay.

## Universal AI portability

A managed project must be recoverable by a fresh AI with no prior chat memory. The AI must discover bootstrap, identity, current state, tasks, decisions, recent evidence, verified/unverified claims, and the safe next action from repository evidence.

## Acceptance

Universal Project Onboarding + Managed Project Lifecycle acceptance includes:

- repository with no DevOS manifest → `ONBOARDING_REQUIRED`;
- compatible but incomplete DevOS context → `ONBOARDING_REQUIRED`;
- valid complete DevOS context → `MANAGED`;
- incompatible managed identity → `HOLD`;
- malformed provider snapshot → `BLOCKED`;
- local apply without explicit authorization → `NEEDS_APPROVAL`;
- authorized local apply → create only missing infrastructure;
- post-apply fresh lifecycle readback → `MANAGED` required;
- second lifecycle apply → preserve/no duplicate creation;
- `repository.create` plan/result → mandatory onboarding postcondition;
- development continuation → false unless state is `MANAGED`;
- provider uncertainty → HOLD and replay forbidden;
- authority remains UNCHANGED;
- regression suite → PASS.

## Safety rules

- Never overwrite existing `.ai` semantic files during onboarding.
- Never overwrite application source during onboarding.
- Never put credentials, tokens, private keys, session cookies, or unnecessary personal/student data into `.ai`.
- Never claim tests passed merely because onboarding succeeded.
- Never claim repository creation succeeded without provider evidence and required readback.
- Never treat repository existence as managed-project completion.
- Never continue feature development on an unmanaged/partial/conflicting repository.
- Never treat provider capability as authorization.
- Never treat authorization as unlimited provider permission.
- Git history remains authoritative for exact repository changes.
- `.ai` is portable project context, not permission.
- AI account memory is supplementary only.

## Completion criterion

Universal Project Onboarding and Managed Project Lifecycle v1 are complete only when DevOS deterministically detects unmanaged/partial/conflicting repositories, holds development until `MANAGED`, applies onboarding only within explicit authorization, verifies fresh managed readback, binds repository creation to onboarding as a mandatory postcondition, exposes the lifecycle through the CLI, and preserves the universal AI/account portability contract.
