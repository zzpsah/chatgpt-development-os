# Security Gate v1

## Purpose

The Security Gate is the mandatory safety layer for security-sensitive development work, releases, data changes, and high-impact operations.

It does not replace project-specific security requirements. It turns the existing security baseline into a repeatable decision gate.

Core flow:

`Scope → Threat surface → AuthN/AuthZ → Data access → Secrets → Inputs/uploads → Dependencies/config → Runtime boundaries → Verification → Residual risk → Authorization`

## 1. When the gate applies

Run the Security Gate when:

- the user explicitly requests a security review;
- authentication, authorization, sessions, permissions, or public/private boundaries change;
- database access, RLS, storage permissions, or sensitive data handling changes;
- file upload/download behavior changes;
- secrets, credentials, tokens, keys, or configuration handling changes;
- external integrations or network-facing behavior changes materially;
- production, deployment, infrastructure, or destructive operations are involved;
- a bug or feature creates a credible security impact.

For low-risk documentation-only changes with no security relevance, the full gate may be marked not applicable with a reason.

## 2. Security review stages

### Stage A — Scope
Identify changed components, affected data, trust boundaries, entry points, and intended users.

### Stage B — Authentication and authorization
Check identity verification, role/permission checks, server-side enforcement, and least privilege.

### Stage C — Data access and privacy
Check database queries, RLS or equivalent controls, exposure of student/staff/identity/portal records, and unnecessary logging or copying of sensitive data.

### Stage D — Secrets and credentials
Check that credentials, tokens, private keys, session cookies, and other secrets are not committed, exposed in client code, logs, screenshots, or documentation.

### Stage E — Inputs and uploads
Check validation of input, file type, size, content, destination, and relevant injection or path-traversal risk.

### Stage F — Dependencies and configuration
Check dependency risk, unsafe defaults, exposed services, environment configuration, CORS/public exposure where relevant, and debug/development settings.

### Stage G — Runtime and deployment boundaries
For production or infrastructure changes, check network exposure, service permissions, deployment configuration, storage/database access, rollback or recovery considerations, and impact scope.

### Stage H — Verification
Record concrete evidence from code review, tests, static checks, configuration review, or security tooling. Absence of findings is not proof of absolute security.

## 3. Security decision states

Use:

- `PASS` — reviewed applicable controls with sufficient evidence and no blocking finding identified.
- `CONDITIONAL` — work may proceed only with explicit handling of listed residual risks or conditions.
- `BLOCKED` — a security issue or missing control prevents safe progression.
- `NOT_APPLICABLE` — the gate is genuinely irrelevant to the change, with a documented reason.
- `UNVERIFIED` — the relevant security property could not be adequately checked.

## 4. Severity

Classify findings:

- `CRITICAL` — credible severe impact such as broad unauthorized access, exposed credentials, destructive compromise, or equivalent.
- `HIGH` — material unauthorized access, sensitive-data exposure, or significant control failure.
- `MEDIUM` — meaningful weakness requiring remediation but with narrower scope or stronger preconditions.
- `LOW` — limited-risk improvement or defense-in-depth issue.
- `INFO` — observation or hardening suggestion without a demonstrated security impact.

Do not assign severity merely from intuition; describe the affected asset, condition, impact, and evidence.

## 5. Authorization rules

Security review and implementation are different authorities.

- Reviewing code/configuration may proceed when relevant access exists.
- Fixing a security issue follows the authorization of the current request/workflow.
- Production, destructive, irreversible, credential-affecting, or sensitive-data operations require appropriate explicit authorization.
- A security finding never automatically authorizes a production change.

## 6. Evidence discipline

For every material security conclusion, distinguish:

- **Observed** — directly verified.
- **Likely** — evidence-supported but not conclusive.
- **Unknown** — not established.

Never state that a system is “100% secure.” Report what was checked, what was not checked, and residual risk.

## 7. Output contract

A security gate result should conceptually contain:

```yaml
scope:
status: PASS | CONDITIONAL | BLOCKED | NOT_APPLICABLE | UNVERIFIED
findings:
  - severity: CRITICAL | HIGH | MEDIUM | LOW | INFO
    area:
    description:
    evidence:
    recommendation:
controls_checked: []
controls_not_checked: []
residual_risk: []
authorization:
verification_evidence: []
```

## 8. Integration contract

The Security Gate must be invoked by:

- `SECURITY_REVIEW` intent in the Human Language Execution Engine;
- the Review workflow when security is relevant;
- Feature and Bug-Fix workflows for security-sensitive changes;
- the Verification/Test Engine when security verification is applicable;
- Resume when the highest-priority unfinished work is a security or data-loss risk.

## 9. Safety invariants

1. Never expose or commit secrets.
2. Never use emotional urgency as authorization.
3. Never treat lack of a known vulnerability as proof of security.
4. Never silently weaken authorization, RLS, privacy, or public/private boundaries.
5. Never copy unnecessary sensitive education or personal data into AI context.
6. Never claim a security review occurred without evidence that it was performed.
7. Preserve project-specific security requirements in addition to this baseline.

## 10. v1 scope

Included:
- security review trigger conditions;
- security review stages;
- severity model;
- PASS / CONDITIONAL / BLOCKED / NOT_APPLICABLE / UNVERIFIED states;
- evidence and residual-risk discipline;
- authorization boundaries;
- workflow and verification integration requirements.

Not included:
- automatic exploitation or penetration testing;
- complete SAST/DAST implementation for every technology;
- automatic vulnerability remediation without authorization;
- guarantees of complete security.
