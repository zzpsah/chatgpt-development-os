# Human Language v2 examples

| Utterance | Explicit context | Expected result |
|---|---|---|
| `fix this error` | none | `BUG_FIX`, route |
| `security dekh` | none | `SECURITY_REVIEW`, route |
| `isko aur acha kro` | none | `QUALITY_IMPROVEMENT`, route |
| `deploy mat karna, fix error` | none | `BUG_FIX` + `NO_DEPLOY`, route |
| `kr do` | prior objective + intent | inherit prior objective/intent, route |
| `wahi continue` | prior objective + intent | inherit prior objective/intent, route |
| `continue` | no prior objective | clarify missing referent |
| `isko kro` | no prior objective | clarify missing referent |

The interpreter intentionally prefers clarification over inventing a materially important referent. Its output is routing evidence only; authorization and execution remain unchanged.
