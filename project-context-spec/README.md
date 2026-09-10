# Portable Project Context Specification

Every managed project should carry its own durable AI context.

## Required

- `AGENTS.md` — AI entry point and project-local operating instructions.
- `.ai/manifest.yaml` — machine-readable context discovery and version.
- `.ai/PROJECT.md` — durable project identity and purpose.
- `.ai/CURRENT-STATE.md` — verified current state.
- `.ai/DECISIONS.md` — durable architectural/product decisions.
- `.ai/TASKS.md` — active and planned work.

## Optional

- `.ai/ARCHITECTURE.md`
- `.ai/SECURITY.md`
- `.ai/DEPLOYMENT.md`
- `.ai/API.md`
- `.ai/SESSIONS/`

## Source-of-truth rule

Project context belongs to the project. It must not depend on a particular ChatGPT, Claude, Codex, Gemini, GitHub, or other AI account.

AI account memory is supplementary. Source code, version-control history, and project-local `.ai/` context are authoritative.
