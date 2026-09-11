# Feature Workflow

Use when the user wants a new capability or meaningful change.

1. Understand the desired outcome.
2. Identify the project.
3. Inspect the current implementation and constraints.
4. Define acceptance criteria.
5. Choose architecture and implementation approach.
6. Implement the smallest coherent change.
7. Invoke the Verification / Test Engine (`core/verification-engine.md`) to detect applicable checks.
8. Execute focused static/unit/integration/E2E/runtime checks as applicable and authorized; delegate to CI/project tooling when appropriate.
9. Review security and regressions.
10. Classify verification evidence and report `VERIFIED`, `PARTIAL`, `UNVERIFIED`, or `FAILED` honestly.
11. Update project context and documentation.
12. Report changed files, verification evidence, limitations, and remaining risks.

Do not claim correctness from an untested diff or from tests that were not actually run. For high-impact or destructive changes, obtain confirmation before execution when needed.
