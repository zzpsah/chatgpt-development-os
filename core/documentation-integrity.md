# Documentation Integrity Contract v1

## Philosophy

> **What is not written was never done.**

DevOS treats repository documentation as part of the implementation, not as optional follow-up work. A code, contract, workflow, architecture, decision, milestone, or operational change is not considered complete until its durable project record is updated in the same development unit.

## Rules

1. **Every material change is documented immediately.** The implementation and its durable record must land together.
2. **No undocumented completion claims.** A task is not `COMPLETE` merely because code exists or tests pass; the corresponding `.ai` and/or authoritative contract record must reflect the change.
3. **Evidence beats assertion.** CI output, tests, Git history, and repository artifacts are evidence. Chat/session memory is not completion evidence.
4. **Version changes propagate.** When a protocol, contract, interface, or behavior version changes, dependent tests, workflows, and documentation must be updated in the same change set.
5. **Documentation is scoped to authority.** Semantic `.ai` files are updated deliberately; generated/derived files may only be repaired within their existing bounded rules.
6. **Atomic documentation boundary.** A change set that introduces a material implementation change without an accompanying durable documentation change must fail the repository contract check.
7. **No retroactive fiction.** Missing documentation means the work remains `UNKNOWN`/`INCOMPLETE`; DevOS must not infer that it was done from conversation history.

## Minimum durable record

For a material development change, the repository should update the applicable authoritative record(s), normally including:

- `.ai/CURRENT-STATE.md` for current milestone/state;
- `.ai/TASKS.md` for active/planned/completed work;
- `.ai/DECISIONS.md` when a design or policy decision changes;
- `.ai/ARCHITECTURE.md` when system structure or data flow changes;
- the relevant `core/` contract when behavior/rules change;
- tests/verifiers when executable behavior or a contract changes.

Not every change requires every file. The rule is **document the affected authority immediately**, not blindly edit all files.

## Completion standard

A work unit may be called complete only when:

`IMPLEMENTED + VERIFIED + DOCUMENTED`

All three are required. If documentation is missing, the work unit is not complete.

## Enforcement direction

DevOS verification should detect documentation drift at the repository boundary and fail CI for known material changes that have no corresponding durable record. The verifier must prefer deterministic repository evidence and should never claim to prove semantic completeness from filenames alone.
