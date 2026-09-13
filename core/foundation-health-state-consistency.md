# Foundation Health & State Consistency

Protocol: `DEVOS-FOUNDATION-HEALTH-v1`.

## Purpose

DevOS must be able to diagnose its structural/project health from repository evidence without treating manually written status prose as the source of truth. This layer does not create a second truth system. It composes the existing Trust-First audit and production-readiness evidence ledger, derives a conservative machine status, and presents that status through a human-readable doctor command.

Canonical flow:

```text
Source / Git / Tests / CI
        ↓
tools/devos-audit.py
        ↓
config/readiness-evidence.json + tools/verify-readiness-evidence.py
        ↓
tools/devos-health.py
        ↓
tools/devos-doctor.py
```

`devos-doctor.py` is presentation only. The authoritative inputs remain source/Git/test/CI evidence, the Trust-First audit, and the versioned readiness ledger.

## Read-only boundary

The health and doctor layers are `READ_ONLY` and must always preserve:

- `authority: UNCHANGED`
- `authorization: UNCHANGED`
- `execution: NONE`
- `mutation: NONE`

They must not grant authorization, execute project work, mutate repository/provider state, rewrite evidence, refresh historical evidence, infer live-provider proof from simulation, or turn `WARN`/`UNKNOWN` into `PASS`.

## Outcomes

The machine health layer uses these conservative states:

- `PASS` — the inspected repository evidence supports the check.
- `WARN` — a real discrepancy or drift is observed but does not by itself prove structural failure.
- `UNKNOWN` — required evidence is absent/incomplete or the fact cannot be proven from the inspected source.
- `FAIL` — a required contract/evidence consistency check is demonstrably invalid.
- `BLOCKED` — continuation should stop because a trust boundary such as canonical identity or exact source-head expectation is violated.

Overall status is the most severe observed state. `WARN` and `UNKNOWN` are never promoted to `PASS`.

## Required diagnostics

The composed health report detects or surfaces at minimum:

1. canonical repository identity mismatch;
2. missing required bootstrap/audit dependencies;
3. malformed required `.ai` durable state;
4. stale/mismatched expected Git source head and dirty source state;
5. historical-source drift without rewriting pinned provenance;
6. inconsistent capability/evidence claims;
7. implemented/partial capabilities with missing verification evidence;
8. contradictory status documentation where machine/Git evidence can disprove prose;
9. missing dependency closure;
10. Security Gate wiring/dependency problems;
11. P15 interpretation, P16 planning, and P17 readiness contract/check availability;
12. evidence stronger than the declared protocol actually proves.

Offline checks cannot prove a remote branch has not moved unless an expected source head is supplied. That remains an explicit limitation, not a guessed PASS.

## Historical evidence rule

Historical evidence remains bound to its original source and run IDs. When current source differs from the archived source inventory, `tools/verify-readiness-evidence.py` exposes `historical_source_drift`, and Foundation Health maps that to `WARN`.

Drift means current-source equivalence is no longer proven by that historical record. It does **not** mean the historical event is false, and it never authorizes silently re-pointing the evidence to current HEAD.

## Safety invariants

These remain mandatory across the health/doctor layer:

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

The universal product target remains:

```text
AI A + Account A
→ repository
→ AI B + Account B
→ correct state recovery
→ safe continuation
```

No AI vendor, model, account, chat/session, machine, or Git-provider adapter is the durable source of project authority.

## Runnable checks

Authoritative component checks:

```bash
python tools/devos-audit.py
python tools/verify-readiness-evidence.py
```

Machine-derived status and human presentation:

```bash
python tools/devos-health.py --no-run-checks
python tools/devos-doctor.py --no-run-checks
```

A truthful `WARN`, `UNKNOWN`, `FAIL`, or `BLOCKED` returns non-zero. This is intentional; diagnostics must not hide unresolved evidence.

Milestone PASS/FAIL regression gate:

```bash
python tools/test-devos-audit.py
python tools/test-foundation-health.py
```

The adversarial corpus covers identity tampering, missing dependencies, unsupported claim promotion, contradictory status prose, historical-source drift, stale expected HEAD, malformed `.ai` state, and doctor non-promotion behavior.

## Non-goals

This layer does not prove production readiness, does not add a live mutation test, does not create an approval service, does not replace the readiness evidence ledger, and does not perform self-healing or automatic mutation replay. Any future mutation remains separately governed by exact authorization, Security Gate, verification, and recovery/no-replay rules.
