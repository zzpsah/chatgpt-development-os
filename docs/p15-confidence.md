# P15 confidence semantics

`HIGH`: interpretation is sufficiently grounded for routing from the available utterance/context.

`MEDIUM`: interpretation is usable but carries visible ambiguity such as compatible multiple intents.

`LOW`: meaning is insufficiently grounded; return `CLARIFY`.

Confidence never represents authorization or technical correctness.
