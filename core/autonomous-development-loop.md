# DevOS Autonomous Development Loop v1

The operational path is now explicit and bounded:

```text
User/project intent
  -> Operational Intelligence (ADVISORY_ONLY)
  -> independent Controller gates
  -> bounded Runtime Handoff
  -> single existing Executor/Runtime
  -> Host Capability Adapter
  -> raw execution evidence
  -> verification
  -> checkpoint/task outcome
  -> durable documentation
  -> next bounded work unit
```

## v1 execution boundary

The loop currently executes only `verification.run` work units through the reference verification adapter. Commands are explicit argv lists targeting an existing Python script inside the project root. Shell strings, inline execution, module execution, and out-of-root scripts are rejected.

The controller does not inherit authority from Operational Intelligence. The handoff does not grant authority. The runtime does not commit. Raw evidence must come from the host/provider execution result; an AI assertion is not evidence.

Authorization remains operation-specific. Security-relevant work requires an explicit `PASS` Security Gate result before handoff. Missing capability, missing authorization, failed security, missing objective, or failed verification stops the loop rather than being converted into success.

## Canonical bounded iteration contract

Every autonomous iteration follows the same explicit lifecycle:

1. **Objective** — identify the bounded work-unit objective and scope.
2. **State resolution** — recover repository/project state and classify evidence as `Observed`, `Likely`, or `Unknown`.
3. **Plan / orchestrate** — select the next bounded work unit and its dependencies without granting authority.
4. **Capability check** — classify the required capability as `AVAILABLE`, `DELEGATABLE`, or `MISSING`.
5. **Authorization check** — verify the operation-specific authorization boundary before handoff.
6. **Checkpoint** — record pre-action and post-action checkpoint signals.
7. **Execute once** — delegate only to the single existing bounded Runtime/Executor.
8. **Verify** — classify the result as `VERIFIED`, `PARTIAL`, `UNVERIFIED`, or `FAILED` using raw evidence.
9. **CONTINUE | STOP | ESCALATE** — choose the next state from evidence; do not convert uncertainty into success.
10. **Persist** — write the durable outcome before another iteration is eligible.

The loop has a **maximum iteration count** supplied by its scheduler/orchestrator. Reaching that bound stops the loop rather than silently extending execution.

`Production-impacting, destructive, irreversible, security-sensitive, or data-affecting` work is not implicitly authorized by autonomy. Such work requires the applicable explicit approval and security gates; when those gates are not satisfied the correct outcome is `ESCALATE` or `STOP`.

Autonomous continuation must **never blindly replay** a prior operation. A persisted completion is evidence of a past outcome, not future permission. **Do not automatically repeat destructive or irreversible operations.**

## Automation meaning

"Autonomous" means DevOS can carry a bounded approved work unit from recommendation through real execution and evidence capture without a human manually driving each internal step. It **does not provide unrestricted autonomous software development**. It does not mean unrestricted authority, arbitrary command execution, production deployment, destructive mutation, or a second executor.

The loop is intentionally one iteration at a time. A future scheduler/worker may invoke it repeatedly, but each iteration must re-enter the same gates and persist its outcome before continuing.

The loop remains **bounded, evidence-driven, checkpointed, and stoppable**. Each iteration has an explicit execution boundary, captures raw evidence, records checkpoint/outcome state, and stops on missing capability, authorization, security, objective, or verification conditions rather than bypassing a gate.

## Documentation boundary

**What is not written was never done.** Every material runtime capability and its durable project-state/documentation record must land in the same change set. Completion is **IMPLEMENTED + VERIFIED + DOCUMENTED**.
