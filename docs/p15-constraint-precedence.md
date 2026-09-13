# P15 constraint precedence

Explicit user prohibitions outrank inferred continuation. If context says the prior task included deployment but the current utterance says `deploy mat karna`, the language envelope must preserve `NO_DEPLOY`; downstream work must be narrowed accordingly rather than inheriting deployment authority.
