# Automatic Project Context

Development OS has two automation layers. **GitHub-side synchronization is the current priority. Local-PC automation is optional and can be added later.**

## A. GitHub repositories — automatic `.ai` synchronization

Managed repositories can include the caller workflow:

```text
.github/workflows/context-sync.yml
```

The Development OS template now includes this caller. It invokes the reusable workflow in the Development OS repository on every push to `main` or `master`.

The synchronizer automatically:

1. records the pushed commit and changed paths in `.ai/CHANGELOG.md`;
2. classifies the push as `meaningful` or `routine` using deterministic path rules;
3. updates `.ai/CURRENT-STATE.md` for meaningful changes with the latest verified repository event;
4. preserves existing project context instead of replacing it;
5. commits the generated context update with the `[devos-context-sync]` marker;
6. ignores its own synchronization commit so it does not recurse forever.

It does **not** invent product requirements, architecture rationale, task meaning, test results, or security conclusions. Those semantic facts remain the responsibility of the AI workflow or developer. The automation records repository evidence only.

### What is automatic vs. AI-owned

| Information | Automatic sync | AI / developer |
|---|---:|---:|
| Commit SHA/date/author | Yes | — |
| Changed paths | Yes | — |
| Routine/meaningful classification | Yes | Can refine later |
| Recent repository event | Yes | — |
| Project purpose | No | Yes |
| Architecture decisions | No | Yes |
| Task interpretation | No | Yes |
| Test result claims | No | Yes, only with evidence |
| Security conclusions | No | Yes, after review |

A repository created from `templates/project` receives the caller workflow automatically. Existing repositories need the caller added once (or another GitHub-level deployment mechanism such as an organization/app rollout).

## B. Local folders — Windows watcher

This remains available for later use. Run once on the PC:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
cd <path-to-chatgpt-development-os>\tools
.\install-windows.ps1 -Roots 'D:\Projects','C:\Users\<you>\Documents\Projects'
```

The watcher starts at Windows logon and observes configured roots recursively. When project markers are detected, it initializes `.ai/` if missing. Existing context files are never overwritten.

**Important:** Do not watch an entire drive such as `C:\` unless intentionally required. Dedicated project roots are safer.

## C. Existing Git repositories

For a repository that is not yet managed:

```powershell
.\init-project.ps1 -Path 'D:\Projects\MyApp'
```

Then add the project-side GitHub caller workflow if GitHub synchronization is desired.

## Safety and persistence

- Initialization is idempotent and preserves existing context.
- `.ai/` must never contain secrets, credentials, tokens, private keys, or unnecessary personal data.
- Automation must not overwrite semantic context blindly.
- Source code, version-control history, and project-local `.ai/` context remain the durable project record.
- The automation mechanism itself is not the source of truth.
