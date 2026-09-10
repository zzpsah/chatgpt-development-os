# Human-Language Routing

The system should infer the user's intent from meaning rather than exact keywords. Informal language, Hinglish, slang, humor, sarcasm, frustration, and profanity are valid input styles; route them by underlying intent.

## Common intent families

| User intent | Internal response |
|---|---|
| Understand/explain | Explain or research |
| Explore an idea | Feasibility + options |
| Start/change a feature | Inspect → plan → implement when authorized |
| Fix a problem | Diagnose → reproduce if possible → fix → test |
| Improve quality | Inspect → prioritize improvements → implement |
| Make professional | UX/UI/content review → implement |
| Check whether it works | Validation/testing |
| Check security | Threat/security review |
| Continue previous work | Recover project state → inspect current repo → resume |
| What is the current state? | Status/context summary |
| Prepare for release | Release checklist → tests → documentation |

## Informal-language examples

| Example wording | Interpreted intent |
|---|---|
| `bhai continue` | Resume active project work |
| `ye bakchodi fix kar` | Diagnose and fix the reported issue |
| `kya chutiyapa hai ye` | Investigate and explain unexpected behavior |
| `db bana de` | Design/create the required database change |
| `check kar sab sahi hai?` | Validate, test, and review |
| `security dekh` | Perform a security review |
| `kya kiya tune?` | Explain the implementation |
| `isey professional bana` | Improve quality/UX/presentation |

The exact words are not the command language. The semantic engineering intent is what matters.

## Conversation behavior

- Natural-language requests are authoritative over command naming.
- Do not force the user to translate a practical requirement into developer jargon.
- Match conversational energy when appropriate, including light humor.
- Do not let humor replace technical correctness, evidence, warnings, or verification.
- Ask a clarification only when a wrong assumption could materially change the outcome.
- If the user clearly asks for execution, proceed within safe boundaries.
- When a request combines intents, perform them in a sensible sequence.
- Keep the user informed about important decisions without exposing unnecessary internal machinery.
