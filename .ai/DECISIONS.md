# Decisions

## Readiness evidence v1
- Machine-readable inventory: `config/readiness-evidence.json`; offline verifier: `tools/verify-readiness-evidence.py`.
- VALID means consistent historical evidence classification, not current runtime verification or production readiness.
- All live-mutation and production claims remain false in v1; a reviewed future protocol and separately authorized evidence are required to expand them.
- Archived run/head/test references remain historical. No automatic claim refresh occurs when CI passes on a later head.
- Current-source evolution does not rewrite historical evidence. Changed referenced paths are exposed as `historical_source_drift`; a new current-source claim requires separate new evidence.
- Fabricated CI run IDs, source-head mismatches, stale evidence relabeled as fresh, malformed/duplicate capability records, missing limitations, and unsupported production/live-mutation promotion fail closed.
- PR #16 is reconciled against PR #17 Trust-First `main`; the readiness ledger composes with `tools/devos-audit.py` and adversarial Security Gate checks rather than duplicating them.
- Foundation bootstrap participates in Contracts and Full CI; diagnostics remain read-only.
- Following matrix closure, prioritize Foundation Health & State Consistency with universal AI portability preserved.

## Durable project state authority
- DevOS project-local `.ai` is the portable durable context layer.
- Source tree + Git are authoritative for implementation state and exact changes.
- AI account memory/chat history are supplementary and not project authority.
- `STATE-INDEX.md` is evidence/navigation, not semantic authority.
- Universal acceptance invariant: `AI A + Account A → repository → AI B + Account B → correct recovery → safe continuation`.

## Canonical repository identity
- Canonical repository: `zzpsah/chatgpt-development-os`.
- Name-only similarity never overrides exact repository identity evidence.

## P9–P11 continuity decisions
- P9 Development Task Controller remains the governed controller boundary for bounded execution candidacy.
- P10 Context Continuity & Recovery established repository-local continuity independent of chat memory.
- P11 Federation & Self-Healing Context remains the repository-first recovery/revalidation/cross-AI continuity baseline.

## P15–P17 decisions
- P15 Human Language Interpretation is the top-level semantic entry capability and never grants authority.
- P16 planning remains non-executing/non-authorizing.
- P17 `READY` means eligibility only; authority/authorization/execution remain unchanged.
- P17 revalidates compiled-step semantic impact against the P16 classifier; a downgraded destructive/security-sensitive impact is blocked.

## Production E2E / recovery / continuation closures
- Production E2E Harness closed through PR #11.
- Failure + Recovery Proof closed through PR #12.
- Multi-Session / Fresh-AI Continuation Proof closed through PR #13 at `cd8524b11f923e5e29eeaf445869b6239954ed1f` from final head `99822037a9e24625f2e7c216300c4aabd94e134e`.
- Multi-session final verification: Contracts 518, Full DevOS 443, External Managed Project 31 all succeeded.
- No-blind-mutation-replay remains a durable safety invariant across recovery and session boundaries.

## Controlled Remote Mutation Proof decision
- This gate strengthens the existing `github.mutate.file` path; it does not add a general remote mutation framework.
- The missing maturity evidence was fresh readback of the exact remote file after a mutation attempt.
- `github.inspect.file` is therefore added as a read-only capability for precondition/current-state and post-mutation observation.
- The reference controlled proof is `fresh inspect.file → exact SHA match → exact-step authorization + Security Gate → one mutate.file attempt → fresh inspect.file readback → observed-state verification`.
- A provider update response is mutation-attempt evidence, not verified completion.
- `VERIFIED` requires fresh readback proving the intended content and current SHA.
- Missing authorization, missing Security Gate, stale SHA, invalid path, or failed pre-read BLOCK before mutation.
- Once the mutation adapter is invoked, conflict, failed/mismatched readback, or unproven final state HOLDs with replay forbidden.
- An uncertain provider response may be reconciled by fresh readback if the exact intended state is observed; the mutation itself is still never automatically retried.
- Normal GitHub commits used to develop DevOS are not counted as the DevOS runtime mutation proof.

## Live-provider boundary decision
- PR #14 is provider-simulated / contract-level evidence only.
- No new live DevOS runtime remote mutation has been authorized or executed by this gate.
- A future live-provider `github.mutate.file` proof requires separate explicit authorization for the exact repository, file path, intended content/change, and operation.
- Branch, pull-request, workflow, deployment, production, database, permission, credential/secret, and destructive mutations remain unproven and unavailable/out of scope unless separately bounded and explicitly authorized.

## Verification / no-replay decision
- Controlled remote mutation is attempted at most once per governed attempt.
- Stale optimistic-concurrency evidence must trigger refresh, not unconditional overwrite.
- Provider uncertainty or failed post-mutation verification inherits Failure + Recovery's `MUTATION_REPLAY_FORBIDDEN` rule.
- A later attempt, if separately justified, is a new governed attempt requiring fresh provider state and current exact authorization/Security Gate evidence.

## Production-readiness decision
- Production readiness is an evidence claim, not a phase label.
- Provider-simulated controlled mutation proof may strengthen the evidence matrix but does not by itself prove live-provider or production mutation safety.
- The readiness matrix distinguishes deterministic/component proof, integrated proof, real read-only managed-project proof, provider-simulated proof, live-provider proof, and unproven capabilities.
- Current v1 deliberately cannot express `LIVE_PROVIDER_VERIFIED` or `PRODUCTION_VERIFIED` as successful proof levels.

## Verification boundary
- Earlier successful runs are historical evidence only for a new head.
- Fresh CI on a later PR head proves that later implementation/checker behavior only; it does not silently refresh historical ledger rows.
- Higher-impact execution remains separately authorized and Security-Gate controlled.
