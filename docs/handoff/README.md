# DevOS AI handoff index

**Stable entry point for any AI reviewing DevOS history or resuming after context loss.**

1. Start with the repository [AGENTS.md](../../AGENTS.md) and [manifest](../../.ai/manifest.yaml).
   For a fresh external AI chat, use the plain [Project Context Guide](../../DEVOS-PROJECT-CONTEXT.md) before this deeper handoff.
2. Recover [current state](../../.ai/CURRENT-STATE.md), [tasks](../../.ai/TASKS.md), and [decisions](../../.ai/DECISIONS.md), then inspect current source and Git.
3. Read the [master handoff](DevOS-Master-Handoff.md) for scratch-to-current history, P0–P17 naming caveats, architecture, PR/CI evidence, proof boundaries, limitations, independent review checklist and roadmap choices.
4. Read the [Master Engineering Map](../DEVOS-MASTER-ENGINEERING-MAP.md) for the product objective, completed architecture, future flow diagrams, semantic model, any-AI/any-platform target, human-language interpreter evolution model, and living-documentation contract.
5. Read the [Interpreter Experiment Ledger](../DEVOS-INTERPRETER-EXPERIMENT-LEDGER.md) when changing P15 behavior. Experiments must remain repository-recorded and authority-neutral.
6. Consult the [evidence snapshot](DevOS-Evidence-Snapshot.json) for source hashes, PR/CI records and local checks. It is historical metadata, not the planned machine-checkable production-readiness gate.
7. Optionally use the [verification helper](verify_devos_snapshot.py) in a disposable clone after reviewing the scripts it runs.

## Snapshot and authority

For the maintained capability ledger and its verifier, see [Production-readiness evidence](../PRODUCTION-READINESS-EVIDENCE.md). This is distinct from the dated handoff archive below. Check `.ai/CURRENT-STATE.md` for gate closure status.

The current handoff documents main at `70c8e0e050660fd6b606150a1370d8fce51e373e` (2026-09-13). Subsequent publication commits are not included in that evidence snapshot. Always compare against current HEAD; historical successful CI must not be represented as verification of a later commit.

Source + Git and explicit current requirements remain authoritative. This index, the handoff, generated metadata and previous approvals never grant execution permission. Live runtime remote mutation remains unproven by this snapshot. The Production-Readiness Evidence Matrix & Limitations gate remains active.

## Maintenance

Keep this directory path stable. When preparing a fresh handoff, update the snapshot SHA/date, evidence records, conclusions and source links together. Do not silently relabel historical runs as current, discard uncertainty labels, or mark a maturity gate closed merely because documentation was published. Preserve relevant session provenance under `.ai/SESSIONS/`.
