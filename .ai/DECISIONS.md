# Decisions

## Durable project state authority

- DevOS project-local `.ai` is the portable durable context layer.
- Source tree + Git are authoritative for implementation state and exact changes.
- AI account memory is supplementary and must not be treated as project authority.
- `STATE-INDEX.md` is an evidence index, not semantic authority.

## P9 milestone status

- P9 Development Task Controller v1 is implemented and integrated into the repository CI contract verification workflow.
- The existence of P9 is established by the Git commits recorded in `.ai/CURRENT-STATE.md`.
- Future work must not restart or re-implement P9 merely because older roadmap text still labels P8 as current.

## Roadmap reconciliation requirement

- `docs/ROADMAP.md` must be reconciled with the implemented P9 state before selecting or defining the next milestone.
- No P10 scope is assumed until explicitly established from repository evidence and updated project records.
