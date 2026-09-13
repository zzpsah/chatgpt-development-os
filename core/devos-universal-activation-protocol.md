# DevOS Universal Project Workflow Discovery Protocol v1

## Purpose

This DevOS-internal protocol resolves a user-supplied DevOS label into an evidence-backed request to discover repository project context. It never requires an external AI host to recognize DevOS, and it does not change that host's system/developer instructions, policies, permissions, tools, safety rules, or capabilities.

`DEVOS`, `DEVOS::CONTINUE`, and `DEVOS::GOD` are optional user workflow labels. A compatible host may use the resolver only after it has a repository-local DevOS bootstrap surface. The labels are never evidence that DevOS or a managed project is available.

## Discovery flow

```text
User supplies DEVOS::<STANCE> as a workflow preference
  -> compatible DevOS host may invoke DEVOS-UNIVERSAL-ACTIVATION-v1
  -> parse the registered stance
  -> discover repository-local AGENTS.md + .ai/manifest.yaml
  -> validate required durable state files
  -> READY_FOR_BOOTSTRAP | DEVOS_NOT_AVAILABLE | PROJECT_UNKNOWN | INVALID_INVOCATION
  -> repository-first bootstrap and governed workflow, subject to host policy
```

The reference entrypoint is `tools/devos-universal-activation.py`. Its status vocabulary is a DevOS integration contract, not an instruction that every external model must emit those exact words.

## Required host input

```yaml
invocation: DEVOS | DEVOS::<STANCE> | DEVOS::<STANCE>::<STYLE>
repository_root: path supplied by the host
```

The host may locate a repository through a workspace, connected project, cloned repository, or explicitly selected directory. It must not fabricate a repository root from chat memory.

## Statuses

| Status | Meaning | DevOS integration response |
|---|---|---|
| `NOT_INVOKED` | No DevOS code or registered alias was supplied. | Continue ordinary host behavior. |
| `INVALID_INVOCATION` | The user wrote an invalid DevOS expression. | Show accepted syntax; do not guess a stance. |
| `DEVOS_NOT_AVAILABLE` | No usable repository root or DevOS bootstrap surface is available. | Request repository selection or report the context limitation. |
| `PROJECT_UNKNOWN` | A partial DevOS bootstrap surface was found. | HOLD; recover/repair context under normal project rules. |
| `READY_FOR_BOOTSTRAP` | Repository evidence is present. | Perform repository-first bootstrap before material work. |

## `DEVOS::GOD` boundary

`DEVOS::GOD` is a user preference for maximum routine autonomy only within the host's existing instructions, current user authorization, project scope, Security Gate, and verification rules. It does not grant approval, override policies, provider access, execution evidence, production authority, or remote mutation permission.

The reference resolver always emits:

```text
host_policy: UNCHANGED
authority: UNCHANGED
authorization: UNCHANGED
execution: NONE
mutation: NONE
```

## Any-chat compatibility

The protocol is host-neutral, but no host is compelled to use it. A ChatGPT Custom GPT, Codex skill, Claude plugin, MCP/App adapter, IDE agent, or future compatible host may call the resolver. A host without repository access can report that project context is unavailable; it cannot honestly claim DevOS was loaded.

## Inter-AI and free-model transport

The protocol has a zero-dependency fallback: [`DEVOS-ACTIVATE.md`](../DEVOS-ACTIVATE.md). A user may provide its public raw URL or copy/paste its project workflow request into any AI chat, including a free model without plugin, MCP, API, or workspace support.

This transport supplies user project guidance only. It neither grants missing capabilities nor instructs an AI to alter its governing behavior. A model with repository access can recover current state. A model without access should state the limitation rather than invent source, Git, CI, or current project facts.

## Bootstrap after readiness

After `READY_FOR_BOOTSTRAP`, a compatible DevOS host must:

1. read the nearest `AGENTS.md` and applicable bootstrap protocol;
2. recover `.ai/CURRENT-STATE.md`, `.ai/TASKS.md`, `.ai/DECISIONS.md`, and relevant session provenance;
3. inspect source, Git, configuration, tests, and relevant CI evidence;
4. interpret the actual user request through P15;
5. continue through P16, P17, controller, runtime, verification, and durable state rules as applicable.

Discovery is not bootstrap completion and bootstrap is not execution.

## Safety invariants

```text
HOST POLICY != DEVOS LABEL
STANCE != REPOSITORY EVIDENCE
STANCE != AUTHORIZATION
BOOTSTRAP != EXECUTION
CHAT MEMORY != DEVOS PROJECT CONTEXT
PROVIDER CREDENTIAL != DEVOS AUTHORIZATION
COPIED WORKFLOW CARD != REPOSITORY ACCESS
```
