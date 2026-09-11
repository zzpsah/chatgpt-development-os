# P11 — DevOS Federation & Self-Healing Context v1

## Objective

Make Development OS resilient to AI-account changes, chat loss, connectivity interruptions, stale generated files, and handoff between different AI tools.

## Core model

```text
AI / Account / Chat
        │
        ▼
   Bootstrap Handshake
        │
        ▼
 .ai/manifest + state
        │
        ▼
 Git + Source Evidence
        │
        ▼
 Freshness / Integrity Resolver
        │
   ┌────┴────┐
   ▼         ▼
Healthy    Drift
   │         │
   │         ▼
   │    Safe Reconciliation
   │         │
   └────┬────┘
        ▼
 Current Project State
        │
        ▼
 AI Handoff / Next Action
```

## P11 boundaries

The repository is the durable project record. AI memories are supplementary. Derived indexes may be regenerated. Semantic decisions must retain provenance and must not be silently overwritten by generated state.

## Planned capabilities

### Versioned identity
`manifest.yaml` identifies the project, DevOS compatibility version, context schema, and supported bootstrap contract.

### Freshness and integrity
Detect stale `CURRENT-STATE.md`, missing context files, inconsistent references, unexpected generated-file drift, and divergence between `.ai` state and Git/source evidence.

### Safe reconciliation
Automatically repair only deterministic/derived context that can be reconstructed from repository evidence. Do not overwrite intentional decisions or semantic project state merely because generated data differs.

### Cross-AI handoff
A fresh AI should receive a compact, provenance-aware handoff containing project identity, current objective, verified state, active blockers, recent work, and recommended next action.

### Self-healing
When a required derived file is missing or malformed, recreate it from the authoritative sources. When ambiguity or semantic conflict exists, surface it instead of guessing.

### Recovery precedence
The canonical machine-readable recovery sources are:

1. `source+git` — source tree and Git for exact implementation state.
2. `requirements+decisions` — explicit project decisions and requirements for intent.
3. `ai-state` — durable `.ai` state for project context and handoff.
4. `generated-index` — deterministic generated indexes for navigation/evidence indexing.
5. `ai-memory` — AI account memory/chat history as supplementary context only.

These labels are contract identifiers used by the recovery resolver and verifier. They are ordered by authority for recovery decisions. AI memory is never authoritative.

### Fresh-AI repository revalidation

A fresh AI/account must first recover the repository identity and durable context, then perform **repository revalidation** against the current source tree and Git before acting on handoff conclusions. A handoff is evidence for navigation, not a substitute for current repository verification. If the handoff commit differs from current `HEAD`, semantic decisions changed, or confidence is insufficient, the receiving AI must revalidate material conclusions before execution.

## Completion standard

P11 is complete only when a fresh AI/account can recover the project from repository evidence alone, repository revalidation is explicit and executable, integrity drift can be detected safely, and deterministic context can self-heal without silently changing semantic project intent.
