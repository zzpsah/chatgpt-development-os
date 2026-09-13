# Decisions

## Durable project state authority
- DevOS project-local `.ai` is the portable durable context layer.
- Source tree + Git are authoritative for implementation state and exact changes.
- AI account memory/chat history are supplementary and not project authority.
- `STATE-INDEX.md` is evidence/navigation, not semantic authority.

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
- The eventual readiness matrix must distinguish deterministic/component proof, provider-simulated proof, real read-only managed-project proof, live-provider mutation proof, and unproven capabilities.

## Verification boundary
- Earlier successful runs are historical evidence only for a new head.
- PR #14 closes only after fresh applicable Contracts, Full DevOS and External Managed Project success on the exact final semantic-state head.
- Higher-impact execution remains separately authorized and Security-Gate controlled.
