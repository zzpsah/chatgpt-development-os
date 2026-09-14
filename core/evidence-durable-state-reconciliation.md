# Evidence → Durable State Reconciliation v1

## Purpose

DevOS repeatedly reaches the same post-feature boundary:

```text
implementation
  ↓
exact-head verification
  ↓
merge
  ↓
manual durable-state cleanup
  ↓
recovery-ready repository
```

`tools/evidence-durable-state-reconciler.py` makes the evidence-to-durable-state boundary deterministic without turning machine evidence into semantic authority.

Protocol: `DEVOS-EVIDENCE-DURABLE-RECONCILIATION-v1`.

## Core rule

> **Machine-verifiable facts may be automated. Semantic project state requires explicit review.**

The reconciler may validate and normalize factual evidence such as:

- repository identity;
- bounded objective ID/label supplied by the caller;
- merged PR number/title;
- exact feature head and merge commit SHA;
- workflow run IDs, names, exact tested head, completion status, and conclusion;
- changed file paths;
- required documentation paths supplied by the bounded objective.

It may **not infer**:

- authority or authorization;
- production readiness;
- permission scope;
- a new architecture phase;
- the next objective;
- which contradictory claim is true;
- whether a semantic roadmap/state statement should be adopted merely because CI passed.

## Required boundary invariants

Every input and emitted record preserves:

```yaml
authority: UNCHANGED
authorization: UNCHANGED
execution: NONE
mutation: NONE
production_ready: false
```

A changed invariant is `BLOCKED`, not downgraded into a warning.

## Evidence gates

### Implemented evidence

The supplied feature evidence must state a valid merged PR with:

- positive PR number;
- non-empty title;
- exact 40-hex feature head;
- exact 40-hex merge commit;
- `merged: true`.

This is evidence that the bounded feature was merged. It does not independently prove semantic correctness or production readiness.

### Verified evidence

All supplied workflow evidence must be completed successfully **on the exact feature head**. The bounded objective supplies `required_workflows`; every required name must be present in successful exact-head evidence.

A failed workflow, missing required workflow, or head mismatch yields `NEEDS_EVIDENCE`.

### Documented evidence

The bounded objective explicitly supplies `required_documentation_paths`. Every required documentation path must be present in the supplied changed-file evidence.

The tool does not guess which documentation is semantically sufficient.

### Semantic review

Even when merge/CI/docs evidence is complete, the tool returns `SEMANTIC_REVIEW_REQUIRED` until a non-empty review reference approves at least:

- `.ai/CURRENT-STATE.md`;
- `.ai/TASKS.md`.

This prevents commit messages, CI success, or generated evidence from silently manufacturing semantic project truth.

## Output statuses

- `BLOCKED` — malformed input or a safety/authority boundary changed.
- `NEEDS_EVIDENCE` — merge, exact-head verification, required workflow, or documentation evidence is incomplete/inconsistent.
- `SEMANTIC_REVIEW_REQUIRED` — machine evidence is sufficient but semantic durable-state review is not approved.
- `READY_FOR_DURABLE_RECONCILIATION` — evidence and semantic-review gates are satisfied; a deterministic audit record may be persisted.

`READY_FOR_DURABLE_RECONCILIATION` is **not execution authorization** and does not itself write repository state.

## Completion evidence model

The tool emits four evidence dimensions:

```yaml
implemented: true | false
verified: true | false
documented: true | false
durable_state: false
```

`durable_state` intentionally remains `false` in the pre-write reconciliation record. It becomes true only after the caller persists the required durable records and performs fresh post-write/readback verification.

This prevents the reconciler from declaring its own persistence successful before persistence happens.

## Reconciliation write plan

When machine evidence is complete, the tool emits a bounded write plan:

1. append a structured machine record to `.ai/RECONCILIATION-LEDGER.jsonl`;
2. create a dated reconciliation session record under `.ai/SESSIONS/`;
3. update `.ai/CURRENT-STATE.md` only through semantic review;
4. update `.ai/TASKS.md` only through semantic review;
5. update `docs/DEVOS-ENGINEERING-STAGE-HISTORY.md` only when materiality review says history changed.

The v1 tool emits the plan and deterministic record; repository/provider writes remain governed by the normal DevOS controller/adapter path.

## Structured durable record

A ready result contains `DEVOS-DURABLE-RECONCILIATION-RECORD-v1` plus a SHA-256 digest over canonical JSON. The record contains exact machine evidence, semantic-review provenance, unchanged safety boundaries, and the rule:

`MACHINE_FACTS_MAY_BE_AUTOMATED_SEMANTIC_STATE_REQUIRES_REVIEW`

`--verify-record --expected-digest <sha256>` revalidates the record and detects tampering.

## Relationship to existing tools

- `tools/context-sync.py` continues to maintain repository/context facts such as HEAD, changed paths, changelog, and state index. It is not promoted into semantic authority.
- `tools/current-source-evidence.py` continues to prove bounded current tests at an exact source head. It does not rewrite historical evidence.
- The reconciliation v1 layer consumes bounded machine evidence after work is verified/merged and determines whether semantic durable-state reconciliation may proceed.

The tools complement each other; reconciliation v1 does not replace P11 recovery, P12 evidence provenance/freshness, P16 planning, P17 readiness/authorization, or provider readback.

## Concurrency rule

Parallel AI/agent work is expected. A reconciliation branch must be compared against fresh `main` immediately before integration. It must not overwrite newer semantic state from another AI merely because its own evidence packet is internally valid.

If current source/state advanced materially, re-read and reconcile; never force stale semantic state over newer work.

## Non-goals

- automatic semantic edits to roadmap/architecture;
- automatic production-ready promotion;
- automatic authorization or approval creation;
- automatic merge based only on CI;
- automatic truth selection for contradictory state;
- blind rewriting of `.ai` Markdown from commit messages;
- replacement of exact-head CI, security gates, provider readback, or post-merge verification.

## Completion law

This pipeline supports the repository law:

`OBSERVE → ACT / CHANGE / DECIDE → VERIFY → DOCUMENT → PERSIST IN GIT`

and makes the final transition toward:

`IMPLEMENTED + VERIFIED + DOCUMENTED + DURABLE STATE`

without allowing the automation to self-certify semantic truth or authority.
