# Security Gate Workflow

Use when security is explicitly requested or when the change touches authentication, authorization, sensitive data, database/storage access, uploads, secrets, external exposure, deployment, or other material security surfaces.

1. Resolve the project and load applicable `AGENTS.md`, `.ai/` context, project requirements, and security baseline.
2. Identify affected assets, trust boundaries, entry points, users, data, and changed components.
3. Run the applicable stages from `core/security-gate.md`.
4. Inspect actual source, configuration, dependencies, deployment settings, database/storage policies, and tests as relevant.
5. Record findings with evidence and severity.
6. Determine `PASS`, `CONDITIONAL`, `BLOCKED`, `NOT_APPLICABLE`, or `UNVERIFIED`.
7. Identify residual risk and controls not checked.
8. Obtain appropriate authorization before security-sensitive production, destructive, credential-affecting, or data-affecting changes.
9. Verify implemented fixes using applicable checks.
10. Persist meaningful security decisions/findings without storing secrets or unnecessary sensitive data.
11. Report what was checked, evidence found, limitations, residual risk, and recommended next action.

## Decision rule

A clean review means **no blocking finding was identified in the controls actually checked**. It does not mean the system is absolutely secure.

## Minimum report

`Scope → Controls checked → Findings → Evidence → Severity → Status → Residual risk → Verification → Authorization`
