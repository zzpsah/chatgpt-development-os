# P12 Recovery Integrity v2

Recovery state is trusted only when the durable record has a coherent shape. The persisted `latest` record must be an object, and when history is present it must contain object records with the final history entry matching `latest`. Corrupt or inconsistent durable state fails closed through the scheduler as `HOLD` / `RECOVERY_STATE_INVALID`; it never authorizes replay or execution.
