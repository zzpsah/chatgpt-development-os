# Production-readiness evidence and limitations

The machine-readable ledger is [config/readiness-evidence.json](../config/readiness-evidence.json).
Run `python tools/verify-readiness-evidence.py` from the repository root. Exit 0 / `VALID` means the ledger passes v1 integrity and claim rules. Exit 2 / `HOLD` means evidence or a claim is inconsistent. Neither outcome authorizes execution or certifies production readiness.

## Gate status

The Production-Readiness Evidence Matrix & Limitations gate closed through PR #16.

- Final PR #16 source head: `6c509d6f65b22666f121dfe86604faae72c08f8c`.
- Merge commit: `b8e31ae76201b32e4617ef6044b29ef285004f54`.
- Exact-final-head PR CI: Trust-First 22 / `34762214579`, Contracts 559 / `34762214457`, Full DevOS 484 / `34762214462`, External Managed Project 52 / `34762214609`, all successful.
- Fresh post-merge main verification: Trust-First 23 / `34762783110`, Contracts 560 / `34762783133`, Full DevOS 485 / `34762783132`, all successful.
- External Managed Project has no `push` trigger, so no post-merge External run exists for that merge commit.

Closure means the ledger/checker gate is implemented and verified. It does **not** mean DevOS is production ready.

## Evidence boundaries

The ledger deliberately keeps evidence historical: source snapshot `70c8e0e050660fd6b606150a1370d8fce51e373e`, with external proof at PR #14 source `bf5da56950d32722ce78898854eb3aa660321c38`. The cited run IDs and exact source heads remain in each row and the archived handoff evidence. A current successful ledger check is not a fresh execution of those historical scenarios and does not silently repoint them to current HEAD.

If a current test/source path changed after the historical snapshot, the verifier reports it under `historical_source_drift`. That means the old evidence remains valid only for its pinned historical source; a new current-source claim needs separate new evidence. Drift is never repaired by changing an old `source_head` or relabeling old evidence as `current`.

Deterministic = component/contract corpus; integrated = composed reference path; `real_read_only` = live GitHub repository/commit reads or real managed-project reads with bounded ephemeral evidence writes; `provider_simulated` = fake-provider controlled mutation. No live-mutation or production-proven level is accepted in v1.

## Capability matrix

| Capability | Implementation | Historical evidence | Known limitation |
|---|---|---|---|
| bootstrap | implemented | deterministic | Literal structural checks do not prove semantic state accuracy, Git identity or production readiness. |
| state | implemented | deterministic | Contract checks do not establish the truth of arbitrary project prose. |
| interpretation | implemented | deterministic | Regex/ASCII normalization is not general multilingual reasoning. |
| planning | implemented | deterministic | Planning never constitutes execution evidence. |
| readiness | implemented | deterministic, integrated | READY is eligibility only; caller approval provenance requires host trust. Current P17 test source has advanced beyond the archived snapshot and is surfaced as historical source drift rather than silently refreshed. |
| controller | implemented | deterministic, real_read_only | Small reference scenarios do not prove sustained arbitrary workload reliability. |
| runtime | implemented | integrated | The controlled mutation supervisor is not mandatory on every direct bridge entry point. |
| verification | implemented | integrated, real_read_only | Explicit argv avoids shell interpretation but does not sandbox a verifier executable. |
| security | implemented | deterministic | Validated gate markers are not a cryptographically authenticated approval service. |
| persistence_recovery | implemented | integrated, real_read_only | Ephemeral evidence writes are not proof of disaster recovery or durable storage guarantees. |
| continuation | implemented | deterministic, integrated, real_read_only | A fresh Python process is not an independent trial of every AI vendor or multi-day work. |
| self_healing | implemented | deterministic, integrated | Bounded reference repairs do not establish general production auto-repair. |
| external_reads | implemented | real_read_only | The live test does not exercise GitHub file readback or a live mutation. |
| remote_mutation | implemented | provider_simulated | No live DevOS runtime file mutation proof; direct-call integration and trusted gate origin remain limitations. |
| high_impact | planned | unproven | No live/production capability claim. Ordinary development commits and PR merges are not runtime proof. |

Every row in the JSON additionally names concrete implementation/test paths, authorization and Security Gate boundaries, recovery/no-replay policy, and the allowed claim. Live mutation and production proof remain explicitly false, including for high-impact paths.

## Trust-First composition

PR #16 was reconciled against Trust-First `main` after PR #17 closure rather than treating its original base as authoritative. The final merged design preserves the ledger and the read-only Trust-First audit, audit-pack dependency closure, adversarial Security Gate regressions, and P17 semantic-impact hardening.

Foundation Health & State Consistency now consumes this ledger through `tools/verify-readiness-evidence.py`; it does not rewrite the ledger. `tools/devos-health.py` combines the verifier result with `tools/devos-audit.py`, and `tools/devos-doctor.py` only presents the machine-derived result.

A health `WARN` for historical-source drift is therefore expected when current source has advanced beyond archived evidence. Doctor output never upgrades it to PASS or modifies provenance.

## Validator scope and maintenance

The verifier checks required families, exact typed invariants, status/level consistency, nonempty limitations, safe local references, archive hash, recorded successful CI run/source-head association, declared workflow coverage, historical source inventory membership, and explicit drift between archived test sources and the current checkout. Duplicate JSON keys, malformed or duplicate capability records, missing limitations, fabricated run IDs, source-head mismatches, stale evidence presented as fresh, unsupported live claims, unsupported production claims, and changed authority fail closed.

The archive is checked-in evidence metadata, not a signed attestation; an adversary able to rewrite code and evidence can rewrite these checks. Review remains necessary.

The verifier does not contact GitHub, run tests, authenticate approvals, prove prose semantics, inspect complete CI logs/artifact content, or infer a production verdict. Evidence classification changes require human review of actual scenarios. No live high-impact action should be run merely to fill a cell.

## Universal portability boundary

DevOS remains repository-first and host-neutral. The acceptance invariant is:

`AI A + Account A → repository → AI B + Account B → correct recovery → safe continuation`

AI vendor/model/account/chat state is not authoritative evidence and never manufactures authorization.

## Current bounded direction

The active bounded objective is Foundation Health & State Consistency: read-only machine-derived diagnostics over the existing Trust-First audit and readiness ledger, with a human `devos-doctor.py` presentation layer. It is not a new phase number and not a competing truth system.

Live-provider mutation requires separate exact authorization and is not part of this objective.
