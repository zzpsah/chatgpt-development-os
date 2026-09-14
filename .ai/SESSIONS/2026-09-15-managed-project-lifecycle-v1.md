# Managed Project Lifecycle v1 — 2026-09-15

## Trigger

A real repository, `zzpsah/Devos-Browser`, existed with only a README and had not become a DevOS-managed project. Fresh inspection showed the architectural reason: `repository.create` / repository discovery and universal onboarding existed as separate capabilities, but no mandatory lifecycle gate prevented development from continuing while a repository remained unmanaged.

## Fresh base

Feature branch: `feature/managed-project-lifecycle-v1`

Base `main`: `95877bb18551af5ce3a4d7f52876dea983551e19`.

Canonical version before feature: `0.20.0`.

Observed gap:

```text
repository created/discovered
        ↓
(no mandatory management-state gate)
        ↓
onboarding could be skipped
```

## Bounded objective

Implement an unnumbered **Managed Project Lifecycle v1** capability and advance distribution identity to `0.21.0`.

Required behavior:

```text
CREATE / DISCOVER
      ↓
fresh repository readback
      ↓
managed-project lifecycle classification
      ↓
MANAGED → recover state → development may continue
UNMANAGED/PARTIAL → onboarding required → fresh readback
CONFLICT/MALFORMED → HOLD/BLOCKED
```

## Source changes

- `tools/devos-project-lifecycle.py`
  - local repository classification;
  - provider snapshot classification via `DEVOS-REPOSITORY-DISCOVERY-SNAPSHOT-v1`;
  - explicit `MANAGED`, `ONBOARDING_REQUIRED`, `HOLD`, `BLOCKED` outcomes;
  - development continuation true only for `MANAGED`;
  - authorized local onboarding followed by fresh managed-state readback;
  - remote snapshot mode remains read-only.
- `tools/devos-create-repository.py`
  - creation plans/results now carry a mandatory managed-project postcondition;
  - provider creation/readback cannot imply onboarding or development continuation.
- `tools/devos.py`
  - new `project-lifecycle` command.
- regression coverage
  - local unmanaged / authorization / apply / idempotency;
  - remote unmanaged / partial / managed / conflict / malformed states;
  - repository-creation postcondition;
  - CLI dispatch.
- dedicated Python 3.11/3.12 CI.
- lifecycle contract + auto-onboarding documentation.
- coherent `0.21.0` VERSION/release-manifest/README/changelog/readiness-version update.

## Permanent invariants

```text
REPOSITORY EXISTS != DEVOS MANAGED
REPOSITORY CREATED != ONBOARDED
REPOSITORY DISCOVERED != SAFE TO CONTINUE
ONBOARDING != APPLICATION VERIFIED
PROVIDER CAPABILITY != AUTHORIZATION
```

`production_ready = false` remains unchanged.

## External proof target

After the core feature is merged and post-merge CI is verified, `zzpsah/Devos-Browser` should be onboarded as the first real remediation case using the same managed-project contract. That repository must receive durable DevOS context and fresh readback before being described as managed.

## Verification / merge boundary

- exact-head lifecycle CI must pass on Python 3.11 and 3.12;
- normal DevOS/release/production-readiness workflows must remain green;
- merge only from the exact verified feature head;
- post-merge `main` and exact-source artifact must be freshly read back;
- durable state must then be reconciled separately.

No production deployment, credential/secret/database/permission mutation, destructive action, public tag/GitHub Release publication, or production-readiness promotion is part of this objective.
