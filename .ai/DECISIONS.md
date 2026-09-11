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

- P10 Context Continuity & Recovery v1 is complete.
- P10 was closed only after fresh primary CI evidence and a real external project-side reusable workflow execution successfully generated durable context files.
- The validated external test project was `zzpsah/automation-suite` on branch `devos-p10-context-sync-test`.
- P10 does not imply completion of higher-impact P8 remote mutations.

## P11 milestone decision

- P11 is the current milestone: DevOS Federation & Self-Healing Context v1.
- P11 exists to make repository-first project continuity resilient across AI tools/accounts, chat loss, connectivity interruptions, stale generated state, and handoffs.
- P11 prioritizes versioned project identity, compatibility, freshness/integrity detection, safe reconciliation, cross-AI handoff, provenance, and deterministic self-healing.

## Future persistence rule

- Meaningful future engineering work must be persisted in repository-local `.ai` state rather than relying on chat history.
- Session-level semantic outcomes belong in `.ai/SESSIONS/`.
- Changes to remaining work, intentional choices, or current project state must be reflected in `TASKS.md`, `DECISIONS.md`, or `CURRENT-STATE.md` as applicable.
- Generated `STATE-INDEX.md` remains deterministic evidence only.

## Verification boundary

- Static context-sync verification proves the repository contract is structurally present; it does not prove that GitHub Actions executed successfully or that a managed project's tests passed.
- External-project execution evidence is required before declaring reusable context synchronization operational.
- P11 is complete only when a fresh AI/account can recover from repository evidence alone and deterministic context can self-heal without silently changing semantic project intent.
