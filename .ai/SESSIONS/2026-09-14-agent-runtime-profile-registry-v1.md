# Session — Agent Runtime Profile Registry + Conformance v1

Date: 2026-09-14

## Objective

Add a durable runtime-profile registry that separates known runtime identifiers from evidence-backed handoff conformance, without duplicating the concurrently owned Automated Software Delivery v1 execution work.

## Starting point

- Fresh `main` at branch creation: `cf048bcfcc9c383859bb76997257561589debbcf`.
- Universal Agent Runtime Adapter v1 was already closed through PR #57 and therefore was not reimplemented.
- Automated Software Delivery v1 is owned by another concurrent AI and this branch intentionally avoids its execution/delivery files.

## Gap observed

`tools/agent-runtime-handoff.py` validates a caller-supplied `DEVOS-AGENT-RUNTIME-PROFILE-v1`, but repository state did not yet provide a durable registry proving whether a runtime profile was merely declared or actually evidence-backed.

Without a separate conformance registry, a future caller could repeatedly construct runtime profiles outside durable repository evidence.

## Implemented

### Registry seed

`config/agent-runtime-profile-registry.json`

- protocol `DEVOS-AGENT-RUNTIME-PROFILE-REGISTRY-v1`;
- `reference-local-agent` repository-only verified contract profile;
- declaration-only templates for `codex`, `claude-code`, and `openhands`;
- vendor templates carry no verified capability claims.

### Validator/exporter

`tools/agent-runtime-profile-registry.py`

- validates registry protocol and exact profile shape;
- rejects duplicate runtime IDs;
- rejects unknown capabilities;
- requires all four Universal Agent Runtime Adapter v1 capabilities for a `VERIFIED` profile;
- requires evidence for `VERIFIED` entries;
- prevents declaration-only or revoked entries from becoming handoff-ready;
- exports only a verified profile into the existing `DEVOS-AGENT-RUNTIME-PROFILE-v1` shape;
- preserves `authority=UNCHANGED`, `authorization=UNCHANGED`, `execution=NONE`, `mutation=NONE`, `production_ready=false`.

### Regression corpus

`tools/test-agent-runtime-profile-registry.py`

Proves:

- registry seed validates;
- repository reference profile exports successfully;
- declaration-only `codex`, `claude-code`, and `openhands` profiles HOLD;
- unknown runtime HOLDs;
- changing a vendor template status to `VERIFIED` without capabilities/evidence still fails closed;
- missing required capability fails closed;
- duplicate runtime IDs fail closed;
- unknown `unscoped.shell` capability fails closed;
- revoked profile cannot export;
- exported profile preserves permanent authority/execution/mutation boundaries.

### Normative contract and CI

- `core/agent-runtime-profile-registry.md` defines declaration vs verification semantics and non-goals.
- `.github/workflows/verify-agent-runtime-profile-registry.yml` runs the registry corpus and contract-marker checks.

## Concurrency boundary

This branch does not implement or claim Automated Software Delivery v1. It does not execute an agent, mutate a target repository, run a managed delivery, grant approval, or integrate a specific vendor runtime.

A future vendor conformance proof or delivery integration must be a separate bounded objective after fresh recovery of both merged capabilities.

## Permanent boundaries

- no deploy/production;
- no credentials/secrets;
- no database mutation;
- no permission change;
- no destructive action;
- no provider/network mutation;
- no automatic approval;
- no vendor capability inferred from familiarity or external reputation;
- `production_ready = false`.

## Remaining before completion

- re-read fresh `main` and open PRs before integration;
- preserve concurrent Automated Software Delivery work;
- open bounded PR;
- require exact-final-head applicable CI;
- repair only verified compatibility failures without weakening conformance rules;
- merge under current bounded authorization only if fresh head/mergeability remain valid;
- reconcile durable state once and avoid recursive bookkeeping PRs.
