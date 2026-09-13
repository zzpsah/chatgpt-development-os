# Session — P17 Final Hardening

Date: 2026-09-13
Repository: `zzpsah/chatgpt-development-os`
Branch: `devos/p17-step-readiness`
PR: #10
Stacked dependency: P16 PR #9

## User direction

Continue DevOS development through completion and document all actions. Preserve authorization, Security Gate, repository freshness, verification, and merge-order boundaries.

## Starting point

P17 already implemented `DEVOS-STEP-READINESS-v1`, exact-step authorization isolation, repository-head staleness detection, a readiness-aware runtime handoff, and an initial P15→P16→P17 reference test. During this continuation P16 itself was hardened further, so P17 first had to inherit that corrected foundation.

## P16 synchronization into P17

P17 was synchronized with the corrected P16 compiler/controller/architecture behavior so a later P17 merge cannot regress P16.

Key sync commits:
- `b98101fe754cfca16c5547d50c0743e16398f8e7` — inherited P16 compiler read-before-write fix, compiled-plan controller path, controller integration verifier, semantic compiler tests, and canonical P16 architecture placement.
- `122c552552c9eb84c2fea6dcc2edbdbeb4914fe6` — inherited the later P16 compiled-plan invariant/controller integration hardening available at that point.

P16 later advanced to documented final head `ce48196aa116eb2b843259ad562a3c27dad3a59f` with durable state/session documentation. P17 remains stacked on the P16 branch and must be revalidated after P16 merges.

## P17 readiness hardening

### Strict plan validation
Updated `tools/step-readiness-orchestrator.py` to fail closed unless the compiled plan:
- is `DEVOS-GOAL-PLAN-v1` + `PLANNED`;
- preserves unchanged authority/authorization and `execution: NONE`;
- has resolved project/objective and no material ambiguity;
- has valid constraints;
- has unique non-empty step ids/objectives;
- has valid dependencies, impact classes, auth flags, expected evidence, verification, and stop/escalation metadata;
- declares authorization for security/high-impact/production-destructive classes;
- has no unknown/self dependencies or dependency cycle;
- does not contradict explicit negative constraints.

Commit:
- `ec8c4e70941c2566805361b2b8364ca4a42cdd73`

### Readiness evidence hardening
The same evaluator now rejects:
- malformed selected step id;
- missing/non-string repository-head evidence;
- already-completed selected step;
- unknown completion ids;
- completed steps whose own dependencies are incomplete;
- invalid capability/authorization/security evidence-map types;
- missing capability;
- missing exact-step approval when required;
- missing/failed Security Gate evidence for gated classes.

`READY` includes selected-step metadata and explicitly marks it `execution_evidence: false`.

### Regression corpus expansion
Updated `tools/test-step-readiness-orchestrator.py` to cover:
- READY/stale/dependency behavior;
- already-complete step rejection;
- fake/impossible completion evidence;
- invalid evidence-map type;
- exact-step approval isolation;
- Security Gate evidence;
- missing verification/evidence/stop metadata;
- changed authority/execution claim;
- PLANNED+ambiguity;
- duplicate ids, unknown dependencies, dependency cycle, empty objective;
- high-impact authorization inconsistency;
- negative-constraint tampering.

Commit:
- `2d17a6dd6a9a14c2516bf7a7e16afed9303b9658`

A first attempt to write this test file hit a GitHub repository-rule validator timeout (`409`). The blob was refreshed and the write retried normally; no forced overwrite was used.

## Runtime handoff hardening

Updated `tools/devos-runtime-handoff.py::build_p17_handoff` so P17 runtime eligibility requires:
- controller protocol `P16-CONTROLLER-v1`;
- controller decision `EXECUTION_CANDIDATE`;
- readiness `DEVOS-STEP-READINESS-v1` over `DEVOS-GOAL-PLAN-v1`;
- all readiness gates true;
- all required controller gates true;
- exact equality of controller task id, controller compiled-step id, readiness step id, and readiness step id metadata;
- matching objective/impact/verification metadata;
- matching repository head;
- unchanged authority/authorization and no execution claim.

A legacy P12 controller candidate is intentionally insufficient for P17 handoff; legacy P12 handoff remains independently supported.

Commit:
- `8706e412fdb30404af7b0bb1fccf4fdb8fc14b12`

## Direct end-to-end proof

Updated `tools/test-p17-end-to-end.py` so the controller consumes the P16 compiled plan directly rather than reconstructing a manual task list.

Current proof:
`P15 human request → P16 compiled plan → P17 readiness → P16 compiled-plan controller → P17-aware runtime handoff`

Negative cases include:
- forged readiness step id;
- forged READY gate state;
- legacy P12 controller at the P17 boundary;
- stale repository readiness.

Commit:
- `22aa027f0e67f8397fa4c972556ad52486c7f7e0`

## Normative contract alignment

Updated `core/step-readiness-authorization-orchestrator.md` to make strict plan integrity, dependency-cycle/closure rules, exact handoff identity, all-gates-true semantics, and non-execution-evidence boundaries normative.

Commit:
- `50575462dc81e56dfa3ab54f552dc303bcf08a26`

## GitHub Actions blocker

The repository-wide verification infrastructure is still stalled based on observed evidence:
- many runs queued;
- zero in-progress runs at observation time;
- observed queued P16 job had `runner_id: 0`, no runner assignment, and no executed steps;
- available connector does not expose queued-run cancellation;
- sandbox cannot resolve `github.com` for direct clone/local branch testing.

This is not treated as pass or failure. No local test pass is claimed.

## Merge safety

P17 remains open and stacked. It must not merge before P16 receives fresh passing final-head verification and merges to `main`. After P16 merge, P17 must be retargeted/revalidated against resulting `main` and must itself receive fresh passing final-head verification.

## Completion status

P17 source/contract/test hardening is complete for the identified P15→P16→P17→Controller→Runtime gaps. Milestone closure remains externally verification-gated.
