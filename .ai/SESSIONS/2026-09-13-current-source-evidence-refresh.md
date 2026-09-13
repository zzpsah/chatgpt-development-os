# Current-Source Evidence Refresh — 2026-09-13

## Objective

Resume the previously started Current-Source Evidence work only after PR #19 (Universal Project Onboarding + Repository Creation) and PR #22 (host-neutral MCP/App `repository.create`) were merged and freshly verified on `main`.

This is an unnumbered bounded objective. No P18/P19 phase was created.

## Starting live state

Verified `main` after PR #22 merge:

`535d20ecf5528d0b118f220a98c4c519578b00cf`

Fresh post-merge main verification:
- Trust-First 68 / `34768878981`: SUCCESS
- Contracts 605 / `34768878980`: SUCCESS
- Full DevOS 527 / `34768878994`: SUCCESS

The preserved Current-Source branch was still at `01ea866a486c63bc60e7c77a842f4c5abe766462`, based on older `a8feb55557daf7d8e10da9aa18415c43d4c75c98`.

## History-safe reconciliation

The old branch added only `tools/current-source-evidence.py` beyond its old base.

It was reconciled with current verified `main` using a two-parent merge commit with the current main tree plus the exact original evidence-tool blob. No force push was used and historical evidence was not rewritten.

Reconciled head:

`990917802ff06ea3bf20289392c0e7ee535600df`

## Implemented protocol

`DEVOS-CURRENT-SOURCE-EVIDENCE-v1`

Current evidence is an ephemeral packet constrained by the existing readiness evidence ledger.

A packet binds:
- canonical repository identity;
- exact current Git HEAD;
- ledger-declared capability/level/test;
- exact test path;
- SHA-256 of current test bytes;
- observed exit code;
- local or CI context metadata.

Packet invariants remain:
- mode `READ_ONLY`;
- authority `UNCHANGED`;
- authorization `UNCHANGED`;
- execution `NONE`;
- mutation `NONE`;
- `production_ready=false`;
- `live_provider_proven=false`.

Historical evidence remains pinned. Current evidence does not change historical `source_head`, run IDs, archive digest or freshness.

Rule:

`CURRENT_EVIDENCE_ADDS_PROOF_BUT_NEVER_REWRITES_HISTORICAL_PROVENANCE`

## Adversarial packet regression

Added `tools/test-current-source-evidence.py` covering:
- stale/fabricated source HEAD;
- test digest tampering;
- undeclared capability claim;
- failed check presented as proof;
- production claim promotion;
- live-provider claim promotion;
- mismatched CI run context;
- arbitrary provider-simulated relabeling;
- historical drift overlay without ledger mutation.

## Foundation Health / Doctor integration

Foundation Health now accepts an optional current-source packet path.

Health:
- reads and validates the packet through `current-source-evidence.py`;
- never executes the packet test;
- keeps historical drift visible;
- exposes exact current proof separately;
- BLOCKS malformed/tampered/path-escape packets;
- reports a requested missing packet as UNKNOWN.

DevOS Doctor only renders the Health result.

Added `tools/test-current-source-health-integration.py` proving:
- valid packet adds current proof without repointing historical evidence;
- historical drift remains WARN;
- tampered packet propagates BLOCKED;
- missing packet remains UNKNOWN;
- packet path escape blocks;
- Doctor does not promote production/live-provider state.

## Documentation

Added:
- `core/current-source-evidence.md`
- `docs/CURRENT-SOURCE-EVIDENCE.md`

Reconciled `.ai/CURRENT-STATE.md` to the actual live Git state:
- PR #19 merged;
- PR #22 merged;
- Current-Source Evidence is the active bounded objective;
- draft PR #24 is the current review vehicle.

## Verification evidence before durable-state closure

Dedicated implementation checks:
- Verify Current-Source Evidence #1 / `34773305510`: SUCCESS
- Verify Current-Source Evidence #5 / `34773410780`: SUCCESS

Implementation-head PR #24 exact head:

`9a998248eb6d9bb7123f67fd767f6a91c1e97182`

Fresh exact-head CI:
- Current-Source Evidence 8 / `34773472433`: SUCCESS
- Trust-First 69 / `34773472435`: SUCCESS
- Contracts 606 / `34773472413`: SUCCESS
- Full DevOS 528 / `34773472487`: SUCCESS

Because documentation and durable state were written only after that implementation evidence, their commits create a new final head. A fresh exact-final-head CI cycle is mandatory before PR #24 can be classified ready.

## Evidence classification

At this checkpoint:
- protocol implementation: VERIFIED at deterministic/integrated CI level on implementation head;
- historical provenance preservation: VERIFIED by regression;
- exact current HEAD/test/SHA-256 binding: VERIFIED by regression;
- Foundation Health consumption: VERIFIED by regression;
- Doctor presentation boundary: VERIFIED by regression;
- live-provider proof: NOT PROVEN;
- production readiness: NOT PROVEN;
- `production_ready=false`;
- `live_provider_proven=false`.

No live/destructive/production/provider/credential/permission/deployment mutation was performed.
