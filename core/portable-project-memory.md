# Portable Project Memory & Fresh-AI Bootstrap

## Purpose

DevOS treats the repository as the durable memory boundary of the project. The project must remain recoverable when the current AI account, chat session, model, or coding tool is unavailable.

> **The project remembers. The AI assists.**

## Recovery contract

A fresh AI/tool MUST be able to recover project context from the repository without depending on account memory or an old chat.

Minimum recovery order:

1. Repository root and Git state
2. `AGENTS.md` and project routing instructions
3. `.ai/PROJECT.md`
4. `.ai/CURRENT-STATE.md`
5. `.ai/TASKS.md`
6. `.ai/DECISIONS.md`
7. `.ai/ARCHITECTURE.md`
8. Relevant source, tests, workflows, and recent Git history

AI account memory and prior chat are supplementary only. They MUST NOT be treated as authoritative completion evidence.

## Fresh-AI bootstrap protocol

On entering an unfamiliar DevOS repository, an AI/tool MUST:

- identify the repository and active branch;
- read the durable project context before proposing work;
- inspect Git/source evidence for the current implementation state;
- distinguish documented facts from inference and unresolved state;
- recover unfinished authorized work from `.ai/TASKS.md`;
- respect decisions and authority boundaries in `.ai/DECISIONS.md`;
- verify claims against repository evidence before continuing;
- persist material decisions, state changes, and implementation documentation in the same change set.

The bootstrap protocol does not grant authorization to perform restricted actions.

## Handoff contract

A handoff is a pointer, not authority. A receiving AI MUST revalidate the repository state and current Git/source evidence before continuing work.

A session may end without losing project continuity because the durable record lives in the repository rather than in the originating AI session.

## Completion contract

A material work unit is complete only when all three conditions are true:

**IMPLEMENTED + VERIFIED + DOCUMENTED**

If durable documentation is missing, status is `INCOMPLETE` or `UNKNOWN`; the AI MUST NOT manufacture a completion claim from chat history.

## Agent neutrality

DevOS is not a Claude-only memory system. Agent-specific tooling such as Claude Code, Codex, or other coding agents may operate on top of DevOS, but the repository contract remains the common recovery layer.

Any compatible AI/tool should be able to follow the same repository-local bootstrap and continue from the same durable project state.

## Safety boundary

Portable project memory does not authorize execution, mutation, publication, deployment, or other privileged actions. Authorization remains governed by the existing DevOS controller, Security Gate, and repository rules.
