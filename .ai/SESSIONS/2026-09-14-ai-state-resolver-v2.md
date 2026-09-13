# Session — 2026-09-14 — AI State Resolver v2

## Objective

Upgrade the existing P0 AI State Resolver document contract into an executable deterministic resolver for evidence-backed state claims, without duplicating P12 evidence intelligence or weakening P17 readiness.

## Implementation

- Added `tools/ai-state-resolver.py` and adversarial regression coverage.
- Added grounded `observed | likely | unknown` claims, duplicate/uncited-claim detection, and recovery/handoff/path-change revalidation.
- Integrated resolver provenance with P16 and fail-closed P17 plan validation.

## Boundaries

The resolver is read-only. It does not parse all repository prose automatically, run tests, normalize P12 evidence, grant authorization, mark completion, or execute actions.

- Wired resolver v2 into the reference continuation path: supplied claims now flow through `P15 -> resolver -> P16 -> P17 -> controller`; uncited claims stop before readiness.

## Grounding correction

- A file/line reference to durable state establishes that an assertion was recorded, not that its underlying implementation or result is freshly true.
- Resolver v2 now caps `durable_state` claims at `likely`; only current P12 `execution_evidence` with citable provenance may retain `observed`.
- This preserves P12 as execution-evidence authority and prevents durable prose from self-upgrading a claim.
