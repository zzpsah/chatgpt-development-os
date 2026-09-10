# ChatGPT Development OS

A persistent, human-language development operating system for working with ChatGPT across projects and conversations.

## Goal

The user talks naturally. The system interprets intent, identifies the relevant project, loads durable context, chooses an appropriate engineering workflow, and persists important state back to GitHub.

## Core flow

**Understand → Inspect → Plan → Implement → Test → Review → Security → Document → Persist**

Not every request requires every stage; the system scales the workflow to the task.

## Human-language first

Commands are optional. The user should never need to know which agent or workflow is required. Examples:

- “Something is wrong with the registration page.” → investigate/debug.
- “Make the page more professional.” → UI analysis/improvement.
- “Can you check whether this is secure?” → security review.
- “Continue where we stopped.” → recover state and resume.
- “Go ahead and do it.” → execute the agreed plan.

## Durable architecture

- **GitHub** — source of truth for rules, project context, decisions, and code references.
- **ChatGPT** — reasoning, orchestration, research, review, and project coordination.
- **Supabase** — application/backend data where applicable.
- **Local Codex/other workers** — optional execution layer to be added later.

## Safety principles

- Never commit secrets, tokens, passwords, or private keys.
- Preserve existing behavior unless a change is intentional.
- Treat production/database/destructive changes as high-risk.
- Verify assumptions before changing important systems.
- Prefer small, reviewable changes.
- Test before declaring work complete.
- Keep project-specific knowledge separate from global rules.

## Repository structure

```text
chatgpt-development-os/
├── README.md
├── AGENTS.md
├── core/
├── agents/
├── workflows/
├── rules/
├── projects/
├── memory/
└── adapters/
```

## Version

0.1 — persistent foundation.