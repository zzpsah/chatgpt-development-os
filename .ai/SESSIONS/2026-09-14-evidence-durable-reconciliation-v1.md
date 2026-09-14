# Session — Automated Evidence → Durable State Reconciliation v1

Date: 2026-09-14

## Objective

Implement a bounded, repository-first pipeline that validates machine-verifiable post-feature evidence and prepares durable-state reconciliation without allowing CI, commit messages, provider capability, or generated metadata to manufacture semantic authority.

## Starting point

- Fresh branch created from `main` after post-PR #52 durable reconciliation.
- No open PR was visible when this slice started.
- Another AI is concurrently developing P15 multilingual request-corpus and P15 → P16 → P17 language-safety hardening in this same repository.
- This branch intentionally avoids P15 multilingual/interpreter files and treats the repository as a concurrent-development environment.

## Existing evidence systems inspected

### `tools/context-sync.py`

Existing context sync already maintains deterministic repository/context facts such as HEAD, changed paths, changelog, generated state index, and a bounded automated-change section. Its own generated index explicitly says repository/context evidence is not semantic authority.

### `tools/current-source-evidence.py`

Existing current-source evidence validates a declared test at an exact source head while preserving authority/authorization boundaries and refusing to rewrite historical provenance.

## Gap

Recent DevOS work repeatedly required a separate manual closure sequence after verified feature merge:

```text
feature implementation
→ exact-head CI
→ merge
→ CURRENT-STATE/TASKS/session/history reconciliation
→ another CI/merge
```

There was no deterministic contract separating:

- machine facts that can be safely normalized automatically; from
- semantic state/roadmap/authority updates that require review.

## Implemented on this branch

### `tools/evidence-durable-state-reconciler.py`

Adds protocol `DEVOS-EVIDENCE-DURABLE-RECONCILIATION-v1`.

It validates:

- repository/objective identity supplied by the bounded caller;
- merged PR metadata;
- exact 40-hex feature head and merge commit;
- completed successful workflow evidence on the exact feature head;
- required workflow presence;
- changed-file evidence;
- explicitly required documentation paths;
- semantic-review provenance for `.ai/CURRENT-STATE.md` and `.ai/TASKS.md`;
- permanent safety invariants.

Statuses:

- `BLOCKED`
- `NEEDS_EVIDENCE`
- `SEMANTIC_REVIEW_REQUIRED`
- `READY_FOR_DURABLE_RECONCILIATION`

The ready path emits a deterministic `DEVOS-DURABLE-RECONCILIATION-RECORD-v1` plus canonical SHA-256 digest and a bounded write plan. It does not perform repository/provider writes.

### Safety invariants

The input and record require:

```yaml
authority: UNCHANGED
authorization: UNCHANGED
execution: NONE
mutation: NONE
production_ready: false
```

The reconciler does not infer architecture stage, next objective, permission scope, contradiction truth winner, or production readiness.

### Completion evidence

The tool reports evidence dimensions:

- implemented
- verified
- documented
- durable_state

`durable_state` intentionally remains false until the caller actually persists the reconciliation and verifies the post-write state. The tool cannot self-certify persistence that has not happened.

### Regression corpus

`tools/test-evidence-durable-state-reconciler.py` covers:

- happy-path exact-head reconciliation readiness;
- deterministic evidence ordering/digest;
- unmerged feature evidence;
- failing CI;
- workflow head mismatch;
- missing required workflow;
- missing required documentation;
- missing semantic review;
- incomplete reviewed targets;
- forged authority/authorization/execution/mutation/production-ready boundaries;
- unknown auto-authorization input;
- ledger-record boundary tampering;
- digest tampering.

### Dedicated CI

`.github/workflows/verify-evidence-durable-reconciliation.yml` runs the regression corpus and contract-marker checks without modifying the existing P15 or shared contract workflow being used by the parallel AI effort.

## Documentation

`core/evidence-durable-state-reconciliation.md` defines the normative v1 contract, relationships to context-sync/current-source evidence, concurrency rule, write plan, semantic-review boundary, and non-goals.

## Concurrency rule for this slice

Before PR/integration:

1. re-read fresh `main`;
2. inspect open PRs/parallel P15 work;
3. compare this branch with fresh main;
4. do not overwrite newer `.ai` semantic state;
5. integrate only non-overlapping or explicitly reconciled changes;
6. require exact-final-head CI.

## Boundaries

- No P18/P19 bookkeeping stage.
- No production deployment.
- No provider mutation from the reconciler.
- No credential/permission changes.
- No automatic merge based only on CI.
- No semantic project truth inferred from commit messages or generated state.
- `production_ready = false` remains intentional.

## Remaining before completion

- Verify branch against fresh parallel repository state.
- Add durable current/task/master-map state only after concurrency reconciliation.
- Open bounded PR.
- Require exact-final-head applicable CI.
- Repair failures without weakening safety invariants.
- Merge only when current authorization and fresh mergeability permit.
- Reconcile post-merge durable state and verify fresh `main`.
