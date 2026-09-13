# P15 Human Language Execution Engine v2 — 2026-09-13

## Objective
Improve DevOS so very short, typo-prone, Hinglish and context-dependent user language can resolve to a safe engineering intent without unnecessary clarification.

## Boundary
Interpretation remains non-executing. It does not grant authorization, does not infer destructive/production permission, and must clarify when a missing referent could materially change the action.

## Implemented slice
- deterministic `tools/human-language-interpreter.py`
- short-command and contextual objective inheritance
- referential phrase detection (`ye/wo/wahi/isko/same/pehle wala` class)
- Hinglish/shorthand intent patterns
- preserved negative constraints such as no-deploy/no-delete/no-merge
- explicit confidence and ambiguity output
- `ROUTE` versus `CLARIFY` decision
- unchanged authorization and `execution: NONE`
- executable regression corpus in `tools/test-human-language-interpreter.py`
- CI integration in the contract workflow
- v2 architecture contract in `core/human-language-execution-engine.md`

## Verification
Pending GitHub Actions evidence on the feature PR. Do not mark P15 complete until the new interpreter tests and existing DevOS contract suite pass with fresh evidence.
