# Session — AI State Resolver v2 envelope integrity hardening

Date: 2026-09-14
Repository: `zzpsah/chatgpt-development-os`
Base `main`: `67663bfedd9d15fed9d2acc2fd80063b0688d5d1`
Branch: `fix/ai-state-resolver-envelope-integrity`
PR: #44

## Trigger

Continuation resumed from the post-PR #43 durable state, where AI State Resolver v2 remained the active bounded work.

Fresh inspection found that P16 trusted a resolver v2 envelope mainly by protocol and `unresolved_claim_ids`, while P17 did not independently revalidate the richer resolver invariants. This left an integrity gap where internally inconsistent resolver status/claims or changed authority/execution fields could be hidden inside a structurally plausible envelope.

Fresh inspection also found that durable-state boundary/path revalidation reasons were only emitted in the code path where an `observed` durable claim was first downgraded to `likely`, despite the contract treating those boundaries as explicit revalidation reasons for durable-state grounding generally.

## Changes

- `tools/ai-state-resolver.py`
  - status now reflects any unknown claim, including an unknown malformed claim without a usable ID;
  - durable-state revalidation reasons also apply to claims already marked `likely`.
- `tools/semantic-goal-to-plan.py`
  - validates complete resolver safety/integrity invariants before planning;
  - rejects inconsistent confidence/status/unresolved metadata;
  - preserves the full validated resolver provenance exactly for downstream validation.
- `tools/step-readiness-orchestrator.py`
  - independently validates the full P16-preserved resolver provenance in a `PLANNED` envelope;
  - fails closed on hidden unknown claims or changed resolver authority/execution state.
- Resolver/P16/P17 regression tests extended with adversarial cases.
- Legacy P16/P17 synthetic fixtures upgraded to complete resolver v2 envelopes rather than weakening runtime validation.
- Added `docs/AI-STATE-RESOLVER-V2-INTEGRITY-HARDENING.md`.

## CI-discovered compatibility repairs

The first PR head correctly exposed an existing P16 contract expectation: a valid resolver result must be retained unchanged in `plan.state_resolution`. The first implementation normalized that result into a compact summary. The implementation was repaired to preserve the full resolver result after validation and to make P17 validate that full provenance directly.

A later candidate then exposed legacy P16 and P17 regression fixtures that constructed partial synthetic resolver dictionaries which were never complete v2 resolver output. Those fixtures were upgraded to full v2 envelopes; runtime validation was not relaxed.

## Verified candidate evidence

Candidate head `c696c4e9dc0e6443ea658c25fa54ce3a03a8c17c` passed every triggered PR gate:

- Verify Development OS Contracts — run `34806582900` — SUCCESS, including P16, P17, P17 handoff, AI State Resolver, controlled mutation proof, and the broader contract corpus.
- Verify Development OS — run `34806582887` — SUCCESS.
- Verify Current-Source Evidence — run `34806582913` — SUCCESS.
- Verify DevOS Trust-First Audit — run `34806582899` — SUCCESS.
- Verify DevOS MCP Repository Create — run `34806582888` — SUCCESS.
- Verify DevOS Actionable Hold — run `34806582884` — SUCCESS.
- Verify P13 External Managed Project — run `34806582879` — SUCCESS.

Historical failed intermediate heads remain part of the PR history and are not rewritten; they directly informed the compatibility repairs above.

## Boundaries

No authority is created. No authorization is created. No execution/provider mutation is performed by the resolver hardening. P12 remains the owner of execution-evidence provenance/freshness. No new numbered phase is created. `production_ready` is not upgraded by this objective.

## Verification state

Implementation, regression coverage, compatibility repair, documentation, and exact-candidate-head CI are established. This session-record update is documentation-only; its resulting final head still requires fresh applicable PR CI before merge readiness is claimed. Merge requires explicit authorization.
