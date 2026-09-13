# MCP/App Permission Control Plane — Implementation

This unnumbered bounded change connects the existing host-neutral MCP/App boundary to the existing provider-independent remote-resource permission model.

## Control flow

```text
AI host
  ↓
MCP/App adapter
  ↓
P15 / P16 / P17
  ↓
Actionable Hold + Scoped Approval
  ↓
Remote Permission Control Plane
  ↓
Provider adapter
  ↓
Fresh readback
  ↓
Durable project evidence
```

## Capabilities governed

`repository.create`, `repository.delete`, `branch.create`, `branch.update`, `branch.force_update`, `branch.delete`.

Each capability has independent approval scope. Repository and project identity are part of the scope, so a prior approval cannot cross project boundaries.

## Token/API rule

Provider API tokens are technical capability only. They must remain inside the provider adapter and never become DevOS authority or be persisted into `.ai`, MCP requests, logs, evidence, or model output.

## Continuation rule

`continue` may reuse an existing approval only when project, workflow, capability, target, impact, freshness, and security conditions are unchanged. Otherwise the gateway returns an actionable HOLD.

## Evidence boundary

The gateway and regression tests are side-effect-free. They prove deterministic governance semantics and control-plane wiring. They do not perform live repository deletion, branch deletion, force updates, permission changes, or production operations.
