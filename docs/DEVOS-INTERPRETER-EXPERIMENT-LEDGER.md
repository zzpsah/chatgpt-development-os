# DevOS Interpreter Experiment Ledger

> Repository-local ledger for controlled evolution of P15 Human Language Interpretation.

P15 should improve from real engineering experience, user corrections, adversarial examples, and regression evidence. It must improve under governance, not by silently learning new authority.

## Experiment status

- `PROPOSED` — hypothesis recorded, not adopted.
- `RUNNING` — bounded experiment against a disposable/test corpus.
- `PASSED` — semantic/safety criteria satisfied.
- `REJECTED` — candidate worsens interpretation or weakens a boundary.
- `DEFERRED` — useful but evidence insufficient.
- `ADOPTED` — merged version with durable evidence.

## Experiment record template

```yaml
experiment_id: "P15-EXP-YYYYMMDD-NNN"
created_at: "YYYY-MM-DDTHH:MM:SSZ"
source_head: "<git-sha>"
status: PROPOSED
input_examples:
  - text: "<human command>"
    context: "<relevant project/workflow state>"
baseline:
  intent: "<canonical intent>"
  constraints: []
  ambiguity: "<NONE|CLARIFY|...>"
candidate:
  intent: "<candidate intent>"
  constraints: []
  semantic_delta: "<what interpretation changes>"
risk:
  false_positive_hypothesis: "<...>"
  false_negative_hypothesis: "<...>"
  security_impact: "NONE|REVIEW"
  authorization_impact: "UNCHANGED|REVIEW"
regression:
  tests_added: []
  adversarial_cases: []
  expected_invariants:
    - "INTERPRETATION != AUTHORIZATION"
    - "CONTINUE != BLANKET AUTHORIZATION"
    - "PROVIDER CREDENTIAL != DEVOS AUTHORIZATION"
observed_result:
  outcome: "<...>"
  evidence_refs: []
decision: "ADOPT|REJECT|DEFER"
notes: "<engineering reasoning>"
```

## Adoption gate

A P15 experiment may be adopted only when:

```text
better semantic behavior
+ regression coverage
+ adversarial coverage
+ unchanged authorization boundary
+ current repository verification
+ durable experiment record
```

A model score, user preference, or benchmark improvement alone is not sufficient to widen authority or remove a security gate.

## P15-EXP-20260914-001 — bounded Devanagari Hindi/Hinglish gating

- **Status:** ADOPTED
- **Source boundary:** current P15 deterministic reference interpreter plus P16/P17 regression path.
- **Hypothesis:** preserve Devanagari Unicode and recognize a small, explicit Hindi/Hinglish corpus without allowing translated high-impact requests to bypass P16/P17 gates.
- **Corpus:** `config/p15-multilingual-corpus.json`.
- **Regression:** `tools/test-p15-multilingual-flow.py` and existing P15/P16/P17 regressions.
- **Safety criteria:** contextless referents clarify; `प्रोडक्शन में तैनात करो` remains production/destructive and needs approval; `डिप्लॉय मत करना` blocks a conflicting plan; all outputs retain unchanged authority/authorization and no execution.
- **Limits:** no universal language, dialect, translation-quality, or host-model competence claim.
- **Observed result:** local P15/P16/P17 regressions passed; exact-head main CI passed Development OS `34812860000`, Contracts `34812859861`, Trust-First `34812859744`, Living Engineering Map `34812859740`, GitHub Identity/Token `34812859825`, Provider Controller Adapter `34812859833`, and Remote Permission Governance `34812859951`.
- **Decision:** ADOPT as bounded deterministic corpus coverage.
