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

The existing PowerShell wrapper remains supported for Windows workflows.

## Repository creation capability

For new remote repositories, DevOS now defines an explicit provider-dependent capability:

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

### Important connector limitation

The ChatGPT GitHub connector may expose branch/file/commit/PR write operations without exposing repository creation. When the selected AI/provider does not expose `repository.create`, DevOS must return a capability-unavailable outcome such as:

`NEEDS_EXTERNAL_REPO_CREATION`

The workflow then becomes:

```text
Create repository outside current provider capability
            ↓
Discover the new repository
            ↓
Universal DevOS onboarding
            ↓
Verify context
```

Never claim that a repository was created when the provider capability was unavailable.

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
DevOS onboarding
   ↓
context verification
   ↓
first development action
```

Repository creation does **not** authorize application development, production deployment, database mutation, credential changes, or other high-impact actions.

## Existing projects

For a project that already exists:

1. Run plan mode.
2. Review paths proposed for creation/preservation.
3. Run `--apply` only when the project is intended to be managed by DevOS.
4. Validate bootstrap/health state.
5. Commit and push onboarding infrastructure if remote portability is required.

## Automatic onboarding levels

DevOS distinguishes:

### Local automatic onboarding
A configured local worker may discover projects under explicitly configured roots and invoke idempotent onboarding.

### Template automatic onboarding
Approved DevOS templates can start with the durable context already present.

### Remote organization automatic onboarding
An explicitly installed GitHub App, organization workflow, or equivalent authorized integration can create/onboard repositories within its granted scope.

The public DevOS repository itself does **not** grant permission to modify arbitrary repositories.

## Semantic onboarding boundary

The initializer may derive basic facts such as project name, project identifier, infrastructure presence, and Git/non-Git state. It must not invent business requirements, architecture, product decisions, security guarantees, deployment correctness, test success, or root causes.

## Health / validation

After onboarding, run the project's DevOS bootstrap/health validation.

```text
ONBOARDED
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

Universal Project Onboarding v1 acceptance includes:

- valid existing project → READY;
- missing infrastructure → CREATE only missing files;
- second onboarding → preserve/no duplicate creation;
- semantic context preservation;
- incompatible managed identity → HOLD;
- new Git project → caller workflow can be created;
- non-Git project → local context can be initialized;
- plan mode → no mutation;
- apply mode → only DevOS infrastructure mutation;
- `repository.create` plan mode → deterministic READY for valid targets;
- repository creation without explicit authorization → NEEDS_APPROVAL;
- repository creation without provider safety enablement → BLOCKED;
- provider uncertainty → HOLD and replay forbidden;
- authority remains UNCHANGED;
- regression suite → PASS.

## Safety rules

- Never overwrite existing `.ai` semantic files during onboarding.
- Never overwrite application source during onboarding.
- Never put credentials, tokens, private keys, session cookies, or unnecessary personal/student data into `.ai`.
- Never claim tests passed merely because onboarding succeeded.
- Never claim repository creation succeeded without provider evidence and required readback.
- Never treat provider capability as authorization.
- Never treat authorization as unlimited provider permission.
- Git history remains authoritative for exact repository changes.
- `.ai` is portable project context, not permission.
- AI account memory is supplementary only.

## Completion criterion

Universal Project Onboarding and Repository Creation v1 are complete only when the repository provides deterministic onboarding, a governed provider-dependent repository-creation capability, regression coverage, explicit unavailable-capability handling, documented local/template/remote automation boundaries, and the universal AI/account portability contract.
