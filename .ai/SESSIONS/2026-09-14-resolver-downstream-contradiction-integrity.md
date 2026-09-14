# Session — resolver downstream contradiction integrity

Date: 2026-09-14
Repository: `zzpsah/chatgpt-development-os`
Base `main`: `7009e8e1b4398462b1a9321bb1e2a38a3c35e478`
Branch: `fix/resolver-downstream-contradiction-integrity`

## Trigger

After PR #46 and its durable closure PR #48, closed superseded PR #47 was reviewed for non-duplicate useful work. That review confirmed one narrower gap: P16/P17 did not independently recompute explicit structured contradictions from preserved `fact_key` / `fact_value` claim values.

## Gap

PR #46 correctly detects contradictions at resolver time. But if resolver provenance were altered after resolution — for example changing a fact value while retaining `RESOLVED` status/confidence metadata — downstream layers needed an independent way to detect the newly-created contradiction.

## Changes

- Resolver keeps PR #46 robust JSON validation and now emits detailed `contradictions` provenance in addition to `contradiction_fact_keys`.
- Valid explicit fact identity is preserved; legacy or malformed identity is not propagated as a valid comparison pair.
- P16 independently canonicalizes preserved fact values and recomputes contradiction groups before trusting resolver metadata.
- P17 independently repeats that recomputation at readiness time, protecting against post-P16 fact-value tampering.
- Existing resolver→P16→P17 adversarial tests now cover hidden contradiction metadata and post-plan value tampering.
- Dedicated contract: `docs/AI-STATE-RESOLVER-DOWNSTREAM-CONTRADICTION-INTEGRITY.md`.

## Provenance handling

The downstream recomputation concept came from review of closed PR #47. The duplicate PR is not merged. Only the narrow defense-in-depth code path is ported from fresh `main`; stale/duplicate `.ai` state and broad feature implementation from #47 are excluded.

## Boundaries

- authority/authorization unchanged;
- no execution or provider mutation from resolver/P16/P17 hardening;
- no production/destructive/credential/permission/database action;
- `production_ready = false` remains unchanged;
- no P18/P19 bookkeeping phase.

## Verification plan

Open a bounded PR from the fresh-main branch, require exact-final-head CI, repair failures without weakening fail-closed behavior, merge under the user's current time-bounded standing authorization only when green and mergeable, then reconcile durable state after merge.
