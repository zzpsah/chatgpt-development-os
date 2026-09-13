# P15 interpreter output schema

Reference output fields:

- `protocol`: `DEVOS-HUMAN-LANGUAGE-v2`
- `utterance`, `normalized`
- `intents`, `primary_intent`
- `objective`, `project`
- `context_inherited`
- `constraints`
- `confidence`: `HIGH | MEDIUM | LOW`
- `ambiguity`
- `decision`: `ROUTE | CLARIFY`
- `authorization`: always `UNCHANGED`
- `execution`: always `NONE`

This is a routing envelope, not a runtime execution envelope.
