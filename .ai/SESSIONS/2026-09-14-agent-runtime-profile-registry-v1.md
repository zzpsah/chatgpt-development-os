# Session — Agent Runtime Profile Registry + Conformance v1

Date: 2026-09-14

## Objective

Add a durable runtime-profile registry that separates known runtime identifiers from evidence-backed handoff conformance, without duplicating the concurrently owned Automated Software Delivery v1 execution work.

## Starting point

- Fresh integration base: `2ef6b6e3df832ca132123b85caa69f7eda67d1f3`.
- Universal Agent Runtime Adapter v1 was already closed through PR #57 and therefore was not reimplemented.
- Managed-repository delivery work is owned by another concurrent AI and this branch intentionally avoids its execution/delivery files.

## Gap observed

`tools/agent-runtime-handoff.py` validates a caller-supplied `DEVOS-AGENT-RUNTIME-PROFILE-v1`, but durable repository state did not yet distinguish a runtime that was merely named from a runtime with evidence-backed conformance.

## Implemented

- `config/agent-runtime-profile-registry.json`: durable registry seed.
- `tools/agent-runtime-profile-registry.py`: deterministic validator/exporter.
- `tools/test-agent-runtime-profile-registry.py`: adversarial conformance corpus.
- `core/agent-runtime-profile-registry.md`: normative declaration-vs-verification contract.
- `.github/workflows/verify-agent-runtime-profile-registry.yml`: dedicated exact-head CI.

The registry includes a repository-only `reference-local-agent` VERIFIED profile and declaration-only templates for `codex`, `claude-code`, and `openhands`. Vendor templates carry no verified capability claims.

A VERIFIED profile must evidence all four Universal Agent Runtime Adapter v1 capabilities: `filesystem.read`, `filesystem.write_scoped`, `git.inspect`, and `verification.run`. Unknown or missing capabilities fail closed. Declaration-only and revoked entries cannot export a handoff-ready runtime profile.

## Regression proof

The tests cover:

- valid registry seed;
- verified reference profile export;
- declaration-only vendor HOLD behavior;
- unknown runtime HOLD;
- forged DECLARED→VERIFIED status without evidence/capabilities;
- missing required capability;
- duplicate runtime IDs;
- unknown `unscoped.shell` capability;
- revoked profile HOLD;
- unchanged authority/authorization/execution/mutation/production-readiness boundaries.

## Concurrency boundary

This branch does not implement Automated Software Delivery v1, managed-repository execution, agent invocation, target-repository writes, approval grants, commits, pushes, provider operations, deployment, credentials, databases, permissions, or destructive actions.

The integration branch was recreated from fresh `main` after the concurrent managed-repository write proof advanced source. Only the six isolated registry files were carried forward.

## Permanent boundaries

- `authority = UNCHANGED`
- `authorization = UNCHANGED`
- `execution = NONE`
- `mutation = NONE`
- `production_ready = false`

## Remaining before completion

- fresh main/open-work comparison before PR;
- exact-final-head applicable CI;
- compatibility repair only if it preserves conformance semantics;
- merge under current bounded authorization when current head and mergeability remain valid;
- post-merge durable reconciliation without recursive bookkeeping.
