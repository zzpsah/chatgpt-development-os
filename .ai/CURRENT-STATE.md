# Current State

## Snapshot

- Repository: `zzpsah/chatgpt-development-os`.
- Source tree + Git are authoritative; ChatGPT Memory/chat history are supplementary only.
- P11 repository-first recovery/revalidation remains a durable invariant.
- P9 through P17 are complete on `main`.
- **Production E2E Harness is verified, merged, and closed on `main`.**
- Active maturity gate: **Failure + Recovery Proof**.

## Canonical governed path

`Human request → P15 interpretation → P16 plan → P17 readiness → P16 controller → P17 runtime handoff → bounded runtime-adapter operation → explicit verification → authorized persistence → recovery / continuation`

Interpretation, planning, readiness, orchestration and successful tests never manufacture permission. Runtime mutation, persistence, remote mutation and production/destructive actions remain independently bounded by capability, exact authorization, Security Gate, verification and recovery rules.

## P16 / P17 verified baseline

P16 merged through PR #9 at `460a212ebb7600619f396a455ac3e47e5a5c80fa`; final head `877833ef0f11d5a869284f9b86407c155125d96f` passed Contracts 476, Full 402, External 11.

P17 merged through PR #10 at `2f29ac1de367fb270c00d73b2ca44405ce09fc00`; final head `8011783962d6dddd33bcc50049c8aa4a8748cc52` passed Contracts 483, Full 408, External 12.

## Production E2E Harness closure

Normative contract: `core/production-e2e-harness.md`.
Executable harness: `tools/production-e2e-harness.py`.
Regression corpus: `tools/test-production-e2e-harness.py`.
Real managed-project verifier: `tools/verify-production-e2e-managed-project.py`.

Final verified source head: `4270440533925628a88daa17a6620aa51295319a`.
PR #11 merged to `main` at `1d6031d3578b859a6afe1dca1032287de5beceba`.

Fresh final-head verification:
- Verify Development OS Contracts — run 490 / `34751784035`: success.
- Verify Development OS — run 415 / `34751784082`: success.
- Verify P13 External Managed Project — run 15 / `34751784049`: success.

The E2E proof composes existing DevOS modules and proves the whole governed read-only path through runtime, verification, persistence and recovery. It does not introduce a general shell executor or new authority source.

### Proven runtime/persistence boundaries

- `READ_ONLY` compiled steps cannot execute mutation operations.
- Every runtime mutation requires exact-step `ALREADY_GRANTED` authorization.
- GitHub remote mutation additionally requires exact-step Security Gate `PASS`.
- Eligibility authorization and runtime-operation authorization remain distinct.
- Verification uses explicit argv through the existing reference verification adapter.
- Evidence persistence is restricted to bounded `.ai/` paths and requires independent authorization.
- Persistence does not itself commit or push.
- Recovery reads the evidence packet back through the bounded host adapter.

### Real managed-project proof

The external workflow checks out `zzpsah/automation-suite` and proves a read-only `filesystem.read` path against its real repository state. The verifier confirms exact origin identity, unchanged HEAD, verification success, bounded evidence persistence and recovery, with no commit or push to the managed repository.

Final External Managed Project run 15 passed the P13 proof, Production E2E proof and evidence artifact upload.

## Active maturity gate — Failure + Recovery Proof

Goal: prove that the merged Production E2E path fails safely, classifies bounded failures, preserves evidence, and can resume or deliberately HOLD after recovery without replaying unsafe work.

Required failure classes include:
- stale plan / repository drift;
- dependency failure;
- missing capability;
- exact-step authorization mismatch;
- Security Gate failure;
- runtime/provider unavailable or failed;
- verification failure;
- persistence write/corruption failure;
- recovery readback failure;
- ambiguous or invalid resume state.

Required outcomes:
- deterministic failure classification;
- no downstream execution after the failing gate;
- evidence of the failure and last safe checkpoint;
- bounded repair/revalidation where deterministic and authorized;
- otherwise safe `HOLD` / escalation;
- no blind replay of a previously uncertain or failed mutation;
- fresh verification after recovery before completion is claimed.

## Recovery precedence

1. Current source tree + Git.
2. Explicit requirements/decisions.
3. `.ai/CURRENT-STATE.md`, `.ai/TASKS.md`, and semantic `.ai` state.
4. `.ai/SESSIONS/` provenance.
5. Generated indexes as navigation/evidence only.
6. ChatGPT Memory/chat history as supplementary context only.

Exact implementation remains authoritative in Git history.
