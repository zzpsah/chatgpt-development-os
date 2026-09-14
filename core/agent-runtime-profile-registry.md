# Agent Runtime Profile Registry + Conformance v1

## Purpose

`tools/agent-runtime-profile-registry.py` gives DevOS a durable, deterministic boundary between a runtime name being known and a runtime actually being verified as compatible with the Universal Agent Runtime Adapter v1.

Protocol: `DEVOS-AGENT-RUNTIME-PROFILE-REGISTRY-v1`.

The registry exists because a caller-supplied runtime profile is not durable evidence. A runtime must not become handoff-ready merely because its name is familiar or because another AI claims that it can edit files or run tests.

## Core rule

> **Declared runtime identity is not verified runtime capability.**

Only an evidence-backed `VERIFIED` registry entry may be exported as `DEVOS-AGENT-RUNTIME-PROFILE-v1` for `tools/agent-runtime-handoff.py`.

## Required handoff capabilities

A verified v1 runtime must have evidence-backed availability for exactly:

- `filesystem.read`
- `filesystem.write_scoped`
- `git.inspect`
- `verification.run`

Unknown capabilities are rejected. Missing required capabilities fail closed.

## Profile states

### `DECLARED`

The runtime is named in the registry but has no repository-accepted conformance proof. It is **not handoff-ready**.

### `VERIFIED`

The required capability set is explicitly present, each required capability is `VERIFIED_AVAILABLE`, and at least one non-empty evidence reference is recorded.

Only this state may export a handoff-compatible runtime profile.

### `REVOKED`

Prior evidence has been withdrawn or superseded. A revoked runtime is not handoff-ready and must retain evidence explaining the revocation boundary.

## Vendor templates

The seed registry contains declaration-only templates for:

- `codex`
- `claude-code`
- `openhands`

These entries intentionally contain no verified capability claims. Their presence means only that DevOS has a stable runtime identifier ready for a future bounded conformance proof.

No product/vendor capability is inferred from marketing, documentation, model familiarity, chat memory, or external reputation.

## Reference profile

`reference-local-agent` is a repository contract profile used to prove registry/export behavior. Its evidence scope is explicitly `static-contract-conformance`.

It does **not** prove a real vendor integration, external execution, provider access, autonomous delivery, deployment, network mutation, or production readiness.

## Export behavior

For a verified entry the registry emits a `DEVOS-AGENT-RUNTIME-PROFILE-v1` object with the required four capabilities marked `AVAILABLE`. This shape is compatible with the existing Universal Agent Runtime Adapter v1 runtime-profile contract.

Export means **contract compatibility only**. It is not approval, readiness, execution, or completion evidence.

## Fail-closed rules

The registry returns HOLD/BLOCKED when:

- registry protocol or shape is invalid;
- runtime IDs are duplicated;
- unknown capabilities are introduced;
- a `VERIFIED` entry is missing any required capability;
- a required verified capability is marked missing;
- a `VERIFIED` entry has no evidence;
- a declaration-only or revoked runtime is requested for handoff;
- the runtime is not registered.

A runtime cannot self-upgrade from `DECLARED` to `VERIFIED` merely by changing the status field; required capability and evidence validation independently fail closed.

## Permanent boundaries

```yaml
authority: UNCHANGED
authorization: UNCHANGED
execution: NONE
mutation: NONE
production_ready: false
```

The registry performs no runtime invocation, repository mutation, provider call, approval creation, deployment, credential access, database action, permission change, or destructive action.

## Relationship to Universal Agent Runtime Adapter v1

- profile registry answers: **is this runtime profile durably verified enough to be considered for a handoff?**
- runtime handoff answers: **does this specific P17 READY + scoped approval + work unit safely compile into a runtime-neutral handoff, and does returned evidence satisfy the handoff?**

The registry does not replace P15, P16, P17, scoped approval, controller/runtime execution, result verification, or durable evidence reconciliation.

## Concurrency rule

Parallel AI development is expected. Runtime-registry work must not modify the concurrently owned Automated Software Delivery v1 execution path unless a separately bounded integration objective is promoted after both features are merged and freshly recovered.

## Completion boundary

This v1 is complete when:

- the registry schema and validator are merged;
- declaration-only vendor templates are proven unable to self-promote;
- a repository-only reference profile can export the existing handoff profile shape;
- adversarial tests pass;
- exact-head CI passes;
- the capability is durably documented and reconciled.
