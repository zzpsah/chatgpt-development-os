# Review Workflow

Use when the user asks to check, review, validate, or assess existing work.

1. Resolve the project and understand the requested review scope.
2. Inspect the implementation, requirements, configuration, tests, and relevant Git/CI evidence.
3. Review correctness against requirements.
4. Review regression and edge-case risk.
5. Review maintainability and clarity.
6. Review security and privacy at a baseline level. If the request or change requires a dedicated security review, invoke `workflows/security.md` and `core/security-gate.md`.
7. Review performance where relevant.
8. Use the Verification / Test Engine (`core/verification-engine.md`) to identify and perform applicable checks.
9. Classify actual evidence as Observed, Likely, or Unknown.
10. Report findings by severity and report verification as `VERIFIED`, `PARTIAL`, `UNVERIFIED`, or `FAILED` according to the verification contract.
11. Keep unsupported correctness claims out of the review; absence of failures is not proof that checks passed.
12. Update documentation/context when the review changes durable project understanding.

Prioritize actionable findings by severity. Do not invent issues unsupported by the inspected code or evidence.
