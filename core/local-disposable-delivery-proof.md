# Local Disposable Delivery Proof v1

## Purpose

Prove one complete DevOS automated software-delivery loop without contacting a provider or changing a real project repository.

`human request → P15 → P16 → P17 → explicit scoped approval → local update → test → readback → durable evidence`

## Scope

- A newly created temporary local Git repository only.
- One update to `delivery-marker.txt` from `before` to `after`.
- A local verification script, Git diff readback, SHA-256 before/after evidence, and `.ai/local-delivery-evidence.json` inside the disposable repository.
- A fresh evidence verifier may read that packet without conversation memory.

## Approval boundary

Preparation reports the exact Git head, project path, target, and required step ID. Execution requires `DEVOS-LOCAL-DELIVERY-APPROVAL-v1` bound to the exact project, Git head, `S2`, `local.file.update`, `delivery-marker.txt`, and `LOW_IMPACT_MUTATION` ceiling.

An approval mismatch, stale head, changed target, missing approval, changed pre-write digest, failed P17 gate, failed controller/handoff, failed test, or failed readback is HOLD. The harness never invents a replacement approval.

## Non-goals

This proof does not deploy, commit, push, access credentials, contact a provider, mutate a production or managed repository, modify a database, alter permissions, delete content, or prove general automated delivery readiness.
