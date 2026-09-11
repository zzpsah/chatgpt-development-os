# Multi-AI Portability v1

Development OS is designed so project continuity survives changes in AI vendor, account, model, coding tool, GitHub account, or machine.

## Authority model

```text
Project .ai context + source + Git
            ↓
     durable project state
            ↓
     any compatible AI
            ↓
     adapter / host capabilities
```

The AI account is supplementary. It is never the sole source of project state.

## Portable contract

Every managed project carries:

- `AGENTS.md` — operating instructions;
- `.ai/manifest.yaml` — context contract and identity;
- `.ai/STATE-INDEX.md` — deterministic repository evidence;
- `.ai/PROJECT.md` — project identity, purpose, scope, technology, constraints;
- `.ai/CURRENT-STATE.md` — current verified state;
- `.ai/ARCHITECTURE.md` — system structure;
- `.ai/DECISIONS.md` — intentional decisions;
- `.ai/TASKS.md` — work state;
- `.ai/CHANGELOG.md` — compact change history;
- `.ai/SESSIONS/` — meaningful session context.

Source code and Git remain the implementation/change authority. Generated state is evidence, not semantic proof.

## Repository-only recovery

A new AI should be able to recover without old chat history:

1. Locate the nearest `AGENTS.md`.
2. Read `.ai/manifest.yaml`.
3. Read `STATE-INDEX.md`, `PROJECT.md`, and `CURRENT-STATE.md`.
4. Read relevant architecture, decisions, tasks, changelog, and recent session records.
5. Inspect source, tests, configuration, deployment metadata, and Git.
6. Resolve Observed / Likely / Unknown facts.
7. Identify active, blocked, and planned work.
8. Determine verification status and the highest-priority unfinished work.
9. Continue only within the authorization and security boundaries of the request.

The recovery result must distinguish recovered facts from hypotheses and must not assume that a prior AI's summary is correct merely because it exists in chat history.

## Vendor/account independence

Project context must not contain:

- ChatGPT account state;
- Claude/Cursor/Gemini account state;
- model-specific hidden instructions;
- provider-specific conversation IDs as required recovery data;
- personal AI memory as the only source of project facts;
- credentials, tokens, private keys, or session cookies.

Host-specific behavior belongs in `adapters/`, while portable engineering rules belong in `core/`, `workflows/`, `rules/`, and project `.ai/` context.

## Adapter boundary

The adapter connects a host AI to the portable contract. It may provide repository access, terminal/build execution, browser automation, or other capabilities. It must report unavailable capabilities rather than pretending they were performed.

See [`adapters/adapter-contract.md`](../adapters/adapter-contract.md).

## Portability test

A portability claim is supported only when the repository contains enough information for an independent AI to identify the project, understand current state, inspect implementation, recover unfinished work, and determine a safe next action.

A documentation-only claim is not proof that an arbitrary AI can actually recover the project; the repository must remain internally coherent and the recovery contract must be validated.
