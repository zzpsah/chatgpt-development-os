# Session — Resolver contradiction envelope-integrity follow-up

Date: 2026-09-14
Repository: `zzpsah/chatgpt-development-os`
Base `main`: `36f3001487fb7ce666bb1e7241b539645878101a`
Branch: `fix/resolver-contradiction-envelope-integrity`

## Trigger

The user requested continued autonomous DevOS development and durable documentation of previous stages. The base cross-claim contradiction feature had already been implemented, exact-head verified, documented, and merged through PR #46 while a concurrent duplicate branch was also being developed.

Fresh recovery therefore used current Git/PR state instead of assuming the duplicate branch remained authoritative. PR #47 was closed without merge after PR #46 became authoritative.

## Observed remaining gap

PR #46 correctly detects structured contradictions in `tools/ai-state-resolver.py` and propagates resolver-produced unknown claims into P16 `CLARIFY`.

Fresh post-merge inspection found a narrower envelope-integrity gap:

- P16 validated confidence/status/unresolved consistency but did not independently recompute contradictions from explicit `fact_key` / `fact_value` claim provenance.
- A crafted resolver result could therefore theoretically restore contradictory claims to `likely`, clear `contradiction_fact_keys` and unresolved IDs, and present a superficially consistent `RESOLVED` envelope.
- P17 revalidated unknown/count consistency but did not independently recompute fact-value contradictions.
- A valid same-value group could therefore theoretically be altered after P16 by changing one `fact_value` while leaving confidence/status/count metadata unchanged.

## Changes

### P16

`tools/semantic-goal-to-plan.py` now independently recomputes structured fact groups from the resolver claims it consumes.

It validates:

- deterministic JSON serialization of fact values;
- contradictory groups remain unknown;
- each contradictory claim retains `CROSS_CLAIM_CONTRADICTION`;
- contradiction reasons do not appear on non-contradictory groups;
- `contradiction_fact_keys` exactly matches recomputed conflicting facts.

A forged hidden contradiction becomes material ambiguity and P16 returns `CLARIFY`.

### P17

`tools/step-readiness-orchestrator.py` independently repeats contradiction-integrity validation on the full resolver provenance preserved by P16.

A post-P16 change to one `fact_value` that creates a contradiction is rejected with `PLAN_STATE_RESOLUTION_HIDDEN_CONTRADICTION` rather than allowing READY.

### Regression coverage

`tools/test-ai-state-resolver-p16-p17.py` adds adversarial cases for:

- forged resolver contradiction metadata/confidence/status hiding rejected by P16;
- a valid same-value fact group compiling normally;
- post-P16 one-value tampering producing P17 BLOCKED.

### Documentation / durable state

- `docs/AI-STATE-RESOLVER-CROSS-CLAIM-CONTRADICTIONS.md` now documents independent P16/P17 recomputation.
- `docs/DEVOS-ENGINEERING-STAGE-HISTORY.md` records PR #46 and the follow-up in the resolver evolution sequence.
- `.ai/CURRENT-STATE.md` and `.ai/TASKS.md` are reconciled so PR #46 is completed and only this narrow follow-up is active.

## Preserved boundaries

- `production_ready = false`.
- authority: unchanged.
- authorization: unchanged.
- execution: none for resolver/planning/readiness validation.
- no provider, deployment, credential, permission, database, production, or destructive mutation is introduced.
- P12 remains owner of execution-evidence provenance/freshness.
- P16 remains plan compiler; P17 remains readiness/authorization gate.
- no P18/P19 bookkeeping phase is created.

## Verification state

Implementation, adversarial tests, current-state reconciliation, and history documentation are committed on the bounded branch. Exact-head applicable CI is required before merge/completion. Compatibility regressions must be repaired without weakening the independent contradiction recomputation.
