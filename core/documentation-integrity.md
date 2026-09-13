# Documentation Integrity Contract v1

## Philosophy

> **What is not written was never done.**

DevOS treats durable repository documentation as part of implementation, not optional follow-up work. A material code, contract, workflow, architecture, policy, or operational change is not complete until the affected durable project record changes in the same verified change boundary.

## Rules

1. **Material change and durable record travel together.**
2. **No undocumented completion claims.** Code + tests without durable state/documentation is incomplete.
3. **Evidence beats assertion.** Git/source, tests, CI, and durable repository artifacts are evidence; chat/account memory is supplementary only.
4. **Version changes propagate.** Contract/interface/protocol changes must update dependent tests/workflows/docs in the same bounded change.
5. **Documentation follows authority.** Update the smallest affected `.ai/` or `docs/` record (or an exact durable root document such as `README.md`, `AGENTS.md`, or `CHANGELOG.md`).
6. **Implementation artifacts do not self-document.** Changes under `tools/`, `tests/`, `core/`, `workflows/`, `rules/`, or `.github/` are material; those paths do not by themselves satisfy the durable-record requirement.
7. **No retroactive fiction.** Missing durable documentation means the result stays `UNKNOWN`/`INCOMPLETE`; DevOS must not infer completion from conversation history.

## Completion standard

A bounded work unit may be called complete only when:

`IMPLEMENTED + VERIFIED + DOCUMENTED`

All three are required.

## Deterministic enforcement boundary

`tools/verify-documentation-integrity.py` inspects the latest Git change boundary. If it contains material implementation paths but no durable record path, verification fails.

Durable record paths are deliberately narrow:

- `.ai/`
- `docs/`
- `AGENTS.md`
- `CHANGELOG.md`
- `README.md`

Material implementation authorities include:

- `tools/`
- `tests/`
- `core/`
- `workflows/`
- `rules/`
- `.github/`
- implementation/config files with executable or machine-contract extensions

This guard is deterministic and syntactic. It does **not** prove semantic documentation completeness, authorize execution, grant mutation authority, or convert CI success into production readiness.
