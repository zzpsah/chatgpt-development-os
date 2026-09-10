# Using the Development OS with a New AI

The Development OS is designed so that a project can move between AI tools without rebuilding project history from chat memory.

## What the new AI should do

When opening a project, the AI should automatically:

1. Read the root `AGENTS.md` if present.
2. Read `.ai/manifest.yaml`.
3. Read `.ai/PROJECT.md` and `.ai/CURRENT-STATE.md` first.
4. Read `.ai/ARCHITECTURE.md`, `.ai/DECISIONS.md`, and `.ai/TASKS.md` when relevant.
5. Inspect the actual source code, configuration, tests, and Git state before making important claims.
6. Continue from the project's durable state instead of relying on an earlier AI conversation.
7. After meaningful changes, update the relevant `.ai/` files.

## The only user commands you normally need

There is deliberately no required command language. Natural language is the interface.

| You say | AI should understand |
|---|---|
| `Continue` | Recover project state and continue the active work. |
| `What have we done?` | Summarize durable project state, recent changes, and pending work. |
| `Continue the registration project` | Resolve the named project, load its context, and resume. |
| `Something is broken` | Investigate and debug. |
| `Make it professional` | Inspect the current implementation and propose/improve it appropriately. |
| `Check it` | Validate the relevant implementation. |
| `Is it secure?` | Perform a security review. |
| `Go ahead` | Execute the previously agreed safe plan. |
| `Document this` | Update the appropriate project documentation/context. |

The AI should ask a clarification only when proceeding without it could modify the wrong project or cause a materially wrong result.

## First message to a completely new AI

You can simply say:

> **Open this project, read `AGENTS.md` and `.ai/manifest.yaml`, recover the current project state, and tell me what we should do next.**

After that, ordinary natural-language requests are enough.

## If the AI does not automatically understand the system

Use this one-time bootstrap instruction:

> **This repository uses ChatGPT Development OS. Treat `AGENTS.md` as the project entry point and `.ai/manifest.yaml` plus the `.ai/` files as portable project context. Inspect those files before substantial work. Do not depend on chat history or AI-account memory. Preserve existing context, follow the project's instructions, and update durable `.ai/` state after meaningful changes.**

## What must NOT be copied into the new AI

Do not paste or commit:

- API keys
- passwords
- access tokens
- private keys
- session cookies
- `.env` contents
- unnecessary student/personal data

The project context should describe the system and its state, not become a secret store.

## Source of truth

When information conflicts, use this order as a general rule:

1. Explicit current user instruction
2. Project-local instructions in `AGENTS.md` and `.ai/`
3. Actual source/configuration and current runtime evidence
4. Git history
5. AI account memory or old chat history

AI memory is helpful for continuity, but the repository is what makes the project portable.
