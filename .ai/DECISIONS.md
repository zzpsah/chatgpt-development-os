# Decisions

## Current-Source Evidence Refresh — closure
- This was a bounded, unnumbered objective; no P18/P19 phase was created.
- The protocol adds fresh exact-current-source proof without rewriting historical readiness evidence.
- Current evidence is ephemeral and additive; historical `source_head`, run IDs, archive digests, and `freshness: historical` remain pinned.
- A valid packet binds exact Git HEAD, ledger-declared capability/level/test path, current test SHA-256, observed exit code, and local/CI context.
- Foundation Health may validate optional current-source evidence but never executes its test or manufactures freshness; Doctor remains presentation-only.
- Historical source drift remains visible as WARN even when a valid packet proves the current version of the exact drifted test.
- `CURRENT_EVIDENCE_ADDS_PROOF_BUT_NEVER_REWRITES_HISTORICAL_PROVENANCE` is the governing rule.
- Final source head `bc400112d0bbaced6ed699a6863bc8dcf91e47c8` merged through PR #24 at `a93f9f435ffab5f81ce070f07a0da694757ab6cb`.
- Final exact-head PR verification: Current-Source Evidence 12 / `34773566913`, Trust-First 71 / `34773566958`, Contracts 608 / `34773566914`, Full DevOS 530 / `34773566926`, MCP Repository Create 9 / `34773566919` — success.
- Fresh post-merge `main`: Trust-First 72 / `34774013758`, Contracts 609 / `34774013791`, Full DevOS 531 / `34774013827` — success.
- The dedicated Current-Source Evidence workflow has no `main` push trigger, so no post-merge dedicated run is claimed.
- `production_ready=false` and `live_provider_proven=false` remain unchanged; this closure grants no authority, authorization, execution, or mutation permission.

## Cross-Host Recovery Friction & Onboarding Proof
- This is a bounded, unnumbered objective; no P18/P19 phase is created.
- The gap is not another portability contract. Existing Multi-AI portability, host-profile, auto-onboarding, fresh-AI recovery, continuation, and P11 repository-first contracts already exist.
- The missing evidence is measurable repository-only recovery/adoption friction: what a fresh host can recover, what is missing/ambiguous, and which host capabilities are unavailable or delegatable.
- The recovery/friction layer must be READ_ONLY and machine-readable.
- It may inspect repository files, Git state, existing host profiles, bootstrap contracts, and existing recovery evidence; it must not create authority, authorize execution, mutate project state, rewrite evidence, or infer live-provider proof.
- Missing/ambiguous recovery inputs are `UNKNOWN` or `BLOCKED`, never PASS.
- Deterministic host-profile simulation is not real cross-vendor/account proof. `SIMULATED EVIDENCE != LIVE PROVIDER PROOF` remains explicit.
- Authorization, Security Gate, verification, and no-replay rules are invariant across AI vendors/models/accounts.
- Recovery/adoption friction should be represented with stable fields/counts so future hosts/revisions can be compared without rewriting historical evidence.

## Foundation Health & State Consistency — closure
- Foundation Health is a bounded objective, not a P18/P19 phase.
- Authoritative flow: `Source / Git / Tests / CI → tools/devos-audit.py → readiness evidence ledger → tools/devos-health.py → tools/devos-doctor.py`.
- `tools/devos-health.py` composes authoritative audit/evidence inputs; it does not become a competing truth source.
- `tools/devos-doctor.py` is presentation-only and READ_ONLY.
- Health/doctor preserve `authority: UNCHANGED`, `authorization: UNCHANGED`, `execution: NONE`, and `mutation: NONE`.
- Status vocabulary is `PASS`, `WARN`, `UNKNOWN`, `FAIL`, `BLOCKED`; WARN/UNKNOWN are never promoted to PASS.
- Historical-source drift is a truthful WARN; it never rewrites the source/run head of historical evidence.
- Canonical identity or exact expected-head mismatch is BLOCKED.
- Unsupported capability/evidence promotion fails through the existing readiness-evidence verifier.
- Status prose may be diagnosed for contradictions but never overrules source/Git/test/ledger evidence.
- No live/destructive/provider mutation is required or authorized by the health objective.
- Final source head `77a8f6f8d8ce012d872b20343bded2e00c53ed7d` merged as PR #18 at `657ae461c0d6df62ca428d8bdd0404bd241b5c84`.
- Final PR verification: Trust-First 29 / `34763332363`, Contracts 566 / `34763332344`, Full DevOS 491 / `34763332347` — success.
- Fresh post-merge main verification: Trust-First 33 / `34764171968`, Contracts 570 / `34764171939`, Full DevOS 495 / `34764171923` — success.
- `tools/test-step-readiness-orchestrator.py` remains intentionally visible historical-source drift; closure does not refresh or promote that historical proof.

## PR #16 readiness-evidence closure
- PR #16 final source head `6c509d6f65b22666f121dfe86604faae72c08f8c` merged at `b8e31ae76201b32e4617ef6044b29ef285004f54` only after exact-head Trust-First 22, Contracts 559, Full DevOS 484, and External Managed Project 52 succeeded.
- Post-merge `main` at `b8e31ae76201b32e4617ef6044b29ef285004f54` independently passed Trust-First 23, Contracts 560, and Full DevOS 485.
- External Managed Project has no `push` trigger and therefore no fabricated post-merge run is recorded.
- PR #16 closure does not promote `production_ready`, live mutation proof, or historical evidence freshness.

## Readiness evidence v1
- Machine-readable inventory: `config/readiness-evidence.json`; offline verifier: `tools/verify-readiness-evidence.py`.
- VALID means consistent historical evidence classification, not current runtime verification or production readiness.
- All live-mutation and production claims remain false in v1; a reviewed future protocol and separately authorized evidence are required to expand them.
- Archived run/head/test references remain historical. No automatic claim refresh occurs when CI passes on a later head.
- Current-source evolution does not rewrite historical evidence. Changed referenced paths are exposed as `historical_source_drift`; a new current-source claim requires separate new evidence.
- Fabricated CI run IDs, source-head mismatches, stale evidence relabeled as fresh, malformed/duplicate capability records, missing limitations, and unsupported production/live-mutation promotion fail closed.
- The readiness ledger composes with `tools/devos-audit.py` and adversarial Security Gate checks rather than duplicating them.

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
- The existing proof covers `github.mutate.file` with fresh pre-read, expected SHA binding, exact-step authorization + Security Gate, one mutation attempt, fresh readback, and observed-state verification.
- Provider mutation response is attempt evidence, not completion proof.
- Stale SHA, missing authorization/Security Gate, failed readback, or unproven state block/hold according to the governing contracts.
- Once mutation is attempted, automatic replay remains forbidden.
- This evidence is provider-simulated / contract-level only, not live-provider production proof.

## Live-provider boundary decision
- No new live DevOS runtime remote mutation is authorized by current portability/health work.
- A future live-provider file-mutation proof requires separate explicit authorization for exact repository, path, intended change, and operation.
- Branch, PR, workflow, deployment, production, database, permission, credential/secret, and destructive mutations remain unproven/out of scope unless separately bounded and explicitly authorized.

## Verification boundary
- Earlier successful runs are historical evidence only for a new head.
- Fresh CI on a later head proves that head's implementation/checker behavior only; it does not silently refresh historical ledger rows.
- Higher-impact execution remains separately authorized and Security-Gate controlled.
