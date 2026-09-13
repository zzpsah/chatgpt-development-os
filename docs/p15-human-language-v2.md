# P15 — Human Language Execution Engine v2

## Goal
Make DevOS reliably understand small, messy, context-dependent human instructions while reducing unnecessary clarification and preserving strict engineering/safety boundaries.

## Acceptance criteria
- Short continuation commands can inherit an explicit prior objective and intent.
- Referential commands do not invent missing referents.
- Common Hinglish/shorthand maps to stable canonical intents.
- Explicit negative constraints survive interpretation.
- Confidence and ambiguity are machine-readable.
- Low-confidence materially ambiguous requests clarify instead of executing.
- Interpretation never changes authorization or directly executes work.
- Regression tests run in primary contract CI.
- Existing DevOS contract verification remains green.

## Non-goals
- unrestricted natural-language understanding;
- probabilistic guessing across unknown projects;
- treating confidence as technical evidence;
- inferring production/destructive authorization;
- replacing repository-first recovery, controller, Security Gate, runtime, or verification.

## Completion evidence
P15 remains active until fresh CI verifies the v2 interpreter and the broader DevOS contracts.
