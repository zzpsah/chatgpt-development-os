# DevOS Execution Runtime Handoff v1

## Purpose

Connect the P12 executable controller to the existing bounded Execution Runtime without creating a second executor or turning Operational Intelligence into authority.

## Contract

```text
Operational Intelligence (advisory)
  -> Controller decision
  -> capability gate
  -> authorization gate
  -> Security Gate
  -> approved work-unit envelope
  -> existing Execution Runtime
  -> raw execution evidence
  -> verification/security result
  -> durable persistence
```

The controller can produce an `EXECUTION_CANDIDATE`, but a candidate is not execution. The handoff layer requires explicit gate results before the existing runtime may receive a work-unit envelope.

## Gate contract

1. **Capability** — required capability must be explicitly `AVAILABLE`.
2. **Authorization** — required authorization must be explicitly `APPROVED`; this layer never creates approval.
3. **Security Gate** — security-relevant work requires `PASS`; `BLOCKED`, `CONDITIONAL`, or `UNVERIFIED` does not become approval.
4. **Objective** — the work objective must be present and bounded.

Any failed gate returns `HOLD` and no runtime envelope.

## Evidence boundary

The handoff starts with an empty evidence list. Only the existing runtime/provider may append raw execution evidence such as exit status, test output, Git diff, file state, or an external response actually obtained. AI assertions are not execution evidence.

A runtime result without raw evidence is `FAILED` with `RAW_EXECUTION_EVIDENCE_REQUIRED`. The handoff layer never fabricates evidence or converts a missing result into success.

## Persistence boundary

After execution, the runtime result is returned for verification and durable state persistence. The handoff layer does not itself mutate project state, grant authorization, or bypass verification/security controls.

## Safety boundary

`APPROVED_FOR_RUNTIME` means only that the envelope passed the explicit handoff checks and may be delegated to the existing bounded runtime. It does **not** grant new authority. Higher-impact, destructive, production, credential-affecting, or sensitive-data operations remain subject to their operation-specific controls.

## v1 scope

Included:
- controller-candidate validation;
- independent capability/authorization/Security Gate checks;
- bounded work-unit envelope;
- raw-evidence requirement;
- runtime result boundary;
- deterministic executable tests.

Not included:
- a second executor;
- unrestricted command execution;
- automatic authorization;
- automatic deployment or publication;
- fabricated or inferred execution evidence.
