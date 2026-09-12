# P12 Operational Intelligence — Recovery Integrity v2

P12 remains `ADVISORY_ONLY`: recovery validation never creates execution authority, authorization, replay permission, or deployment permission.

## Implemented

- Runtime persistence now fails closed when `latest` is neither an object nor null.
- Runtime history must be a list of object records and may not exceed the bounded `MAX_HISTORY` size.
- A non-null `latest` record requires history and must exactly match the final history record.
- Scheduler recovery converts these persistence validation failures into `HOLD` / `RECOVERY_STATE_INVALID` with no execution.
- Executable scheduler proof covers malformed latest records, malformed history records, orphaned latest records, and existing replay/iteration guards.

## Safety invariant

Malformed durable state is never interpreted as authority or a recoverable work instruction. Recovery classifies state only; fresh controller/runtime gates are required before continuation.
