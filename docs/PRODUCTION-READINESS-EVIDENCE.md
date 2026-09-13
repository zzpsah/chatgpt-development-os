# Production-readiness evidence and limitations

The machine-readable ledger is [config/readiness-evidence.json](../config/readiness-evidence.json).
Run `python tools/verify-readiness-evidence.py` from the repository root. Exit 0 / `VALID` means the ledger passes v1 integrity and claim rules. Exit 2 / `HOLD` means evidence or a claim is inconsistent. Neither outcome authorizes execution or certifies production readiness.

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

## Reconciliation with Trust-First main

PR #16 was reconciled against current `main` after PR #17 Trust-First closure rather than treating its original base as authoritative. The reconciliation preserved PR #16's ledger design and PR #17's read-only audit, audit-pack dependency closure, adversarial Security Gate regressions, and P17 semantic-impact hardening.

Reconciled implementation head `53492a4c842efcb2b8f07c2b71227599502a00a4` passed:
- Verify DevOS Trust-First Audit — run 16 / `34761934422`;
- Verify Development OS Contracts — run 553 / `34761934455`;
- Verify Development OS — run 478 / `34761934428`;
- Verify P13 External Managed Project — run 46 / `34761934406`.

Those runs prove the reconciled implementation/checking behavior at that exact head. They do **not** upgrade any historical ledger row to current evidence, do not establish live-provider mutation proof, and do not establish production readiness.

## Validator scope and maintenance

The verifier checks required families, exact typed invariants, status/level consistency, nonempty limitations, safe local references, archive hash, recorded successful CI run/source-head association, declared workflow coverage, historical source inventory membership, and explicit drift between archived test sources and the current checkout. Duplicate JSON keys, malformed or duplicate capability records, missing limitations, fabricated run IDs, source-head mismatches, stale evidence presented as fresh, unsupported live claims, unsupported production claims, and changed authority fail closed.

The archive is checked-in evidence metadata, not a signed attestation; an adversary able to rewrite code and evidence can rewrite these checks. Review remains necessary.

The verifier does not contact GitHub, run tests, authenticate approvals, prove prose semantics, inspect complete CI logs/artifact content, or infer a production verdict. Evidence classification changes require human review of actual scenarios. No live high-impact action should be run merely to fill a cell.

## Universal portability boundary

DevOS remains repository-first and host-neutral. The acceptance invariant is:

`AI A + Account A → repository → AI B + Account B → correct recovery → safe continuation`

AI vendor/model/account/chat state is not authoritative evidence and never manufactures authorization.

## Next direction

After this gate's exact-final-head CI closure, the smallest bounded direction is Foundation Health & State Consistency: stronger read-only doctor diagnostics, semantic status-drift detection, and portable onboarding/fresh-AI evidence. Live-provider mutation requires a separate exact authorization and is not the default next step.
