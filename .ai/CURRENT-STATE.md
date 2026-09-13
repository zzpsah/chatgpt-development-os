# Current State

## Snapshot

- Repository: `zzpsah/chatgpt-development-os`.
- Source tree + Git are authoritative; ChatGPT Memory/chat history are supplementary only.
- P11 repository-first recovery/revalidation remains a durable invariant.
- P9 through P17 are complete on `main`.
- **P17 Step Readiness & Authorization Orchestrator v1 is verified and merged through PR #10.**
- Active maturity work: **Production E2E Harness** on branch `devos/production-e2e-harness` / PR #11.
- Production E2E implementation and real managed-project proof are source-complete; closure remains gated on fresh CI for the eventual final branch head and merge.

## Canonical governed path

`Human request → P15 interpretation → Project/State Resolution → P16 goal-to-plan → P17 step readiness → P16 compiled-plan controller → P17 runtime handoff → bounded runtime-adapter operation → explicit verification → authorized durable evidence persistence → recovery readback`

Interpretation, planning, readiness, orchestration and successful tests never manufacture permission. Runtime execution remains capability-, scope-, authorization-, Security-Gate- and verification-bounded.

## P16 and P17 verified baseline

P16 merged through PR #9 at `460a212ebb7600619f396a455ac3e47e5a5c80fa`; final head `877833ef0f11d5a869284f9b86407c155125d96f` passed Contracts 476, Full 402, External 11.

P17 merged through PR #10 at `2f29ac1de367fb270c00d73b2ca44405ce09fc00`; final head `8011783962d6dddd33bcc50049c8aa4a8748cc52` passed Contracts 483, Full 408, External 12.

P17 closure state was persisted on `main` at `747082635094c458d72e9f3914fe661bee29803c`.

## Production E2E Harness implementation

Normative contract: `core/production-e2e-harness.md`.
Executable harness: `tools/production-e2e-harness.py`.
Regression corpus: `tools/test-production-e2e-harness.py`.
Real managed-project verifier: `tools/verify-production-e2e-managed-project.py`.

Reference protocol: `DEVOS-PRODUCTION-E2E-v1`.

The harness composes existing DevOS modules instead of creating a parallel executor. It fails closed at the earliest stage and records a stage trace across interpretation, planning, readiness, controller, handoff, runtime, verification, persistence and recovery.

### Runtime semantic binding

- Explicit bounded read allowlist: `filesystem.read`, `git.inspect`, and supported GitHub inspect operations.
- Explicit bounded mutation allowlist: `filesystem.write_scoped`, `github.mutate.file`.
- A `READ_ONLY` compiled step cannot execute a mutation operation.
- Any runtime mutation requires exact-step `ALREADY_GRANTED` authorization.
- GitHub remote mutation additionally requires exact-step Security Gate `PASS`.
- Eligibility authorization and runtime-operation authorization remain distinct; an approved security review may still execute a read operation using adapter-level `NOT_REQUIRED` authorization.
- Unknown runtime operations are blocked.

### Verification, persistence and recovery

- Verification uses the existing explicit-argv reference verification adapter; the harness introduces no shell interpretation.
- Runtime success is insufficient; verification must return `VERIFIED` before persistence.
- Evidence persistence is restricted to bounded `.ai/` paths and requires independent `ALREADY_GRANTED` persistence authorization.
- Persistence does not commit or push.
- Recovery reads the evidence packet back through the bounded reference host adapter.
- The persisted packet is marked `execution_evidence: true` only after observed runtime success + verification success; planning/readiness/controller metadata remain non-execution evidence.

## Regression proof

The isolated regression corpus proves:
- successful read-only whole path to `COMPLETE / RECOVERY`;
- stale compiled repository head stops at P17 readiness;
- READ_ONLY → mutation mismatch is blocked before mutation;
- failed verification blocks persistence success;
- missing persistence authorization blocks evidence write;
- missing capability blocks at readiness.

On branch head `4ae1cfa21a2c6149829d9a5b104f165f33cc5ed3`, Contracts run 488 executed `Verify Production E2E Harness` successfully and completed successfully overall.

## Real managed-project proof

CI checks out the real DevOS-managed repository `zzpsah/automation-suite` on `main` and runs the harness with a read-only `filesystem.read` operation against `README.md`.

The verifier independently confirms:
- Git remote identity is exactly `zzpsah/automation-suite`;
- repository HEAD is unchanged;
- runtime operation is read-only;
- README/AGENTS/.ai verification succeeds;
- the only local delta created by the proof is the explicitly authorized `.ai/EVIDENCE/production-e2e-managed-project.json` packet;
- no commit or push is performed by the verifier.

External Managed Project run 13 / `34751659403` succeeded, including the new Production E2E proof and evidence upload.

Evidence artifact:
- artifact id: `10316730199`
- name: `production-e2e-managed-project-evidence`
- digest: `sha256:bea3ec2c742be2a57d7f09066802dd31731b2b863dbb96c7c149a7085a42f7eb`
- associated proof head: `4ae1cfa21a2c6149829d9a5b104f165f33cc5ed3`

This artifact is CI evidence only; it does not mutate or deploy the managed project's remote repository.

## Current closure rule

The branch is not closed merely because the implementation and first proof are green. This semantic-state commit creates a newer final candidate head, so fresh applicable Contracts, Full DevOS and External Managed Project verification must pass on the eventual final head before PR #11 may merge.

If final-head CI fails, repair only the demonstrated defect and require newer fresh verification.

## Recovery precedence

1. Current source tree + Git.
2. Explicit requirements/decisions.
3. `.ai/CURRENT-STATE.md`, `.ai/TASKS.md`, and semantic `.ai` state.
4. `.ai/SESSIONS/` provenance.
5. Generated indexes as navigation/evidence only.
6. ChatGPT Memory/chat history as supplementary context only.

Exact implementation remains authoritative in Git history.
