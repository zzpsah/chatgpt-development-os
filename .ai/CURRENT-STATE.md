# Current State

## Current source and authority

- Repository: `zzpsah/chatgpt-development-os` on current `main`.
- Source tree + Git are authoritative for implementation and exact state. `.ai` records carry durable semantic context. Chat/model memory is supplementary only.
- `docs/DEVOS-MASTER-ENGINEERING-MAP.md` is the living architecture index; `docs/handoff/README.md` is the stable historical handoff entry.

## Core documentation law

> **What is not written was never done.**

Material work requires `IMPLEMENTED + VERIFIED + DOCUMENTED + DURABLE STATE`.

## Canonical governed path

`Human request -> P15 interpretation -> P16 plan -> P17 readiness -> Actionable HOLD / Scoped Approval -> controller -> bounded runtime -> verification -> persistence -> recovery / continuation`

## Active state

### GitHub App live read-only verification — evidence pending

The repository-side GitHub Identity & Token Control Plane v1 is merged through PR #32. The remaining active gate is a fresh read-only GitHub Actions proof against the installed GitHub App and `zzpsah/chatgpt-development-os`.

The proof must establish provider authentication and repository readback without mutation. It must preserve `authorization: UNCHANGED`, `execution: NONE`, `mutation: NONE`, and must not disclose credential material.

## User-reported external setup — not live proof

- A GitHub App named **DevOS GitHub** was reportedly created and installed for this repository.
- The App ID, client ID, and Actions-secret setup are recorded only in dated session provenance; secret values are never durable repository state.
- Treat these as user-reported until a fresh workflow proves them.

## Implemented and closed foundations

- P9 through P17 are complete at their recorded evidence levels.
- AI State Resolver v2 is merged and documented. Current P12 execution evidence is required for `observed`; durable state is capped at `likely`.
- Plain Project Context and Recovery Guide v1 is merged and is the default first-contact path.
- GitHub Identity & Token Control Plane repository implementation is merged and contract-tested; live-provider proof remains separate.

## Current boundaries

- `production_ready = false`.
- `live_provider_proven = false`.
- Controlled remote mutation remains provider-simulated / contract-level evidence unless separately proven.
- Provider credentials are technical capability only and never DevOS authorization.
- Provider response is attempt evidence, not completion proof. Uncertain mutation is never blindly replayed.

## Recovery and next action

1. Inspect current Git/CI evidence for the read-only GitHub App workflow.
2. If live evidence is absent, remain HOLD and report the exact required external setup/evidence.
3. If a fresh workflow succeeds, record only non-secret observed results, then reassess the next bounded objective.
4. Do not create P18/P19 merely for bookkeeping.

## Historical evidence

Historical PR hashes, CI counts, and prior closure details are preserved in Git history, `.ai/SESSIONS/`, `docs/handoff/`, and the master engineering map. They are intentionally not mixed into this live state view.
