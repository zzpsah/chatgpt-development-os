# AI State Resolver v2 — Envelope Integrity Hardening

## Objective

Harden the existing AI State Resolver v2 → P16 → P17 propagation boundary so a malformed or tampered resolver envelope cannot hide uncertainty or manufacture authority/execution state.

This is an unnumbered bounded hardening objective. It does not create P18/P19 and does not expand runtime or provider authority.

## Observed gap

Before this hardening, P16 primarily checked the resolver protocol and `unresolved_claim_ids`. A crafted envelope could therefore omit or falsify uncertainty metadata while retaining the expected protocol. P17 similarly checked the unresolved list but did not validate the richer resolver invariants.

A second implementation mismatch existed for durable-state claims: recovery/handoff/path revalidation reasons were emitted only when the input confidence started as `observed`. The v2 contract states that those reasons remain explicit revalidation signals for durable-state grounding generally, including claims already supplied as `likely`.

## Changes

- Resolver status now becomes `NEEDS_EVIDENCE` whenever any resolved claim is `unknown`, even when a malformed claim has no usable claim ID.
- Durable-state recovery/handoff/path revalidation reasons are surfaced for already-`likely` claims as well as observed claims that decay to likely.
- P16 validates resolver v2 protocol, status, authority, authorization, execution, mutation, claim list, confidence summary, weakest confidence, and unresolved-claim consistency before planning.
- P16 preserves the full validated resolver provenance in the plan instead of replacing it with a reduced summary.
- P17 independently recomputes and validates that preserved resolver provenance. A `PLANNED` envelope with hidden unknown claims, changed authority/execution state, inconsistent counts, or an unresolved resolver status fails closed.

## Preserved boundaries

- Resolver authority: `UNCHANGED`.
- Resolver authorization: `UNCHANGED`.
- Resolver execution: `NONE`.
- Resolver mutation: `NONE`.
- `likely` remains an uncertainty signal but does not automatically block planning.
- `unknown`/`NEEDS_EVIDENCE` prevents governed continuation until clarified.
- P12 remains the owner of execution-evidence provenance and freshness.
- No provider call, production mutation, deployment, credential change, permission change, or destructive action is introduced.

## Regression coverage

The deterministic regression corpus now covers:

- durable-state boundary/path revalidation for claims already marked `likely`;
- unknown claims without a usable ID still producing `NEEDS_EVIDENCE`;
- P16 rejection of forged resolver authority/execution fields;
- P16 rejection of a forged `RESOLVED` envelope that hides an unknown claim;
- exact preservation of valid resolver provenance through P16;
- P17 rejection of preserved resolver provenance tampered to contain hidden uncertainty;
- P17 rejection of preserved resolver provenance whose authority boundary is changed.

## Completion standard

This objective is complete only when the exact candidate head has applicable automated verification and the durable session record is committed. Merge remains a separate authorization boundary.
