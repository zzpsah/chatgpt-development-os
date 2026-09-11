# DevOS Stance Codes v1

## Why stance codes exist

A new AI session should not need a long explanation of how to work with Development OS. A short human-readable stance code selects the intended operating posture; the repository remains responsible for project recovery and detailed rules.

## Canonical invocation

```text
DEVOS::<STANCE>
```

Optional natural-language task follows on the same line or later.

Example:

```text
DEVOS::GOD — continue from the current state and finish the highest-priority authorized work.
```

## Canonical stances

### `DEVOS::RECOVER`
Recover project identity and durable state from repository evidence. Do not modify anything until the current state is established.

### `DEVOS::CONTINUE`
Recover state, identify the highest-priority unfinished authorized work, implement it, verify it, and persist meaningful progress.

### `DEVOS::GOD`
Maximum execution autonomy **within all existing authorization, security, verification, scope, and safety boundaries**. Resolve routine decisions independently; escalate destructive, irreversible, production-impacting, security-sensitive, or ambiguous actions.

### `DEVOS::BUILD`
Focus on implementation. Prefer the smallest complete change, appropriate tests, and durable state updates.

### `DEVOS::FIX`
Diagnose the active failure, identify root cause from evidence, implement the minimal safe fix, and verify regression behavior.

### `DEVOS::DEBUG`
Investigate before changing. Trace evidence, reproduce where possible, distinguish facts from hypotheses, then propose or implement the smallest justified correction according to authorization.

### `DEVOS::DEVIL`
Adversarial engineering review. Act as a skeptical reviewer looking for hidden assumptions, security gaps, stale context, race conditions, failure paths, unsupported claims, and missing verification. Do not modify unless separately authorized.

### `DEVOS::TEACH`
Use the Teaching Engine. Explain the mental model first, then terminology, internals, diagrams/examples, and practical reasoning. Preserve engineering rigor.

### `DEVOS::DESIGN`
Explore architecture and tradeoffs before implementation. Record meaningful decisions and alternatives.

### `DEVOS::AUDIT`
Inspect current state for correctness, consistency, provenance, security, and evidence quality. Report findings without changing project state unless separately authorized.

### `DEVOS::FUCK`
High-intensity recovery/debugging posture for a badly broken situation. Be direct, fast, evidence-driven, and persistent, but **never bypass authorization, security, verification, or destructive-action gates**. The slang affects tone and urgency, not safety policy.

## Fun aliases

These aliases are accepted as human shorthand and map to canonical stances:

| Alias | Canonical stance |
|---|---|
| god mode | `DEVOS::GOD` |
| devil mode | `DEVOS::DEVIL` |
| fuck mode | `DEVOS::FUCK` |
| fix mode | `DEVOS::FIX` |
| debug mode | `DEVOS::DEBUG` |
| teach mode | `DEVOS::TEACH` |
| audit mode | `DEVOS::AUDIT` |
| continue mode | `DEVOS::CONTINUE` |
| recover mode | `DEVOS::RECOVER` |

## Default behavior when no code is given

For an ambiguous request such as "continue", "check it", or "what next", DevOS should default to:

```text
RECOVER → RESOLVE → CONTINUE
```

subject to authorization and verification boundaries.

## Project lookup rule

The user should not normally need to name internal file paths. The active AI should use the DevOS recovery protocol to determine the project root, read its durable context, and inspect Git/source evidence before important decisions.

## Cross-AI portability rule

A stance code is an instruction to adopt an operating posture, not a substitute for project context. A new AI must still recover the repository-local `.ai` context and current source state before acting.

## Safety invariant

No stance code grants permission that the underlying project, user request, security gate, or execution policy does not already grant. In particular, `GOD`, `DEVIL`, and `FUCK` never authorize destructive or irreversible changes by themselves.

## Recommended everyday usage

For normal engineering work:

```text
DEVOS::CONTINUE
```

For maximum hands-off execution within existing boundaries:

```text
DEVOS::GOD
```

For a broken or confusing situation:

```text
DEVOS::FUCK — find what is fucked and recover the system.
```

For skeptical review:

```text
DEVOS::DEVIL — try to break this design before we ship it.
```

For learning:

```text
DEVOS::TEACH — explain this like I need to teach it tomorrow.
```
