# Session — Isolated Managed-Repository Write Proof v1

This bounded objective proves a one-file update only in a newly created local Git fixture. It requires the read-only preflight and exact derived approval, validates runtime diff/test/readback evidence, and writes the evidence packet outside the fixture. It never commits, pushes, calls a provider, or affects a real managed repository.

Pending exact-head CI and durable closure.
