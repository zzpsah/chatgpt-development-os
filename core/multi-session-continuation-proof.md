# Multi-Session / Fresh-AI Continuation Proof

Protocol: `DEVOS-MULTI-SESSION-v1`

## Purpose

Prove that meaningful DevOS work can span processes, sessions, AI agents, or vendors using repository-local evidence only, without relying on chat/account memory and without replaying stale execution authority.

This contract composes existing DevOS bootstrap, repository-first recovery, checkpoint, readiness, authorization, verification, and persistence boundaries. It does not create a second state store or execution system.

## Reference sequence

`Session A governed work → bounded continuation packet → persist repository-local evidence → process/AI boundary → Session B repository bootstrap → current Git revalidation → candidate reconstruction → fresh P16/P17/controller gates → bounded continuation → fresh verification → durable outcome`

## Continuation packet

A persisted continuation packet must contain only recoverable facts:

- protocol version;
- canonical project identity;
- active objective;
- repository head observed by Session A;
- optional exact compiled step/task id;
- last safe stage/checkpoint reference;
- constraints and verification obligations needed to understand the pending work;
- evidence references, not opaque claims of success;
- `authority: UNCHANGED`;
- `authorization: UNCHANGED`;
- `execution: NONE`.

A continuation packet must never contain a reusable bearer permission, secret, session cookie, provider credential, or statement that a prior candidate is automatically executable.

## Session B bootstrap

A fresh session/AI must:

1. identify the exact canonical repository from `AGENTS.md` / `.ai/manifest.yaml`;
2. read repository-local current state/tasks/decisions/recent relevant session provenance;
3. inspect current source + Git HEAD;
4. load the continuation packet only as supplementary repository evidence;
5. compare packet repository head to current repository head;
6. reconstruct the pending objective/step from current authoritative state;
7. re-run ordinary planning/readiness/controller gates before any runtime handoff.

Chat history, AI account memory, or an earlier agent's unstored reasoning cannot substitute for these steps.

## Repository-head outcomes

### Same head

If Session B observes the same repository head as Session A, the packet may establish continuity of facts but the saved candidate still requires `REVALIDATE_REQUIRED` semantics. Same-head continuity is not execution authority.

### Changed head

If Session B observes a different repository head:

- the saved compiled plan/candidate is stale;
- automatic replay is forbidden;
- outcome must be `RECOMPILE_REQUIRED`, `STOP`, or `ESCALATE` until the current repository is inspected and the objective is freshly compiled/revalidated;
- prior authorization evidence must not silently migrate to a newly compiled step.

## Authorization isolation

Authorization/Security Gate evidence is scoped to the exact current step/work unit and current governed attempt.

Across a fresh-session boundary:

- do not infer permission from the packet;
- do not infer permission from an earlier success;
- do not infer permission from a matching task id alone;
- do not infer permission after repository drift;
- do not copy approval from one step to another.

The packet may record that authorization was previously required or observed, but Session B must use current gate evidence according to existing P17/controller/runtime contracts.

## Mutation replay boundary

If Session A reached an uncertain/failed mutation runtime attempt, Session B must inherit the Failure + Recovery Proof's no-blind-replay rule. A continuation packet cannot downgrade `HOLD / MUTATION_REPLAY_FORBIDDEN` into a replay-safe candidate.

## Completion

Session B may declare continuation complete only when:

- current repository state has been revalidated;
- the current step is eligible under ordinary gates;
- bounded runtime work, if any, has current authorization;
- fresh applicable verification succeeds;
- outcome/evidence is persisted durably.

## Failure conditions

Fail closed on:

- malformed or unsupported continuation protocol;
- canonical project identity mismatch;
- missing repository-head evidence;
- changed repository head without fresh recompilation/revalidation;
- missing/contradictory active objective;
- packet authority/authorization fields not `UNCHANGED`;
- packet execution not `NONE`;
- stale candidate replay attempt;
- leaked authorization/Security Gate evidence;
- missing fresh verification after resumed work;
- corrupted or unavailable continuation evidence.

## Safety invariant

> Repository-local state preserves context, not permission. Continuation may reconstruct what work remains, but every executable candidate must earn current eligibility again.
