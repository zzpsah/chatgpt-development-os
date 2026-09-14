# DevOS Decisions

## Core documentation law
- **What is not written was never done.**
- Every material AI engineering action, decision, repair, experiment, verification result, evidence change, architecture change, roadmap change, or externally relevant outcome must leave a durable repository record.
- Completion requires `IMPLEMENTED + VERIFIED + DOCUMENTED + DURABLE STATE`.
- The durable record must preserve what happened, why, where, how it was verified, supporting evidence, remaining unknowns, and next-AI continuation guidance.
- `docs/DEVOS-MASTER-ENGINEERING-MAP.md` is the living architecture/navigation layer and must be updated when material architecture, capability, evidence-boundary, interpreter, portability, security/authorization, or future-goal semantics change.
- Automation may synchronize machine-observable facts; semantic decisions require evidence-driven AI/engineering judgment.

## GitHub Identity & Token Control Plane v1
- GitHub App is the preferred long-term authentication mechanism for DevOS GitHub integration because it supports fine-grained permissions and short-lived installation tokens.
- GitHub App user authorization and installation authorization are distinct authentication modes and must remain distinguishable in project bindings.
- Authentication establishes provider identity/capability only; it never manufactures DevOS authorization.
- Raw access tokens, refresh tokens, App private keys, OAuth client secrets, JWT signing material, and equivalent credentials never enter Git, `.ai`, MCP arguments, logs, evidence, or model output.
- Only non-secret identity/capability metadata may enter durable DevOS state.
- Interactive OAuth callbacks require cryptographically random pending state, constant-time comparison, bounded freshness, and one-time consumption; stale/reused/mismatched state fails closed.
- Token expiry/revocation requires reauthorization or token renewal; authentication failure never authorizes blind retry of a mutation.
- Project-to-GitHub identity binding is explicit and isolated per project; credentials/provider bindings and approval scopes cannot cross projects.
- Provider capability must be discovered and recorded as non-secret metadata before capability-dependent execution is considered.
- Provider-permission to DevOS-capability mappings are adapter-supplied and versioned at the integration boundary; generic DevOS must not infer stale provider permission semantics.
- Capability discovery is permission-level-aware and repository-scope-aware; `read` cannot satisfy required `write`, and an out-of-scope target cannot be `AVAILABLE`.
- Capability discovery returns `AVAILABLE`, `UNAVAILABLE`, or `UNCONFIRMED`; `UNCONFIRMED` fails closed and never manufactures authorization.
- Capability discovery evidence remains `authorization: UNCHANGED`, `execution: NONE`, `mutation: NONE`, and excludes credential material.
- “Full access” means maximum access explicitly granted by GitHub to the authorized user/app installation within its actual repository/organization scope, further constrained by DevOS capability, P17, Security Gate, and exact authorization. It does not mean a master bypass token.

## GitHub-hosted runtime authentication
- When DevOS executes inside GitHub Actions, use GitHub App installation-token authentication as the primary live runtime path.
- A browser OAuth callback is not required for the GitHub Actions runtime because the runner can authenticate directly with the App private key and App ID, resolve an installation for the target repository, and mint a short-lived installation token.
- Store `DEVOS_GITHUB_APP_ID` and `DEVOS_GITHUB_APP_PRIVATE_KEY` only as GitHub Actions secrets; never commit them.
- `tools/devos-github-actions-auth.py` performs JWT signing, installation resolution, token minting, and read-only repository verification only.
- `.github/workflows/devos-github-app-runtime.yml` is a read-only authentication/verification workflow and must not be treated as DevOS authorization or mutation permission.
- Installation-token access proves provider authentication/capability only; it does not prove production readiness or authorize future mutations.

## MCP/App Permission Control Plane
- Remote provider/API write access is a technical capability, not DevOS authorization.
- MCP/App host adapters must route remote mutation eligibility through the provider-independent DevOS permission control plane.
- Remote capabilities are distinct: repository create/delete, branch create/update/force-update/delete.
- `FULL APPROVAL` is scoped approval, never blanket permission.
- `continue` reuses approval only when project, workflow, capability, target, impact ceiling, freshness, and security conditions remain valid.
- Multi-project operation requires isolated state and approval scope per project/repository.
- Provider credentials/tokens never enter `.ai`, MCP arguments, logs, evidence, or model output.
- Provider mutation response is not completion proof; fresh readback is required.
- Uncertain remote mutation enters HOLD/reconciliation and cannot be blindly replayed.

