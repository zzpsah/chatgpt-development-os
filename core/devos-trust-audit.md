# DevOS Trust-First Audit v1

## Purpose

The Trust-First Audit is a deterministic, read-only way to distinguish what a DevOS source tree or audit pack can actually prove from what documentation merely claims.

It exists to close the failure mode discovered by independent review where an audit ZIP omitted dependencies required by checks it advertised.

## Core distinction

```text
NOT INCLUDED IN AUDIT PACK
        !=
NOT PRESENT IN DEVOS
```

A missing dependency in a supplied source pack is `UNKNOWN / PACK_INCOMPLETE` until the canonical repository is inspected. It is not an implementation defect by itself.

## Command

```bash
python tools/devos-audit.py
```

The command is read-only with respect to the audited repository.

It may execute explicitly declared deterministic tests/checks. Those checks must not grant authorization, execute project work, or perform live provider mutations.

Use:

```bash
python tools/devos-audit.py --manifest
```

to print the dependency-closed path manifest required for all v1 advertised checks.

Use:

```bash
python tools/devos-audit.py --root <unpacked-pack> --no-run-checks
```

to validate whether a supplied pack contains the complete v1 dependency set without executing checks.

## v1 audited checks

- bootstrap / canonical identity;
- P16 planning regression;
- P17 readiness regression;
- Security Gate repository contract;
- cross-layer adversarial Security Gate/authorization boundary corpus;
- controlled remote mutation provider-simulated regression.

The manifest also requires the principal status/documentation surfaces needed for independent review.

## Result semantics

- `PASS` — the declared check ran successfully or, in no-run mode, its dependency closure is present.
- `FAIL` — the declared executable check ran and failed.
- `UNKNOWN` — the advertised check cannot be evaluated because the supplied source is incomplete or required external evidence is unavailable.
- `BLOCKED` — canonical identity is contradicted or another fail-closed trust boundary prevents the audit from treating the source as DevOS.

Evidence labels include:

- `OBSERVED` — structure/dependencies were inspected but not executed;
- `VERIFIED` — the declared deterministic check executed and its result was observed;
- `PACK_INCOMPLETE` — source-pack packaging prevents execution;
- `BLOCKED` — a trust boundary failed.

The audit intentionally does not convert documentation claims into verification.

## Non-goals

The audit is not:

- authorization;
- execution authority;
- mutation authority;
- an auto-repair command;
- production-readiness certification;
- live-provider mutation proof;
- a substitute for current CI or Git/provider evidence.

## Security invariants

The audit preserves:

- `PLAN != EXECUTION`;
- `READY != EXECUTION`;
- `INTERPRETATION != AUTHORIZATION`;
- `OLD APPROVAL != NEW APPROVAL`;
- `SIMULATED EVIDENCE != LIVE PROVIDER PROOF`;
- `CHAT MEMORY != SOURCE OF TRUTH`;
- `VERIFICATION != ASSERTION`;
- `PROVIDER RESPONSE != COMPLETION PROOF`;
- `RECOVERY != AUTOMATIC MUTATION REPLAY`.

## Dependency-closure rule

Every check advertised by the v1 audit has an explicit entry point and dependency list in `tools/devos-audit.py`.

The audit-pack manifest is the union of those dependencies plus the principal documentation/status surfaces. A packaging mechanism may copy/archive that manifest, but the read-only audit command itself does not write a ZIP or modify the audited tree.

If a new advertised check is added, its execution dependencies and reproducibility regression must be added in the same bounded change.

## P16/P17 impact integrity

P17 must revalidate the declared compiled-step impact using the same deterministic P16 classifier before readiness can become `READY`.

A compiled envelope that relabels a destructive/security-sensitive objective as lower impact is invalid and must be `BLOCKED` before authorization/Security Gate evaluation can be bypassed.

This is defense in depth. Planning remains non-authorizing and readiness remains non-executing.
