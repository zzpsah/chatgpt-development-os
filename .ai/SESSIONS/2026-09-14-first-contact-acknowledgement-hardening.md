# First-contact acknowledgement hardening

## What changed

The plain first-contact guide no longer calls its recovery signal an activation handshake or asks a host to state `DEVOS MODE: ACTIVE`.

It now uses the neutral phrases `DevOS context recovered` and `DevOS context not verified`.

## Why

The guide is intended for fresh AI hosts. Mode/activation packaging can be misread as a request to change host behavior even though DevOS does not have that authority. The replacement keeps the recovery-status signal while making its scope explicit.

## Verification

- `python tools/test-devos-project-context.py`
- `python tools/test-devos-bootstrap.py`
- `python tools/test-devos-audit.py`
- `python tools/verify-documentation-integrity.py`

## Boundaries

This is a repository-documentation and deterministic-guardrail change only. It does not run a GitHub workflow, access credentials, create authorization, or prove live-provider capability.
