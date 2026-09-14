# Session — Universal Agent Runtime Adapter v1

Date: 2026-09-14

## Objective

Build a vendor-neutral, side-effect-free runtime boundary that compiles a P17 READY step plus exact scoped approval into a tamper-evident agent handoff, then validates returned diff/test/readback evidence without trusting an agent's self-reported completion.

## Concurrency context

Another AI is separately developing `Automated Software Delivery v1` in a temporary disposable local Git repository. That work owns the actual local create/update/test/readback delivery loop.

This slice intentionally does **not** implement a duplicate filesystem mutation engine. It standardizes the runtime handoff/result boundary that a delivery loop may consume.

The branch started from fresh `main` at `ec77c2efed145fe2c419fba365aad33a6f10990e` after Evidence → Durable State Reconciliation v1 was durably closed. No open PR was visible at branch creation.

## Existing foundations inspected

- `adapters/adapter-contract.md` — vendor-neutral host portability contract.
- `adapters/host-adapter.md` — bounded host capabilities including scoped filesystem write, Git inspection, verification, and remote-operation boundaries.
- `adapters/reference-host.py` — local bounded reference adapter with explicit authorization required for writes.
- `tools/verify-host-profile.py` / `adapters/host-profile.example.json` — portable host capability declaration.
- `tools/step-readiness-orchestrator.py` — P17 READY envelope and exact-step gates.
- `tools/devos-actionable-hold.py` — scoped approval semantics and `CONTINUE != BLANKET AUTHORIZATION` behavior.

## Gap

DevOS had host capability declarations and governed execution semantics, but no deterministic runtime-neutral envelope that:

1. revalidates P17 READY;
2. revalidates exact scoped approval;
3. binds repository HEAD, target paths, operations, and runtime identity;
4. makes the handoff tamper-evident;
5. independently checks returned diff/test/readback evidence.

Without that boundary, each coding-agent integration could invent its own execution contract and accidentally weaken scope or evidence semantics.

## Implemented

### `tools/agent-runtime-handoff.py`

Protocols:

- `DEVOS-AGENT-RUNTIME-HANDOFF-INPUT-v1`
- `DEVOS-AGENT-RUNTIME-PROFILE-v1`
- `DEVOS-AGENT-RUNTIME-HANDOFF-v1`
- `DEVOS-AGENT-RUNTIME-RESULT-v1`
- `DEVOS-AGENT-RUNTIME-VERDICT-v1`

Handoff compilation requires:

- P17 `READY`;
- every P17 gate true;
- exact repository-head freshness;
- low-impact mutation only;
- explicit step approval required and present;
- exact project/workflow/capability/target/HEAD approval scope;
- required local runtime capabilities `AVAILABLE`;
- safe relative paths;
- only `file.create` / `file.update` operation classes.

The canonical handoff is SHA-256 hashed into `handoff_id`.

The adapter performs no execution or mutation.

### Result validation

A runtime's `COMPLETED` claim becomes `VERIFIED_RUNTIME_RESULT` only if:

- handoff digest is intact;
- runtime identity and pre-execution HEAD match;
- touched files stay within approved paths;
- observed diff paths exactly match touched files;
- diff carries a digest;
- tests pass with exit code 0 and output digests;
- every touched file has final PRESENT readback with content digest;
- no prohibited operation is reported as used.

Returned evidence remains evidence, not authority.

### Adversarial regression corpus

`tools/test-agent-runtime-handoff.py` covers:

- happy-path handoff;
- deterministic normalized scope;
- non-READY P17 state;
- high-impact step rejection;
- missing explicit approval requirement;
- stale approval/work repository HEAD;
- path escape;
- delete operation request;
- target outside approval;
- missing runtime verification capability;
- tampered handoff;
- out-of-scope touched file;
- failed tests;
- missing readback;
- prohibited operation use;
- diff/touched-file mismatch;
- stale result HEAD.

### Documentation and CI

- `core/agent-runtime-adapter.md` defines the normative contract and separation from Automated Software Delivery v1.
- `adapters/agent-runtime-profile.example.json` provides a generic local-agent capability profile without claiming any vendor-specific integration is already implemented.
- `.github/workflows/verify-agent-runtime-adapter.yml` runs dedicated regression and contract-marker checks.

## Permanent boundaries

- `authority = UNCHANGED`
- `authorization = UNCHANGED`
- validator `execution = NONE`
- validator `mutation = NONE`
- `production_ready = false`
- no delete/deploy/production/credential/secret/database/permission/external mutation
- no direct runtime provider/API invocation in v1
- no automatic approval
- no P18/P19 bookkeeping phase

## Remaining before completion

1. Compare against fresh `main` and any parallel Software Delivery v1 branch/PR.
2. Open a bounded PR only if non-overlapping/reconciled.
3. Require exact-final-head CI including the dedicated runtime-adapter workflow.
4. Repair failures without weakening scope or evidence gates.
5. Merge under current bounded authorization only if fresh mergeability and concurrency checks pass.
6. Use Evidence → Durable State Reconciliation v1 for post-merge closure and leave a fresh recoverable state.
