# Fresh-AI Bootstrap Procedure

Use this procedure when a new AI account, model, agent, or coding tool opens the project.

## 1. Recover

Read `AGENTS.md`, then the `.ai/` durable context files. Inspect the current Git branch, status, recent commits, relevant source, tests, and workflows.

## 2. Resolve

Determine the active milestone and unfinished work from `.ai/CURRENT-STATE.md` and `.ai/TASKS.md`. Check decisions and architecture constraints before changing anything.

## 3. Verify

Treat Git, source, tests, CI, runtime output, and security results as evidence. Treat previous AI assertions, plans, and chat history as context only.

## 4. Continue

Implement only work that is authorized by the repository's existing rules. Do not infer permission from the stance code or from a previous AI session.

## 5. Persist

For every material change, update the appropriate durable project record in the same change set. A material change without durable documentation is incomplete.

## 6. Handoff

Before ending a session, leave the repository in a recoverable state: current state, task state, decisions, verification evidence, and next authorized action must be discoverable from the repository.

## Canonical flow

`RECOVER → RESOLVE → VERIFY → CONTINUE → PERSIST → HANDOFF`
