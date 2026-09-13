# DevOS MCP/App Integration — Repository Creation

## Purpose

This document describes how an AI host can expose DevOS `repository.create` through a custom MCP/App interface without making that AI host the semantic or authorization authority.

## Host-neutral model

```text
AI Host Adapter
  ↓
DevOS MCP/App Protocol
  ↓
DevOS Core / P15 / P16 / P17
  ↓
repository.create
  ↓
Provider Adapter
  ↓
Provider API
  ↓
Fresh Readback
  ↓
Universal Onboarding
```

The same DevOS semantics may be surfaced through ChatGPT, Claude, Gemini, Codex, or another compatible host. The host is replaceable; repository-local DevOS state remains authoritative.

## Tool

Preferred host tool name:

`devos.create_repository`

Example structured request:

```json
{
  "provider": "github",
  "owner": "example-owner",
  "repository": "example-project",
  "visibility": "private",
  "description": "Example project",
  "initialization_policy": "empty",
  "default_branch": "main",
  "project_identity": "example-project"
}
```

The request may not contain credentials, arbitrary prompt text, or undocumented provider options.

## Host behavior

The AI host should:

1. collect explicit structured target fields;
2. pass the request into DevOS governance;
3. discover provider capabilities;
4. surface `NEEDS_APPROVAL`, `BLOCKED`, `HOLD`, or capability-unavailable states exactly;
5. invoke a provider mutation only after DevOS eligibility and exact authorization exist;
6. never retry repository creation automatically;
7. obtain fresh provider readback before claiming `VERIFIED`;
8. hand the verified repository to universal onboarding.

The AI host must not convert conversational confidence into structured authorization.

## Current ChatGPT connector limitation

The GitHub connector available in the current ChatGPT environment does not expose a create-repository action. Therefore the built-in connector cannot honestly satisfy the live `github.repository.create` provider step.

For this integration, capability discovery must return the equivalent of:

```text
NEEDS_EXTERNAL_REPO_CREATION
```

until a custom MCP/App/provider adapter with an authorized create-repository operation is installed.

This limitation must not be hidden by simulating or claiming a live creation.

## Custom MCP/App requirement

A custom host integration needs two provider operations at minimum:

```text
<provider>.repository.create
<provider>.repository.inspect
```

The create operation performs exactly one bounded provider mutation. The inspect operation obtains fresh target state after the attempt.

Credentials remain inside the provider integration. They are never DevOS authorization and must never be returned to the model or written into `.ai/`, logs, tool results, or repository files.

## Status contract

Hosts should display the DevOS machine status directly:

- `READY`: eligible for the provider boundary, not executed;
- `NEEDS_APPROVAL`: exact DevOS authorization missing;
- `CAPABILITY_UNAVAILABLE`: required provider/readback capability absent;
- `NEEDS_EXTERNAL_REPO_CREATION`: selected integration cannot create repositories;
- `BLOCKED`: malformed/boundary-invalid request;
- `HOLD`: stale, conflicting, or uncertain state;
- `CREATION_ATTEMPTED`: one provider request occurred but completion is not yet verified;
- `VERIFIED`: fresh provider readback matched the exact requested target.

Do not map `CREATION_ATTEMPTED` to success.

## Evidence boundary

The deterministic command:

```bash
python tools/test-devos-mcp-repository-create.py
```

proves schema validation, authorization/capability separation, one-attempt/no-replay semantics, simulated provider-result handling, readback matching, secret rejection, and onboarding handoff semantics.

It does **not** prove live-provider creation. Live proof requires a real disposable sandbox repository request plus fresh provider readback under separate explicit authorization.

## Portability

The final durable project state must support:

```text
AI A / Account A / Host A
  → repository.create
  → onboard
  → persist repository-local DevOS state
  → AI B / Account B / Host B
  → bootstrap
  → recover
  → continue safely
```

No host-specific memory becomes authoritative.
