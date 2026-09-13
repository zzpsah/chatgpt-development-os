# Human Language Execution Engine v2

## Status

Normative top-level DevOS input layer. Every human-originated DevOS request enters through this contract before project workflow selection, planning, execution, verification, or persistence.

## Purpose

The Human Language Execution Engine converts natural-language requests into safe, evidence-driven engineering workflows without requiring the user to know internal command names.

Core transformation:

`Human phrase + conversation context + durable project state → Canonical intent(s) + constraints + ambiguity → Project/Workflow → Scope → Authorization → Evidence → Action → Verification → Persistence`

Human-language interpretation is not an optional helper or side feature. It is the top-level semantic interface of DevOS. Stance codes, host adapters, project routers, task controllers, workflows, and runtimes consume the interpreted objective; they do not bypass it for ordinary human requests.

The engine never grants authority. It does not replace source inspection, project identity evidence, workflow rules, security controls, or verification.

## Canonical intents

Stable intents include `RESUME_WORK`, `BUG_FIX`, `FEATURE_CHANGE`, `VALIDATION`, `SECURITY_REVIEW`, `INVESTIGATE`, `QUALITY_IMPROVEMENT`, `DATABASE_IMPLEMENTATION`, and `EXPLAIN_CHANGE`. Wording, language, slang, emotion, spelling quality, or brevity must not redefine authorization.

## Contextual interpretation

v2 treats short and elliptical language as first-class input. Phrases such as `continue`, `kr do`, `wahi continue`, `same wala`, `jo error tha fix`, and `pehle wala` may inherit a referent only from explicit available context such as the previous interpreted intent, active objective, resolved project, or durable project state.

The interpreter must:

1. interpret meaning rather than exact keywords;
2. tolerate common Hinglish/code-switching, shorthand, spelling variation, and incomplete conversational phrasing;
3. resolve pronouns/deictic phrases (`ye`, `wo`, `wahi`, `this`, `that`, `same`) only when a usable referent exists;
4. preserve corrections and negative constraints such as `deploy mat karna`;
5. support safe multiple-intent composition rather than dropping compatible intents;
6. distinguish interpretation confidence from technical evidence;
7. clarify when project, intent, or referent ambiguity is material;
8. never infer high-impact authorization from context, urgency, profanity, or prior low-impact authorization.

## Top-level entry contract

For human-originated work the default DevOS path is:

`Human input → Human Language Execution Engine → Project Router / State Resolver → Development Task Controller → bounded workflow/runtime → Verification + Security → durable state`

The selected repository and its project-local `.ai/` context remain authoritative after project resolution. The interpreter may use context to resolve language, but it must not invent a project identity or override repository evidence.

A stance such as `DEVOS::CONTINUE` or `DEVOS::GOD` modifies operating posture after semantic interpretation; it is not a separate language bypass. Likewise, host-specific AI interpretation may enrich semantics, but its output must conform to this contract before technical action.

## Executable interpreter

`tools/human-language-interpreter.py` provides the deterministic v2 reference interpreter for common language forms. It emits a structured envelope containing:

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

The reference interpreter is a deterministic minimum behavior contract, not the ceiling of DevOS language understanding. DevOS may evolve richer model-assisted semantic interpretation for multilingual language, corrections, ellipsis, referents, temporal context, intent composition, and conversational continuity. Richer interpretation must preserve the same structured boundaries and must never manufacture authority.

## Short-command rule

Shortness alone is not ambiguity. `continue` can be sufficient when the active project/objective is established. Conversely, a long sentence can remain ambiguous. Clarification is required only when unresolved ambiguity could materially select the wrong project, referent, objective, or high-impact action.

## Constraints and negation

Negative constraints are durable for the interpreted objective and must not be lost during intent composition. For example:

`pehle wala hi but deploy mat karna`

may resolve the prior objective while adding `DO_NOT_DEPLOY`. A negative constraint never becomes a positive authorization later merely because work continues.

## Multiple intents

Compatible intents must compose safely. For example, `continue, fix the error, then check security` can normalize to `RESUME_WORK → BUG_FIX → SECURITY_REVIEW → VALIDATION` when context supports that ordering. Composition must preserve constraints, project identity, and authorization boundaries and must not silently broaden into unrelated work.

## Authorization boundary

Interpretation does not grant authority. Reading and ordinary analysis may proceed under their normal rules. Production-impacting, destructive, irreversible, security-sensitive, deployment, merge, database, credential, or other high-impact operations remain independently gated. The v2 interpreter explicitly returns `authorization: UNCHANGED`, `authority: UNCHANGED`, and `execution: NONE`.

**No technical action is justified solely by emotional intensity.** Urgency, frustration, praise, slang, or profanity may affect conversational interpretation but never independently authorizes code, data, infrastructure, security, deployment, or production changes.

## Evidence boundary

For technical conclusions distinguish `Observed`, `Likely`, and `Unknown`. HIGH interpretation confidence does not establish implementation correctness or root cause.

## Workflow routing

After interpretation:

1. resolve the project with `core/project-router.md`;
2. load durable project `.ai` context and recover current state;
3. select or compose the appropriate workflow;
4. route `SECURITY_REVIEW` explicitly through `workflows/security.md` and the Security Gate rather than treating security review as a generic workflow;
5. inspect actual source/config/tests/Git;
6. determine scope and authorization;
7. execute the smallest authorized action;
8. verify with fresh applicable evidence;
9. persist meaningful semantic progress.

## Verification contract

Execution outcomes remain `VERIFIED`, `PARTIAL`, `UNVERIFIED`, or `FAILED`. Never infer success from absence of an error.

## Evolution contract

Human-language interpretation is a continuously evolvable top-level DevOS capability. Future versions may improve language coverage, contextual reasoning, correction handling, multilingual understanding, referent resolution, intent decomposition, and confidence calibration without forcing downstream workflows to change their safety contracts.

Evolution must be regression-tested against prior language behavior. A language upgrade must not weaken project isolation, explicit constraints, authorization, evidence, security, or verification.

## Test corpus

`tools/test-human-language-interpreter.py` exercises short commands, contextual continuation, Hinglish shorthand, referential language, multi-intent phrases, explicit negative deployment constraints, unknown-context clarification, and high-impact authorization escalation. It runs in the contract CI suite.

## Safety invariant

> **Understand the smallest human phrase that context can safely complete; never complete missing authority.**

Simple language for the human; rigorous engineering underneath.
