# Current State

## Snapshot

- Repository: `zzpsah/chatgpt-development-os`.
- Source tree + Git are authoritative; ChatGPT Memory/chat history are supplementary only.
- P11 repository-first recovery/revalidation remains a durable invariant.
- P9 through P17 are complete on `main`.
- Production E2E Harness, Failure + Recovery Proof, Multi-Session / Fresh-AI Continuation Proof, and **Controlled Remote Mutation Proof are verified and closed**.
- Foundation Bootstrap Hardening is implemented at v1 contract/checker level.
- Active maturity gate: **Production-Readiness Evidence Matrix & Limitations**.
- **Product vision invariant:** DevOS is an OS for AI-assisted software development across AI vendors, models, accounts, coding agents, machines, and Git providers; no single AI account, model, chat, or vendor-specific memory may be authoritative project state.

## Canonical governed path

`Human request → P15 interpretation → P16 plan → P17 readiness → controller → bounded runtime → verification → persistence → recovery / continuation`

Interpretation, planning, readiness, provider credentials, prior approvals, prior successful runs, recovery checkpoints, continuation packets, and simulated provider evidence never manufacture permission.

## Universal Project Onboarding + Repository Creation

Universal Project Onboarding is implemented on the feature branch `feat/universal-project-onboarding` and is intended to be the next foundation capability once its exact-head CI is green and the change is accepted.

Normative contract:
- `core/devos-universal-project-onboarding.md`
- `core/devos-universal-onboarding-policy.md`
- `core/devos-repository-creation-capability.md`

Implementation:
- `tools/devos-onboard.py` — cross-platform idempotent onboarding, plan by default, `--apply` creates only missing DevOS infrastructure.
- `tools/test-devos-onboard.py` — preservation, idempotency, new-project, Git caller, and incompatible-framework HOLD regression corpus.
- `tools/devos-create-repository.py` — provider-neutral repository creation adapter with GitHub REST support; plan by default; explicit `--apply` plus explicit authorization and local safety enablement required for a live attempt.
- `tools/test-devos-create-repository.py` — deterministic capability, authorization, timeout, and no-secret-leak regression corpus.

Repository creation is a separate high-impact remote mutation capability: `repository.create` / provider example `github.repository.create`.

Safety invariants:
- provider capability != DevOS authorization;
- repository creation authorization != authorization for application code or production work;
- provider response != verified completion;
- uncertain creation response -> HOLD / reconcile, never blind replay;
- no provider credential is printed or persisted by the reference tool;
- current ChatGPT GitHub connector does not expose a `create repository` action, so a live creation cannot be claimed through that connector until an appropriate provider integration exposes the capability.

The intended governed new-project flow is:

`P15 interpretation → P16 plan → P17 exact repository.create readiness → explicit authorization + provider capability → one repository-create request → fresh provider verification → universal onboarding → context validation`

A provider without repository-creation capability must return/lead to `NEEDS_EXTERNAL_REPO_CREATION`, not a false success.

## Foundation Bootstrap Hardening

Normative contract: `core/devos-bootstrap-contract.md`.
Bootstrap checker: `tools/devos-bootstrap.py`.
Regression coverage: `tools/test-devos-bootstrap.py`.

The bootstrap checker is deterministic and read-only. It validates the canonical repository identity and minimum required bootstrap context, including `AGENTS.md`, `.ai/manifest.yaml`, `.ai/CURRENT-STATE.md`, and `core/ai-bootstrap-protocol.md`.

Bootstrap outcomes are `READY` or `HOLD`. A bootstrap PASS is structural evidence only; it does not grant authorization, prove feature correctness, or claim production readiness.

Every bootstrap run explicitly reports:
- `Execution authority: UNCHANGED`
- `Mutation performed: NONE`

Next foundation-hardening targets are broader health/doctor diagnostics, state/contract consistency checks, documentation-drift detection, migration/version handling, partial-installation detection, and fresh-AI onboarding proof.

## Multi-Session / Fresh-AI Continuation closure

PR #13 merged at `cd8524b11f923e5e29eeaf445869b6239954ed1f` from final source head `99822037a9e24625f2e7c216300c4aabd94e134e` after Contracts 518, Full DevOS 443, and External Managed Project 31 passed.

## Controlled Remote Mutation Proof closure

Normative contract: `core/controlled-remote-mutation-proof.md`.
Supervisor: `tools/controlled-remote-mutation-proof.py`.
Regression corpus: `tools/test-controlled-remote-mutation-proof.py`.
Existing mutation capability under proof: `github.mutate.file` only.
Read-only current-state/readback capability: `github.inspect.file`.

Final verified source head: `bf5da56950d32722ce78898854eb3aa660321c38`.
PR #14 merged at `ffbdd7a4849dd012604911accd1211f172bde53b`.

Fresh final-head verification:
- Verify Development OS Contracts — run 528 / `34757546919`: success.
- Verify Development OS — run 453 / `34757546920`: success.
- Verify P13 External Managed Project — run 37 / `34757546868`: success.

### Proven simulated/provider-contract mutation invariants

