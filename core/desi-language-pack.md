# Desi Language Pack v1

## Purpose

The Desi Language Pack is a language-resource layer for the Human Language Execution Engine. It improves interpretation of Hindi, Hinglish, common Indian-language transliteration, colloquial phrasing, spelling variation, and short conversational commands.

It is a **language resource, not an authority layer**.

`Human wording → Language Pack normalization → Human Language Execution Engine → Canonical intent → Controller`

## Boundary

The language pack may provide:

- Hindi and Hinglish vocabulary and phrase patterns;
- common Roman-script spellings and typo tolerance;
- colloquial confirmations such as `haan`, `haa`, `kar do`, `theek hai`, and `ok`;
- continuation phrases such as `continue kro`, `wahi se continue`, and `jahan chhoda tha wahi se`;
- mixed-language engineering phrases such as `bug fix kar`, `security check bhi kar`, and `production grade bana`;
- language-specific normalization resources for additional supported Indian languages as packs are added.

The language pack must **not**:

- grant authorization;
- select or expand a project scope;
- bypass security or approval gates;
- convert emotional language into permission;
- fabricate evidence or execution results;
- directly invoke execution, mutation, deployment, or publication.

## Normalization examples

| Human wording | Canonical interpretation |
|---|---|
| `continue`, `continiue`, `continue kro` | `RESUME_WORK` |
| `haan`, `haa kar do`, `ok do it` | confirmation of the current plan when an unambiguous current plan exists |
| `wahi se continue` | `RESUME_WORK` using recovered project state |
| `kya pending hai?` | `STATUS_QUERY` |
| `ruk ja` | `STOP_WORK` |
| `isko production grade bana` | `QUALITY_IMPROVEMENT → FEATURE_CHANGE` |
| `bug fix kar aur security check bhi kar` | `BUG_FIX → SECURITY_REVIEW → VALIDATION` |

These examples describe interpretation, not automatic permission to perform high-impact actions.

## Layering

```text
User
  ↓
Desi / Human Language
  ↓
Desi Language Pack(s)
  ↓
Human Language Execution Engine
  ↓
Conversation + Repository Context
  ↓
Canonical DevOS Intent
  ↓
Project Router / Controller
  ↓
Authorization + Security Gates
  ↓
Bounded Execution
  ↓
Verification + Persistence
```

## Future language packs

Additional language packs can be added without changing the execution contract. Each pack should define its supported language/locale, normalization resources, ambiguity rules, and regression examples. All packs share the same invariant:

> **Language can change how a request is understood; it cannot change what DevOS is authorized to do.**

## Verification expectation

Every material language-resource change should include deterministic regression examples covering positive normalization, ambiguity, typo tolerance where supported, and authorization-boundary preservation.
