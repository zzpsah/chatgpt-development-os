# Resume Workflow

Use when the user asks to continue, resume, pick up previous work, or asks what remains.

1. Resolve the project using `core/project-router.md`.
2. Read the project's durable context: `AGENTS.md`, `.ai/manifest.yaml`, `.ai/STATE-INDEX.md`, `.ai/PROJECT.md`, `.ai/CURRENT-STATE.md`, and relevant tasks, decisions, architecture, changelog, and session records.
3. Run the AI State Resolver v1 from `core/ai-state-resolver.md` against the recovered evidence.
4. Classify the recovered situation as Observed, Likely, or Unknown and determine active, blocked, and planned work.
5. Check recent commits, open issues/PRs, and documented blockers where relevant.
6. Inspect actual source, tests, configuration, deployment files, and Git state to validate important semantic assumptions. The resolver does not replace source inspection.
7. Reconstruct the current objective, verification status, and highest-priority unfinished work.
8. Continue the recommended unfinished work when the user's request authorizes continuation. Destructive, production-impacting, security-sensitive, irreversible, or data-affecting actions still require explicit authorization.
9. Implement the smallest appropriate change and perform the applicable verification.
10. Persist meaningful semantic progress in the project's `.ai` context, including tasks, decisions, current state, and session evidence where appropriate.
11. Allow deterministic project automation to update generated state such as `STATE-INDEX.md` and `CHANGELOG.md` from repository evidence.

## Resolver flow

```text
User request
    ↓
Project Router
    ↓
Durable project context
    ↓
AI State Resolver v1
    ↓
Observed / Likely / Unknown
    ↓
Active / Blocked / Planned work
    ↓
Verification status
    ↓
Candidate next actions
    ↓
Priority + risk + authorization
    ↓
Recommended action
    ↓
Inspect source → Implement → Verify → Persist
```

## Safety and evidence

- Do not guess the project when multiple plausible projects exist.
- Do not treat `STATE-INDEX.md` as semantic truth; it is generated repository evidence.
- Do not treat the last edited file as automatically being the next task.
- Do not infer correctness, test success, security, or deployment status from silence or absence of errors.
- Keep facts, likely interpretations, and unknowns separate.
- Do not expose secrets, tokens, passwords, private keys, session cookies, or unnecessary personal/student data.
- Do not convert emotional language into destructive authority.
- Preserve the distinction between recommendation and execution.
