# Current State

## Snapshot

- Repository: `zzpsah/chatgpt-development-os`.
- Source tree + Git are authoritative; this file is recovery context only.
- `main` is merged/verified through P15 and includes `.ai/P16-P17-AUDIT.md` at commit `f338270429d31df5691f6a02234a1a35553f57af`.
- P16 Semantic Goal-to-Plan Compiler v1 is source-complete on PR #9 / branch `devos/p16-goal-to-plan`; latest documented final head: `ce48196aa116eb2b843259ad562a3c27dad3a59f`.
- P16 is not closed/merged because fresh final-head GitHub Actions verification has not completed.
- P17 Step Readiness & Authorization Orchestrator v1 is source-complete in the stacked branch `devos/p17-step-readiness` after strict readiness/handoff hardening; it must not merge before P16 closes.

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

P17 emits `DEVOS-STEP-READINESS-v1` with:

- `READY`
- `NEEDS_EVIDENCE`
- `NEEDS_APPROVAL`
- `BLOCKED`
- `STOP`

Every outcome preserves `authority: UNCHANGED`, `authorization: UNCHANGED`, `execution: NONE`.

`tools/step-readiness-orchestrator.py` now fails closed unless:

- plan is `DEVOS-GOAL-PLAN-v1`, `PLANNED`, unchanged authority/authorization, execution NONE;
- project/objective are resolved and ambiguity is empty;
- constraints are valid and not contradicted by a non-read-only step;
- step ids/objectives/dependencies/impact/auth/evidence/verification/stop metadata are structurally valid;
- high-impact/security/production-destructive steps explicitly require authorization;
- dependency references are known, not self-referential, and acyclic;
- selected step exists and is not already complete;
- compilation/current repository heads are non-empty and equal;
- completion evidence references real steps and obeys dependency closure;
- selected-step dependencies are complete;
- capability/auth/security evidence maps are valid;
- exact-step authorization exists when required;
- Security Gate evidence is explicit for security/high-impact/destructive classes;
- verification path exists.

`READY` selected-step metadata is explicitly marked `execution_evidence: false`.

## Exact runtime handoff

`tools/devos-runtime-handoff.py::build_p17_handoff` now requires:

- controller protocol `P16-CONTROLLER-v1`;
- controller `EXECUTION_CANDIDATE`;
- readiness protocol `DEVOS-STEP-READINESS-v1` over `DEVOS-GOAL-PLAN-v1`;
- all readiness gates true;
- all P16 controller gates true;
- exact identity equality across controller task id, controller compiled-step id, readiness step id, and readiness step metadata;
- matching repository head;
- matching objective, impact, and verification metadata;
- unchanged authority/authorization and no prior execution claim.

A legacy P12 controller candidate alone is intentionally insufficient for P17 handoff. Legacy P12 handoff remains available separately for backward compatibility.

## End-to-end proof

`tools/test-p17-end-to-end.py` now exercises the direct path without manually rebuilding tasks:

`P15 human request → P16 compiled plan → P17 readiness → P16 compiled-plan controller → P17-aware runtime handoff`

It also rejects:

- forged readiness step id;
- forged READY gate state;
- legacy P12 controller candidate at the P17 boundary;
- stale repository readiness.

`tools/test-step-readiness-orchestrator.py` covers strict plan/evidence integrity, exact-step approval isolation, dependency cycles, fake/impossible completion evidence, stale plan, missing capability/security/verification evidence, authority/execution tampering, negative-constraint tampering, and malformed metadata.

## Verification infrastructure blocker

GitHub Actions remains the only known closure blocker after source hardening.

Observed repository-level evidence:

- about 40 workflow runs queued;
- zero in-progress runs;
- an observed P16 `ubuntu-latest` job had `runner_id: 0`, no assigned runner, no executed steps;
- older P16/P17 workflows are queued rather than failed;
- connector tooling available in this session cannot cancel queued workflows;
- sandbox shell cannot resolve `github.com`, so direct clone/local branch testing was not available.

No queued workflow is treated as pass/fail. No local test pass is claimed.

## Merge order

1. Require fresh passing verification for final P16 head.
2. Merge PR #9 with verified expected head and persist P16 closure on `main`.
3. Retarget/revalidate P17 against resulting `main`.
4. Require fresh passing verification for the final P17 head.
5. Merge PR #10 only after that evidence is green.
6. Then run a real managed-project end-to-end maturity proof and use observed failures to drive subsequent hardening.

## Detailed provenance

Earlier P16/P17 work is recorded in:
- `.ai/SESSIONS/2026-09-13-p16-p17-gap-closure.md`
- `.ai/SESSIONS/2026-09-13-p16-p17-gap-closure-appendix.md`

Final P17 hardening is recorded in `.ai/SESSIONS/2026-09-13-p17-final-hardening.md`.
