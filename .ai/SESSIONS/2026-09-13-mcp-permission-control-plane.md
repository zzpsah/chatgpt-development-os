# Session — 2026-09-13 — MCP/App Permission Control Plane

## Objective
Integrate the host-neutral MCP/App repository-creation boundary with a provider-independent remote-resource permission control plane, and make multi-project agent authorization isolation explicit.

## Architecture

```text
AI host
  ↓
MCP/App adapter
  ↓
P15 → P16 → P17
  ↓
Actionable Hold / Scoped Approval
  ↓
Remote Permission Control Plane
  ↓
Provider adapter
  ↓
Fresh readback
  ↓
Durable repository evidence
```

## Governed capabilities

`repository.create`, `repository.delete`, `branch.create`, `branch.update`, `branch.force_update`, `branch.delete`.

Each capability is distinct. Provider/API write permission is not DevOS authorization.

## Implementation

- `tools/devos-mcp-governed-gateway.py` — side-effect-free MCP control-plane gateway.
- `tools/devos-governed-continuation.py` — scoped-approval continuation bridge.
- `tools/test-devos-mcp-governed-gateway.py` — deterministic gateway regression corpus.
- `tools/test-devos-governed-continuation.py` — deterministic continuation integration corpus.
- `docs/DEVOS-MCP-PERMISSION-CONTROL-PLANE.md` — operational architecture and token/permission boundary.
- `.github/workflows/verify-mcp-permission-control-plane.yml` — dedicated CI gate.
- `core/remote-resource-permission-governance.md` — normative capability/authorization contract.

## Safety rules

- `FULL APPROVAL` is only full within explicit scope.
- `continue` may reuse valid scoped approval only while project, workflow, capability, target, impact, freshness, and security conditions remain valid.
- New/out-of-scope/high-impact actions require fresh approval and actionable HOLD.
- Repository approvals cannot be reused for another repository.
- Branch deletion is not implied by repository deletion or branch creation approval.
- Force update requires distinct capability/approval.
- Provider credentials remain provider integration material only.
- Uncertain mutation requires HOLD/reconciliation and no blind replay.

## Evidence boundary

The implementation is side-effect-free and intended for deterministic/integrated verification. It does not prove live-provider mutation, production mutation, repository deletion, branch deletion, force update, permission mutation, or credential mutation.

## Next verification

Run the dedicated control-plane regression, Contracts, Trust-First, and Full DevOS against the exact final PR head. Only after exact-head evidence is green should the PR be considered verified.
