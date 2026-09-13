# P15 language-routing boundary

Human-language interpretation is upstream of project routing, controller authorization, runtime capability, Security Gate, and verification.

A `ROUTE` result means only that DevOS has enough interpretation evidence to continue into those independent gates. It never means `execute`, `authorized`, `safe for production`, or `verified`.

A `CLARIFY` result is required when a missing referent or unresolved intent could materially select the wrong objective/project/action.

Explicit negative constraints emitted by the interpreter must be treated as narrowing constraints by downstream components. No downstream layer may reinterpret `NO_DEPLOY`, `NO_DELETE`, or `NO_MERGE` as permission.