## Actionable HOLD + Scoped Approval — closure
- PR #23 is merged at `7c60c3a4a36982ba894e2f30ba9dd98500f98d02`.
- Final source head before merge: `954b094a3832c300d371426d682eac90156cbb04`.
- Scoped approval never replaces P17/controller authorization.
- `continue` may reuse approval only within exact project/workflow/capability/target/impact/freshness/security scope.
- Stale repository state, changed target/capability, impact escalation, or changed Security Gate requires fresh evaluation.
- No live/destructive/provider/production mutation was performed for this objective.

## Current-Source Evidence Refresh — closure
- This was a bounded, unnumbered objective; no P18/P19 phase was created.
- The protocol adds fresh exact-current-source proof without rewriting historical readiness evidence.
- Historical provenance remains pinned; `production_ready=false` and `live_provider_proven=false` remain unchanged.

## Durable project state authority
- DevOS project-local `.ai` is the portable durable context layer.
- Source tree + Git are authoritative for implementation state and exact changes.
- AI account memory/chat history are supplementary and not project authority.
- `STATE-INDEX.md` is evidence/navigation, not semantic authority.
- Universal acceptance invariant: `AI A + Account A → repository → AI B + Account B → correct recovery → safe continuation`.

## P9–P11 continuity decisions
- P9 Development Task Controller remains the governed controller boundary for bounded execution candidacy.
- P10 Context Continuity & Recovery established repository-local continuity independent of chat memory.
- P11 Federation & Self-Healing Context remains the repository-first recovery/revalidation/cross-AI continuity baseline.

## P15–P17 decisions
- P15 Human Language Interpretation is the top-level semantic entry capability and never grants authority.
- P16 planning remains non-executing/non-authorizing.
- P17 `READY` means eligibility only; authority/authorization/execution remain unchanged.
- Higher-impact execution remains separately authorized and Security-Gate controlled.

## AI State Resolver v2
- The original P0 resolver contract is retained. v2 adds a deterministic, read-only implementation with claim-specific grounding and boundary-triggered revalidation.
- `observed` requires current P12 execution evidence with citable grounding; uncited observed claims and duplicate claim IDs resolve to `unknown`.
- Durable-state grounding is capped at `likely` even when cited because it records an assertion rather than proving the underlying outcome.
- P12 remains the sole normalizer/freshness owner of execution evidence. The resolver only references P12 evidence IDs.
- Unresolved resolver claims force P16 `CLARIFY`; P17 rejects a tampered planned envelope that still carries unresolved claim IDs.
- State confidence is never authorization, completion, execution, or mutation authority.

## Plain Project Context and Recovery Guide v1
- First-contact material is ordinary repository context, not authority over a host's rules.
- Refusal of unavailable or consequential work is compatible behavior; the guide requires honest context recovery.
- The core bootstrap and base operating rule require the guide; embedded bypass instructions are documentation anomalies.
- The optional first-contact acknowledgement must report only that context was recovered or not verified. It must not ask a host to enter a mode, alter permissions, or change behavior.

## P15 bounded multilingual interpretation and gating
- The deterministic P15 reference interpreter may preserve Unicode and add bounded language patterns only with regression evidence through P16 and P17.
- Language recognition must not create authority, authorization, execution, a truth winner, or production readiness.
- High-impact terms must be recognized consistently by P15 and P16 so a translated request cannot be downgraded to read-only; P17 remains the independent readiness/authorization gate.
- The corpus is an explicit bounded contract, not a claim of universal language or dialect support.

## Local Disposable Delivery Proof v1
- The first automated-delivery proof is restricted to a newly created temporary local Git repository and one low-impact file update.
- The approval must bind the exact project path, Git head, target, capability, impact ceiling, and P16 step. A mismatch or stale pre-write state holds rather than updating.
- P15 interpretation, P16 planning, P17 readiness, controller/runtime handoff, testing, readback, and evidence recovery remain independently visible evidence stages.
- Successful local proof does not authorize commits, pushes, managed-repository operations, provider access, deployment, production, credentials, database, permission, destructive operations, or general automated delivery.

## Universal Agent Runtime Adapter v1

- PR #57 provides a vendor-neutral, side-effect-free runtime handoff/result-validation boundary.
- A P17 READY step and scoped approval are prerequisites, not execution authority. The adapter accepts only low-impact `file.create` / `file.update` operations and exact repository-head/path/capability/approval/runtime-profile scope.
- A runtime completion claim becomes verified only after independent diff, test, and final-readback validation. Returned evidence is not authority.
- This does not establish a vendor-specific runtime integration, managed-repository delivery, external mutation, or production readiness.
