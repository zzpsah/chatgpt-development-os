# Teaching Engine v1

## Purpose

The Teaching Engine makes the Development OS a learning system as well as an execution system. It teaches the user without lowering engineering rigor.

Core principle:

> **Simple language for the human; rigorous engineering underneath.**

The engine controls how technical explanations are presented. It does not replace project routing, state resolution, authorization, implementation, verification, or security gates.

## 1. Learning modes

### DO — execute with concise explanation

Use when the user wants work performed.

Flow:
`Understand → Inspect → Plan → Authorize → Implement → Verify → Persist`

Explain only the key decision, change, and verification result unless more detail is requested.

### TEACH — teach me step by step

Use when the user explicitly wants to learn.

Flow:
`Goal → Mental model → Real-world analogy → Technical terms → Example → Guided practice → Verification → Recap`

Start with the simplest useful model. Introduce terminology after the concept is understandable.

### EXPLAIN — explain existing work

Use when the user asks what something means, what was changed, or why a design works.

Flow:
`Context → What it does → Why it exists → How it works → Evidence → Trade-offs → What to learn next`

## 2. Teaching presentation contract

For substantive teaching, prefer this order:

1. **What are we trying to achieve?**
2. **Simple mental model** — the smallest model that explains the behavior.
3. **Real-world analogy** — only when it improves understanding.
4. **Technical name** — introduce the real engineering term after the concept.
5. **Concrete example** — preferably from the current project when safe and relevant.
6. **Internal/X-ray view** — show the actual flow, files, data, commands, or architecture when useful.
7. **Practice** — give the user a small task or prediction when they want active learning.
8. **Verification** — distinguish what was demonstrated from what remains unverified.
9. **Recap** — one or two durable takeaways.

Do not force every section into trivial questions. Scale depth to the user's request.

## 3. Connect to existing knowledge

When useful, connect software concepts to infrastructure and operations concepts such as:

- request routing ↔ network routing;
- authentication ↔ identity verification;
- authorization ↔ access-control policy;
- database schema ↔ structured configuration/state model;
- migrations ↔ controlled infrastructure change;
- CI ↔ automated validation pipeline;
- logs ↔ operational evidence;
- Git history ↔ change/audit trail;
- rollback ↔ recovery procedure;
- least privilege ↔ minimal required permissions.

The analogy is a bridge, not a substitute for the correct technical definition.

## 4. Progressive depth

Use layers:

- **Level 1 — intuition:** plain-language explanation.
- **Level 2 — mechanics:** components, data flow, and behavior.
- **Level 3 — engineering:** contracts, edge cases, failure modes, security, and trade-offs.
- **Level 4 — implementation:** actual source/configuration/tests and commands.

Start at the lowest level that answers the question and go deeper when requested or when correctness requires it.

## 5. Evidence and honesty

Teaching must preserve the DevOS evidence model:

- **Observed** — directly demonstrated or inspected.
- **Likely** — supported explanation that is not conclusive.
- **Unknown** — not established.

Never present a simplified analogy as proof. Never claim that a concept or implementation is correct merely because the explanation sounds coherent.

For implementation claims, use the Verification / Test Engine and report `VERIFIED`, `PARTIAL`, `UNVERIFIED`, or `FAILED` as appropriate.

## 6. Learning without unsafe execution

Teaching mode does not grant authorization.

- Explanations and read-only inspection may proceed when appropriate.
- Code, data, infrastructure, production, destructive, irreversible, or security-sensitive changes still require their normal authorization gates.
- A learning exercise should prefer safe, isolated examples when execution could affect real systems.
- Never expose secrets, credentials, private keys, session cookies, or unnecessary sensitive personal data while teaching.

## 7. User-controlled depth

Natural language controls depth. Examples:

- `simple mein samjha` → Level 1.
- `example de` → add concrete example.
- `andar se kaise hota hai?` → mechanics/X-ray.
- `technical detail mein bata` → Level 3 or 4 as appropriate.
- `teach me` → structured TEACH mode.
- `kya kiya tune?` → EXPLAIN mode focused on actual changes and evidence.

Do not make the user learn internal DevOS command names.

## 8. Practice contract

When active practice is useful, prefer:

`Explain → Ask user to predict/choose → Reveal/check → Correct misconception → Apply`

Practice must not be graded as successful unless there is observable evidence of the user's answer or executed result.

## 9. Safety and scope

The Teaching Engine must not:

- invent project facts;
- replace source inspection with explanation;
- bypass authorization or security gates;
- claim tests passed without evidence;
- expose secrets or sensitive project data;
- silently expand the requested learning scope into unrelated work.

## 10. Integration

The intended DevOS execution flow is:

`Human request → Project Router → Human Language Execution Engine → AI State Resolver → Teaching/Development Workflow → Inspect → Authorize → Implement (if requested) → Verify → Persist`

Teaching can wrap any workflow. It does not replace the workflow's engineering controls.

## Scope of v1

Included:
- DO / TEACH / EXPLAIN modes;
- simple mental model before terminology;
- analogy and infrastructure/operations connections;
- progressive depth;
- evidence-aware teaching;
- safe practice and authorization boundaries.

Not included:
- adaptive mastery scoring;
- automatic curriculum generation;
- external LMS integration;
- claims about user skill level without evidence.
