# Session — Resolver contradiction envelope-integrity follow-up

Date: 2026-09-14
Repository: `zzpsah/chatgpt-development-os`
Base `main`: `7009e8e1b4398462b1a9321bb1e2a38a3c35e478`
Branch: `fix/resolver-contradiction-envelope-integrity-v2`

## Trigger

The user requested continued autonomous DevOS development and documentation of previous stages. Cross-claim contradiction handling and the engineering-stage ledger were already implemented, verified, documented, and merged through PR #46; PR #48 subsequently reconciled post-#46 durable state.

A concurrent duplicate PR #47 was closed without merge after fresh Git/PR recovery established PR #46 as authoritative.

## Observed remaining gap

Post-merge source inspection found one narrower envelope-integrity gap:

- P16 validated resolver confidence/status/unresolved consistency but did not independently recompute explicit `fact_key` / `fact_value` contradictions.
- A crafted resolver envelope could theoretically restore contradictory claims to `likely`, clear contradiction/unresolved metadata, and present a superficially consistent `RESOLVED` result.
- P17 revalidated unknown/count consistency but did not independently recompute explicit fact contradictions.
- A valid same-value fact group could therefore theoretically be altered after P16 by changing one `fact_value` while preserving status/confidence/count metadata.

## Changes

### P16

`tools/semantic-goal-to-plan.py` now independently recomputes explicit fact groups and validates:

- canonical deterministic JSON fact values;
- contradictory groups remain `unknown`;
- every contradictory claim retains `CROSS_CLAIM_CONTRADICTION`;
- contradiction reasons do not appear on non-conflicting facts;
- `contradiction_fact_keys` matches the recomputed conflicting facts.

A forged hidden contradiction becomes material ambiguity and P16 returns `CLARIFY`.

### P17

`tools/step-readiness-orchestrator.py` independently repeats contradiction-integrity validation on the full resolver provenance preserved by P16.

A post-P16 change to one `fact_value` that creates a hidden contradiction is rejected with `PLAN_STATE_RESOLUTION_HIDDEN_CONTRADICTION` rather than allowing READY.

### Regression coverage

`tools/test-ai-state-resolver-p16-p17.py` adds adversarial coverage for:

- forged resolver contradiction metadata/confidence/status hiding rejected by P16;
- a valid same-value fact group planning normally;
- post-P16 one-value tampering producing P17 `BLOCKED`.

### Documentation and durable state

- `docs/AI-STATE-RESOLVER-CROSS-CLAIM-CONTRADICTIONS.md` documents independent P16/P17 recomputation.
- `.ai/CURRENT-STATE.md` and `.ai/TASKS.md` preserve PR #46/#48 closure and mark only this narrow follow-up active.
- Previous numbered stages and major unnumbered milestones remain documented in `docs/DEVOS-ENGINEERING-STAGE-HISTORY.md` from the PR #46 line of work.

## Preserved boundaries

- `production_ready = false`.
- authority and authorization remain unchanged.
- resolver/planning/readiness validation performs no provider execution or mutation.
- P12 remains owner of execution-evidence provenance/freshness.
- P16 remains plan compiler; P17 remains readiness/authorization gate.
- no P18/P19 bookkeeping phase is created.
- no production, deployment, credential, permission, database, or destructive capability is introduced.

## Verification state

Implementation, adversarial tests, contract documentation, and durable state are committed on the bounded branch. Exact-head applicable CI is required before merge/completion. Any compatibility repair must preserve the new independent contradiction recomputation.
