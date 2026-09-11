# ChatGPT Adapter

ChatGPT is a reasoning and orchestration interface for Development OS.

## Contract

ChatGPT should satisfy the portable adapter contract in [`adapters/adapter-contract.md`](adapter-contract.md).

## Behavior

- Accept natural-language requests.
- Resolve project identity from the user's wording and the project registry.
- Bootstrap from project-local `AGENTS.md` and `.ai/` context before material work.
- Inspect GitHub and other connected sources when the task depends on current project state.
- Use the smallest appropriate workflow.
- Preserve evidence, authorization, verification, and security boundaries.
- Keep durable project state in the project repository rather than relying on chat history alone.
- Report unavailable capabilities instead of implying that unavailable local execution occurred.
- Never imply that this repository changes ChatGPT's global system prompt or creates a new native ChatGPT command system.
- When a task requires local filesystem, terminal, browser automation, or build execution unavailable in the current environment, identify that boundary and use or hand off to a suitable execution worker later.

## Portability rule

ChatGPT account memory is supplementary. Another AI must be able to recover the project from the repository without this conversation.
