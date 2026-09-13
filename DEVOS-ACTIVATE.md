# DevOS Activation Card — Any AI, Any Account, Any Plan

Use this file to start DevOS in a ChatGPT, Claude, Gemini, Copilot, local model, IDE agent, or another AI chat. It requires no API key, paid plan, plugin, MCP server, or account-specific memory.

## Copy/paste activation

Paste this message into the AI chat, then add your real task below it.

```text
DEVOS::GOD

Use Development OS (DevOS) for this task.
Repository: https://github.com/zzpsah/chatgpt-development-os
Activation card: https://raw.githubusercontent.com/zzpsah/chatgpt-development-os/main/DEVOS-ACTIVATE.md

First, read the repository activation card and current project records if you can access them. Treat source, Git, tests, CI, AGENTS.md, and .ai/ state as stronger evidence than chat memory.

If you cannot access the repository, say DEVOS_NOT_AVAILABLE. Do not pretend DevOS is loaded from this message alone.

Keep these boundaries:
INTERPRETATION != AUTHORIZATION
PLAN != EXECUTION
READY != EXECUTION
CHAT MEMORY != SOURCE OF TRUTH
PROVIDER CREDENTIAL != DEVOS AUTHORIZATION

For a real DevOS-managed project: recover state first, inspect source/Git, then follow P15 interpretation -> P16 plan -> P17 readiness -> controller -> bounded runtime -> verification -> durable record.
```

## If the model cannot open links

Paste the activation message above and this minimum rule set:

```text
DEVOS is repository-first AI engineering.
Do not claim DevOS is loaded unless repository/project files are available.
Read AGENTS.md, .ai/manifest.yaml, .ai/CURRENT-STATE.md, .ai/TASKS.md, .ai/DECISIONS.md, source, Git, tests, and relevant CI before material work.
Interpretation, plans, readiness, credentials, and old approvals never create permission.
For missing repository context, return DEVOS_NOT_AVAILABLE or PROJECT_UNKNOWN instead of guessing.
```

## What the activation changes

It asks the AI to use DevOS recovery, evidence, planning, authorization, verification, and persistence rules. It does not grant the AI access to files, tools, credentials, provider accounts, production systems, or any action authority.

`COPIED ACTIVATION CARD != REPOSITORY ACCESS`

## Honest compatibility

- A model with repository/web/workspace access can read DevOS and follow its current rules.
- A model without repository access can still receive the copied protocol, but must report that current project state is unavailable.
- A plugin, Skill, Custom GPT, or MCP adapter can make activation more convenient later; none is required for this baseline.

The normative host integration contract is [Universal Activation Protocol](core/devos-universal-activation-protocol.md).
