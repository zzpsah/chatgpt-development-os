# Project Auto-Onboarding

Development OS can make a repository managed with a small, safe onboarding step. The design is intentionally idempotent: existing project context is preserved and only missing infrastructure is added.

## Existing-repository flow

```text
Detect candidate
    ↓
Resolve project root
    ↓
Check existing AGENTS.md / .ai/
    ↓
Preserve existing context
    ↓
Create only missing required files
    ↓
Inspect repository metadata when semantic onboarding is requested
    ↓
Validate context contract
    ↓
Report created / preserved / unknown state
```

## What onboarding creates

For a Git repository, `tools/onboard-project.ps1`:

1. initializes missing `.ai/` portable project context through `tools/init-project.ps1`;
2. preserves existing `.ai` files instead of replacing semantic project knowledge;
3. adds `.github/workflows/context-sync.yml` when it is missing;
4. leaves source code untouched;
5. prepares the repository for automatic GitHub-side context synchronization.

## Usage

From the Development OS repository:

```powershell
.\tools\onboard-project.ps1 -Path 'D:\Projects\MyApp'
```

Optional identity overrides:

```powershell
.\tools\onboard-project.ps1 -Path 'D:\Projects\MyApp' -Name 'My App' -ProjectId 'my-app'
```

Preview first:

```powershell
.\tools\onboard-project.ps1 -Path 'D:\Projects\MyApp' -DryRun
```

After onboarding, commit and push the generated files. The caller invokes the reusable Development OS workflow on pushes to `main` or `master`.

## Preservation rule

Existing project files and existing `.ai/` content are preserved. If a required context file already exists, the initializer leaves it unchanged. Onboarding is infrastructure establishment, not permission to overwrite project decisions or application code.

## Context generation boundary

The initializer may derive simple repository facts such as project name and identifier. It must not silently invent business requirements, architecture, security guarantees, deployment correctness, test success, product decisions, or root causes. Semantic understanding requires repository inspection and evidence.

## Health check

Run:

```powershell
.\tools\check-project.ps1 -Path 'D:\Projects\MyApp'
```

It checks the expected durable-context files, the GitHub caller, and obvious secret-named files. It does not prove application correctness or security.

## Automation levels

### New projects from the template

A project created from `templates/project` already contains the caller workflow and the standard `.ai` structure. GitHub synchronization starts after the project is pushed to `main` or `master`.

### Existing repositories

Existing repositories need one onboarding action, unless an organization-level rollout or GitHub App performs it. The onboarding script is designed to make this action safe and repeatable.

### Fully automatic arbitrary repositories

Development OS cannot silently modify every newly created GitHub repository merely because this repository exists. Full organization-wide automatic onboarding requires a separately installed GitHub App, organization workflow, or equivalent administrative deployment. That is a future infrastructure layer, not something the current repository should falsely imply is automatic.

## GitHub-side versus local automation

### GitHub-side

GitHub Actions can validate the context contract and synchronize repository-derived evidence after pushes and pull requests.

### Local worker

A resident local worker can detect newly created repositories or projects under configured roots and invoke the idempotent initializer. This is necessary for arbitrary local filesystem activity because a cloud workflow cannot silently observe a user's machine.

### AI agent

An AI agent is responsible for semantic onboarding: understanding purpose, architecture, requirements, decisions, current work, and verification by inspecting repository evidence.

## Safety rules

- Never overwrite existing `.ai` semantic files during onboarding.
- Never put credentials, tokens, private keys, session cookies, or unnecessary personal/student data into `.ai`.
- Never claim tests passed merely because onboarding succeeded.
- Git history remains authoritative for exact repository changes.
- `.ai` remains the portable project memory; ChatGPT account memory is supplementary only.

## Completion criterion

Auto-onboarding v1 is complete when the repository provides a documented existing-repository flow, an idempotent onboarding initializer, a context validation harness, CI validation, and clearly documented local-versus-GitHub automation boundaries.
