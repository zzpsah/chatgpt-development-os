# DevOS MCP/App Permission Control Plane

## Purpose

DevOS is a long-lived Development OS for AI across vendors, models, accounts, coding agents, sessions, machines, and Git providers. MCP/App is a host interface, not an authority layer.

The governed architecture is:

```text
AI Host
(ChatGPT / Claude / Gemini / other)
        ↓
MCP/App adapter
        ↓
DevOS P15 → P16 → P17
        ↓
Actionable Hold / Scoped Approval
        ↓
Remote Permission Control Plane
        ↓
Provider Adapter
        ↓
Provider API
        ↓
Fresh Readback
        ↓
Durable repository evidence
```

## Permission layers

```text
Provider credential/API token
  = technical capability

DevOS capability
  = supported operation

DevOS authorization
  = explicit permission for exact operation and scope

P17 readiness
  = current eligibility

Execution
  = bounded provider/local action

Verification
  = observed post-action state
```

These layers are never interchangeable.

## Governed remote capabilities

- `repository.create` — HIGH
- `repository.delete` — DESTRUCTIVE
- `branch.create` — LOW by default, higher for protected/default/production targets
- `branch.update` — HIGH for canonical/protected/release/production refs
- `branch.force_update` — DESTRUCTIVE
- `branch.delete` — DESTRUCTIVE

Normal file operations and PR merge remain separately governed capabilities.

## Exact approval scope

The approval envelope binds, where applicable:

- provider;
- owner/namespace;
- repository;
- branch/ref/resource;
- capability;
- workflow;
- project identity;
- impact ceiling;
- freshness/state anchor;
- authorization identifier/provenance.

`FULL APPROVAL` means full approval **within the represented scope**. It is never blanket access.

Therefore:

```text
repo A approval != repo B approval
repo A state    != repo B state
branch.create   != branch.delete
branch.update   != branch.force_update
repository.create != repository.delete
```

## Continue behavior

`continue` resumes a currently valid bounded workflow only when the next operation remains inside the existing authorization envelope.

Otherwise DevOS returns an actionable HOLD rather than repeatedly asking for approval without context.

A HOLD should provide:

- status;
- exact reason;
- next action;
- what will happen;
- impact/consequence;
- exact approval/evidence required;
- safe alternatives;
- natural-language wording the user can use next.

## Provider permissions / API token requirements

A provider adapter may require API permissions or tokens to perform a capability. Those credentials are stored and used only inside the provider integration.

They must never be:

- copied into `.ai/`;
- included in MCP tool arguments;
- exposed in model output;
- written to logs;
- treated as DevOS authorization.

The provider permission set should be the minimum needed for the capabilities actually enabled.

Example capability mapping for GitHub-style integrations:

| DevOS capability | Typical provider/API capability | DevOS risk |
|---|---|---|
| `repository.create` | repository administration/create permission | HIGH |
| `repository.delete` | repository administration/delete permission | DESTRUCTIVE |
| `branch.create` | repository contents/ref write | LOW/HIGH by target |
| `branch.update` | ref update/write | HIGH |
| `branch.force_update` | force ref update | DESTRUCTIVE |
| `branch.delete` | ref delete | DESTRUCTIVE |

The exact provider permission names are adapter-specific and must be verified against current provider APIs before activation.

## Exactly-once mutation boundary

The permission plane authorizes a bounded operation; it does not authorize blind retries.

```text
provider request sent
        ↓
response uncertain
        ↓
HOLD
        ↓
fresh read/reconcile
        ↓
actual state known?
  ├─ yes → verify outcome
  └─ no  → remain HOLD
```

A timeout or connection loss never grants a second mutation request automatically.

## MCP/App boundary

The MCP/App adapter may expose structured tools such as:

`devos.create_repository`

but it must route mutation eligibility through the DevOS control plane.

```text
MCP tool availability
        !=
provider capability
        !=
DevOS authorization
        !=
P17 readiness
        !=
execution
```

The current built-in ChatGPT GitHub connector has no repository-create action; DevOS therefore uses `NEEDS_EXTERNAL_REPO_CREATION` when that host/provider boundary is selected.

## Multi-project isolation

A single AI may operate multiple repositories concurrently, but authorization and context are project-scoped:

```text
Project A
├─ state
├─ workflow
├─ approvals
├─ evidence
└─ credentials/provider binding

Project B
├─ state
├─ workflow
├─ approvals
├─ evidence
└─ credentials/provider binding
```

An approval from Project A must never be used for Project B.

## Evidence

The control plane is initially verified through deterministic/provider-simulated regression. It does not imply live-provider or production proof.

Live-provider proof requires a separately authorized disposable sandbox operation with fresh provider readback and exact recorded evidence.
