# Session — AI State Resolver v2 envelope integrity hardening

Date: 2026-09-14
Repository: `zzpsah/chatgpt-development-os`
Base `main`: `67663bfedd9d15fed9d2acc2fd80063b0688d5d1`
Branch: `fix/ai-state-resolver-envelope-integrity`

## Trigger

Continuation resumed from the post-PR #43 durable state, where AI State Resolver v2 remained the active bounded work.

Fresh inspection found that P16 trusted a resolver v2 envelope mainly by protocol and `unresolved_claim_ids`, while P17 trusted the reduced planned summary similarly. This left an integrity gap where inconsistent resolver status/claims or changed authority/execution fields could be hidden inside a structurally plausible envelope.

Fresh inspection also found that durable-state boundary/path revalidation reasons were only emitted in the code path where an `observed` durable claim was first downgraded to `likely`, despite the contract treating those boundaries as explicit revalidation reasons for durable-state grounding generally.

## Changes

- `tools/ai-state-resolver.py`
  - status now reflects any unknown claim, including an unknown malformed claim without a usable ID;
  - durable-state revalidation reasons also apply to claims already marked `likely`.
- `tools/semantic-goal-to-plan.py`
  - validates complete resolver safety/integrity invariants before planning;
  - rejects inconsistent confidence/status/unresolved metadata;
  - preserves a compact normalized resolver summary for downstream validation.
- `tools/step-readiness-orchestrator.py`
  - validates the compact resolver summary in a `PLANNED` envelope;
  - fails closed on hidden unknown claims or changed resolver authority/execution state.
- Resolver/P16/P17 regression tests extended with adversarial cases.
- Added `docs/AI-STATE-RESOLVER-V2-INTEGRITY-HARDENING.md`.

## Boundaries

No authority is created. No authorization is created. No execution/provider mutation is performed by the resolver hardening. P12 remains the owner of execution-evidence provenance/freshness. No new numbered phase is created.

## Verification state

Implementation and deterministic regression coverage are committed on the candidate branch. Exact-head CI evidence must be checked after the pull request is opened. Merge requires explicit authorization.
