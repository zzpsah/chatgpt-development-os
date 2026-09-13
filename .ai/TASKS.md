# DevOS Tasks

## Active
- **Foundation Health & State Consistency** is the current bounded objective. No P18/P19 phase is created.
- Preserve the architecture: `Source / Git / Tests / CI → devos-audit.py → readiness evidence ledger → machine-derived status → devos-doctor.py`.
- Keep `devos-doctor.py` presentation-only and READ_ONLY; it must not grant authority, execute work, mutate state, rewrite evidence, refresh historical proof, or promote `WARN`/`UNKNOWN` to `PASS`.
- Preserve P11 Federation & Self-Healing Context as the repository-first recovery/revalidation baseline.
- Require conservative detection for canonical identity, bootstrap/dependency closure, malformed `.ai`, Git/source mismatch, historical-source drift, capability/evidence inconsistency, missing verification evidence, contradictory status documentation, Security Gate wiring, P15/P16/P17 check consistency, and unsupported evidence promotion.
- Require the adversarial regression gate: `python tools/test-devos-audit.py && python tools/test-foundation-health.py`.
- Fresh exact-final-head Trust-First, Contracts and Full DevOS CI is required after durable documentation is complete. External Managed Project is required only when its path-filtered workflow is applicable; never invent a non-triggered run.
- Keep `production_ready = false` and all live-mutation proof false unless a reviewed future protocol plus separately authorized appropriate evidence genuinely proves otherwise.
- Do not run live/destructive/production/provider mutation merely to fill a diagnostic or evidence cell.

## Foundation Health implementation evidence
- Verified implementation head: `f7e0dd67561efedc27819bcd7b2fe2788565be2a`.
- Trust-First Audit 24 / `34763165651`: success.
- Contracts 561 / `34763165669`: success; Foundation Health regression step passed.
- Full DevOS 486 / `34763165638`: success; dedicated Foundation Health job passed.
- These runs precede durable documentation updates and are not final-head closure evidence.

## Completed recently
- Production E2E Harness — PR #11.
- Failure + Recovery Proof — PR #12.
- Multi-Session / Fresh-AI Continuation Proof — PR #13.
- Controlled Remote Mutation Proof — PR #14 at `ffbdd7a4849dd012604911accd1211f172bde53b`.
- Trust-First audit gap closure / adversarial Security Gate proof — PR #17, merged at `e13ce8df8c46ae95e26b3a8d02be374274eb2185`.
- Production-Readiness Evidence Matrix & Limitations — PR #16 final head `6c509d6f65b22666f121dfe86604faae72c08f8c`, merged at `b8e31ae76201b32e4617ef6044b29ef285004f54`.

## PR #16 final verification
- Trust-First Audit 22 / `34762214579`: success.
- Contracts 559 / `34762214457`: success.
- Full DevOS 484 / `34762214462`: success.
- External Managed Project 52 / `34762214609`: success.

## PR #16 post-merge main verification
At merge commit `b8e31ae76201b32e4617ef6044b29ef285004f54`:
- Trust-First Audit 23 / `34762783110`: success.
- Contracts 560 / `34762783133`: success.
- Full DevOS 485 / `34762783132`: success.
- External Managed Project does not run on `main` push and therefore has no post-merge run for this commit.

## Foundation Health acceptance targets
- `tools/devos-audit.py` remains an authoritative read-only dependency/check audit and includes bootstrap, P15 interpretation, P16 planning, P17 readiness, evidence-ledger, Security Gate/adversarial, and controlled-mutation dependency closure.
- `tools/devos-health.py` composes audit + ledger results into PASS/WARN/UNKNOWN/FAIL/BLOCKED without creating a new authority source.
- `tools/devos-doctor.py` only renders machine-derived status for humans.
- Historical source drift remains pinned and visible; it is never silently refreshed.
- Stale expected HEAD blocks; unavailable Git provenance remains UNKNOWN rather than guessed.
- Contradictory prose can warn, but prose never overrules source/Git/test/evidence truth.
- Missing dependencies/evidence remain UNKNOWN or FAIL according to the governing contract, never PASS.
- Unsupported production/live-provider promotion fails closed.
- Exact final-head CI must pass before closure.

## Universal portability invariant
`AI A + Account A → repository → AI B + Account B → correct recovery → safe continuation`

The repository, not any AI account/chat/model/vendor memory, carries authoritative project state.

## Safety invariants
- `PLAN != EXECUTION`
- `READY != EXECUTION`
- `INTERPRETATION != AUTHORIZATION`
- `OLD APPROVAL != NEW APPROVAL`
- `SIMULATED EVIDENCE != LIVE PROVIDER PROOF`
- `CHAT MEMORY != SOURCE OF TRUTH`
- `PROVIDER RESPONSE != COMPLETION PROOF`
- `RECOVERY != AUTOMATIC MUTATION REPLAY`
