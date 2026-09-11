# AI Handoff Provenance Contract v1

## Purpose
Every persisted AI handoff must be traceable to repository evidence so a receiving AI can distinguish recovered facts from generated summary.

## Required provenance
A handoff MUST record:

- protocol version
- project identity
- repository
- source Git commit (`git_commit`) when available
- generation source (`generated_from`)
- evidence file references
- semantic-state sources used for the summary
- generation timestamp from the project manifest when available
- confidence level
- explicit revalidation requirement

## Authority

- Git/source is authoritative for implementation state.
- `DECISIONS.md` and explicit requirements are authoritative for intent.
- `.ai` is durable project context.
- Generated handoff JSON is a portable summary, not a substitute for source inspection.

## Persistence

Persisted session records under `.ai/SESSIONS/` should reference the handoff artifact and record the originating Git commit when known.

## Revalidation

A receiving AI MUST revalidate material conclusions against current source/Git when the handoff commit differs from current HEAD, when confidence is not high, or when semantic decisions have changed.

## Safety

Provenance metadata must not contain secrets, tokens, passwords, session cookies, private keys, or unnecessary sensitive data.
