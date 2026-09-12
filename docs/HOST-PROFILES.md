# Portable AI Host Profiles v1

DevOS works with any AI host that can honestly describe how it meets or delegates the portable adapter contract. `DEVOS-HOST-PROFILE-v1` is an optional machine-readable declaration; it is not project memory, authorization, execution evidence, or a permission grant.

## Profile format

Copy [`adapters/host-profile.example.json`](../adapters/host-profile.example.json), set a neutral host identifier, and declare every required capability as exactly one of:

- `AVAILABLE` — the host can perform the bounded capability.
- `DELEGATABLE` — the host needs an explicitly supported handoff.
- `MISSING` — the host cannot perform it and must report that fact.

The required capabilities are `project_discovery`, `bootstrap`, `inspection`, `intent_routing`, `state_resolution`, `execution`, `verification`, and `persistence`.

Validate a profile with:

```text
python tools/verify-host-profile.py path/to/host-profile.json
```

## Boundary

The profile never upgrades a missing capability, grants authorization, bypasses a Security Gate, or turns an AI statement into execution evidence. A project still recovers from `AGENTS.md`, `.ai/`, source, and Git; profile data describes only the current host's honest capability boundary.
