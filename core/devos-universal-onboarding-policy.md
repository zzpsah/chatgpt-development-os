# DevOS Universal Onboarding Policy v1

## Rule

Every project that is intentionally managed with DevOS should carry repository-local DevOS context so the project remains portable across AI vendors, AI accounts, sessions, models, and coding agents.

## Existing projects

When DevOS is introduced to an existing project:

1. Run the onboarding inspection first.
2. Preserve existing application source and existing semantic `.ai` context.
3. Create only missing DevOS infrastructure.
4. If another framework is already authoritative, return `HOLD` rather than overwriting it.
5. Validate the resulting context before substantial AI work.
6. Commit and push the onboarding infrastructure when the repository is intended to be remotely portable.

## New projects

For new projects:

1. Start from the DevOS project template when practical, or run the cross-platform initializer before substantial development.
2. Include the durable context in the first repository commits.
3. Keep project-local `.ai` state as the portable memory layer.
4. Enable repository-side synchronization when the project uses GitHub and the owner wants it.

## Automatic onboarding

DevOS provides three distinct automation levels:

- **Local automatic:** a configured local worker may discover projects under explicitly configured roots and invoke idempotent onboarding.
- **Template automatic:** projects created from an approved DevOS template start with the expected context.
- **Remote organization automatic:** a separately installed GitHub App, organization workflow, or equivalent integration may onboard authorized repositories.

The mere existence of the public DevOS repository does not grant DevOS permission to modify arbitrary remote repositories.

## Authorization boundary

Onboarding infrastructure creation is itself a mutation. It must be initiated through an explicit onboarding operation and must never be interpreted as authorization to modify application code, production systems, database state, credentials, permissions, or secrets.

## Evidence boundary

Onboarding success means:

`DevOS infrastructure present / preserved + bootstrap structurally valid`

It does not mean:

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

Do not guess.
