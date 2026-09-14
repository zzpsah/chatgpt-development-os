# Agent Runtime Conformance Evidence Intake v1

## Purpose

`tools/agent-runtime-conformance-evidence.py` defines a deterministic intake boundary for evidence produced during a future direct runtime conformance exercise.

Protocols:

- `DEVOS-AGENT-RUNTIME-CONFORMANCE-CHALLENGE-v1`
- `DEVOS-AGENT-RUNTIME-CONFORMANCE-EVIDENCE-v1`
- `DEVOS-AGENT-RUNTIME-CONFORMANCE-VERDICT-v1`

This capability exists to make runtime portability evidence reproducible without allowing a runtime name, caller-supplied JSON, or a familiar vendor to become verified by assertion.

## Core rule

> **A valid conformance evidence packet is candidate evidence, not runtime verification and not registry promotion.**

The tool never changes `config/agent-runtime-profile-registry.json`. A `DECLARED` runtime remains `DECLARED` until separate direct invocation evidence is actually observed, reviewed, persisted, and merged through normal DevOS governance.

## Challenge binding

A challenge is bound to exactly:

- `runtime_id`;
- `adapter_version`;
- exact 40-character Git `repository_head`;
- a non-empty caller nonce; and
- the required conformance capability set.

The canonical challenge payload is SHA-256 hashed into `challenge_id`. Any runtime/head/nonce/capability mutation invalidates challenge integrity.

## Required capabilities

The evidence packet must cover exactly the same v1 capabilities required by the runtime profile registry and Universal Agent Runtime Adapter:

- `filesystem.read`
- `filesystem.write_scoped`
- `git.inspect`
- `verification.run`

Unknown or missing capability keys fail closed.

Each capability evidence item contains:

- `status`: `PASS` or `FAIL`;
- a non-empty evidence `ref`;
- a non-empty evidence `scope`; and
- a SHA-256 `digest` for the referenced probe/evidence material.

A failed required capability yields `HOLD`.

## Invocation provenance

A packet must contain non-empty invocation provenance:

- `kind`
- `ref`
- `observed_by`

This preserves where a future direct proof claims to have come from. The fields are provenance metadata only; their presence is not trusted attestation by itself.

## Verdict semantics

### `BLOCKED`

The challenge or evidence is malformed, tampered, mismatched, replayed against another challenge, incomplete, or outside the exact capability schema.

### `HOLD`

The packet is structurally valid but one or more required capability probes reported `FAIL`.

### `EVIDENCE_PACKET_VALID`

The packet is challenge-bound and structurally complete with all required capability probes reporting `PASS`.

Even in this state:

```yaml
registry_promotion_allowed: false
direct_runtime_verified: false
authority: UNCHANGED
authorization: UNCHANGED
execution: NONE
mutation: NONE
production_ready: false
```

The verdict explicitly requires separate direct invocation attestation plus semantic review before any durable runtime-profile promotion can be proposed.

## Replay and tamper resistance

The validator rejects:

- modified challenge payload with an old `challenge_id`;
- evidence for another runtime ID;
- evidence for another adapter version;
- evidence for another repository head;
- evidence from another nonce/challenge;
- missing or extra capability keys;
- malformed evidence digests;
- missing invocation provenance; and
- invalid boundary fields in the challenge bundle.

## Relationship to the runtime profile registry

The profile registry answers whether a runtime has already been durably accepted as verified enough to export a handoff profile.

The conformance evidence intake answers only whether one candidate proof packet is internally challenge-bound and schema-valid enough for later review.

Therefore:

```text
EVIDENCE_PACKET_VALID != VERIFIED runtime
EVIDENCE_PACKET_VALID != registry mutation
EVIDENCE_PACKET_VALID != authorization
EVIDENCE_PACKET_VALID != execution
EVIDENCE_PACKET_VALID != production readiness
```

No vendor template is promoted by this feature. `codex`, `claude-code`, and `openhands` remain declaration-only unless separate direct evidence is later performed and merged.

## Permanent boundaries

The tool is side-effect-free with respect to repositories/providers. It creates JSON challenge/verdict data only. It does not invoke a vendor runtime, edit the registry, mutate Git, push, deploy, access credentials, alter permissions, change databases, or perform destructive operations.

`production_ready = false` remains intentional.
