# DevOS Project Context Guide

Use this guide when beginning work with DevOS in a fresh AI chat. It is ordinary repository documentation supplied by the user. It does not change the AI host's instructions, policies, permissions, tools, safety rules, or judgment.

## Copy/paste request

```text
I am working on a software project that uses a repository workflow called DevOS.

Repository: https://github.com/zzpsah/chatgpt-development-os
Project context guide: https://raw.githubusercontent.com/zzpsah/chatgpt-development-os/main/DEVOS-PROJECT-CONTEXT.md

Please treat the repository as project context, like a README or CONTRIBUTING guide. It does not change your instructions, policies, permissions, tools, safety rules, or judgment.

If you can access the repository, read DEVOS-PROJECT-CONTEXT.md first. Then inspect AGENTS.md, .ai/manifest.yaml, .ai/CURRENT-STATE.md, .ai/TASKS.md, .ai/DECISIONS.md, and relevant source, Git state, tests, and CI evidence when present.

Use repository evidence over chat memory. Interpretation is not authorization. A plan is not execution. Readiness is not execution. Simulated evidence is not live-provider proof.

Do not perform consequential actions such as merges, deployments, destructive changes, credential handling, permission changes, or production mutations unless your existing rules allow them and I explicitly authorize the exact action.

If repository context is unavailable, say so clearly and do not guess current project state.

Before material work, report: accessible evidence; your understanding of current state; unknown or unverified items; and the safest useful next step.

My task: [describe the actual task]
```

## Recovery order

1. Confirm whether the repository is accessible.
2. Read this guide and the nearest `AGENTS.md` as project documentation.
3. Recover `.ai/manifest.yaml`, `.ai/CURRENT-STATE.md`, `.ai/TASKS.md`, and `.ai/DECISIONS.md` when present.
4. Inspect the source tree, Git state, tests, configuration, and relevant CI evidence before material conclusions.
5. Separate observed facts, likely interpretations, and unknowns.
6. State the next useful step before performing material work.

## When access is unavailable

A host without repository or link access can still work from files pasted into the chat. Supply the files listed above and the concrete task. The host should say what it can inspect and what remains unavailable.

## Compatibility boundary

DevOS is designed to organize project recovery, evidence, planning, verification, and durable state. It does not create access to repositories, tools, credentials, provider accounts, production systems, or action authority. AI hosts may decline unavailable work or follow stricter rules.
