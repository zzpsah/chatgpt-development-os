# Session — AI State Resolver v2 cross-claim contradiction hardening

Date: 2026-09-14
Repository: `zzpsah/chatgpt-development-os`
Branch: `feat/resolver-cross-claim-contradictions`
Initial base `main`: `aa38761270ac9acdf6af90a4bae64890c766ec91` (post-PR #45)
Concurrent `main`: `040c7d21b5fac6224ced1bdbfeaa7c3b71b78c78` (`docs: separate active state from historical evidence`)
PR: #46

## Trigger

After PR #44 envelope-integrity hardening and PR #45 durable-state reconciliation, the next explicitly promoted bounded resolver objective is deterministic cross-claim contradiction detection. The user also requested durable documentation of previous DevOS stages.

## Fresh observations

- Existing resolver v2 validates individual claim identity, grounding, confidence, freshness, duplicate claim IDs, revalidation boundaries, and downstream envelope integrity.
- It intentionally did not yet define a stable identity for different claims asserting values about the same fact.
- P16 already converts resolver `NEEDS_EVIDENCE` / unresolved claim IDs into `CLARIFY`.
- P17 already recomputes preserved resolver claim confidence consistency and fails closed if unknown claims are hidden in a forged planned envelope.
- Therefore the smallest safe extension is to generate ordinary unresolved claims from deterministic contradiction detection and reuse the existing P16/P17 path.

## Design

Optional claim metadata:

```yaml
fact_key: stable.fact.identity
fact_value: deterministic JSON value
```

Rules:

- legacy claims with neither field retain existing behavior;
- supplying only one field fails closed;
- statement text is never paired by semantic guesswork;
- claims compare only when they explicitly share a valid `fact_key`;
- JSON values are canonicalized with stable object-key ordering;
- different canonical values for the same fact make all involved otherwise-resolved claims `unknown` with `CROSS_CLAIM_CONTRADICTION`;
- the result records `contradiction_fact_keys`;
- no winner is automatically selected.

## Implementation

- `tools/ai-state-resolver.py`
  - adds explicit fact identity validation;
  - canonicalizes deterministic JSON values;
  - detects cross-claim contradictions;
  - exposes `contradiction_fact_keys`;
  - preserves authority/execution/mutation invariants.
- `tools/test-ai-state-resolver.py`
  - covers incomplete fact identity, same-value claims, contradictory booleans, canonical structured equality, unrelated facts, and legacy behavior.
- `tools/test-ai-state-resolver-p16-p17.py`
  - proves contradictions propagate to P16 `CLARIFY`;
  - proves a forged `PLANNED` envelope cannot hide resulting unknown claims from P17.
- `core/ai-state-resolver.md`
  - promotes the bounded contradiction contract into the current v2 normative documentation.
- `docs/AI-STATE-RESOLVER-CROSS-CLAIM-CONTRADICTIONS.md`
  - records detailed behavior and non-goals.

## Previous-stage documentation

Added `docs/DEVOS-ENGINEERING-STAGE-HISTORY.md` as a durable navigation ledger covering:

- numbered architecture history P9–P17;
- major unnumbered proof/hardening milestones through PR #45;
- live GitHub governed-mutation evidence boundary;
- accumulated authority invariants;
- repository-first recovery order.

The ledger explicitly does not create P18/P19 and does not replace Git/source/tests/PR metadata as authority.

## Concurrent-main reconciliation

While PR #46 was being opened, `main` advanced from `aa387612...` to `040c7d21...` via `docs: separate active state from historical evidence`.

The intent to separate active state from historical evidence is retained. Fresh comparison and CI found two regressions in the new compact `.ai/CURRENT-STATE.md`:

1. it removed the explicit `ChatGPT Memory/chat history` supplementary-only wording required by fresh-AI recovery tests;
2. it downgraded already-proven live GitHub App/provider evidence to `pending` / user-reported state despite durable run/provider evidence already established in earlier sessions and commits.

PR #46 repairs these durable-state regressions while preserving the compact active/history separation. It explicitly records:

- ChatGPT Memory/chat history is supplementary only;
- live read-only App run `34785659043` is proven;
- isolated governed provider create/update/delete mutation evidence remains proven;
- `production_ready = false` remains unchanged.

The first PR CI candidate failed at Cross-Host Recovery because of the missing account-memory boundary in the concurrent-main state; the feature code had not reached its later resolver test steps in that run. The repair is performed in the same branch rather than weakening recovery tests.

## Safety / authority boundaries

- `authority = UNCHANGED`
- `authorization = UNCHANGED`
- `execution = NONE`
- `mutation = NONE` for resolver behavior
- P12 retains evidence provenance/freshness ownership.
- P16 retains planning ownership.
- P17 retains readiness/authorization ownership.
- `production_ready = false` is not upgraded.
- No production, credential, permission, database, destructive, or provider mutation is part of the resolver feature.

## Verification / integration plan

1. Reconcile the feature branch with current `main` without discarding unrelated concurrent changes.
2. Require exact-head CI across triggered DevOS gates.
3. Repair any compatibility failure on the same branch without weakening fail-closed semantics.
4. Under the user's time-bounded standing authorization, merge only after the exact final head is green and mergeable.
5. Reconcile `.ai/CURRENT-STATE.md` / `.ai/TASKS.md` after merge so the feature is not left as stale active work.
