# Portable Project Memory

DevOS treats the repository as the durable memory boundary for development. A fresh AI, account, model, or tool must be able to recover the project from repository evidence without depending on chat history or vendor-specific memory.

## Recovery contract

A fresh tool follows:

`RECOVER -> RESOLVE -> VERIFY -> CONTINUE -> PERSIST -> HANDOFF`

Recovery starts with `AGENTS.md`, then `.ai/manifest.yaml`, `.ai/STATE-INDEX.md`, `.ai/PROJECT.md`, `.ai/CURRENT-STATE.md`, and the relevant architecture, decisions, tasks, changelog, source, tests, workflows, and Git history.

The repository/source and Git remain authoritative for implementation. Durable `.ai` records carry project context and handoff state. Generated indexes are evidence/navigation aids only. AI account memory and old chats are supplementary and never authoritative.

## Fresh-tool boundary

`tools/devos-bootstrap.py` is a deterministic, non-executing inspector. It reports whether the required portable context exists, identifies the current Git branch/HEAD, and explicitly reports that execution is `NONE` and authorization is `UNCHANGED`.

`tools/test-devos-bootstrap.py` runs the inspector twice and requires identical output plus complete required context. This proves the bootstrap discovery path is deterministic without granting execution authority.

## Persistence rule

What is not written was never done. Material implementation changes must carry their affected durable repository record in the same commit. Completion requires:

`IMPLEMENTED + VERIFIED + DOCUMENTED`

Portable memory never authorizes execution, mutation, deployment, publication, or security bypass. It only makes project context recoverable.
