# Portable AI Bootstrap Protocol

## Purpose

This protocol defines how any AI development agent should discover and use Development OS when working on a managed project.

The goal is **project-portable continuity**, not dependence on a particular AI account, chat history, model, or vendor.

## Core principle

> The project carries its durable engineering context. AI account memory is supplementary.

An AI agent must not assume that its own memory contains the authoritative project state.

## Bootstrap sequence

When entering a Development OS-managed project, an AI agent should:

1. Find and read the nearest applicable `AGENTS.md`.
2. Locate `.ai/manifest.yaml`.
3. Read `.ai/STATE-INDEX.md` when present.
4. Read `.ai/PROJECT.md` and `.ai/CURRENT-STATE.md`.
5. Read relevant `.ai/ARCHITECTURE.md`, `.ai/DECISIONS.md`, and `.ai/TASKS.md`.
6. Read recent `.ai/CHANGELOG.md` and the latest relevant session record when resuming work.
7. Inspect the actual source code, tests, configuration, and Git state before making material technical conclusions.
8. Treat repository evidence and explicit project context as more authoritative than remembered assumptions.

## State authority

Use these sources in roughly this order for different questions:

| Question | Primary evidence |
|---|---|
| What code exists? | Source tree + Git |
| What changed? | Git history + CHANGELOG |
| What is the current project state? | CURRENT-STATE + source/Git verification |
| What was intentionally decided? | DECISIONS |
| What remains to do? | TASKS + current evidence |
| What is the project for? | PROJECT |
| What should an AI read first? | AGENTS + manifest |
| What did the latest automated sync observe? | STATE-INDEX |

`STATE-INDEX.md` is an evidence index, not semantic authority. It must not be treated as proof of architecture, correctness, security, root cause, or the true next task.

## Intent and language

The agent should understand ordinary language, Hinglish, informal expressions, slang, frustration, humor, and the engineering slang dictionary defined by Development OS.

Interpret:

`Human language → semantic intent → technical workflow → evidence → action → verification`

Do not execute technical changes merely because a phrase sounds forceful or emotional.

## Learning and teaching behavior

If the user asks for development work, preserve rigorous engineering reasoning while explaining at the user's requested depth.

If the user asks for teaching material, switch to student-first educational mode. Where useful, structure material as:

`Theory → Mental Model → Visual → Diagram → X-ray/Under-the-Hood → Example → Practice → Common Mistakes → Revision → Assessment`

Use only the layers that genuinely improve learning. Visuals do not replace theory.

## Evidence discipline

Classify important conclusions as:

- **Observed** — directly verified.
- **Likely** — evidence-supported hypothesis, not yet conclusive.
- **Unknown** — not established.

Never convert an assumption into a fact simply because another AI agent, chat, or memory previously stated it.

## Change discipline

Before material changes:

- inspect existing implementation;
- understand project constraints and decisions;
- identify affected areas;
- choose the smallest safe change;
- preserve unrelated behavior;
- verify with appropriate tests/review.

For high-impact operations such as production changes, destructive database operations, security-sensitive changes, or deletion, require appropriate explicit authorization and safety checks.

## Persistence contract

After meaningful work, update the project's durable context when applicable:

- `CURRENT-STATE.md` for current verified state;
- `TASKS.md` for active/planned/completed work;
- `DECISIONS.md` for material decisions;
- a session record for meaningful session-level context;
- `CHANGELOG.md` when the project's change-recording process requires it.

Do not store secrets, credentials, session cookies, private keys, or unnecessary sensitive/student data.

## Vendor independence

This protocol does not require a specific AI vendor. An agent may be ChatGPT, Codex, Claude, Gemini, Cursor, another coding agent, or a future system.

The project should remain understandable if the previous AI is unavailable.

## Missing or incomplete context

If required context files are missing, malformed, stale, or contradictory:

1. inspect the repository and Git state;
2. identify what can be established from evidence;
3. avoid inventing missing project intent;
4. repair or propose context updates when authorized;
5. clearly distinguish recovered facts from assumptions.

## Non-authoritative external memory

AI account memory, conversation history, cached context, or personal notes may help provide continuity, but they must not silently override explicit project files, source code, Git history, or verified current state.

## Completion standard

A task is not complete merely because an AI generated code or documentation. Completion requires an appropriate verification statement describing what was actually checked and any known limitations.

## Short bootstrap instruction

For systems that support only a compact instruction, use:

> **Read `AGENTS.md`, then `.ai/manifest.yaml`, `.ai/STATE-INDEX.md`, `.ai/PROJECT.md`, and `.ai/CURRENT-STATE.md`. Read relevant `.ai` decisions/tasks/architecture and recent session/change history. Inspect source and Git before material conclusions. Treat `.ai` + source + Git as project-durable context, not your personal memory. Interpret natural language semantically, preserve safety, and verify claims before reporting completion.**
