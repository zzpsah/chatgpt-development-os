# DevOS Multi-Project Agent Context Isolation v1

## Purpose

DevOS is a long-lived agent system that may operate multiple projects/repositories in the same AI account, process, or session. Project state, approvals, credentials/provider bindings, workflows, and evidence must remain isolated.

## Isolation rules

```text
PROJECT A state != PROJECT B state
PROJECT A approval != PROJECT B approval
PROJECT A workflow != PROJECT B workflow
PROJECT A provider binding != PROJECT B provider binding
PROJECT A evidence != PROJECT B evidence
```

An approval or continuation packet from one project cannot authorize work in another project.

## Context selection

Before a mutation-capable operation, DevOS must resolve:

- project identity;
- repository identity;
- provider/owner;
- workflow identity;
- target branch/resource;
- current repository state.

If more than one candidate matches and the target is not uniquely established, DevOS must HOLD rather than guess.

## Approval reuse

A recovered approval may be reused only when its exact project, repository, workflow, capability, target, impact ceiling, freshness, and security conditions still match the current operation.

Changing project/repository/branch/capability/impact/freshness/security scope requires fresh approval.

## Durable agent continuity

The authoritative continuity chain is:

`repository + Git + durable .ai state → fresh AI bootstrap → project/workflow recovery → current eligibility → safe continuation`

Private model memory, account context, or chat history cannot replace repository-local evidence.

## Credential separation

Provider credentials are bound to the provider/project integration and are never copied into another project's state, approval record, MCP request, logs, or model output.

## Safety

This contract does not itself execute a provider mutation. It defines the isolation boundary consumed by P15/P17/controller and the MCP/App permission control plane.
