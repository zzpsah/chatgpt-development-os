# P15 interpretation threat model

Primary risks are false referent resolution, silent scope broadening, loss of negative constraints, confidence being mistaken for evidence, and language being mistaken for authorization.

Controls:
- missing material referent => `CLARIFY`;
- explicit context only in the deterministic interpreter;
- negative constraints emitted structurally;
- confidence describes interpretation only;
- authorization always `UNCHANGED`;
- execution always `NONE`;
- downstream controller/Security Gate/runtime/verification remain independent.
