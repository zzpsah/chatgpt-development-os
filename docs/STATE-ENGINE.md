# Project State Engine

## Purpose

The Project State Engine makes a Development OS project recoverable from its repository without depending on chat history or an AI account's memory.

## State Engine v1

Version 1 is deliberately deterministic. GitHub automation aggregates repository evidence into `.ai/STATE-INDEX.md` and updates `.ai/CHANGELOG.md` and, for meaningful changes, repository-fact fields in `.ai/CURRENT-STATE.md`.

It records signals such as:
- current branch and HEAD commit
- latest commit subject, date, and author
- files changed by the triggering push
- deterministic meaningful/routine classification
- presence of required project-context files
- active, planned, and blocked task counts
- latest session record

The engine does **not** infer architecture, business intent, root cause, risk, or the true next development task from filenames alone.

## Semantic layer

The AI remains responsible for semantic project understanding. Before important work it must inspect:
1. user instructions
2. project-local instructions
3. `STATE-INDEX.md`
4. `CURRENT-STATE.md`, `PROJECT.md`, tasks, decisions, and architecture
5. actual source/configuration/tests
6. Git history and relevant runtime evidence

After meaningful development, the AI should persist semantic state in the appropriate `.ai` files and session record.

## Why this separation matters

Deterministic automation can safely answer **what changed**. The AI must investigate before claiming **why it changed**, **whether it is correct**, or **what should happen next**.

## Recovery flow

```text
User: Continue
      ↓
Project routing
      ↓
STATE-INDEX + durable .ai context
      ↓
Git/source inspection
      ↓
AI determines actual next action
      ↓
Plan / authorization
      ↓
Implement
      ↓
Test / review / security
      ↓
Persist semantic state
      ↓
GitHub automation refreshes deterministic state
```

## Safety

- Never store secrets or credentials in `.ai`.
- Never claim tests passed unless they were actually run.
- Never replace semantic project context with generated guesses.
- Never treat AI chat history as the authoritative project record.
