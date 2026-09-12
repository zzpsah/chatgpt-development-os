# P12 Recovery Integrity v2

Recovery state is trusted only when the durable record has a coherent shape. The persisted `latest` record must be an object or null; history must be a bounded list of object records; and when a latest record exists, the final history entry must match it. Corrupt or inconsistent durable state fails closed through the scheduler as `HOLD` / `RECOVERY_STATE_INVALID`; it never authorizes replay or execution.
