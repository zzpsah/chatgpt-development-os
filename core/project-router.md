# Project Router

## Purpose
Project Router maps a user's natural-language reference to the correct managed project before substantial work begins.

The router is a resolution layer, not the source of project truth. The selected repository and its project-local `.ai/` context remain authoritative.

## Resolution order

1. Explicit repository/path supplied by the user.
2. Explicit project name or alias matching `projects/registry.md`.
3. A project name mentioned in the current conversation when it unambiguously identifies a managed project.
4. Active project from the current workflow/session, when supported by durable evidence.
5. If multiple projects remain plausible, ask one concise clarification instead of guessing.

## Examples

| User request | Route |
|---|---|
| `Continue Tetahali` | `zzpsah/umv-tetahali` |
| `Continue Sahaspur` | `zzpsah/umvsahaspur` |
| `Work on photo signature` | `zzpsah/photo-signature-studio` |
| `Continue the staging project` | `zzpsah/umv-tetahali-staging` when registry/context confirms |
| `What have we done?` | Resolve the active/referenced project, then recover its durable state |

## Recovery after routing

Once a project is resolved:

1. Read its `AGENTS.md`.
2. Read `.ai/manifest.yaml`.
3. Read `.ai/STATE-INDEX.md` when present.
4. Read `.ai/PROJECT.md` and `.ai/CURRENT-STATE.md`.
5. Read relevant `.ai/TASKS.md`, `.ai/DECISIONS.md`, `.ai/ARCHITECTURE.md`, and recent `.ai/CHANGELOG.md`/session records.
6. Inspect the actual source, tests, configuration, and Git state before making important claims.
7. Determine the user's requested intent from the recovered state and current request.

## Safety

- Never select a project merely because its name is similar when another project is plausible.
- Never treat the registry as a substitute for project-local context.
- Never copy one project's context into another project.
- Do not expose secrets or unnecessary personal/student data while routing or reporting state.
- If routing is ambiguous and proceeding could modify the wrong project, stop and ask.

## Future automation

The router can later be backed by a local worker, GitHub App, or other integration that discovers managed repositories. Such automation must preserve the same resolution order and safety rules.
