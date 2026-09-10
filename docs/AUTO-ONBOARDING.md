# Project Auto-Onboarding

Development OS can make a repository managed with a small, safe onboarding step. The design is intentionally idempotent: existing project context is preserved and only missing infrastructure is added.

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

## Safety rules

- Never overwrite existing `.ai` semantic files during onboarding.
- Never put credentials, tokens, private keys, session cookies, or unnecessary personal/student data into `.ai`.
- Never claim tests passed merely because onboarding succeeded.
- Git history remains authoritative for exact repository changes.
- `.ai` remains the portable project memory; ChatGPT account memory is supplementary only.
