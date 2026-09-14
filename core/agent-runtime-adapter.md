# Universal Agent Runtime Adapter v1

## Purpose

`DEVOS-AGENT-RUNTIME-HANDOFF-v1` is the runtime-neutral boundary between DevOS governance and an external/local coding agent runtime.

It exists so DevOS can govern **what may be attempted** while Codex-, Claude-, OpenHands-, Gemini-, or other compatible runtimes remain responsible for their own implementation mechanics.

The reference implementation is `tools/agent-runtime-handoff.py`.

## Core rule

> **DevOS governs the work unit; the agent runtime performs the bounded work; returned runtime claims become evidence only after independent validation.**

The adapter is deliberately side-effect free. It does not:

- edit files;
- run shell commands or tests;
- commit or push Git state;
- call a remote provider;
- grant approval;
- create authority;
- declare production readiness.

## Input boundary

A handoff may be compiled only from all of the following:

1. a `DEVOS-STEP-READINESS-v1` result with `status: READY`;
2. all P17 gates true;
3. `authority: UNCHANGED`, `authorization: UNCHANGED`, `execution: NONE`;
4. a low-impact mutation step that explicitly requires approval;
5. exact step-scoped approval bound to project, workflow, capabilities, targets, repository HEAD, and impact ceiling;
6. a `DEVOS-AGENT-RUNTIME-PROFILE-v1` runtime profile with the required local capabilities actually `AVAILABLE`;
7. a bounded work unit whose file paths are inside the approval target set.

A readiness result is not execution permission by itself. The separate approval scope is revalidated by the adapter.

## Runtime profile

Protocol: `DEVOS-AGENT-RUNTIME-PROFILE-v1`.

V1 requires these capabilities to be `AVAILABLE`:

- `filesystem.read`
- `filesystem.write_scoped`
- `git.inspect`
- `verification.run`

The profile is a capability declaration, not proof of successful execution and not authorization.

## V1 operation scope

The only mutation operation classes accepted by the reference handoff are:

- `file.create`
- `file.update`

Every target path must be a safe relative path and must be included in the exact approval target set.

The emitted handoff explicitly prohibits:

- file deletion;
- Git push or force update;
- deployment;
- production mutation;
- credential or secret changes;
- database mutation;
- permission changes;
- external network mutation;
- unscoped shell execution.

These are fail-closed boundaries, not advisory labels.

## Handoff integrity

A ready handoff contains normalized runtime identity, project/workflow, repository root token/path, exact repository HEAD, P17 step, approval scope, allowed paths/operations, constraints, prohibited operations, and evidence requirements.

The complete canonical handoff is SHA-256 hashed. The resulting digest is the `handoff_id`.

A runtime result must echo this ID. If the handoff content is modified after compilation, result validation returns `BLOCKED` with `HANDOFF_INTEGRITY_INVALID`.

## Result contract

Protocol: `DEVOS-AGENT-RUNTIME-RESULT-v1`.

A runtime may report `COMPLETED`, `FAILED`, or `BLOCKED`, but its self-reported status is not sufficient evidence.

For a completed mutation to become `VERIFIED_RUNTIME_RESULT`, the validator requires:

- the exact handoff ID;
- the exact runtime ID;
- the exact pre-execution repository HEAD;
- touched files contained within the approved path set;
- an observed diff whose changed paths exactly match the touched-file set;
- a SHA-256 digest for the observed diff;
- at least one passing test result with exit code `0` and output digest;
- final readback for every touched file with `PRESENT` status and content digest;
- no prohibited operation reported as used.

Any scope mismatch, failed test, missing readback, stale repository head, malformed evidence, prohibited operation, or integrity mismatch yields `HOLD` or `BLOCKED`.

## Evidence semantics

A verified runtime result is **execution evidence**, not authority.

The normalized evidence preserves:

```yaml
authority: UNCHANGED
authorization: UNCHANGED
execution: NONE
mutation: NONE
production_ready: false
```

`execution: NONE` here means the validator itself did not execute anything. The normalized evidence records what a runtime actually reported and what the validator was able to verify against the handoff contract.

The evidence rule is:

`RUNTIME_RESULT_IS_EVIDENCE_NOT_AUTHORITY`

## Relationship to P15 → P16 → P17

```text
human request
  ↓
P15 interpretation
  ↓
P16 bounded plan
  ↓
P17 exact-step readiness
  ↓
exact scoped approval
  ↓
Universal Agent Runtime Adapter v1
  ↓
runtime-specific implementation mechanics
  ↓
diff + tests + readback
  ↓
validated runtime evidence
  ↓
DevOS verification / durable reconciliation
```

The adapter does not bypass or replace P15, P16, P17, Actionable HOLD/Scoped Approval, the Development Task Controller, verification, or Evidence → Durable State Reconciliation.

## Relationship to Automated Software Delivery v1

Automated Software Delivery v1 may use this contract as the vendor-neutral handoff/result boundary for a local disposable repository.

The two concerns remain separate:

- **Software Delivery v1** proves an actual safe local delivery loop.
- **Runtime Adapter v1** standardizes how a governed work unit and its resulting evidence cross the boundary to/from an agent runtime.

The adapter therefore does not duplicate the local file mutation engine.

## Concurrency and portability

The contract intentionally contains no vendor-specific command syntax, model API, credentials, or account state. A concrete runtime integration may translate this envelope into its own execution mechanism, but it must preserve the same scope and evidence invariants.

Parallel AI development must re-check fresh `main` before integration and must not overwrite a newer delivery/runtime contract from another branch.

## Non-goals

- universal unattended execution;
- direct Codex/Claude/OpenHands API invocation;
- production deployment;
- remote Git mutation;
- destructive file operations;
- secret or credential management;
- database or permission mutation;
- arbitrary shell execution;
- automatic approval creation;
- automatic production-readiness promotion;
- a new numbered P18/P19 phase.

## Completion boundary

V1 is complete only when implementation, regression tests, documentation, exact-head CI, merge evidence, and durable post-merge reconciliation are present.

`production_ready = false` remains unchanged.
