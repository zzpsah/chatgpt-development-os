# Executable Development Runtime Workflow v1

## Purpose

Execute one authorized work unit at a time and return evidence to the Autonomous Development Loop.

## Flow

1. Receive an authorized work unit from Agent Orchestration.
2. Resolve required capabilities.
3. Confirm authorization and Security Gate requirements.
4. Create a pre-action checkpoint.
5. Execute the bounded action through a supported host/tool adapter.
6. Capture actual execution evidence.
7. Create a post-action checkpoint.
8. Run applicable verification.
9. Persist semantic outcome and generated state evidence.
10. Return the work-unit outcome to orchestration and the autonomous loop.

## Resume flow

On restart, load the latest valid checkpoint, compare repository/source state, re-check capability and authority, and determine whether the previous action completed. Never blindly replay an uncertain action.

## Outcome routing

```text
COMPLETE  -> verification -> persist -> next work unit
FAILED    -> preserve evidence -> safe recovery decision
BLOCKED   -> report missing prerequisite -> STOP/ESCALATE
CANCELLED -> persist reason -> STOP
```

## Guardrails

- The runtime executes only authorized scope.
- Capability absence is reported, not simulated.
- High-risk operations remain behind explicit approval.
- Verification evidence comes from actual checks.
- Checkpoints never become a source of authority.
- A runtime failure is not silently converted to project success.