- `github.inspect.file` provides bounded fresh current-state/readback evidence.
- Exact authorization and Security Gate PASS are required before `github.mutate.file`.
- Fresh provider SHA must match the expected SHA before mutation.
- The mutation adapter is invoked at most once per governed attempt.
- Provider mutation response is mutation-attempt evidence, not verified completion.
- Fresh post-mutation readback must observe the intended content and current SHA before `VERIFIED`.
- Stale SHA blocks before mutation.
- Conflict, failed/mismatched readback, or unproven final state HOLDs with mutation replay forbidden.
- An uncertain provider response may be reconciled by readback if the exact intended state is observed, but no second mutation call is issued automatically.

### Explicit evidence boundary

This closure is **provider-simulated / contract-level proof**, not a live DevOS runtime mutation against a real repository/provider resource.

Normal GitHub repository edits used to implement DevOS are development actions through the connected GitHub tooling; they are not treated as DevOS runtime mutation-proof authorization/evidence.

Still unproven or unavailable unless separately explicitly authorized/bounded:
- live real-provider `github.mutate.file` runtime proof;
- branch mutation;
- pull-request mutation;
- workflow mutation;
- deployment/production mutation;
- database mutation;
- permission/credential/secret mutation;
- destructive mutation.

## Active maturity gate — Production-Readiness Evidence Matrix & Limitations

Implementation is present at v1 on PR #16; closure requires reconciliation against current `main` plus fresh exact-final-head verification.
See `config/readiness-evidence.json`, `tools/verify-readiness-evidence.py`, and `docs/PRODUCTION-READINESS-EVIDENCE.md`.
The offline verifier covers 15 capability families and rejects unsupported evidence promotion. `VALID` never means production ready. Bootstrap checks participate in primary CI.
Historical evidence remains pinned to its original source heads and is not silently repointed when the branch advances.

Goal: produce an evidence-based readiness view rather than a blanket “production ready” label.

The matrix must distinguish at least:
- deterministic/component contract proof;
- integrated repository proof;
- real managed-project read-only proof;
- provider-simulated mutation proof;
- live-provider mutation proof;
- production/destructive capabilities;
- known limitations and unproven boundaries.

It must map each major DevOS capability to:
- implementation status;
- verification level;
- real/simulated evidence source;
- authorization/Security Gate boundary;
- recovery/no-replay behavior;
- production-readiness claim allowed or explicitly not allowed.

No live high-impact mutation should be performed merely to fill a matrix cell. A live-provider mutation proof, if desired later, requires separate explicit authorization for an exact target/path/operation.

## Universal AI/account portability gate

DevOS is intended to be **host-neutral**. A fresh AI should be able to enter a managed project without the previous AI's hidden memory and recover the same authoritative state from repository evidence.

The portability gate therefore requires evidence that:

- project semantics are stored in portable repository state;
- host-specific capabilities are isolated behind adapters/capability profiles;
- no ChatGPT/Claude/Gemini/Cursor/etc. account memory is required for authoritative recovery;
- changing model/vendor/account does not change authorization rules;
- a new AI can detect stale/conflicting state instead of silently trusting the previous session;
- the same project can continue through different AI hosts when the required capabilities are available.

This is a **product-level acceptance property**, not merely a documentation statement. Cross-host proof remains part of the hardening direction.

## Recovery precedence

1. Current source tree + Git.
2. Explicit requirements/decisions.
3. `.ai/CURRENT-STATE.md`, `.ai/TASKS.md`, and semantic `.ai` state.
4. `.ai/SESSIONS/` provenance.
5. Generated indexes as navigation/evidence only.
6. ChatGPT Memory/chat history as supplementary context only.

## Independent audit feedback

An independent AI audit was performed from the supplied audit source pack and separately accessible public repository artifacts. The audit correctly identified the risk of relying on claims without executable source evidence and highlighted documentation/roadmap drift, including an open Issue #1 with a separate P0/P1/P2 taxonomy. It also initially classified P16/P17 as unknown because those source files were not accessible in its environment.

The live repository subsequently confirmed that P16 and P17 contracts are present on `main`. Therefore, inability to fetch a file is treated as an **evidence-access limitation**, not proof that the implementation does not exist.

PR #17 subsequently closed the audit-pack dependency gap with read-only `tools/devos-audit.py`, added cross-layer adversarial Security Gate coverage, and hardened P17 against semantic impact downgrades. PR #16 must preserve those Trust-First controls rather than duplicating them.

The audit feedback remains valuable as a permanent hardening requirement: DevOS must make contradictory status records, stale README/version information, incomplete audit bundles, and unsupported completion claims detectable rather than relying on AI interpretation.

## Handoff documentation

Stable AI discovery path: [`docs/handoff/README.md`](../docs/handoff/README.md).
It links the comprehensive master handoff, dated evidence snapshot and local verification helper. The snapshot records main at `70c8e0e050660fd6b606150a1370d8fce51e373e`; later publication commits do not refresh that historical evidence. This documentation publication does not close the active production-readiness matrix gate or prove live runtime mutation.

The full scratch-to-current history, status matrix, foundation bootstrap work, independent audit feedback, universal AI portability direction, limitations, recommended direction, invariants, and a fresh-AI verification prompt are documented in `docs/DEVOS-COMPLETE-STATUS.md`.

Exact implementation remains authoritative in Git history.
