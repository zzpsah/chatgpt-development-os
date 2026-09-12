# Human Language Execution Engine v2

## Purpose

The Human Language Execution Engine converts natural-language requests into safe, evidence-driven engineering workflows without requiring the user to know internal command names.

Core transformation:

`Human phrase + conversation context + project state → Canonical intent(s) + constraints + ambiguity → Workflow → Scope → Authorization → Evidence → Action → Verification → Persistence`

The engine is an interpretation and routing layer. It never grants authority and does not replace project routing, source inspection, workflow rules, security controls, or verification.

## Canonical intents

Stable intents include `RESUME_WORK`, `BUG_FIX`, `FEATURE_CHANGE`, `VALIDATION`, `SECURITY_REVIEW`, `INVESTIGATE`, `QUALITY_IMPROVEMENT`, `DATABASE_IMPLEMENTATION`, and `EXPLAIN_CHANGE`. Wording, language, slang, emotion, spelling quality, or brevity must not redefine authorization.

## Contextual interpretation

v2 treats short and elliptical language as first-class input. Phrases such as `continue`, `kr do`, `wahi continue`, `same wala`, `jo error tha fix`, and `pehle wala` may inherit a referent only from explicit available context such as the previous interpreted intent, active objective, resolved project, or durable project state.

The interpreter must:

1. interpret meaning rather than exact keywords;
2. tolerate common Hinglish/code-switching and shorthand;
3. resolve pronouns/deictic phrases (`ye`, `wo`, `wahi`, `this`, `that`, `same`) only when a usable referent exists;
4. preserve corrections and negative constraints such as `deploy mat karna`;
5. compose multiple compatible intents rather than dropping them;
6. distinguish interpretation confidence from technical evidence;
7. clarify when project, intent, or referent ambiguity is material;
8. never infer high-impact authorization from context, urgency, profanity, or prior low-impact authorization.

## Executable pre-interpreter

`tools/human-language-interpreter.py` provides a deterministic v2 pre-interpreter for common language forms. It emits a structured envelope containing:

```yaml
protocol: DEVOS-HUMAN-LANGUAGE-v2
intents: []
project: null
objective: null
constraints: []
context_used: false
confidence: HIGH | MEDIUM | LOW
ambiguity: []
decision: INTERPRETED | CLARIFY
authorization: UNCHANGED
authority: UNCHANGED
execution: NONE
```

This deterministic layer is intentionally not presented as universal natural-language understanding. A host AI/model may provide richer semantic interpretation, but the resulting objective remains subject to the same project, authorization, security, evidence, and verification contracts.

## Short-command rule

Shortness alone is not ambiguity. `continue` can be sufficient when the active project/objective is established. Conversely, a long sentence can remain ambiguous. Clarification is required only when unresolved ambiguity could materially select the wrong project, referent, objective, or high-impact action.

## Constraints and negation

Negative constraints are durable for the interpreted objective and must not be lost during intent composition. For example:

`pehle wala hi but deploy mat karna`

may resolve the prior objective while adding `DO_NOT_DEPLOY`. A negative constraint never becomes a positive authorization later merely because work continues.

## Authorization boundary

Interpretation does not grant authority. Reading and ordinary analysis may proceed under their normal rules. Production-impacting, destructive, irreversible, security-sensitive, deployment, merge, database, credential, or other high-impact operations remain independently gated. The v2 interpreter explicitly returns `authorization: UNCHANGED`, `authority: UNCHANGED`, and `execution: NONE`.

## Evidence boundary

For technical conclusions distinguish `Observed`, `Likely`, and `Unknown`. HIGH interpretation confidence does not establish implementation correctness or root cause.

## Workflow routing

After interpretation: resolve the project; load durable `.ai` context; select workflow; inspect actual source/config/tests/Git; determine scope and authorization; execute the smallest authorized action; verify with fresh applicable evidence; persist meaningful semantic progress.

## Verification contract

Execution outcomes remain `VERIFIED`, `PARTIAL`, `UNVERIFIED`, or `FAILED`. Never infer success from absence of an error.

## Test corpus

`tools/test-human-language-interpreter.py` exercises short commands, contextual continuation, Hinglish shorthand, referential language, multi-intent phrases, explicit negative deployment constraints, unknown-context clarification, and high-impact authorization escalation. It runs in the contract CI suite.

## Safety invariant

> **Understand the smallest human phrase that context can safely complete; never complete missing authority.**

Simple language for the human; rigorous engineering underneath.
