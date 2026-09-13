# Cross-Host Recovery Friction & Onboarding Proof — 2026-09-13

## Scope

Bounded unnumbered Trust-First portability objective. No P18/P19 phase was created.

## Gap

DevOS already had repository-only fresh-AI recovery, Multi-AI portability contracts, host profiles, auto-onboarding, and multi-session continuation proof. The missing evidence was a stable machine-readable measurement of repository recovery/adoption friction across host capability profiles.

## Implemented

- `tools/recovery-friction.py`
  - protocol `DEVOS-RECOVERY-FRICTION-v1`
  - READ_ONLY
  - exact canonical repository identity checks
  - required repository recovery-pack inspection
  - optional expected-HEAD binding
  - reuses `DEVOS-HOST-PROFILE-v1`
  - separates `recovery_status` from `continuation_status`
  - exposes transparent issue-count `friction_units`
  - always classifies deterministic output as `DETERMINISTIC_HOST_PROFILE_SIMULATION`
  - always keeps `real_cross_vendor_account_proven: false`
- `tools/test-recovery-friction.py`
  - clean repository/all-available profile
  - example profile delegation friction
  - missing durable state
  - tampered canonical identity
  - missing critical capability
  - missing noncritical capability
  - stale expected HEAD
  - invalid host profile
- `core/cross-host-recovery-friction.md`
  - normative evidence/status/safety contract
- Contracts and Full DevOS workflows execute the new gate.

## Preserved boundaries

```text
mode: READ_ONLY
authority: UNCHANGED
authorization: UNCHANGED
execution: NONE
mutation: NONE
```

No chat/account memory fills missing repository evidence. No host label or simulated capability profile becomes real provider/account proof. Authorization, Security Gate, verification, and mutation replay policy do not vary by AI host.

## Runnable gate

```bash
python tools/test-host-profile.py && python tools/test-fresh-ai-recovery.py && python tools/test-recovery-friction.py
```

## Implementation-head verification

Implementation head: `d7b4a84d3f9321091aac0bff2a3438647dcf8ec2`.

- Trust-First Audit 39 / `34764579792`: success
- Contracts 576 / `34764579787`: success
- Full DevOS 501 / `34764579789`: success
- Dedicated Full DevOS recovery-friction job: success

These are implementation-head results only. Durable documentation was committed afterward, so a fresh exact-final-head CI cycle is required before closure/merge.

## Remaining UNKNOWN

A real independent AI vendor/account trial has not been performed by this deterministic objective. The universal product property remains the goal, while this evidence proves only repository/profile-level recoverability and friction measurement.

No live/destructive/provider/production mutation was performed.
