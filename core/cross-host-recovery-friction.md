# Cross-Host Recovery Friction & Onboarding Proof

## Purpose

Measure how much repository-only friction a fresh AI host encounters when recovering a DevOS project. This objective extends existing P11 repository-first recovery, Multi-AI portability, host profiles, auto-onboarding, and fresh-AI recovery checks. It does **not** create a second portability or state-authority system.

## Architecture

```text
Repository evidence + Git + DEVOS-HOST-PROFILE-v1
→ tools/recovery-friction.py
→ DEVOS-RECOVERY-FRICTION-v1 machine-readable report
→ tests / CI / later presentation
```

The repository remains the source of truth. Host profiles are capability declarations used to calculate deterministic friction; they are not observations of a real provider.

## Read-only invariant

Every report must preserve:

```text
mode: READ_ONLY
authority: UNCHANGED
authorization: UNCHANGED
execution: NONE
mutation: NONE
```

The analyzer must not:
- authorize or execute project work;
- mutate the repository or external providers;
- rewrite durable state or historical evidence;
- fill missing repository evidence from chat/account memory;
- convert deterministic host-profile simulation into live-provider proof;
- change authorization, Security Gate, verification, or replay rules based on host/vendor/account.

## Recovery inputs

The deterministic v1 recovery pack requires:
- `AGENTS.md`
- `.ai/manifest.yaml`
- `.ai/CURRENT-STATE.md`
- `.ai/TASKS.md`
- `.ai/DECISIONS.md`
- `core/ai-bootstrap-protocol.md`
- `core/project-router.md`
- `docs/handoff/README.md`

The analyzer also checks exact canonical repository identity, repository/source authority, an active-task section, durable authorization/authority decisions, and a stable handoff/recovery entrypoint.

## Host capability boundary

The existing `DEVOS-HOST-PROFILE-v1` vocabulary remains authoritative:
- `AVAILABLE`
- `DELEGATABLE`
- `MISSING`

Critical repository-recovery capabilities are:
- `project_discovery`
- `bootstrap`
- `inspection`
- `state_resolution`

A critical `MISSING` capability blocks recovery. `DELEGATABLE` is visible friction and never silently becomes AVAILABLE. Execution, verification, persistence, and intent-routing gaps affect continuation without changing recovered project authority.

## Friction metrics

`DEVOS-RECOVERY-FRICTION-v1` reports transparent counts:
- missing repository inputs;
- ambiguous repository inputs;
- blocked repository conditions;
- critical capabilities missing;
- noncritical capabilities missing;
- delegatable capabilities;
- total `friction_units`, defined as the sum of those issue counts.

`friction_units` is deliberately not a probability, quality percentage, production-readiness score, or authorization score.

## Status semantics

- `PASS` — deterministic repository recovery requirement is present at the checked source and host requirements are available for the stated scope.
- `WARN` — recovery can proceed but delegation or noncritical continuation friction remains.
- `UNKNOWN` — required repository evidence is missing/ambiguous or cannot be established.
- `BLOCKED` — canonical identity/source-head integrity fails, the host profile is invalid, or a critical recovery capability is missing.

`WARN` and `UNKNOWN` are never promoted to `PASS`.

The report separately exposes `recovery_status` and `continuation_status` so successful state recovery is not confused with ability to execute/verify/persist work on that host.

## Evidence classification

Deterministic output from this objective is classified:

`DETERMINISTIC_HOST_PROFILE_SIMULATION`

and must always state:

`real_cross_vendor_account_proven: false`

A real independent AI/vendor/account trial, if performed later, is a separate evidence class and requires actual observation. Host names, adapter labels, or simulated capability profiles do not prove that trial.

## Preserved safety invariants

```text
PLAN != EXECUTION
READY != EXECUTION
INTERPRETATION != AUTHORIZATION
OLD APPROVAL != NEW APPROVAL
SIMULATED EVIDENCE != LIVE PROVIDER PROOF
CHAT MEMORY != SOURCE OF TRUTH
PROVIDER RESPONSE != COMPLETION PROOF
RECOVERY != AUTOMATIC MUTATION REPLAY
```

## Universal product acceptance property

```text
AI A + Account A
→ repository
→ AI B + Account B
→ correct state recovery
→ safe continuation
```

This v1 objective measures deterministic repository/host-profile readiness for that property. It does not claim the final independent-host trial has happened.

## Runnable milestone gate

```bash
python tools/test-host-profile.py
python tools/test-fresh-ai-recovery.py
python tools/test-recovery-friction.py
```

All three must exit successfully for the deterministic implementation gate. Fresh exact-final-head CI remains required before closure.
