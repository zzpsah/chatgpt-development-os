# DevOS Repository Creation Capability v1

## Purpose

Define repository creation as an explicit, provider-dependent DevOS capability so a new project can be created and immediately onboarded without tying the DevOS state model to one AI vendor or account.

## Capability identifier

`repository.create`

Provider example: `github.repository.create`

## Boundary

Repository creation is a **high-impact remote mutation**. It is never implied by:

- natural-language interpretation;
- a P16 plan;
- a P17 READY result;
- an available provider credential;
- an existing repository write permission;
- a previous approval for another repository;
- a prior successful creation.

## Preconditions

A governed repository-creation attempt requires:

1. explicit target owner/account or provider namespace;
2. globally unique or provider-valid repository name;
3. explicit visibility and initialization policy;
4. exact action authorization for `repository.create`;
5. capability discovery proving that the selected provider exposes repository creation;
6. current authorization/target evidence suitable for the provider;
7. no conflict with the intended project identity;
8. a post-create verification plan.

## Provider capability discovery

If the connected AI/provider does not expose repository creation, DevOS must return:

`NEEDS_EXTERNAL_REPO_CREATION`

and must not pretend the repository was created.

Provider capability availability is separate from DevOS authorization.

## Execution safety

The reference DevOS implementation is dry-run by default. Applying a remote repository creation requires an explicit apply flag plus an externally supplied authorization signal. The tool must never log or persist provider credentials.

The provider adapter must perform exactly one repository-create request per governed attempt. An uncertain provider response must trigger reconciliation/readback, not automatic retry.

## Post-create verification

A creation response is attempt evidence, not sufficient completion proof.

Completion requires fresh observation of the provider state confirming at minimum:

- expected owner/namespace;
- expected repository name;
- repository exists and is addressable;
- intended visibility/policy where observable;
- initial branch/default branch where applicable;
- no unexpected target substitution.

## Onboarding handoff

After verified repository creation, the normal onboarding flow becomes:

`repository.create → verify target → universal onboarding → initial commit/branch → context validation`

Repository creation must not silently bundle arbitrary application mutations.

## Safety / recovery

If the provider response is uncertain:

`HOLD → inspect/reconcile → fresh authorization if another mutation is needed`

Never blindly replay repository creation because the first response timed out or was ambiguous.

## Evidence levels

Keep these distinct:

- capability contract verified;
- deterministic adapter test verified;
- provider-simulated creation verified;
- live-provider sandbox creation verified;
- production/organization-scale creation verified.

A simulated adapter test never becomes live-provider proof automatically.

## Universal AI/account requirement

The repository created through this capability must immediately become repository-portable DevOS context. No AI account or vendor may become the authoritative owner of the project's durable memory.

Acceptance path:

`AI A / Account A → create repository → onboard → persist state → AI B / Account B → bootstrap → recover → continue`
