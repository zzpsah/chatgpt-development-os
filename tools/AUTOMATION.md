# Automatic Project Context

The Development OS supports three levels of automatic context creation.

## A. Local folders — Windows watcher

Run once on the PC:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
cd <path-to-chatgpt-development-os>\tools
.\install-windows.ps1 -Roots 'D:\Projects','C:\Users\<you>\Documents\Projects'
```

The watcher starts at Windows logon and observes the configured roots recursively. When a newly created project directory or file is detected, it looks upward for project markers such as `.git`, `package.json`, `pyproject.toml`, or `requirements.txt`, then initializes `.ai/` if it is missing. Existing context files are never overwritten.

**Important:** Do not watch an entire drive such as `C:\` unless you intentionally want context detection across that drive. Configure dedicated project roots to avoid creating `.ai/` in unrelated folders.

## B. Git repositories

For a repository that already exists, run:

```powershell
.\init-project.ps1 -Path 'D:\Projects\MyApp'
```

For new repositories, use the project template under `templates/project` or run the initializer immediately after creating/cloning the repository.

## C. GitHub repositories

A GitHub repository cannot execute a local PC watcher merely because the repository was created. The portable solution is a repository template containing `AGENTS.md` and `.ai/`. A new repository created from that template starts with its project context. For an empty repository created without the template, initialize it once with the local initializer or an AI/automation that has write access.

## Safety and persistence

- The initializer is idempotent: it creates only missing files.
- It never writes secrets or credentials.
- Project memory belongs to the project, not to an AI account or GitHub account.
- The watcher is an automation mechanism, not the authoritative source of truth.
- If a folder is merely a document/archive folder and has no project markers, it is not treated as a software project by default.
