# ChatGPT Development OS

A portable, human-language development operating system for working across projects, AI accounts, AI coding tools, and machines.

## Core idea

The Development OS defines **how AI develops software**. Each project owns its own durable `.ai/` memory. The project must not depend on ChatGPT Memory, a particular AI account, or a particular GitHub account.

**Understand → Inspect → Plan → Implement → Test → Review → Security → Document → Persist**

Not every request requires every stage; the workflow scales to the task.

## Portable project memory

Every managed software project should contain:

```text
project/
├── AGENTS.md
└── .ai/
    ├── manifest.yaml
    ├── PROJECT.md
    ├── CURRENT-STATE.md
    ├── ARCHITECTURE.md
    ├── DECISIONS.md
    ├── TASKS.md
    └── SESSIONS/
```

This makes project context portable between ChatGPT, Codex, Claude, Gemini, Cursor, other AI tools, GitHub accounts, Git providers, and local machines.

## Automatic initialization

The repository now includes:

- `tools/init-project.ps1` — idempotent initializer for an existing local project.
- `tools/watch-projects.ps1` — Windows recursive watcher that detects project activity and initializes missing `.ai/` context.
- `tools/install-windows.ps1` — installs the watcher at Windows logon for configured project roots.
- `templates/project/` — portable project-context starter files.
- `project-context-spec/` — the context specification shared by all projects.

See `tools/AUTOMATION.md` for setup and safety details.

## Human-language first

The user should not need to know which agent or workflow is required. Examples:

- “Something is wrong with the registration page.” → investigate/debug.
- “Make the page more professional.” → UI analysis/improvement.
- “Can you check whether this is secure?” → security review.
- “Continue where we stopped.” → recover project state and resume.
- “Go ahead and do it.” → execute the agreed plan.

## Architecture

- **Development OS** — reusable methodology, workflows, roles, rules, and adapters.
- **Project `.ai/`** — authoritative portable project context.
- **Source code** — actual implementation.
- **Git history** — durable change history when version control is used.
- **AI account memory** — optional personal/contextual assistance, never the sole project memory.
- **GitHub/Supabase/local workers** — infrastructure used when appropriate.

## Safety

- Never commit secrets, tokens, passwords, private keys, or session cookies.
- Preserve existing behavior unless a change is intentional.
- Treat production/database/destructive changes as high-risk.
- Verify assumptions before changing important systems.
- Prefer small, reviewable changes.
- Test before declaring work complete.
- Keep project-specific knowledge separate from global rules.
- Do not watch entire drives by default; configure dedicated project roots.

## Repository structure

```text
chatgpt-development-os/
├── README.md
├── AGENTS.md
├── core/
├── agents/
├── workflows/
├── rules/
├── project-context-spec/
├── templates/
├── tools/
├── projects/
├── memory/
└── adapters/
```

## Version

0.2 — portable project memory and automatic initialization foundation.