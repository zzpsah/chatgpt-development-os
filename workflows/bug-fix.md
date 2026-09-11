# Bug-Fix Workflow

Use when the user reports something broken, incorrect, unstable, or unexpected.

1. Restate the observed behavior and expected behavior.
2. Inspect relevant code, configuration, logs, issues, tests, and CI evidence.
3. Identify the most likely root cause; distinguish evidence from hypotheses.
4. Reproduce or validate the failure where possible.
5. Implement a focused fix.
6. Use the Verification / Test Engine (`core/verification-engine.md`) to identify the regression check and other applicable checks.
7. Execute the failure-case regression test and relevant focused checks when supported and authorized.
8. Review security and side effects.
9. Classify evidence as Observed, Likely, or Unknown and assign `VERIFIED`, `PARTIAL`, `UNVERIFIED`, or `FAILED` honestly.
10. Update documentation/context if behavior changed.
11. Report root cause, fix, verification evidence, limitations, and any remaining uncertainty.

Do not claim a bug is fixed merely because the code changed or because a test was proposed. If an applicable regression check cannot be run, state the limitation explicitly.
