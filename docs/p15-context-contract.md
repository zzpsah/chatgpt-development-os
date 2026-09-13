# P15 explicit context contract

The v2 reference interpreter accepts only context explicitly supplied to it. Initial fields are:

- `project`
- `last_intent`
- `last_objective`

This prevents the deterministic layer from pretending it can read arbitrary chat history, account memory, or unseen repositories. A host may construct this context from authoritative DevOS recovery/project state before invoking the interpreter.

Inheritance is allowed only when a short/referential request and the supplied context form an unambiguous continuation. Otherwise the interpreter must return `CLARIFY`.
