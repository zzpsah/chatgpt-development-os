# DevOS Universal Onboarding Policy v1

## Rule

Every project intentionally managed with DevOS should carry repository-local DevOS context so the project remains portable across AI vendors, AI accounts, sessions, models, and coding agents.

## Existing projects

When DevOS is introduced to an existing project:

1. Run onboarding inspection first.
2. Preserve existing application source and existing semantic `.ai` context.
3. Create only missing DevOS infrastructure.
4. If another framework is already authoritative, return `HOLD` rather than overwriting it.
5. Validate the resulting context before substantial AI work.
6. Commit and push onboarding infrastructure when the repository is intended to be remotely portable.

## New projects

For new projects:

1. Start from the DevOS project template when practical, or run the cross-platform initializer before substantial development.
2. If the remote repository does not exist, use the separate governed `repository.create` capability when the selected provider exposes it and explicit authorization is available.
3. Include durable context in the first repository commits.
4. Keep project-local `.ai` state as the portable memory layer.
5. Enable repository-side synchronization when the project uses GitHub and the owner wants it.

## Repository creation capability

`repository.create` is a **high-impact remote mutation** and is separate from onboarding permission.

Repository creation requires:

- explicit target owner/namespace;
- explicit repository name/visibility policy;
- provider capability discovery confirming creation is exposed;
- exact repository-creation authorization;
- a post-create verification/readback path.

A provider credential or general repository write permission does not automatically authorize repository creation.

If the selected AI/provider does not expose repository creation, DevOS must return an unavailable-capability result such as:

`NEEDS_EXTERNAL_REPO_CREATION`

and must not claim creation occurred.

A provider response is not completion proof. Creation must be reconciled/read back before `VERIFIED` can be claimed. An uncertain creation response must lead to `HOLD → reconcile`; automatic creation replay is prohibited.

## Automatic onboarding

DevOS provides three distinct automation levels:

- **Local automatic:** a configured local worker may discover projects under explicitly configured roots and invoke idempotent onboarding.
- **Template automatic:** projects created from an approved DevOS template start with the expected context.
- **Remote organization automatic:** a separately installed GitHub App, organization workflow, or equivalent integration may create/onboard authorized repositories.

The mere existence of the public DevOS repository does not grant permission to modify arbitrary remote repositories.

## Authorization boundary

Onboarding infrastructure creation and remote repository creation are mutations. They require explicit governed operations and never authorize:

- application-code changes beyond the stated onboarding infrastructure;
- production changes;
- database mutation;
- credential/secret changes;
- permission changes;
- destructive operations;
- arbitrary remote execution.

## Evidence boundary

Onboarding success means:

`DevOS infrastructure present / preserved + bootstrap structurally valid`

Repository creation success means:

`provider creation attempt + fresh provider readback confirms intended repository`

Neither means:

`application correct + secure + tested + production ready`.

## Universal portability requirement

The minimum acceptance scenario is:

`AI A / Account A → repository state → AI B / Account B → recover → verify → continue`

The implementation must remain vendor-neutral and account-neutral. Avoid durable formats or workflows that require a particular AI provider to be authoritative.

## Fail-closed rule

Onboarding must HOLD when:

- project path is invalid;
- required repository identity is incompatible;
- existing managed context belongs to another framework and would be overwritten;
- required infrastructure cannot be created safely.

Repository creation must BLOCK/HOLD when:

- provider capability is unavailable;
- exact authorization is absent;
- target identity/name is invalid;
- required verification evidence is unavailable;
- provider response is uncertain.

Do not guess.
