# DevOS Maturity Roadmap

## Why this roadmap exists

DevOS has accumulated substantial capability across P0–P17. From this point, progress is measured by **system capability and evidence**, not by creating milestone numbers for their own sake.

## Verified foundation

P0–P15 remain the foundation. Their value is recorded in `docs/P0-P15-FOUNDATION-VALUE-AUDIT.md`.

The current verified mainline state is P15. P16 and P17 are active stacked development branches and must satisfy their own verification and merge gates before becoming mainline state.

## Gate 1 — P16

**Semantic Goal-to-Plan Compiler**

Acceptance:
- deterministic `DEVOS-GOAL-PLAN-v1` output;
- explicit dependencies, constraints, authority classes, evidence expectations, verification obligations, stop/escalation;
- mutating steps include read-before-write requirements;
- negative constraints and material ambiguity are preserved;
- no execution or authority is granted by compilation;
- fresh final-head CI passes.

## Gate 2 — P17

**Step Readiness & Authorization Orchestrator**

Acceptance:
- exact P16 step binding;
- current repository-head freshness;
- dependency completion;
- capability availability;
- exact-step authorization;
- Security Gate evidence for sensitive/high-impact work;
- verification path presence;
- stale/malformed plans stop safely;
- READY means eligible, never executed;
- fresh P17 E2E regression proof against resulting main after P16 merge.

## Gate 3 — Production E2E Harness

Prove the complete path on a managed software project:

```text
Human request
  ↓
Human Language Interpretation
  ↓
Project / state resolution
  ↓
Goal → Plan
  ↓
Step readiness
  ↓
Controller
  ↓
Authorization + Security
  ↓
Bounded Runtime
  ↓
Verification
  ↓
Persistence
  ↓
Recovery / continuation
```

This is the first major post-P17 maturity gate.

## Gate 4 — Failure and recovery proof

Inject bounded failures and prove:

- deterministic diagnosis where evidence permits;
- explicit `ROOT_CAUSE_UNCONFIRMED` when evidence is insufficient;
- smallest safe repair within authority;
- dry test/read-only probe where possible;
- fresh re-verification;
- regression protection;
- durable evidence;
- safe resume or explicit HOLD/ESCALATE.

Required failure classes include stale plan, dependency failure, capability absence, authorization mismatch, verification failure, persistence corruption, and connection-layer failures.

## Gate 5 — Long-running development

Prove that work can span multiple sessions without relying on chat memory:

```text
Session A → plan → bounded work → checkpoint
Session B → repository recovery → fresh gates → next step
Session C → verification → persistence → completion
```

A fresh AI must be able to recover the project from repository-local evidence and continue without replaying uncertain actions.

## Gate 6 — Controlled remote mutation maturity

Expand remote mutation only operation-by-operation:

`read current state → plan → authorization → Security Gate → dry-run/preview → bounded mutation → verification → evidence → recovery`

Production, destructive, deployment, database, credential, permission, merge, and other high-impact actions remain explicitly gated.

## Gate 7 — Production release readiness

Release readiness requires at minimum:

- whole-system E2E evidence;
- failure/recovery evidence;
- fresh-AI continuation evidence;
- security/authorization boundary tests;
- deterministic persistence/recovery tests;
- operational observability;
- documented limitations and known gaps;
- reproducible CI evidence;
- no unsupported claims of autonomy.

## Operating rule after P17

Do **not** create a new milestone number merely to create another layer. Create a new milestone only when a distinct capability boundary is demonstrated, independently testable, and required by a real gap.

The preferred unit of progress is now:

**GAP → IMPLEMENT → VERIFY → E2E PROVE → DOCUMENT → PERSIST → RESUME**
