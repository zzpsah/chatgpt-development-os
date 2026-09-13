# Remote Permission Control Plane Index

Primary documents:
- `core/remote-resource-permission-governance.md`
- `core/multi-project-agent-context-isolation.md`
- `docs/DEVOS-MCP-PERMISSION-CONTROL-PLANE.md`

Implementation tools:
- `tools/devos-remote-permission-check.py`
- `tools/devos-mcp-governed-gateway.py`
- `tools/devos-governed-continuation.py`

Regression tools:
- `tools/test-devos-remote-permission-check.py`
- `tools/test-devos-mcp-governed-gateway.py`
- `tools/test-devos-governed-continuation.py`

CI:
- `.github/workflows/verify-mcp-permission-control-plane.yml`

All components are side-effect-free at this layer. Live provider mutations require separate explicit authorization and evidence.