# Session — AI State Resolver structured cross-claim contradiction hardening

Date: 2026-09-14
Repository: `zzpsah/chatgpt-development-os`
Branch base: `040c7d21b5fac6224ced1bdbfeaa7c3b71b78c78`
Branch: `feat/ai-state-resolver-cross-claim-contradictions`

## Trigger

The user requested continued autonomous DevOS development and explicit documentation of previous stages.

Fresh source inspection confirmed that resolver v2 already handled individual claim confidence, grounding, revalidation, P16 propagation, P17 readiness validation, and PR #44 envelope-integrity hardening, while cross-claim semantic contradiction handling remained an explicit non-goal pending a stable fact identity and deterministic policy.

Fresh inspection also found semantic drift in the latest durable state: direct documentation commit `040c7d21b5fac6224ced1bdbfeaa7c3b71b78c78` had reintroduced stale wording that live GitHub provider proof was pending even though repository/provider history already contained successful read-only provider proof and governed isolated mutation proof. Current source/Git/provider evidence therefore required durable-state repair.

## Bounded design decision

Cross-claim contradiction detection is structured rather than NLP-inferred.

Claims may opt in with:

- `fact_key`: explicit stable fact identity;
- `fact_value`: JSON value for that fact.

No resolver logic guesses that two free-text statements describe the same fact.

Values are canonicalized with deterministic JSON serialization. Multiple canonical values under one fact key produce a contradiction. Every involved claim becomes `unknown` and receives `CROSS_CLAIM_CONTRADICTION`.

The resolver does not silently select a winner by freshness, source type, confidence, or claim order. Even stale-vs-current disagreement remains unresolved until upstream evidence reconciliation removes the conflict.

## Implementation

### Resolver

`tools/ai-state-resolver.py`

- adds optional `fact_key` + `fact_value` pair;
- incomplete structured identity becomes unknown with `FACT_IDENTITY_INCOMPLETE`;
- canonical JSON comparison avoids object-key-order false conflicts;
- cross-claim contradictions mark all involved claims unknown;
- result adds deterministic `contradictions` summary;
- authority/authorization remain unchanged; execution/mutation remain none.

### P16

`tools/semantic-goal-to-plan.py`

- independently recomputes structured fact groups and canonical values;
- rejects incomplete fact identity;
- rejects forged resolver envelopes that hide contradictions by retaining likely/observed confidence;
- validates contradiction summary consistency;
- contradiction-produced unknown claims continue through existing `CLARIFY` behavior.

### P17

`tools/step-readiness-orchestrator.py`

- independently recomputes structured contradictions from P16-preserved claims;
- rejects post-P16 fact-value tampering even when status/confidence summaries are left unchanged;
- preserves all existing authorization/security/capability/freshness gates.

### Regression coverage

`tools/test-ai-state-resolver.py`

- same fact/same value;
- structured JSON object key-order equivalence;
- incomplete fact identity;
- same fact/different values;
- stale-vs-current disagreement remains unresolved.

`tools/test-ai-state-resolver-p16-p17.py`

- contradiction result propagates to P16 as `CLARIFY`;
- forged contradiction-hidden resolver envelope fails P16;
- post-P16 fact-value tampering fails P17.

## Documentation and previous-stage record

- `core/ai-state-resolver.md` updated to the current executable contradiction contract.
- `docs/AI-STATE-RESOLVER-EVOLUTION.md` records resolver evolution from semantic/v1 context through deterministic v2 grounding, P16/P17 propagation, PR #44 envelope integrity, PR #45 durable reconciliation, and the current contradiction stage.
- `.ai/CURRENT-STATE.md` and `.ai/TASKS.md` repaired to remove stale pre-proof provider wording and to mark contradiction hardening as the active bounded objective.

## Preserved boundaries

- `production_ready = false`.
- P12 remains owner of execution-evidence provenance/freshness.
- Resolver confidence never grants authorization, execution, mutation, completion, or production readiness.
- No production, credential, permission, database, deployment, or destructive mutation is introduced by this objective.
- No P18/P19 is created merely for bookkeeping.

## Verification state

Implementation and durable documentation are committed on the bounded branch. Exact-head applicable CI must pass before this objective is treated as verified/merge-complete. Any CI compatibility failure must be repaired without weakening the fail-closed contradiction policy merely to preserve an outdated fixture.
