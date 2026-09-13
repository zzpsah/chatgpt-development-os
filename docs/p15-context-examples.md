# P15 context examples

```json
{
  "utterance": "kr do",
  "context": {
    "project": "umv-portal",
    "last_intent": "BUG_FIX",
    "last_objective": "Fix registration form validation"
  }
}
```

Expected interpretation: inherit the prior bug-fix objective and route it onward with unchanged authorization and no execution.

Without `last_objective`, a materially referential phrase should clarify rather than invent a target.
