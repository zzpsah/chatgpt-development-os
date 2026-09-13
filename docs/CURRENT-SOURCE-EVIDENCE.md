# DevOS Current-Source Evidence

Current-Source Evidence lets DevOS prove that a readiness-ledger-declared test passes against the exact current source without rewriting older historical proof.

## Why this exists

The readiness ledger deliberately preserves the original source heads and CI provenance that produced historical evidence. When source changes later, DevOS may report `historical_source_drift`.

That drift is not an error to hide. It means the old proof remains historical.

Current-Source Evidence adds a new ephemeral packet for the exact current checkout.

## Generate current evidence

Example for the P17 deterministic readiness test:

```bash
python tools/current-source-evidence.py \
  --capability readiness \
  --level deterministic \
  --test tools/test-step-readiness-orchestrator.py \
  --output .ai/EVIDENCE/current-readiness.json
```

The command executes only a test already declared by `config/readiness-evidence.json`.

A successful packet binds the exact Git HEAD, current test SHA-256, observed exit code, and execution context.

## Inspect through Foundation Health

```bash
python tools/devos-health.py \
  --no-run-checks \
  --current-source-packet .ai/EVIDENCE/current-readiness.json
```

Health validates the packet but does not execute its test.

Historical drift remains visible. A valid packet may additionally show the current test under `current_source_verified`.

## Inspect through DevOS Doctor

```bash
python tools/devos-doctor.py \
  --no-run-checks \
  --current-source-packet .ai/EVIDENCE/current-readiness.json
```

Doctor is presentation only. It does not recalculate evidence, grant authorization, or mutate the repository.

## Acceptance commands

```bash
python tools/verify-readiness-evidence.py
python tools/test-current-source-evidence.py
python tools/test-current-source-health-integration.py
python tools/test-foundation-health.py
```

## Evidence meaning

A valid current packet means only that the declared check succeeded against the exact current source represented by the packet.

It does **not** mean:

- historical evidence was refreshed or replaced;
- production readiness is proven;
- live provider behavior is proven;
- DevOS authorization exists;
- a READY step has executed;
- a provider response proves completion.

The packet always keeps:

```text
production_ready=false
live_provider_proven=false
authority=UNCHANGED
authorization=UNCHANGED
execution=NONE
mutation=NONE
```

## Conservative failure behavior

- malformed packet → `BLOCKED`
- tampered/stale packet → `BLOCKED`
- requested packet missing → `UNKNOWN`
- historical drift without current packet → historical WARN remains
- valid packet with remaining drift → current evidence may be valid while overall health remains WARN

WARN and UNKNOWN are never treated as PASS.
