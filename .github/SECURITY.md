# Security Policy

## Scope

DevOS is a governance, automation, evidence, and development-workflow repository. Security-sensitive behavior includes authorization gates, provider adapters, runtime handoffs, repository mutation controls, release evidence, and any code that handles credentials or execution boundaries.

Current distribution boundary: `production_ready = false`.

## Reporting a vulnerability

Prefer GitHub's private **Report a vulnerability / Security Advisory** flow for this repository when it is available. If private reporting is unavailable, contact the repository maintainer through the GitHub account associated with `zzpsah` and provide only the minimum information needed to establish a private channel.

**Do not include secrets, tokens, passwords, private keys, session cookies, private user/school documents, or production data in a public issue, discussion, pull request, log, screenshot, or test fixture.**

For an initial report, include:

- affected file/component and commit SHA if known;
- impact and preconditions;
- a minimal safe reproduction that does not expose real credentials or private data;
- whether the issue could cross an authorization, execution, mutation, or evidence-integrity boundary; and
- any suggested containment.

## Supported security posture

Release-readiness and CI do not authorize production execution. The following invariants remain in force:

- `INTERPRETATION != AUTHORIZATION`
- `PLAN != EXECUTION`
- `READY != EXECUTION`
- `CI PASS != AUTHORIZATION`
- `PROVIDER CREDENTIAL != DEVOS AUTHORIZATION`
- `PROVIDER RESPONSE != COMPLETION PROOF`
- `RECOVERY != AUTOMATIC MUTATION REPLAY`
- `production_ready = false`

A runtime/provider name is not proof of verified capability. Uncertain mutations must not be blindly replayed. Release artifacts must be built from exact committed source and must not contain untracked local state.

## Secret handling

Never commit real credentials. Tests and documentation must use synthetic placeholders. GitHub Actions secrets must remain in the platform secret store and should be scoped to the minimum required repository/action permissions. Durable evidence may record non-secret identifiers and outcomes, never raw private keys or access tokens.

## Fix and disclosure expectations

Security fixes should be isolated, reviewed against the relevant DevOS gates, tested with adversarial regression coverage where practical, and documented without publishing exploit-enabling secrets. Public disclosure should follow the private fix/verification path when a vulnerability could materially weaken authorization, execution, mutation, or data-integrity controls.
