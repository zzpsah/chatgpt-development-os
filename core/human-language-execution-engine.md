# Human Language Execution Engine v2

## Purpose

The Human Language Execution Engine converts natural-language requests into safe, evidence-driven engineering workflows without requiring the user to know internal command names. v2 adds executable, context-aware interpretation for short, elliptical, typo-prone, Hinglish, and referential requests.

Core transformation:

`Human phrase + explicit context → normalized meaning → canonical intent → constraints → confidence/ambiguity → route or clarify → normal DevOS gates`

The engine is an interpretation and routing layer. It never grants authority and never executes a technical action by itself.

## Canonical intents

Stable intents include `RESUME_WORK`, `BUG_FIX`, `FEATURE_CHANGE`, `VALIDATION`, `SECURITY_REVIEW`, `INVESTIGATE`, `QUALITY_IMPROVEMENT`, `DATABASE_IMPLEMENTATION`, and `EXPLAIN_CHANGE`.

Meaning is more important than exact keywords. Hinglish, shorthand, spelling variation, humor, frustration, and profanity are valid language signals but never authorization signals.

## Contextual ellipsis and referents

v2 may resolve short phrases such as `kr do`, `wahi continue`, `isko kro`, `same wala`, or `pehle wala` only from explicit supplied context such as the current project, last objective, and last canonical intent.

A short command may inherit a prior objective when the referent is unambiguous. If the required referent is missing, the engine returns `CLARIFY` rather than inventing one.

Examples:

- prior objective `Fix registration form validation` + `kr do` → inherit `BUG_FIX` objective;
- prior objective + `wahi continue` → resume the same bounded objective;
- no prior objective + `isko kro` → `CLARIFY / MISSING_REFERENT`.

## Explicit constraints

Negative constraints are first-class interpretation output. Examples include `deploy mat karna`, `delete mat karna`, and `merge mat karna`. They must survive downstream routing and cannot be silently discarded by a more general action intent.

## Confidence and ambiguity

The reference interpreter emits `HIGH`, `MEDIUM`, or `LOW` confidence and explicit ambiguity reasons. Low confidence produces `CLARIFY`; high/medium confidence may produce `ROUTE` to the normal DevOS controller path.

Confidence is interpretation confidence only. It is not evidence that the requested technical outcome is correct.

## Multiple intents

Compatible intents may be composed safely. A generic action phrase must not dilute a more specific intent. Ambiguous multi-intent requests remain visible to downstream routing instead of silently broadening scope.

## Authorization boundary

Interpretation does not grant authority. All outputs preserve `authorization: UNCHANGED` and `execution: NONE`.

Production-impacting, destructive, irreversible, security-sensitive, database/data-affecting, deployment, and other higher-impact operations remain subject to their existing explicit authorization, Security Gate, runtime, and verification contracts. Emotional intensity, slang, or a high-confidence interpretation never bypasses these gates.

## Evidence boundary

Important conclusions remain `Observed`, `Likely`, or `Unknown`. Intent confidence must never be confused with technical evidence. A HIGH-confidence interpretation can still lead to an UNKNOWN technical root cause.

## Executable reference interpreter

`tools/human-language-interpreter.py` is the deterministic v2 reference layer. Its input contains an `utterance` plus optional explicit context. Its output includes:

- canonical intent(s);
- resolved objective/project when available;
- whether context was inherited;
- preserved negative constraints;
- confidence and ambiguity reasons;
- `ROUTE` or `CLARIFY`;
- unchanged authorization and no execution authority.

`tools/test-human-language-interpreter.py` covers direct requests, Hinglish, short continuation, referential phrases, missing referents, and negative deployment constraints. The test is wired into contract CI.

## Workflow routing

After interpretation:

1. resolve the project with repository-first evidence;
2. load durable `.ai` context;
3. preserve interpreted constraints;
4. select the applicable workflow/controller path;
5. inspect actual source/config/tests/Git;
6. independently determine scope and authorization;
7. execute only through an authorized runtime capability;
8. verify with fresh applicable evidence;
9. persist meaningful semantic progress.

## Safety invariant

> **Understand the smallest human phrase possible; invent the least possible; preserve every safety boundary.**

## Scope of v2

Included: executable deterministic reference interpretation, contextual ellipsis, short-command inheritance, referent detection, Hinglish/shorthand patterns, negative constraints, explicit ambiguity/confidence, and CI regression coverage.

Not included: unrestricted probabilistic mind-reading, silent cross-project guessing, authorization inference from emotion or brevity, or bypassing project/security/verification rules.
