# Managed-Repository Delivery v1 — Read-Only Preflight

## Purpose

`DEVOS-MANAGED-REPOSITORY-PREFLIGHT-v1` prepares a proposed low-impact file change for a **local checkout of a managed repository** without changing that repository.

It is the bridge between the completed disposable-local delivery proof and any future separately authorized managed-repository mutation. It is not a mutation engine.

## Governed flow

```text
human request
  → P15 interpretation
  → P16 read-then-change plan
  → fresh Git-root / HEAD / clean-worktree inspection
  → P17 read readiness
  → P17 explicit approval requirement for the proposed change
  → deterministic approval request + external evidence packet
  → HOLD
```

The reference implementation is `tools/managed-repository-preflight.py`.

## Required inputs

- an existing local Git checkout supplied with `--repository`;
- a human-language `--phrase` that produces a bounded read-then-low-impact-change plan;
- one or more safe relative `--allow-path` values.

The checkout must be clean and the exact current `HEAD` must be available. Absolute paths, traversal paths, duplicate targets, a non-Git directory, a dirty worktree, unclear P15 objective, or an unsuitable P16 classification return `HOLD`.

## Approval request

A successful preflight returns `HOLD`, never `READY_FOR_EXECUTION`. Its deterministic approval request binds:

- project and workflow;
- local repository root and exact Git HEAD;
- P16/P17 change-step ID;
- `managed.repository.file.update` capability;
- exact permitted paths;
- only `file.create` and `file.update` operation classes;
- `LOW` impact ceiling;
- required diff, test, and final-readback evidence;
- explicit prohibited operations.

The preflight intentionally marks even a low-impact managed-repository change as requiring explicit step-scoped approval. Generating the request does not grant it.

## Evidence and persistence

`--output` may write the JSON packet only **outside** the inspected repository. This preserves the read-only target-repository boundary. The packet has an `evidence_id`, but it is external preflight evidence; it becomes durable repository evidence only through a later separately governed documentation/persistence step.

A fresh AI can recover the packet from its supplied path and re-check the exact repository head. If the head has changed, the request is stale and must be regenerated.

## Explicit non-goals

V1 does not:

- edit, test, commit, or push the managed repository;
- call a Git provider or external runtime;
- create approval or authority;
- use credentials, secrets, databases, permissions, deployment, production, deletion, or destructive actions;
- claim managed-repository delivery, provider proof, or production readiness.

`production_ready = false` remains unchanged.

## Example

```powershell
python tools/managed-repository-preflight.py `
  --repository C:\work\example `
  --phrase "Inspect current repository state then update docs note" `
  --allow-path docs/note.md `
  --output C:\evidence\example-preflight.json
```

A correct run exits zero with `status: HOLD` and both `READ_ONLY_PREFLIGHT_COMPLETE` and `EXPLICIT_STEP_SCOPED_APPROVAL_REQUIRED`. Any other result is not an authorization to write.
