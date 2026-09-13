# DevOS Foundation Bootstrap Contract v1

## Purpose

Define the deterministic first-boot contract for any AI entering DevOS or a DevOS-managed project.

## Core rule

> Bootstrap establishes whether DevOS may safely proceed. It never grants execution authority.

A bootstrap PASS means the repository context is structurally coherent enough to continue into the normal DevOS workflow. It does **not** mean that a task is authorized, a plan is READY, code is correct, or the project is production-ready.

## Required checks

1. Canonical repository identity is exact.
2. Required bootstrap files exist and are readable.
3. `.ai/manifest.yaml` declares the canonical repository and project identity.
4. `.ai/CURRENT-STATE.md` exists and contains a current-state snapshot.
5. `AGENTS.md` points to the bootstrap protocol.
6. `core/ai-bootstrap-protocol.md` exists.
7. Git/source evidence remains the authority over conversational memory.
8. Bootstrap reports a deterministic PASS or HOLD result.

## Required bootstrap inputs

- `AGENTS.md`
- `.ai/manifest.yaml`
- `.ai/CURRENT-STATE.md`
- `core/ai-bootstrap-protocol.md`

Recommended context remains governed by the existing protocol: `.ai/PROJECT.md`, `.ai/ARCHITECTURE.md`, `.ai/DECISIONS.md`, `.ai/TASKS.md`, `.ai/CHANGELOG.md`, and relevant session records.

## Identity boundary

The canonical DevOS repository is exactly:

`zzpsah/chatgpt-development-os`

A repository named `devos`, a search result, a remembered repository, or a similar project must never substitute for this identity.

## Fail-closed behavior

Bootstrap must return `HOLD` when a required file is missing, the manifest identity conflicts with the canonical identity, or a required structural invariant cannot be established.

Bootstrap must not:

- execute project mutations;
- grant authorization;
- reuse prior approvals;
- infer permission from conversational language;
- repair source files automatically;
- hide contradictory state.

## Evidence levels

Bootstrap output is structural evidence only. It must not claim:

- feature correctness;
- security correctness beyond the checked structural invariant;
- live-provider mutation capability;
- production readiness.

## Fresh-AI sequence

`AGENTS.md → bootstrap contract/protocol → manifest → current state → relevant project state → source/tests/Git → P15/P16/P17 workflow`

## Completion criteria

Foundation bootstrap is complete only when the implementation, deterministic regression test, durable contract, and verification evidence are all present in Git.
