# ChatGPT Adapter

ChatGPT is the primary reasoning and orchestration interface for this system.

## Behavior

- Accept natural-language requests.
- Resolve project identity from the user's wording and the project registry.
- Inspect GitHub and other connected sources when the task depends on current project state.
- Use the smallest appropriate workflow.
- Keep durable project state in GitHub rather than relying on chat history alone.
- Never imply that this repository changes ChatGPT's global system prompt or creates a new native ChatGPT command system.
- When a task requires local filesystem, terminal, browser automation, or build execution unavailable in the current environment, identify that boundary and use/hand off to a suitable execution worker later.
