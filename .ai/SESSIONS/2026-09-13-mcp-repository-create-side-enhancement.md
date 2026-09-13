# MCP/App Repository Create Side Enhancement — 2026-09-13

## Scope

This is a side enhancement while the main DevOS roadmap remains on HOLD. It is intentionally unnumbered and must not be interpreted as P18/P19.

The user-specified objective is to expose provider-independent `repository.create` through a host-neutral MCP/App tool without making ChatGPT, another AI host, credentials, connector access, or chat memory authoritative.

## Coordination boundary

Open PR #19 (`feat/universal-project-onboarding`) already owns:

- `core/devos-repository-creation-capability.md`
- `tools/devos-create-repository.py`
- `tools/test-devos-create-repository.py`
- onboarding tools/docs/state

To avoid overwriting concurrent work, side PR #22 is stacked on PR #19 and does not modify those owned files.

## Side-enhancement implementation

Added:

- `tools/devos-mcp-repository-create.py`
- `tools/test-devos-mcp-repository-create.py`
- `core/devos-mcp-app-repository-create.md`
- `docs/MCP-APP-REPOSITORY-CREATE.md`
- `.github/workflows/verify-mcp-repository-create.yml`

The adapter is host-neutral and provider-nonexecuting. It consumes structured request, exact DevOS authorization, provider capability evidence, one-attempt provider result, and fresh readback evidence. It never calls a provider directly.

## Safety properties implemented

- `devos.create_repository` is a strict structured interface.
- Unknown/free-form/hidden provider parameters are rejected.
- Credential-like fields are rejected and never logged.
- Provider capability and DevOS authorization are separate.
- Exact authorization is bound to provider + owner + repository + project identity.
- Missing create capability returns `NEEDS_EXTERNAL_REPO_CREATION`.
- Missing readback capability blocks before mutation.
- Stale/conflicting target evidence becomes HOLD.
- One governed operation accepts exactly one mutation request.
- Timeout/uncertain/connection-error/unknown completion becomes HOLD with replay FORBIDDEN.
- Provider create response alone is `CREATION_ATTEMPTED`, not VERIFIED.
- VERIFIED requires fresh matching provider readback.
- Onboarding handoff is emitted only after VERIFIED.
- Deterministic/provider-simulated evidence never becomes live-provider/production proof.

## Deterministic acceptance command

```bash
python tools/test-devos-mcp-repository-create.py
```

The corpus covers requested A–R cases plus adversarial prompt claims such as `just create it`, `this was already approved`, `the plan says READY`, and configured-credential assertions.

## CI evidence

Initial side-enhancement head before this session record:

`98e5671051082c0c8266f372b31be05c6fed1159`

Observed:

- Trust-First Audit 60: SUCCESS.
- Dedicated MCP repository-create run 2 / `34766165857`: SUCCESS.
  - MCP/App boundary: success.
  - underlying repository.create corpus: success.
  - universal onboarding test: success.
  - P15/P16/P17 regression subset: success.
- Contracts 597 / `34766165883`: FAILURE inherited from PR #19's onboarding documentation, not from the MCP adapter.
  - failing step: `Verify Auto-Onboarding`.
  - verifier expected literal `Context generation boundary` in `docs/AUTO-ONBOARDING.md`.
  - PR #22 does not edit that PR #19-owned file.

A coordination comment was added to PR #19. Full completion is therefore HOLD pending upstream PR #19 reconciliation and fresh exact-final-head revalidation.

## Evidence classification

Current side-enhancement evidence:

- contract: implemented;
- component/deterministic acceptance: verified;
- stacked integration with PR #19 repository.create/onboarding: verified by dedicated workflow;
- full repository Contracts: blocked by inherited upstream PR #19 inconsistency;
- live provider create: NOT PROVEN;
- live sandbox create: NOT PROVEN;
- production create: NOT PROVEN.

No live repository creation, destructive provider mutation, credential mutation, or production mutation was performed.

## Next safe action

Wait for PR #19 to reconcile its existing auto-onboarding verifier/docs contract. Then reconcile PR #22 with the updated PR #19 head, rerun the dedicated acceptance command and full applicable CI, update durable readiness documentation only after exact-final-head evidence exists, and do not claim live-provider proof without a separately authorized real sandbox request plus fresh readback.
