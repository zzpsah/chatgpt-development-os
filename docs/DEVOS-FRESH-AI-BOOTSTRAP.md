# DevOS Fresh-AI Bootstrap

## Purpose

A new AI/tool should be able to enter this repository, recover project context, and continue development without requiring the original ChatGPT account, conversation, or vendor memory.

## Canonical sequence

1. **RECOVER** — read `AGENTS.md`, `.ai/manifest.yaml`, and the durable `.ai` context.
2. **RESOLVE** — establish current state, remaining tasks, decisions, architecture, and Git/source reality.
3. **VERIFY** — use source, tests, Git, CI, runtime, and security evidence; do not treat AI assertions as execution evidence.
4. **CONTINUE** — perform only work permitted by the repository's authorization and security contracts.
5. **PERSIST** — record material implementation/state changes in the same change set.
6. **HANDOFF** — leave enough durable context and evidence for the next tool to recover the work.

## Bootstrap inspector

Run:

```text
python tools/devos-bootstrap.py
```

The inspector is deliberately non-executing. It checks required/recommended durable context and reports Git identity, readiness, authority, execution, and authorization state. It does not perform project mutations.

The deterministic proof is:

```text
python tools/test-devos-bootstrap.py
```

The proof runs the inspector twice and requires identical repository-derived output, complete required context, `execution == NONE`, and `authorization == UNCHANGED`.

## Authority

Repository source and Git are authoritative for implementation. `.ai` is the durable project-context layer. Chat history and AI-account memory are supplementary only.

## Documentation boundary

**What is not written was never done.** Material changes must be implemented, verified, and documented together. Portable memory itself does not authorize execution, mutation, deployment, publication, or security bypass.
