# DevOS MCP / App Repository Creation Contract v1

## Scope

Expose the existing provider-independent DevOS capability `repository.create` through AI hosts that support MCP/App-style tools without making any host, vendor, model, account, chat, or connector authoritative.

The tool surface is:

`devos.create_repository`

The host adapter is an interface only. DevOS semantics, authorization, readiness, execution boundaries, verification, recovery, and durable state remain repository-governed.

## Architecture

```text
Human
  ↓
AI host (ChatGPT / Claude / Gemini / Codex / other)
  ↓
DevOS MCP/App host adapter
  ↓
DevOS semantic/governance layer
  ↓
P15 → P16 → P17
  ↓
repository.create
  ↓
provider adapter (github.repository.create / future provider)
  ↓
provider API
  ↓
fresh provider readback
  ↓
universal onboarding
```

Host-specific logic must not move into DevOS core.

## Structured request

Allowed request fields are exactly:

- `provider`
- `owner`
- `repository`
- `visibility`
- `description`
- `initialization_policy`
- `default_branch`
- `project_identity`

Unknown or hidden fields are rejected. Credential-like fields are forbidden. Free-form prompt text is not a provider parameter.

## Structured statuses

The adapter may emit:

- `READY`
- `NEEDS_APPROVAL`
- `CAPABILITY_UNAVAILABLE`
- `NEEDS_EXTERNAL_REPO_CREATION`
- `BLOCKED`
- `HOLD`
- `CREATION_ATTEMPTED`
- `VERIFIED`

`SUCCESS` is intentionally not a completion state.

## Authorization and capability separation

```text
provider capability != DevOS authorization
user intent != DevOS authorization
P17 READY != execution
provider credential != DevOS authorization
provider response != completion proof
```

Repository creation is a high-impact remote mutation. Exact authorization must bind:

- `repository.create`
- provider
- owner/namespace
- repository name
- project identity

A prior approval, prior successful creation, provider write access, configured credentials, or a plan saying READY cannot satisfy this requirement.

## Provider adapter boundary

A provider adapter may implement an operation equivalent to:

`create_repository(request)`

and a fresh inspection operation equivalent to:

`inspect_repository(target)`

The provider adapter is responsible only for provider communication. It must not decide authorization, P17 readiness, production readiness, or whether a higher-impact operation is allowed.

The MCP/App adapter does not directly contact the provider. It consumes provider capability, one-attempt result, and fresh readback evidence supplied through the provider boundary.

## Capability unavailable

If the selected integration lacks `<provider>.repository.create`, return:

`NEEDS_EXTERNAL_REPO_CREATION`

No live action may be implied. This is the expected result for a ChatGPT connector that exposes repository inspection/normal repository writes but no create-repository action.

If create exists but fresh repository inspection is unavailable, return `CAPABILITY_UNAVAILABLE` before mutation because the operation cannot satisfy post-create verification.

## Exactly-once / no blind replay

One governed repository-creation operation permits at most one mutation request.

After timeout, connection loss, ambiguous response, or unknown completion state:

```text
HOLD
  ↓
reconcile/read
  ↓
fresh evidence
  ↓
no automatic second create request
```

A new mutation requires a new governed operation and fresh authorization.

## Verification

A provider create response is attempt evidence only.

`VERIFIED` requires fresh provider readback matching:

- provider
- owner/namespace
- repository name
- existence
- requested visibility when observable
- intended default branch when observable

Any target/visibility/branch mismatch becomes `HOLD`.

After `VERIFIED`, the adapter may emit an onboarding handoff to the existing `universal.onboard` capability. Repository creation must not silently add unrelated application code.

## Evidence levels

Keep these distinct:

- `CONTRACT_VERIFIED`
- `COMPONENT_TEST_VERIFIED`
- `INTEGRATED_VERIFIED`
- `PROVIDER_SIMULATED_VERIFIED`
- `LIVE_SANDBOX_VERIFIED`
- `PRODUCTION_VERIFIED`

The reference MCP/App acceptance corpus supplies deterministic/provider-simulated semantic evidence only. It does not prove a live provider request.

## Safety invariants

```text
PLAN != EXECUTION
READY != EXECUTION
INTERPRETATION != AUTHORIZATION
OLD APPROVAL != NEW APPROVAL
CHAT MEMORY != SOURCE OF TRUTH
PROVIDER CREDENTIAL != DEVOS AUTHORIZATION
PROVIDER RESPONSE != COMPLETION PROOF
SIMULATED EVIDENCE != LIVE PROVIDER PROOF
RECOVERY != AUTOMATIC MUTATION REPLAY
```

## Universal portability invariant

```text
AI A + Account A
  → governed repository.create
  → verified target
  → universal onboarding
  → repository-local DevOS state
  → AI B + Account B
  → bootstrap
  → recover
  → continue safely
```

No private AI memory is required.
