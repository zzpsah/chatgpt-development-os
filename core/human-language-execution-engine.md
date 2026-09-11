# Human Language Execution Engine v1

## Purpose

The Human Language Execution Engine converts natural-language requests into safe, evidence-driven engineering workflows without requiring the user to know internal command names.

Core transformation:

`Human phrase → Canonical intent → Workflow → Scope → Authorization → Evidence → Action → Verification → Persistence`

The engine is an interpretation and routing layer. It does not replace project routing, source inspection, workflow rules, security controls, or verification.

## 1. Canonical intent

Natural-language variants should normalize to a small set of stable engineering intents. Examples:

| Canonical intent | Typical language | Workflow |
|---|---|---|
| `RESUME_WORK` | continue, resume, pick up where we stopped | `workflows/resume.md` |
| `BUG_FIX` | fix this, this is broken, remove this bug | `workflows/bug-fix.md` |
| `FEATURE_CHANGE` | add, build, change, implement | `workflows/feature.md` |
| `VALIDATION` | check it, test it, is it correct? | `workflows/review.md` + applicable tests |
| `SECURITY_REVIEW` | security dekh, check security | `workflows/review.md` + security rules |
| `INVESTIGATE` | why is this happening? what is wrong? | inspect → diagnose → explain |
| `QUALITY_IMPROVEMENT` | make it better/professional | inspect → prioritize → improve |
| `DATABASE_IMPLEMENTATION` | db bana de, database change | inspect schema → design → migration → verify |
| `EXPLAIN_CHANGE` | what did you do? explain this | inspect change → explain evidence |

The canonical intent is stable even when the user's wording, language, emotion, or slang changes.

## 2. Interpretation rules

1. Interpret meaning, not exact keywords.
2. Use the current project context and conversation context to disambiguate.
3. Treat slang, Hinglish, humor, frustration, and profanity as valid language signals.
4. Separate emotional signal from technical intent.
5. Do not treat emotional intensity as authorization.
6. If multiple canonical intents are clearly present, compose them in a safe order rather than forcing the user to repeat themselves.
7. If ambiguity could select the wrong project or materially change a technical outcome, clarify before acting.
8. Preserve explicit user constraints and project constraints.

## 3. Intent normalization

Normalization should produce a structured internal representation conceptually equivalent to:

```yaml
intent:
  canonical: FEATURE_CHANGE
  confidence: HIGH | MEDIUM | LOW
  user_phrase: "the original request"
  emotional_signal: NONE | URGENT | FRUSTRATED | PRAISE | OTHER
  project_reference: "resolved project or unknown"
  scope: "known scope or unknown"
  authorization: NOT_REQUIRED | REQUIRED | ALREADY_GRANTED
  workflow: "selected workflow"
```

`confidence` describes interpretation confidence, not implementation correctness.

## 4. Multiple intents

When a request contains multiple compatible intents, combine them without losing safety boundaries.

Example:

`"Continue and fix the registration bug, then check security."`

becomes:

`RESUME_WORK → BUG_FIX → SECURITY_REVIEW → VALIDATION`

The engine should not silently broaden a request into unrelated feature work.

## 5. Authorization boundary

Interpretation does not grant authority.

- Reading, analysis, explanation, and ordinary validation may proceed when appropriate.
- Code changes require the authorization implied by the current request/workflow.
- Production-impacting, destructive, irreversible, security-sensitive, or data-affecting operations require appropriate explicit authorization.
- A phrase such as `gand faad de`, `bakchodi fix kar`, or other profanity never bypasses a safety gate.

## 6. Evidence boundary

For important conclusions, distinguish:

- **Observed** — directly verified.
- **Likely** — evidence-supported but not conclusive.
- **Unknown** — not established.

Intent confidence must never be confused with technical evidence. A HIGH-confidence interpretation can still lead to an UNKNOWN technical root cause.

## 7. Workflow routing

After normalization:

1. Resolve the project with `core/project-router.md`.
2. Load the project's durable `.ai` context.
3. Select the appropriate workflow.
4. Inspect actual source/configuration/tests/Git as required.
5. Determine scope and authorization.
6. Execute the smallest appropriate action when authorized.
7. Verify the result with applicable evidence.
8. Persist meaningful semantic progress in project context.

## 8. Verification contract

Every execution path should end in one of these states:

- `VERIFIED` — appropriate checks provide sufficient evidence for the claim.
- `PARTIAL` — some checks passed, but meaningful limitations remain.
- `UNVERIFIED` — the requested outcome has not been adequately checked.
- `FAILED` — verification demonstrates the intended outcome is not working.

Never infer success from the absence of an error message alone.

## 9. Learning behavior

The engine should hide unnecessary internal terminology from the user. When the user asks to learn, it should expose the mapping gradually:

`what you said → what DevOS understood → what workflow that means → what was checked → what changed`

This supports progressive developer growth without lowering engineering rigor.

## 10. Safety invariant

> **Simple language for the human; rigorous engineering underneath.**

Natural language makes the interface easier. It does not weaken evidence, authorization, security, or verification requirements.

## Scope of v1

Included:
- canonical intent normalization;
- workflow routing;
- multiple-intent composition;
- authorization preservation;
- evidence/verification expectations;
- integration with existing project routing and workflows.

Not included:
- autonomous interpretation of every possible human phrase;
- probabilistic model implementation;
- bypassing project or security rules;
- claiming application correctness without executing appropriate checks.
