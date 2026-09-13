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

`tools/verify-readiness-evidence.py` is offline and read-only. It checks schema invariants, coverage, safe paths, archived metadata integrity, successful recorded run/head matches, referenced workflow coverage and archived source inventory membership. Archived historical evidence remains pinned to its original source SHA and is never silently repointed to current HEAD.

If a current referenced test has changed since the archived snapshot, the verifier reports that path in `historical_source_drift`. That drift does not rewrite or falsify the older proof; it means the historical evidence does not by itself prove the current source. A fresh/current claim requires separate fresh evidence rather than relabeling the historical row.

The verifier rejects duplicate keys, malformed/duplicate capability records, missing families/limitations, evidence-level mismatch, fabricated CI run IDs, source-head mismatches, stale evidence presented as fresh, unsupported live/production proof and changed authority.

Outputs: `VALID` (exit 0) or `HOLD` (exit 2), always with `production_ready: false`, `authority: UNCHANGED`, `authorization: UNCHANGED`, `execution: NONE`. VALID is ledger consistency, not a fresh runtime proof. No network requests, writes, test execution, credential use or mutations are performed by the verifier.

## Trust-First composition

PR #17 added the independent read-only Trust-First audit (`tools/devos-audit.py`), audit-pack dependency closure, cross-layer adversarial Security Gate coverage and P17 semantic impact revalidation. The readiness ledger composes with those controls; it does not duplicate or supersede them.

The universal portability invariant remains:

`AI A + Account A → repository → AI B + Account B → correct recovery → safe continuation`

No AI vendor/account/chat memory is authoritative evidence or authorization.

## Trust and freshness limitations

The checked-in archive is not a signed attestation. Its source SHA, run references and inventory are historical facts requiring independent provider/source review. The validator cannot prove natural-language claim truth, prevent a trusted repository editor from changing policy, or certify host isolation. Fresh CI for the validator proves its current behavior only; it does not refresh external historical proof. The readable companion lives at `docs/PRODUCTION-READINESS-EVIDENCE.md`.

## Closure criteria

All required families represented; concrete evidence and explicit unproven boundaries; meaningful negative regression coverage; Trust-First compatibility; inclusion in Contracts and Full CI; fresh applicable exact-final-source-head CI; durable status/decisions/session records. Closing this documentation/validation gate does not mean DevOS is production ready.
