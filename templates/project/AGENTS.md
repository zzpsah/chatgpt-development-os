# Project AI Entry Point

This project uses the Portable Project Context Specification from ChatGPT Development OS.

Before substantial work:
1. Read `.ai/manifest.yaml`.
2. Read `.ai/PROJECT.md` and `.ai/CURRENT-STATE.md`.
3. Read relevant `.ai/DECISIONS.md`, `.ai/TASKS.md`, and `.ai/ARCHITECTURE.md` when present.
4. Read recent `.ai/CHANGELOG.md` and the latest relevant session record when resuming ongoing work.
5. Inspect the actual source code and tests before making changes.

During work:
- Keep facts, assumptions, decisions, and pending work distinct.
- Do not treat automated repository evidence as semantic project understanding.
- Ask for clarification only when proceeding could affect the wrong project or cause a materially wrong result.

After meaningful work:
1. Update `.ai/CURRENT-STATE.md` with verified facts.
2. Update `.ai/TASKS.md` when work changes.
3. Record important decisions in `.ai/DECISIONS.md`.
4. Record a concise session summary in `.ai/SESSIONS/` when the session changes project state or leaves important unfinished work.
5. Never store secrets, tokens, passwords, private keys, session cookies, or sensitive credentials in project context.

Do not treat AI chat history as the authoritative project state. The repository-local `.ai/` context, source code, and version-control history are the durable project record.
