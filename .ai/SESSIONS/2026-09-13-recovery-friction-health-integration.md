# Recovery Friction → Foundation Health/Doctor Integration — 2026-09-13

## Scope

Bounded unnumbered Trust-First integration objective. No P18/P19 phase is created.

## Architecture

```text
Trust-First audit + readiness evidence + DEVOS-RECOVERY-FRICTION-v1
→ tools/devos-health.py
→ tools/devos-doctor.py
```

No competing truth system is introduced. Recovery truth stays in `tools/recovery-friction.py`; Doctor remains presentation only.

## Implemented

- `tools/devos-health.py`
  - composes the existing recovery-friction analyzer;
  - adds `cross_host_recovery` health row;
  - preserves analyzer protocol/evidence class/recovery status/continuation status/friction counts/host and repository detail;
  - missing profile is UNKNOWN;
  - malformed profile is BLOCKED;
  - unsupported deterministic-to-real-host claim promotion is BLOCKED;
  - preserves worst-status health semantics.
- `tools/devos-doctor.py`
  - renders only the health-supplied recovery result;
  - shows evidence class, recovery/continuation status, friction units and real-cross-vendor/account flag;
  - does not import/call the recovery analyzer directly.
- `tools/test-foundation-health.py`
  - tampered identity propagation;
  - stale expected HEAD propagation;
  - missing/malformed profile;
  - critical host-capability BLOCKED propagation;
  - malformed durable state with recovery uncertainty;
  - doctor non-promotion of WARN/simulated evidence.
- `core/foundation-health-state-consistency.md`
  - documents the subordinate recovery-friction composition boundary.

## Safety boundary

All layers remain READ_ONLY with authority and authorization UNCHANGED, execution NONE, and mutation NONE.

`DETERMINISTIC_HOST_PROFILE_SIMULATION` remains distinct from an actual independent cross-vendor/account trial. Doctor cannot upgrade it.

No live/destructive/production/provider mutation was performed.

## Implementation-head verification

Implementation head: `40eea000d57f160781f2e2d846c126d366f42b86`.

- Trust-First Audit 51 / `34764991027`: success
- Contracts 588 / `34764990970`: success
- Full DevOS 513 / `34764991036`: success

Documentation commits followed this evidence, so fresh exact-final-head CI is required before closure/merge.

## Runnable gate

```bash
python tools/test-devos-audit.py && \
python tools/test-recovery-friction.py && \
python tools/test-foundation-health.py
```

## Remaining unproven boundary

No actual independent cross-vendor/account AI trial is established by this integration. Production readiness and live-provider mutation remain unproven.
