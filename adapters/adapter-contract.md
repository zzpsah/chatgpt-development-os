# Multi-AI Adapter Contract v1

## Purpose

The adapter layer makes Development OS portable across AI vendors, accounts, models, coding tools, and execution environments.

The adapter is an integration boundary. It is **not** project memory, semantic authority, or a replacement for Development OS workflows.

## Required capabilities

A conforming adapter should provide or clearly delegate these capabilities:

1. **Project discovery** — identify the managed project from an explicit path, repository, or project reference.
2. **Bootstrap** — read `AGENTS.md`, `.ai/manifest.yaml`, `STATE-INDEX.md`, `PROJECT.md`, and `CURRENT-STATE.md`, then relevant context.
3. **Inspection** — inspect source, tests, configuration, deployment metadata, and Git state before material conclusions.
4. **Intent routing** — map natural language to canonical Development OS intents and workflows.
5. **State resolution** — distinguish Observed / Likely / Unknown and recover active / blocked / planned work.
6. **Execution** — perform or delegate authorized workflow actions without bypassing safety gates.
7. **Verification** — run or delegate applicable checks and report VERIFIED / PARTIAL / UNVERIFIED / FAILED with evidence.
8. **Persistence** — preserve meaningful project context in repository-local `.ai` files and Git history where applicable.

## Adapter responsibilities

- Translate host-specific capabilities into the Development OS contract.
- Declare capability limitations honestly.
- Preserve project-local context as the durable source.
- Preserve authorization boundaries, evidence classifications, and verification states.
- Avoid account-specific or vendor-specific assumptions in project context.
- Keep secrets, tokens, credentials, private keys, and session cookies out of durable context.

## Non-responsibilities

An adapter must not:

- become the authoritative project memory;
- silently rewrite project intent;
- infer correctness from missing evidence;
- bypass the Security Gate;
- treat emotional language as authorization;
- claim tests passed when they were not executed;
- require the previous AI account or chat history for recovery.

## Minimum recovery contract

A new AI using only repository access must be able to:

`AGENTS.md → .ai/manifest.yaml → .ai/STATE-INDEX.md → .ai/PROJECT.md → .ai/CURRENT-STATE.md → relevant context → source/Git → state resolution → next authorized action`

If context is missing or contradictory, the AI must recover facts from source/Git, label uncertainty, and avoid inventing intent.

## Portability invariant

> **If the previous AI disappears, the project must remain understandable and recoverable from the repository.**

This contract defines portability behavior; host-specific adapter files describe how an individual AI environment satisfies or delegates it.

## Machine-readable host profiles

Any AI host may declare its portable capability boundary using `DEVOS-HOST-PROFILE-v1`. The required capability names are `project_discovery`, `bootstrap`, `inspection`, `intent_routing`, `state_resolution`, `execution`, `verification`, and `persistence`; each is `AVAILABLE`, `DELEGATABLE`, or `MISSING`.

Profiles are validated by `tools/verify-host-profile.py` and documented in `docs/HOST-PROFILES.md`. They communicate honest host limitations only. A profile cannot grant authorization, create execution evidence, or replace repository-local context.
