# Decisions

## Durable project state authority

- DevOS project-local `.ai` is the portable durable context layer.
- Source tree + Git are authoritative for implementation state and exact changes.
- AI account memory is supplementary and must not be treated as project authority.
- `STATE-INDEX.md` is an evidence index, not semantic authority.

## P9 milestone status

- P9 Development Task Controller v1 is implemented and integrated into the repository CI contract verification workflow.
- The existence of P9 is established by the Git commits recorded in project state.
- Future work must not restart or re-implement P9 merely because older roadmap text labels an earlier phase as current.

## P10 milestone status

- P10 Context Continuity & Recovery v1 is explicitly established from the post-P9 recovery incident and the documented context-sync verification gap.
- P10 focuses on repository-first recovery, durable session persistence, context-sync correctness, and evidence-backed continuity.
- P10 does not imply completion of higher-impact P8 remote mutations.

## Future persistence rule

- Meaningful future engineering work must be persisted in repository-local `.ai` state rather than relying on chat history.
- Session-level semantic outcomes belong in `.ai/SESSIONS/`.
- Changes to remaining work, intentional choices, or current project state must be reflected in `TASKS.md`, `DECISIONS.md`, or `CURRENT-STATE.md` as applicable.
- Generated `STATE-INDEX.md` remains deterministic evidence only.

## Verification boundary

- Static context-sync verification proves the repository contract is structurally present; it does not prove that GitHub Actions executed successfully or that a managed project's tests passed.
- P10 is complete only after fresh CI evidence and an actual project-side context-sync execution establish the end-to-end path.
