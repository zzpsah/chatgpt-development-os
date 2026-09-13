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

A language-model score, user preference, or benchmark improvement alone is not sufficient to widen authority or remove a security gate.
