# Verification Workflow

Use after meaningful implementation, bug fixes, or review work when verification evidence is required.

1. Identify the exact changed scope and expected behavior.
2. Inspect repository tooling, tests, configuration, and CI to discover applicable checks.
3. Select focused checks first; expand to broader checks when risk or system boundaries justify it.
4. Execute supported read-only/static/test checks or delegate them to CI/project tooling.
5. Obtain explicit authorization before checks that can modify production, data, or protected external systems.
6. Record actual check results as evidence; distinguish Observed, Likely, and Unknown.
7. Determine status using `VERIFIED`, `PARTIAL`, `UNVERIFIED`, or `FAILED` semantics from `core/verification-engine.md`.
8. Do not claim a check ran when it was only proposed or assumed.
9. Report passed checks, failed checks, missing checks, limitations, and the justified conclusion.
10. Persist meaningful verification evidence in project-local context according to `AGENTS.md`.

Verification is evidence gathering, not authorization. A passing check does not authorize deployment or destructive operations.
