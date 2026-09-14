# Isolated Managed-Repository Write Proof v1

`DEVOS-ISOLATED-MANAGED-WRITE-PROOF-v1` proves one real file update only in a newly created local Git fixture. It consumes a successful Managed-Repository Delivery v1 read-only preflight and requires an exact scoped approval derived from that preflight.

Flow: P15 → P16 → P17 → read-only preflight/HOLD → exact approval → runtime handoff → one `managed-marker.txt` update → fixture test → diff/readback → external evidence packet.

The fixture is newly created and identified by a non-secret marker. Existing repositories are rejected. The sole permitted change is the fixture marker changing from `before` to `after`; missing/mismatched approval holds before the write. Evidence must be outside the fixture.

This proof does not commit, push, contact a provider, deploy, change production, credentials, secrets, databases, permissions, or delete anything. `production_ready = false`.
