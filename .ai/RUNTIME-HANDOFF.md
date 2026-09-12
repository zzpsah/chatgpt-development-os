# Controller → Execution Runtime Handoff v1

## Purpose

Bridge the P12 executable controller decision envelope into the existing Executable Development Runtime without allowing Operational Intelligence to become execution authority.

## Contract

A handoff is eligible only when the controller returns `EXECUTION_CANDIDATE` and independently confirms capability, authorization, and Security Gate conditions. The handoff creates a bounded runtime work-unit envelope; it does not execute the work.

The runtime remains responsible for pre-action checkpointing, bounded execution, raw evidence capture, post-action checkpointing, verification, persistence, and the final outcome. An AI decision is never execution evidence.

## Boundary

```text
OI (ADVISORY_ONLY)
  -> Controller
  -> capability gate
  -> authorization gate
  -> security gate
  -> runtime work-unit envelope
  -> existing execution runtime
```

No step in the handoff grants authorization, expands scope, fabricates evidence, or claims execution before the runtime actually performs the work.

## Completion standard

A runtime action is complete only when it is **IMPLEMENTED + VERIFIED + DOCUMENTED** and the runtime has captured factual execution evidence. A blocked or failed handoff remains blocked or failed; it is never converted into success by the controller.
