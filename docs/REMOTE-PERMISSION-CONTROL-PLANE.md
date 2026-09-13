# DevOS Remote Permission Control Plane

This unnumbered bounded objective connects the existing host-neutral MCP/App boundary to provider-independent remote permission governance and multi-project agent isolation.

Governed path: AI host → MCP/App adapter → P15 → P16 → P17 → Actionable Hold/Scoped Approval → remote permission control plane → provider adapter → fresh readback → durable evidence.

Governed capabilities: repository.create, repository.delete, branch.create, branch.update, branch.force_update, branch.delete.

Provider credentials/API tokens are technical capabilities only. They are never DevOS authorization and are never persisted in `.ai`, passed as MCP arguments, logged, or returned to the model.

FULL APPROVAL is full only within its explicit project/repository/workflow/capability/target/impact/freshness/security scope. `continue` cannot broaden that scope.

Project and approval isolation is mandatory: Project A state != Project B state; Project A approval != Project B approval.

The control plane is side-effect-free in this implementation. It authorizes provider handoff only; it does not itself perform a remote mutation. Uncertain operations must HOLD and reconcile rather than blindly retry.

Deterministic/integration verification does not establish live-provider or production proof.