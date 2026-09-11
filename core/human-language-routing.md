# Human-Language Routing

The system should infer the user's intent from meaning rather than exact keywords. Informal language, Hinglish, slang, humor, sarcasm, frustration, and profanity are valid input styles; route them by underlying intent.

Routing answers **what kind of work the user is asking for**. The detailed normalization, authorization, evidence, composition, and verification contract is defined by `core/human-language-execution-engine.md`.

## Common intent families

| User intent | Internal response |
|---|---|
| Understand/explain | Explain or research |
| Learn/teach | Teaching Engine: DO / TEACH / EXPLAIN mode |
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
| `simple mein samjha` | Teach at intuitive Level 1 depth |
| `andar se kaise hota hai?` | Teach mechanics/X-ray view |
| `teach me` | Use structured TEACH mode |

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
- Do not infer authorization from frustration, urgency, profanity, praise, or emotional intensity alone.

## Delegation boundary

This routing document identifies the broad semantic intent and should delegate detailed execution behavior to `core/human-language-execution-engine.md`.

The Human Language Execution Engine determines:

`Human phrase → Canonical intent → Workflow → Scope → Authorization → Evidence → Action → Verification → Persistence`

When the intent is learning or teaching, presentation depth and learning behavior are governed by `core/teaching-engine.md`.

Project selection remains the responsibility of `core/project-router.md`; routing must not guess between multiple plausible projects.
