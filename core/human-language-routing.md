# Human-Language Routing

The system should infer the user's intent from meaning rather than exact keywords.

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

## Conversation behavior

- Natural-language requests are authoritative over command naming.
- Ask a clarification only when a wrong assumption could materially change the outcome.
- If the user clearly asks for execution, proceed within safe boundaries.
- When a request combines intents, perform them in a sensible sequence.
- Keep the user informed about important decisions without exposing unnecessary internal machinery.
