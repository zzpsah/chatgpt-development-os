# Session — 2026-09-13 — Failure + Recovery Proof

## Starting point

- Canonical repo: `zzpsah/chatgpt-development-os`.
- Production E2E Harness was already verified and merged through PR #11.
- Main closure checkpoint: `02e86393bf155404208a116f9fac2675b6d30acf`.
- Active branch created from that checkpoint: `devos/failure-recovery-proof`.
- PR: #12, `Failure + Recovery Proof: safe classification, HOLD, and resume`.

## Objective

Prove that DevOS can fail safely and continue deliberately after recoverable failures without manufacturing permission, bypassing gates, or blindly replaying uncertain mutations.

Reference recovery flow:

`E2E failure → deterministic classification → last-safe checkpoint → bounded repair or HOLD → fresh repository/gate revalidation → replay-safe retry → fresh verification → persistence/recovery`

## Material implementation actions

1. Added `core/failure-recovery-proof.md` defining `DEVOS-FAILURE-RECOVERY-v1`.
2. Added `tools/failure-recovery-proof.py` as a supervisor over existing DevOS contracts, not a second executor.
3. Added deterministic failure classes spanning interpretation/planning/readiness/controller/runtime/verification/persistence/recovery boundaries.
4. Added failed checkpoints containing failure class, failed stage, last safe stage, repository provenance, exact step, runtime operation, reason, and unchanged authority boundaries.
5. Required recompilation/revalidation after repository drift.
6. Added checkpoint authority-tamper rejection and persisted-evidence integrity checks.
7. Defined replay policy:
   - read-only/replay-safe failures may retry only after normal gates re-run;
   - once a mutation operation reaches the runtime adapter, recovery must `HOLD / MUTATION_REPLAY_FORBIDDEN` rather than replay automatically.
8. Distinguished mutation preflight rejection from an actual mutation adapter attempt.
9. Added `tools/test-failure-recovery-proof.py` covering stale plans, missing capability, authorization, Security Gate, provider/runtime failure, verification failure, persistence authorization, evidence corruption, checkpoint tampering, mutation preflight repair, and post-mutation no-replay behavior.
10. Wired the deterministic recovery corpus into `Verify Development OS Contracts`.
11. Added `tools/verify-failure-recovery-managed-project.py` for a real read-only recovery proof against `zzpsah/automation-suite`.
12. Extended the external managed-project workflow to run the recovery proof and upload checkpoint/result/proof evidence artifacts.

## CI-discovered cross-layer defect

The first deterministic recovery run showed that the test request `check security` never reached P17 authorization gating.

Root cause:
- P15 correctly emitted `HIGH_IMPACT_REQUIRES_AUTHORIZATION_CHECK`.
- P16 treated every ambiguity marker as material ambiguity and returned `CLARIFY`.
- Therefore the high-impact request was prevented from reaching the authorization/Security Gate designed to govern it.

Repair:
- P16 now treats `HIGH_IMPACT_REQUIRES_AUTHORIZATION_CHECK` as a gating annotation, not material ambiguity by itself.
- Genuine unresolved ambiguity still blocks.
- Authorization remains unchanged; security/high-impact steps still require independent authorization/Security Gate checks downstream.
- Added direct P16 regression coverage.

Evidence:
- Contracts run 497 passed the dedicated Failure + Recovery Proof after this repair.

## Real managed-project proof sequence

Target: `zzpsah/automation-suite`, ephemeral checkout only.

Injected failure:
- exact step capability set to `MISSING`.
- E2E stopped at READINESS.
- recovery classifier produced `CAPABILITY_MISSING`.
- checkpoint persisted locally under `.ai/EVIDENCE/`.

Repair:
- capability evidence changed from `MISSING` to `AVAILABLE`.
- recovery supervisor re-ran the normal E2E gates.
- read-only runtime path completed.
- verification returned `VERIFIED`.
- persisted E2E evidence was readable and structurally valid.
- repository HEAD/origin remained unchanged.
- no commit or push was performed.

## External proof wrapper defects and repairs

### First wrapper defect

The verifier assumed Git would produce one porcelain status line per new evidence file.

Observed behavior:
- Git coalesced untracked evidence into `?? .ai/EVIDENCE/`.

Repair:
- validate expected evidence files directly instead of counting status lines.

### Second wrapper defect

The Production E2E step runs earlier in the same checkout and had already created `.ai/EVIDENCE/`, so the recovery verifier saw the same `?? .ai/EVIDENCE/` line before and after adding recovery evidence.

Repair committed at `424a770fdd247fc318bb7a4a1bd8025634b1be1b`:
- explicitly require checkpoint/result/proof evidence files to exist and be non-empty;
- require unchanged HEAD and origin;
- require all worktree status entries to remain under `.ai/EVIDENCE`;
- require zero tracked source diff;
- do not require a new porcelain line when the evidence directory already exists.

## Verification evidence observed before final semantic-state commit

- Contracts 497: dedicated Failure + Recovery Proof passed after high-impact gating fix.
- Contracts 498 on `790d6eb7523719ce677c050a81715e07c41b71bd`: all contract steps through Failure + Recovery Proof passed.
- External 19 on the same verifier-fix lineage demonstrated successful P13 and Production E2E proofs; the recovery flow itself completed but the proof wrapper still had the preexisting-directory porcelain assumption, which was then repaired at `424a770f...`.

## Safety invariants preserved

- Interpretation, planning, readiness, recovery, retry requests, checkpoints, and successful earlier runs never create authorization.
- Security Gate remains independent.
- A saved checkpoint is not executable authority.
- No blind replay after a mutation reaches the runtime adapter.
- Managed-project proof remains read-only apart from authorized local `.ai/EVIDENCE/` writes in the ephemeral checkout.
- No commit/push to `automation-suite`.
- No production/destructive mutation introduced.

## Durable-state updates in this session

- `.ai/CURRENT-STATE.md` updated to reflect implemented recovery behavior, cross-layer fix, verifier repairs, and remaining final-head CI gate.
- `.ai/TASKS.md` updated from pending implementation to pending final verification/closure.
- `.ai/DECISIONS.md` updated with no-replay, high-impact gating, and real managed-project proof decisions.
- This session file records the action/provenance chain.

## Remaining closure steps

1. Take fresh Contracts, Full DevOS, and External Managed Project CI on the exact final branch head after semantic-state documentation.
2. Repair only evidence-backed defects if any.
3. Confirm PR #12 mergeable.
4. Merge only at the exact verified final head.
5. Persist Failure + Recovery Proof closure on `main`.
6. Advance to long-running multi-session / fresh-AI continuation proof.
