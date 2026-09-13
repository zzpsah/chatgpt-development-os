# Current State

## Snapshot

- Repository: `zzpsah/chatgpt-development-os`.
- Source tree + Git are authoritative for implementation state; this file is recovery context only.
- **ChatGPT Memory and chat history are supplementary only and must never be required to recover authoritative project state.** Fresh-AI recovery must work from repository-local source/Git/`.ai` evidence.
- **P11 Federation & Self-Healing Context remains part of the durable recovery baseline.** Repository-first recovery, repository revalidation, and cross-AI continuity remain active invariants for all later milestones.
- `main` is merged/verified through P15 and includes `.ai/P16-P17-AUDIT.md` at commit `f338270429d31df5691f6a02234a1a35553f57af`.
- P16 Semantic Goal-to-Plan Compiler v1 is source-complete on PR #9 / branch `devos/p16-goal-to-plan`. Fresh CI repairs have been limited to restoring durable repository-only recovery markers in `CURRENT-STATE.md`; runtime/compiler/controller logic did not need repair.
- P16 is not closed/merged until its latest repaired head receives fresh passing applicable verification.
- P17 Step Readiness & Authorization Orchestrator v1 is source-complete on stacked branch `devos/p17-step-readiness`; it must not merge before P16 closes and must be revalidated against resulting `main`.

## Canonical pipeline under development

`Human input → P15 Human Language Interpretation → Project Router / State Resolver → P16 Semantic Goal-to-Plan Compiler → P17 Step Readiness & Authorization Orchestrator → P16 compiled-plan Development Task Controller → bounded runtime handoff → Verification + Security → durable state`

Interpretation, planning, readiness, intelligence, and orchestration never manufacture permission. Runtime execution remains independently gated.

## P16 foundation inherited by P17

P17 carries the corrected P16 foundation:

- generated read-before-write inspection is genuinely read-only;
- generalized negative-constraint preservation;
- direct `DEVOS-GOAL-PLAN-v1` consumption by `tools/development-task-controller.py`;
- strict plan/project/step/dependency/evidence/verification/stop-condition validation;
- completed-step identity + dependency-closure validation;
- plan/step metadata preserved as `execution_evidence: false`;
- independent repository/capability/authorization/Security Gate/verification gates;
- high-impact/security/production-destructive controller candidacy requires `ALREADY_GRANTED` authorization + `PASS` Security Gate;
- canonical `.ai/ARCHITECTURE.md` placement of P16.

## P17 implemented behavior

P17 emits `DEVOS-STEP-READINESS-v1` with `READY`, `NEEDS_EVIDENCE`, `NEEDS_APPROVAL`, `BLOCKED`, or `STOP`. Every outcome preserves `authority: UNCHANGED`, `authorization: UNCHANGED`, `execution: NONE`.

`tools/step-readiness-orchestrator.py` fails closed unless:

- the plan is `DEVOS-GOAL-PLAN-v1`, `PLANNED`, with unchanged authority/authorization and `execution: NONE`;
- project/objective are resolved and ambiguity is empty;
- constraints are valid and not contradicted by a non-read-only step;
- step ids/objectives/dependencies/impact/auth/evidence/verification/stop metadata are structurally valid;
- high-impact/security/production-destructive steps explicitly require authorization;
- dependency references are known, not self-referential, and acyclic;
- the selected step exists and is not already complete;
- compilation/current repository heads are non-empty and equal;
- completion evidence references real steps and obeys dependency closure;
- selected-step dependencies are complete;
- capability/auth/security evidence maps are valid;
- exact-step authorization exists when required;
- Security Gate evidence is explicit for gated classes;
- verification path exists.

`READY` selected-step metadata is explicitly marked `execution_evidence: false`.

## Exact runtime handoff

`tools/devos-runtime-handoff.py::build_p17_handoff` requires:

- controller protocol `P16-CONTROLLER-v1` and decision `EXECUTION_CANDIDATE`;
- readiness protocol `DEVOS-STEP-READINESS-v1` over `DEVOS-GOAL-PLAN-v1`;
- all readiness and controller gates true;
- exact identity equality across controller task id, controller compiled-step id, readiness step id, and readiness step metadata;
- matching repository head, objective, impact, and verification metadata;
- unchanged authority/authorization and no prior execution claim.

A legacy P12 controller candidate alone is intentionally insufficient for P17 handoff. Legacy P12 handoff remains available separately for backward compatibility.

## End-to-end proof

`tools/test-p17-end-to-end.py` exercises the direct path without manually rebuilding tasks:

`P15 human request → P16 compiled plan → P17 readiness → P16 compiled-plan controller → P17-aware runtime handoff`

It rejects forged readiness step identity, forged READY gates, a legacy P12 controller at the P17 boundary, and stale repository readiness.

`tools/test-step-readiness-orchestrator.py` covers strict plan/evidence integrity, exact-step approval isolation, dependency cycles, fake/impossible completion evidence, stale plan, missing capability/security/verification evidence, authority/execution tampering, negative-constraint tampering, and malformed metadata.

## Verification history

P16 fresh CI at head `ce48196aa116eb2b843259ad562a3c27dad3a59f` produced Contracts + external managed-project success and a Full DevOS failure only because the compact recovery summary had dropped the explicit ChatGPT Memory/chat-history boundary. P16 commit `9445546dee68f3220acf22bca0a4f9c8db6a048e` restored that boundary. The next Full DevOS run advanced to the next recovery invariant: explicit `P11` continuity in `CURRENT-STATE.md`. P16 commit `877833ef0f11d5a869284f9b86407c155125d96f` restores that marker.

P17 proactively preserves both recovery invariants. Final verification is still required after P16 closure and P17 retarget/revalidation.

No local test pass is claimed; the sandbox shell could not resolve `github.com` for direct clone-based testing. GitHub Actions evidence remains authoritative for closure.

## Merge order

1. Require fresh passing verification for the latest repaired P16 head.
2. Merge PR #9 with verified expected head and persist P16 closure on `main`.
3. Retarget/revalidate P17 against resulting `main`.
4. Require fresh passing verification for final P17 head.
5. Merge PR #10 only after that evidence is green.
6. Then run a real managed-project end-to-end maturity proof and use observed failures to drive subsequent hardening.

## Detailed provenance

Earlier and final hardening actions are recorded in `.ai/SESSIONS/`; exact source changes remain authoritative in Git history.
