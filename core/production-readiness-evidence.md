# Production-Readiness Evidence Matrix & Limitations v1

Protocol: `DEVOS-READINESS-EVIDENCE-v1`.

## Purpose

Inventory current capabilities and constrain readiness claims using inspectable historical provenance. This contract is an evidence-classification boundary, not execution authority or a production release certificate.

## Required representation

`config/readiness-evidence.json` covers bootstrap, project/state resolution, interpretation, planning, readiness, controller/orchestration, runtime, verification, security, persistence/recovery, continuation, self-healing, external reads, remote mutation and high-impact operations.

Each row records implementation status, concrete source references, verification levels, historical test/run/head references, authorization and Security Gate boundaries, recovery/no-replay behavior, an allowed claim, limitations, and explicit live-mutation/production non-claims. Planned or unavailable capability rows must not contain proof.

## Accepted evidence dimensions

- `deterministic`: component/contract checks.
- `integrated`: composed reference execution.
- `real_read_only`: live read or real managed-project read evidence; bounded ephemeral evidence persistence is described separately.
- `provider_simulated`: controlled mutation with a simulated provider.
- Empty evidence: unproven. Absence is never interpreted as success.

This protocol deliberately rejects live-provider mutation and production-proven promotion. A future version needs separately authorized live proof, a reviewed provenance model, and negative regression cases before it can express those claims. Labels alone cannot upgrade simulation.

## Verifier

`tools/verify-readiness-evidence.py` is offline and read-only. It checks schema invariants, coverage, safe paths, archived metadata integrity, successful recorded run/head matches, referenced workflow coverage and archived test-content hashes. Archived CRLF or LF source hashes are supported for portability. It rejects duplicate keys, missing families/limitations, evidence-level mismatch, stale test content, unsupported proof and changed authority.

Outputs: `VALID` (exit 0) or `HOLD` (exit 2), always with `production_ready: false`, `authority: UNCHANGED`, `authorization: UNCHANGED`, `execution: NONE`. VALID is ledger consistency, not a fresh runtime proof. No network requests, writes, test execution, credential use or mutations are performed by the verifier.

## Trust and freshness limitations

The checked-in archive is not a signed attestation. Its source SHA, run references and inventory are historical facts requiring independent provider/source review. The validator cannot prove natural-language claim truth, prevent a trusted repository editor from changing policy, or certify host isolation. Fresh CI for the validator proves its current behavior only; it does not refresh external historical proof. The readable companion lives at `docs/PRODUCTION-READINESS-EVIDENCE.md`.

## Closure criteria

All required families represented; concrete evidence and explicit unproven boundaries; meaningful negative regression coverage; inclusion in Contracts and Full CI; fresh applicable final-source-head CI; durable status/decisions/session records. Closing this documentation/validation gate does not mean DevOS is production ready.
