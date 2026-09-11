# Documentation Integrity Contract v1

## Philosophy

> **What is not written was never done.**

DevOS treats repository documentation as part of implementation, not optional follow-up work. A code, contract, workflow, architecture, decision, milestone, or operational change is not considered complete until its durable project record is updated in the same development unit.

## Rules

1. **Every material change is documented immediately.** Implementation and its durable record must land together.
2. **No undocumented completion claims.** A task is not `COMPLETE` merely because code exists or tests pass; the corresponding durable project record must reflect the change.
3. **Evidence beats assertion.** CI output, tests, Git history, and repository artifacts are evidence. Chat/session memory is not completion evidence.
4. **Version changes propagate.** When a protocol, contract, interface, or behavior version changes, dependent tests, workflows, and documentation must be updated in the same change set.
5. **Documentation follows authority.** Update the affected `.ai`, `core`, workflow, rules, or docs record rather than blindly editing every document.
6. **Atomic documentation boundary.** A material implementation change without a durable documentation change in the same commit is incomplete and must fail the repository contract check.
7. **No retroactive fiction.** Missing documentation means the work remains `UNKNOWN`/`INCOMPLETE`; DevOS must not infer completion from conversation history.

## Minimum durable record

For a material development change, update the affected authoritative record immediately. Normally this means one or more of:

- `.ai/CURRENT-STATE.md` — current milestone/state;
- `.ai/TASKS.md` — active/planned/completed work;
- `.ai/DECISIONS.md` — design/policy decisions;
- `.ai/ARCHITECTURE.md` — system structure/data flow;
- relevant `core/`, `workflows/`, or `rules/` contract;
- tests/verifiers when executable behavior or a contract changes.

Not every change requires every file. The rule is **document the affected authority immediately**.

## Completion standard

A work unit may be called complete only when:

`IMPLEMENTED + VERIFIED + DOCUMENTED`

All three are required. If documentation is missing, the work unit is not complete.

## Enforcement

Repository verification checks the latest commit boundary. Material implementation changes must be accompanied by a durable repository record in that same commit. This is a deterministic guard against documentation drift; it does not claim to prove semantic completeness.
