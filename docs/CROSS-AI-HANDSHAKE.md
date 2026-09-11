# Cross-AI Bootstrap / Recovery Handshake v1

## Purpose

Define a vendor-neutral handoff contract for a fresh AI tool, account, or chat entering a DevOS-managed project.

## Handshake inputs

The receiving AI reads, in order:

1. `AGENTS.md`
2. `.ai/manifest.yaml`
3. `.ai/STATE-INDEX.md` when present
4. `.ai/PROJECT.md`
5. `.ai/CURRENT-STATE.md`
6. `.ai/DECISIONS.md`
7. `.ai/TASKS.md`
8. latest relevant `.ai/SESSIONS/*.md`
9. actual source tree and Git history

## Handoff payload

A session handoff should contain these fields when evidence exists:

- `protocol_version`
- `project_id`
- `project_name`
- `repository`
- `devos_context_version`
- `current_objective`
- `verified_state`
- `active_work`
- `blocked_work`
- `recent_work`
- `recommended_next_action`
- `evidence_refs`
- `confidence`
- `unknowns`
- `generated_at`

## Evidence rules

- `verified_state` must come from repository evidence and explicit project context.
- `recommended_next_action` is a recommendation, not authorization.
- Unknown facts remain unknown.
- Generated indexes are navigation/evidence aids, not semantic authority.
- A receiving AI must inspect actual source/Git before making material technical conclusions.

## Conflict precedence

```text
Source + Git
   > explicit requirements/decisions
   > durable .ai semantic state
   > deterministic indexes
   > previous AI/chat memory
```

## Failure behavior

If the manifest is incompatible, identity is ambiguous, required semantic context is missing, or evidence conflicts materially:

```text
HANDSHAKE = NEEDS_REVIEW
```

The receiving AI must not silently overwrite semantic context to make the handshake appear healthy.

## Portability requirement

The handshake must not depend on:

- a particular AI vendor;
- a ChatGPT account or Memory state;
- a specific local machine;
- a specific GitHub account beyond repository access;
- undocumented chat history.

## Example flow

```text
Fresh AI
   ↓
Read AGENTS + manifest
   ↓
Resolve identity/compatibility
   ↓
Read durable state
   ↓
Check freshness/integrity
   ↓
Read session handoff
   ↓
Inspect source/Git
   ↓
Recover objective + blockers
   ↓
Produce HANDSHAKE = READY / NEEDS_REVIEW
```
