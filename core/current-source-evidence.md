# Current-Source Evidence Protocol v1

## Purpose

DevOS historical readiness evidence is intentionally pinned to the source head that originally produced it. When current source legitimately changes, historical evidence must not be silently rewritten or repointed.

Current-Source Evidence adds fresh, bounded proof for the exact checked-out source while preserving historical provenance.

## Architecture

```text
current repository source
  + exact Git HEAD
  + readiness-ledger-declared capability/level/test
  + exact test path
  + SHA-256 of current test bytes
  + observed exit code
  + optional current CI context
        ↓
current-source-evidence.py
        ↓
ephemeral validated packet
        ↓
Foundation Health
        ↓
DevOS Doctor presentation
```

The readiness evidence ledger remains authoritative for claim vocabulary and historical provenance. Current-source evidence does not replace it.

## Core rule

```text
CURRENT EVIDENCE ADDS PROOF
!=
HISTORICAL EVIDENCE REWRITE
```

A valid current packet may demonstrate that a historically drifted test passes at the exact current Git HEAD. The original historical `source_head`, run metadata, archive and freshness classification remain unchanged.

## Packet invariants

A valid packet must keep:

- protocol: `DEVOS-CURRENT-SOURCE-EVIDENCE-v1`
- repository: `zzpsah/chatgpt-development-os`
- mode: `READ_ONLY`
- authority: `UNCHANGED`
- authorization: `UNCHANGED`
- execution: `NONE`
- mutation: `NONE`
- `production_ready=false`
- `live_provider_proven=false`

The evidence entry binds:

- exact current `source_head`;
- capability already declared by the readiness ledger;
- supported proof level already declared by the ledger;
- exact repository test path;
- SHA-256 of current test bytes;
- observed exit code;
- local or CI execution context;
- when in CI, run/workflow context metadata.

## Supported proof levels

v1 accepts only bounded levels already used for deterministic current-source refresh:

- `deterministic`
- `integrated`
- `provider_simulated`

`provider_simulated` remains simulated evidence. It must never become live-provider proof.

Real external-provider or production proof is outside this protocol.

## Historical-source drift

`historical_source_drift` remains visible even after valid current evidence exists.

A packet may add:

- `current_source_verified`
- `unresolved_historical_drift`

It must not remove or edit historical rows in `config/readiness-evidence.json`.

Foundation Health therefore continues to report historical drift conservatively while also exposing the validated current-source result.

## Health / Doctor boundary

Foundation Health accepts an optional packet path.

Health may:

- read the packet;
- validate it through `current-source-evidence.py`;
- classify valid current proof;
- surface unresolved drift;
- BLOCK malformed/tampered packets;
- mark a missing requested packet UNKNOWN.

Health must not:

- execute the packet's test;
- rewrite readiness evidence;
- manufacture CI metadata;
- convert historical evidence to current;
- grant authorization;
- promote production or live-provider claims.

DevOS Doctor only renders the Health result.

## Adversarial boundaries

The regression corpus rejects at minimum:

- stale or fabricated source HEAD;
- tampered test digest;
- undeclared capability/level/test claims;
- failed test result presented as current proof;
- fabricated/mismatched CI run context;
- `production_ready=true` promotion;
- `live_provider_proven=true` promotion;
- arbitrary provider-simulated relabeling;
- packet path escape;
- malformed/tampered packet supplied to Health.

## Runnable acceptance

```bash
python tools/test-current-source-evidence.py
python tools/test-current-source-health-integration.py
```

Dedicated CI:

```text
Verify Current-Source Evidence
```

## Preserved invariants

```text
PLAN != EXECUTION
READY != EXECUTION
INTERPRETATION != AUTHORIZATION
OLD APPROVAL != NEW APPROVAL
CHAT MEMORY != SOURCE OF TRUTH
PROVIDER RESPONSE != COMPLETION PROOF
SIMULATED EVIDENCE != LIVE PROVIDER PROOF
RECOVERY != AUTOMATIC MUTATION REPLAY
```

Current-source verification changes evidence about current code only. It creates no execution authority.
