# Session — 2026-09-17 — Project Fleet Watch v1

## Objective

Extend Managed Project Lifecycle from one-repository enforcement to read-only multi-repository visibility so newly accessible/unmanaged repositories and management regressions cannot silently disappear outside DevOS awareness.

## Trigger

After Managed Project Lifecycle v1 successfully remediated `zzpsah/Devos-Browser`, the user requested additional DevOS feature enhancement. Fresh `main`, open PRs/issues, current durable state, and lifecycle source were recovered before selecting this bounded objective. No open DevOS PR or issue conflicted with the work.

## Selected capability

Project Fleet Watch v1:

- deterministic fleet snapshot assessment;
- per-repository classification delegated to Managed Project Lifecycle v1;
- `HEALTHY | ATTENTION | HOLD | EMPTY | BLOCKED` fleet verdicts;
- previous/current drift detection;
- explicit `new_unmanaged`, `newly_managed`, and `management_regressions` signals;
- bounded read-only GitHub account/user discovery;
- `devos project-fleet` CLI dispatch;
- `--require-clean` fail-closed mode;
- Python 3.11/3.12 CI and adversarial regression coverage.

## Security / authority boundaries

```text
REPOSITORY ACCESSIBLE != DEVOS MANAGED
FLEET DISCOVERY != ONBOARDING AUTHORIZATION
FLEET ATTENTION != AUTOMATIC MUTATION
FLEET HEALTHY != APPLICATION VERIFIED
FLEET HEALTHY != PRODUCTION READY
```

Fleet Watch performs observation/classification only. It does not onboard repositories, deploy, publish, mutate provider resources, alter credentials/secrets/permissions/databases, or create authorization.

GitHub live discovery is GET/read-only. `GITHUB_TOKEN` is environment-only and must never be printed or persisted.

`production_ready = false` remains unchanged.

## Release identity

Because this adds a distribution capability after exact-source 0.21.0 release readiness, canonical version metadata advances coherently to `0.22.0` rather than reusing the prior source-version identity.

## Verification target

Before merge:

1. Fleet Watch regression corpus passes on Python 3.11 and 3.12.
2. Existing lifecycle/CLI/release/production-readiness/security/integration workflows remain green on the exact feature head.
3. Release gate accepts the 0.22.0 metadata/documentation/path set.
4. Exact-source distribution artifact is produced from the exact candidate head.
5. Merge uses exact-head protection.
6. Post-merge main readback/CI/artifact evidence is captured and durably reconciled before the objective is called closed.

## Non-actions

No production deployment, public release/tag/package publication, credential/permission/database mutation, destructive action, runtime promotion, or production-readiness promotion is part of this objective.
