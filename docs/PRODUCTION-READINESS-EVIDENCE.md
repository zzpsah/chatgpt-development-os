# Production-readiness evidence and limitations

The machine-readable ledger is [config/readiness-evidence.json](../config/readiness-evidence.json).
Run `python tools/verify-readiness-evidence.py` from the repository root. Exit 0 / VALID means the ledger passes v1 integrity and claim rules. Exit 2 / HOLD means evidence or a claim is inconsistent. Neither outcome authorizes execution or certifies production readiness.

## Evidence boundaries

The ledger deliberately keeps evidence historical: source snapshot `70c8e0e050660fd6b606150a1370d8fce51e373e`, with external proof at PR #14 source `bf5da56950d32722ce78898854eb3aa660321c38`. The cited run IDs and exact source heads are in each row and the archived handoff evidence. A current successful ledger check is not a fresh execution of those historical scenarios or a latest-main external proof.

Deterministic = component/contract corpus; integrated = composed reference path; real_read_only = live GitHub repository/commit reads or real managed-project reads with bounded ephemeral evidence writes; provider_simulated = fake-provider controlled mutation. No live-mutation or production-proven level is accepted in v1.

## Capability matrix

| Capability | Implementation | Historical evidence | Known limitation |
|---|---|---|---|
| bootstrap | implemented | deterministic | Literal structural checks do not prove semantic state accuracy, Git identity or production readiness. |
| state | implemented | deterministic | Contract checks do not establish the truth of arbitrary project prose. |
| interpretation | implemented | deterministic | Regex/ASCII normalization is not general multilingual reasoning. |
| planning | implemented | deterministic | Planning never constitutes execution evidence. |
| readiness | implemented | deterministic, integrated | READY is eligibility only; caller approval provenance requires host trust. |
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

## Validator scope and maintenance

The verifier checks required families, exact typed invariants, status/level consistency, nonempty limitations, safe local references, archive hash, recorded successful CI head/run association, workflow test presence, and test content against the archived source inventory. Windows checkout line endings are normalized for source comparison. Duplicate JSON keys, stale test content, missing coverage, fake run IDs and unsupported live/production promotions fail closed. The archive is checked-in evidence metadata, not a signed attestation; an adversary able to rewrite code and evidence can rewrite these checks. Review remains necessary.

The verifier does not contact GitHub, run tests, authenticate approvals, prove prose semantics, inspect complete CI logs/artifact content, or infer a production verdict. A changed test requires evidence refresh rather than editing a hash to hide drift. Evidence classification changes require human review of actual scenarios. No live high-impact action should be run merely to fill a cell.

## Next direction

After this gate's final-head CI closure, prioritize Foundation Health & State Consistency: stronger read-only bootstrap/doctor diagnostics, semantic status-drift detection, and portable onboarding evidence. Preserve the independent-audit universal AI portability direction. Live-provider mutation requires a separate exact authorization and is not the default next step.
