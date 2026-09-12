# Human Command Interpretation Layer v1

## Purpose

This layer turns short, casual, typo-tolerant human messages into bounded DevOS intent without requiring the user to learn internal command syntax.

Examples:

- `continue`, `continiue`, `wahi se continue` → `RESUME_WORK`
- `ok`, `haan`, `do it` → `CONFIRM_CURRENT_PLAN` when a current objective exists; otherwise remain ambiguous
- `fix this bug and check security` → `BUG_FIX → SECURITY_REVIEW`
- `isko production grade bana` → `QUALITY_IMPROVEMENT → FEATURE_CHANGE`
- `kya pending hai?` → `STATUS_QUERY`
- `ruk ja` → `STOP_WORK`

The implementation is deliberately deterministic. It is a routing primitive, not a claim that every natural-language request can be understood perfectly.

## Interpretation contract

`human phrase → normalized phrase → canonical intent(s) → bounded action → existing gates`

The interpreter may use the supplied current objective/scope as context, but it must not invent a project, scope, authority, evidence, or completion state.

### Canonical intents

| Intent | Meaning |
|---|---|
| `RESUME_WORK` | recover the active objective and select the next bounded work unit |
| `CONFIRM_CURRENT_PLAN` | confirm continuation only when a current objective is known |
| `STOP_WORK` | hold autonomous continuation |
| `STATUS_QUERY` | report repository/durable-state status |
| `EXPLAIN_CHANGE` | route to evidence-backed explanation |
| `BUG_FIX` | route to bug-fix workflow |
| `SECURITY_REVIEW` | route to security review |
| `QUALITY_IMPROVEMENT` | route to bounded hardening/improvement |
| `FEATURE_CHANGE` | route to feature workflow |
| `AUTHORIZATION_ESCALATION` | blocked request attempting to bypass or weaken authorization/security |

Multiple compatible intents are returned in the order they occur in the user's message. Duplicate intents are collapsed.

## Safety boundaries

1. Interpretation never grants authorization.
2. `ok`/`haan` without a recoverable current objective remains `AMBIGUOUS` and does not execute.
3. Requests to bypass/disable security or authorization, or force production, become `BLOCKED` with `execution: NONE`.
4. `STOP_WORK` always produces a hold action.
5. Unknown language remains `AMBIGUOUS` instead of being guessed into a technical action.
6. The interpreter delegates actual work only after the existing controller, authorization, security, runtime, verification, and persistence boundaries.

## Relationship to Human Language Execution Engine v1

`core/human-language-execution-engine.md` remains the normative semantic contract. This layer provides a small executable normalization primitive beneath that contract. It does not replace project routing, workflow selection, controller gates, Security Gate, runtime restrictions, or repository persistence.

## Verification

`tools/test-devos-command-interpreter.py` exercises common English/Hinglish commands, typo tolerance, multi-intent ordering, confirmation with and without context, authorization escalation, and unknown-language fail-closed behavior.

The executable checks verify deterministic mapping and safety boundaries only; they do not establish general semantic AI understanding.
