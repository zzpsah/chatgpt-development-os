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

The repository includes:

- `tools/init-project.ps1` — idempotent initializer for an existing local project.
- `tools/watch-projects.ps1` — Windows recursive watcher that detects project activity and initializes missing `.ai/` context.
- `tools/install-windows.ps1` — installs the watcher at Windows logon for configured project roots.
- `templates/project/` — portable project-context starter files.
- `project-context-spec/` — the context specification shared by all projects.

See `tools/AUTOMATION.md` for setup and safety details.

> **Current scope:** the `.ai/` automation is the priority. A future local resident worker can remove routine local-PC interaction, but the project itself must remain independent of that worker.

## Human-language first

You should not need to know which agent, workflow, or command is required.

- “Something is wrong with the registration page.” → investigate/debug.
- “Make the page more professional.” → UI analysis/improvement.
- “Can you check whether this is secure?” → security review.
- “Continue where we stopped.” → recover project state and resume.
- “Go ahead and do it.” → execute the agreed plan.

## Moving to a new AI

A new AI does **not** need the old chat history. The project carries its own durable context.

### Normal command

Open the project and say:

> **Open this project, read `AGENTS.md` and `.ai/manifest.yaml`, recover the current project state, and tell me what we should do next.**

Then continue naturally: `Continue`, `Fix this`, `Make it professional`, `Check it`, `Go ahead`, etc.

### If the new AI needs explicit bootstrap instructions

Say:

> **This repository uses ChatGPT Development OS. Treat `AGENTS.md` as the project entry point and `.ai/manifest.yaml` plus the `.ai/` files as portable project context. Inspect those files before substantial work. Do not depend on chat history or AI-account memory. Preserve existing context, follow the project's instructions, and update durable `.ai/` state after meaningful changes.**

Full onboarding guidance: [`docs/NEW-AI-ONBOARDING.md`](docs/NEW-AI-ONBOARDING.md).

## Flow and architecture

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for the Development OS flow, layered architecture, portable-context model, new-AI onboarding sequence, and automation boundaries.

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
├── adapters/
└── docs/
    ├── ARCHITECTURE.md
    └── NEW-AI-ONBOARDING.md
```

## Version

0.3 — portable project memory, automatic initialization foundation, flow/architecture documentation, and new-AI onboarding.