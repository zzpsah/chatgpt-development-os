# MCP/App Permission Control Plane — Implementation Checkpoint

## Status

Implemented on branch `feat/remote-permission-governance-v2` as an unnumbered bounded objective.

## What is integrated

- Existing host-neutral `devos.create_repository` MCP/App boundary remains provider-nonexecuting.
- Remote-resource permission evaluator governs repository and branch mutations as distinct capabilities.
- `tools/devos-mcp-governed-gateway.py` provides the control-plane gateway that must approve a remote operation before provider handoff.
- `tools/devos-governed-continuation.py` provides continuation decisions that reuse only valid, scoped approvals.
- Multi-project/project-approval isolation is enforced by exact project/repository checks.
- Actionable HOLD information includes reason, consequence, impact, required approval and safe options.
- Provider credentials are not accepted by these control-plane interfaces.

## Required invariants

`PROVIDER CREDENTIAL != DEVOS AUTHORIZATION`

`FULL APPROVAL != BLANKET PERMISSION`

`CONTINUE != BLANKET AUTHORIZATION`

`REPOSITORY DELETE != REPOSITORY CREATE`

`BRANCH DELETE != BRANCH CREATE`

`NORMAL BRANCH UPDATE != FORCE UPDATE`

`UNCERTAIN MUTATION != AUTOMATIC RETRY`

## Evidence boundary

The control-plane implementation and tests are side-effect-free. They establish deterministic and integration semantics only. They do not prove a live provider delete, branch delete, force update, permission mutation, or production mutation.

## Final verification requirement

The branch must receive fresh exact-head CI for:

- remote permission regression;
- governed continuation;
- MCP governed gateway;
- Contracts;
- Trust-First Audit;
- Full DevOS.

Only after all applicable exact-head checks pass should this checkpoint be considered VERIFIED.
