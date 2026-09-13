# DevOS Remote Permission + MCP Control Plane

The MCP/App adapter is an AI-host interface only. Remote provider/API write permissions are technical capability, not DevOS authorization.

Governed path:

`AI host → MCP/App adapter → P15 → P16 → P17 → Actionable Hold/Scoped Approval → remote permission control plane → provider adapter → fresh readback → durable evidence`

Capabilities are independently scoped:
`repository.create`, `repository.delete`, `branch.create`, `branch.update`, `branch.force_update`, `branch.delete`.

Approval binds exact provider/project/repository/resource/workflow/capability/impact/freshness as applicable. `FULL APPROVAL` is full only within that scope. `continue` can reuse approval only while those conditions remain valid.

Multi-project isolation:
`Project A state != Project B state`
`Project A approval != Project B approval`

Provider tokens stay inside provider adapters and are never copied into MCP arguments, `.ai`, logs, evidence, or model output.

The control plane is side-effect-free in this implementation. Uncertain provider operations require HOLD/reconciliation and never blind replay. Deterministic/integration evidence does not become live-provider or production proof.
