# Development OS — Session Persistence

## Purpose

A development session is temporary. The project must retain the useful result of that session without requiring the next AI to recover it from chat history.

## When to create a session record

Create `.ai/SESSIONS/YYYY-MM-DD-<short-topic>.md` when a session changes source/configuration, makes an important decision, changes active tasks, discovers a significant issue, establishes a useful verification result, or stops with important unfinished work. Do not create records for trivial conversation.

## Required structure

```markdown
# Session — YYYY-MM-DD — Short topic

## Objective
What this session was trying to accomplish.

## Work completed
- Verified changes actually made.

## Decisions
- Decisions made during this session, with rationale when important.

## Verification
- Tests/checks actually run and their result.
- Do not claim tests passed if they were not run.

## Open issues
- Known unresolved problems or risks.

## Next action
The single most useful next step for the next AI/session.

## Evidence
- Relevant commit/PR/file references.
```

## Persistence rules

1. Session records supplement `CURRENT-STATE.md`; they do not replace it.
2. `CURRENT-STATE.md` contains the latest verified project state.
3. `TASKS.md` contains actionable remaining work.
4. `DECISIONS.md` contains durable decisions and rationale.
5. `CHANGELOG.md` contains automatically recorded repository events.
6. Git history remains the authoritative exact record of code changes.

## Resume behavior

When the user says `Continue`, the AI should read `AGENTS.md` and `.ai/manifest.yaml`, then `CURRENT-STATE.md` and `TASKS.md`, inspect recent `CHANGELOG.md` entries and the latest relevant session, and finally inspect current source and Git state. It should derive the next safe action from evidence rather than assuming the old chat is available.

## Automation boundary

GitHub synchronization can safely record commits, changed paths, and deterministic classifications. It cannot reliably infer the semantic intent of a developer's session. Semantic session records therefore remain AI-owned unless a future trusted automation layer has sufficient evidence.

## Security

Never place credentials, tokens, passwords, private keys, session cookies, or unnecessary personal/student data in a session record.
