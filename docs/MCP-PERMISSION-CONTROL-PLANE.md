# DevOS MCP/App Permission Control Plane

DevOS is a long-lived, provider-neutral Development OS. MCP/App is a host interface, not an authority layer.

## Governed path

`AI host → MCP/App adapter → P15 → P16 → P17 → Actionable Hold/Scoped Approval → remote permission control plane → provider adapter → fresh readback → durable repository evidence`

## Remote capabilities

- `repository.create` — HIGH
- `repository.delete` — DESTRUCTIVE
- `branch.create` — LOW by default; higher for protected/default/release/production targets
- `branch.update` — HIGH for canonical/protected/release/production refs
- `branch.force_update` — DESTRUCTIVE
- `branch.delete` — DESTRUCTIVE

Provider/API write permission is technical capability only. It never becomes DevOS authorization.

## Exact approval scope

Authorization binds provider, project identity, owner/namespace, repository, branch/resource, capability, workflow, impact ceiling, freshness/state anchor, and authorization provenance as applicable.

`FULL APPROVAL` is full only within the represented scope. `continue` may reuse it only while all relevant scope/freshness/security conditions remain valid.

## Multi-project isolation

`Project A state != Project B state`

`Project A approval != Project B approval`

`Project A provider binding != Project B provider binding`

An approval from one repository can never authorize another repository.

## Token/API boundary

Provider tokens/credentials stay inside the provider adapter. They are never passed as MCP arguments, written to `.ai`, logs, evidence, or model output.

Provider-specific permissions are adapter concerns and must be minimized and verified against current provider APIs before live activation.

## Actionable holds

When a remote operation is blocked, DevOS exposes status, reason, next action, consequence/impact, required approval/evidence, valid safe alternatives, and natural-language examples.

## Uncertain mutations

A timeout, connection loss, or ambiguous mutation result causes `HOLD → reconcile/read → determine state`. Automatic blind replay is forbidden.

## Evidence boundary

The control plane is initially established by deterministic/integration tests. This does not prove live-provider destructive operations or production readiness. Live sandbox proof must be separately authorized and must include fresh provider readback.
