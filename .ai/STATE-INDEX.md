# DevOS State Index

This index is the durable map for fresh AI recovery. It intentionally points to repository-local evidence instead of relying on chat history.

## Read order
1. `AGENTS.md` — operating instructions, stance codes, security, completion rules.
2. `.ai/manifest.yaml` — portable-context schema and canonical repository identity.
3. `.ai/STATE-INDEX.md` — this map.
4. `.ai/PROJECT.md` — project purpose and scope.
5. `.ai/CURRENT-STATE.md` — current milestone, boundaries, verification, next target.
6. `.ai/repository-identity.json` — machine-readable canonical identity.
7. `core/devos-repository-identity.md` — normative repository-resolution rule.
8. `.ai/ARCHITECTURE.md` — system structure.
9. `.ai/DECISIONS.md` — durable architectural decisions.
10. `.ai/TASKS.md` — active/planned/completed work.
11. `.ai/SESSIONS/` — historical context where needed.
12. `.ai/AI-HANDOFF.md` — current fresh-AI recovery snapshot and repository map.

## Authority hierarchy
1. Git/source and live repository metadata are authoritative for implementation and current repository state.
2. `.ai` is the durable project-context layer.
3. Tests and CI are verification evidence.
4. Chat history and AI/account memory are supplementary and must not override repository evidence.

## Core operating contracts
- `core/devos-base-operating-rule.md` — constitutional rule and failure lifecycle.
- `core/devos-failure-resolution-engine.md` — bounded diagnosis/repair/re-verification.
- `core/documentation-integrity.md` — implementation/documentation synchronization.
- `core/human-language-execution-engine.md` — casual human command interpretation boundary.
- `core/desi-language-pack.md` — Hindi/Hinglish and colloquial language resources.
- `core/devos-worker-lifecycle.md` — worker state/observability boundary.

## Runtime implementation map
- `tools/devos-autonomous-loop.py` — bounded autonomous iteration.
- `tools/devos-runtime-persistence.py` — atomic runtime outcome persistence.
- `tools/devos-runtime-recovery.py` — deterministic recovery without replay authority.
- `tools/devos-scheduler.py` — one-unit Scheduler/Worker and bounded batch scheduling.
- `tools/devos-connection-preflight.py` — read-only configuration/DNS/network/TLS diagnostics.
- `tools/devos-command-interpreter.py` — bounded casual command normalization.
- `tools/test-*.py` — executable regression and contract guards.

## Repository identity
Canonical: `zzpsah/chatgpt-development-os`. The name `DEVOS` is an alias for this project, not a repository-search keyword that permits substitution. `SamyPesse/devos` is unrelated and must not be selected.

## Verification snapshot
The current documented development branch is `devos/documentation-integrity-v2` at `5e1d71844eb31157436577987412eeb5ba632cee`. PR #2 is open/draft/unmerged. Contract workflow run #414 (`34713521846`) completed successfully for that HEAD. Always re-check live Git/CI before acting because this index is a snapshot, not a lock.

## Documentation maintenance rule
Whenever material project state changes, update the affected durable record in the same change boundary. If this index or the handoff snapshot becomes stale, correct it before treating the recovery state as complete.
