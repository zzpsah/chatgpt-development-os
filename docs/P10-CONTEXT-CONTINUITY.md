# P10 — Context Continuity & Recovery v1

## Purpose

P10 hardens DevOS against loss of chat continuity, stale project state, and silent durable-context failures. The repository must remain sufficient for another AI session to reconstruct the engineering state and continue safely.

## Scope

1. Validate the durable `.ai` contract structurally in CI.
2. Keep the reusable context-sync workflow deterministic and configurable.
3. Ensure meaningful-path configuration is actually honored rather than silently replaced by a hardcoded classifier.
4. Preserve future engineering decisions, progress, blockers, and recovery notes in repository-local state.
5. Keep Git/source as implementation authority and `.ai` as portable project context.
6. Distinguish repository facts from semantic interpretation and verification claims.

## Completion criteria

- Context-sync contract verifier passes in primary DevOS CI.
- Configured meaningful-path patterns are consumed by the reusable workflow.
- Context-sync recursion guard remains present.
- Required durable context files are validated in the project template.
- Roadmap, tasks, decisions, and current state record the P10 scope and evidence.
- A future AI can recover from the repository without relying on this chat transcript.

## Explicit non-goals

- No unrestricted autonomous mutation.
- No production deployment automation.
- No claim that static context verification proves project correctness.
- No storage of secrets, tokens, passwords, session cookies, or unnecessary sensitive data.
- No inference that higher-impact P8 remote mutations are complete.

## Future continuity rule

Every meaningful DevOS session should persist the durable engineering outcome in `.ai/SESSIONS/` and update the appropriate `.ai/TASKS.md`, `.ai/DECISIONS.md`, and `.ai/CURRENT-STATE.md` records. Chat remains a working interface; the repository remains the recovery record.
