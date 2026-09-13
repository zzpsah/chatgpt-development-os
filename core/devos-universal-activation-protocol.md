# DevOS Universal Activation Protocol v1

## Purpose

This protocol makes a DevOS stance usable from any compatible AI host without pretending that a copied phrase, chat memory, provider credential, or model identity has loaded DevOS.

`DEVOS`, `DEVOS::CONTINUE`, and `DEVOS::GOD` are activation requests. They become an active DevOS workflow only after the host finds a repository-local DevOS bootstrap surface.

## Activation flow

```text
User writes DEVOS::<STANCE>
  -> host invokes DEVOS-UNIVERSAL-ACTIVATION-v1
  -> parse the registered stance
  -> discover repository-local AGENTS.md + .ai/manifest.yaml
  -> validate required durable state files
  -> READY_FOR_BOOTSTRAP | DEVOS_NOT_AVAILABLE | PROJECT_UNKNOWN | INVALID_INVOCATION
  -> repository-first bootstrap and governed workflow
```

The reference entrypoint is `tools/devos-universal-activation.py`.

## Required host input

```yaml
invocation: DEVOS | DEVOS::<STANCE> | DEVOS::<STANCE>::<STYLE>
repository_root: path supplied by the host
```

The host may locate a repository through a workspace, connected project, cloned repository, or explicitly selected directory. It must not fabricate a repository root from chat memory.

## Statuses

| Status | Meaning | Host response |
|---|---|---|
| `NOT_INVOKED` | No DevOS code or registered alias was supplied. | Continue ordinary host behavior. |
| `INVALID_INVOCATION` | The user wrote an invalid DevOS expression. | Show accepted syntax; do not guess a stance. |
| `DEVOS_NOT_AVAILABLE` | No usable repository root or DevOS bootstrap surface is available. | Ask the host/user to select or connect the repository. |
| `PROJECT_UNKNOWN` | A partial DevOS bootstrap surface was found. | HOLD; recover/repair context under normal project rules. |
| `READY_FOR_BOOTSTRAP` | Repository evidence is present. | Perform repository-first bootstrap before material work. |

## `DEVOS::GOD` boundary

`DEVOS::GOD` selects maximum routine autonomy only within current user authorization, project scope, Security Gate, and verification rules. It does not grant approval, provider access, execution evidence, production authority, or remote mutation permission.

The activation resolver always emits:

```text
authority: UNCHANGED
authorization: UNCHANGED
execution: NONE
mutation: NONE
```

## Any-chat compatibility

The protocol is host-neutral. A ChatGPT Custom GPT, Codex skill, Claude plugin, MCP/App adapter, IDE agent, or future compatible host may call the same resolver. A host without repository access can recognize the request, but it must report `DEVOS_NOT_AVAILABLE`; it cannot honestly claim DevOS was loaded.

## Bootstrap after readiness

After `READY_FOR_BOOTSTRAP`, the host must:

1. read the nearest `AGENTS.md` and applicable bootstrap protocol;
2. recover `.ai/CURRENT-STATE.md`, `.ai/TASKS.md`, `.ai/DECISIONS.md`, and relevant session provenance;
3. inspect source, Git, configuration, tests, and relevant CI evidence;
4. interpret the actual user request through P15;
5. continue through P16, P17, controller, runtime, verification, and durable state rules as applicable.

Activation is not bootstrap completion and bootstrap is not execution.

## Safety invariants

```text
STANCE != REPOSITORY EVIDENCE
STANCE != AUTHORIZATION
BOOTSTRAP != EXECUTION
CHAT MEMORY != DEVOS ACTIVATION
PROVIDER CREDENTIAL != DEVOS AUTHORIZATION
```
