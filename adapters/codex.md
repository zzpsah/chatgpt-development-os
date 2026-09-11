# Codex Adapter

Codex is an execution-oriented AI adapter for Development OS.

## Contract

Codex should satisfy the portable adapter contract in [`adapters/adapter-contract.md`](adapter-contract.md).

## Behavior

- Consume the same project-level `AGENTS.md`, `.ai/` context, decisions, tasks, and workflow artifacts as other compatible AIs.
- Inspect source, tests, configuration, and Git before material conclusions.
- Preserve authorization, Security Gate, evidence, and verification requirements.
- Use local machines as disposable execution workers; do not treat local state as the durable project record.
- Persist meaningful project context back to the repository when authorized and required by the workflow.
- Report execution limitations or unavailable capabilities honestly.

## Portability rule

Codex must not require a particular ChatGPT account, conversation, hidden memory, or machine to recover the project. The repository remains the durable source of project context and implementation history.
