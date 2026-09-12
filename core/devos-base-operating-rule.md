# DevOS Base Operating Rule — Diagnose, Repair, Dry-Test, Document

## Status
Normative P12+ operating rule.

## Rule
When DevOS encounters **any configuration, dependency, tool, connector, API, CI, repository, runtime, or execution error** while working on a project, the error becomes part of the current work objective until it is resolved or safely proven to require an external authorization unavailable to DevOS.

DevOS must:

1. **Detect** the failure explicitly; never silently continue as if the operation succeeded.
2. **Classify** the failure (configuration, connection, authentication/authorization, dependency, repository/Git, runtime, test/verification, or unknown).
3. **Trace root cause** using available evidence: exact error, failing operation, boundary, recent change, and reproducible condition.
4. **Repair safely** within the existing authorization boundary. Do not bypass security or permissions to make a test pass.
5. **Dry-test first** after repair using the smallest deterministic check that proves the affected boundary works.
6. **Verify end-to-end** when the dry test passes, including regression checks for affected behavior.
7. **Document the failure → root cause → repair → dry test → verification flow** in the repository.
8. **Persist the current state before continuing** so a fresh AI can recover the same reasoning and evidence.

A connection failure must not be treated merely as “network error”. The diagnostic path must identify the failing layer where evidence permits: local configuration, DNS/network reachability, TLS, credentials, API endpoint, permission, rate limit, provider outage, repository state, or tool/connector boundary. If evidence is insufficient, the system must report `ROOT_CAUSE_UNCONFIRMED` and keep the work gated rather than inventing a cause.

## Self-application
This rule applies to **implementation of the rule itself** and to every issue encountered while implementing it. A failure caused by a DevOS tool, connector, configuration, or intermediate change is itself a first-class defect to diagnose, repair, dry-test, verify, and document before declaring the rule complete.

## Project flow diagram
```text
Human Goal / Command
        |
        v
Interpret + Recover Context
        |
        v
Plan bounded work
        |
        v
Preflight / Configuration / Connection checks
        |
   +----+----+
   |         |
 PASS      ERROR
   |         |
   v         v
Execute   Detect + Classify
   |         |
   v         v
Verify   Root-cause evidence
   |         |
   |         v
   |      Safe repair
   |         |
   |         v
   |      Dry test
   |         |
   |    +----+----+
   |    |         |
   |  PASS       FAIL
   |    |         |
   |    v         v
   |  Verify   Repeat diagnosis
   |    |       within bounds
   +----+---------+
        |
        v
Persist evidence + state
        |
        v
Document flow + result
        |
        v
Select next bounded objective
```

## Connection diagnostic contract
Every connection-dependent operation should expose enough evidence for a deterministic health check. At minimum record:
- dependency/provider and endpoint identity (without secrets)
- configuration presence/shape (never secret values)
- reachability result
- authentication/authorization result when testable
- response/status or connector error class
- timestamp/duration
- remediation attempted
- dry-test result
- root-cause confidence

Secrets, tokens, cookies, and private credentials must never be persisted as evidence.

## Completion gate
The affected work is not complete until:

`IMPLEMENTED + ROOT_CAUSE_DETERMINED_OR_EXPLICITLY_UNCONFIRMED + DRY_TEST_PASS + VERIFIED + DOCUMENTED`

For an unresolved external dependency or authorization boundary, the correct terminal state is a documented `BLOCKED`/`HOLD` with evidence and next action; never a fabricated success.
