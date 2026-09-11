# Host Adapter v1

This adapter profile describes the minimum host-facing capabilities expected by the Executable Development Runtime.

## Capability discovery

A compatible host should expose whether each capability is `AVAILABLE`, `DELEGATABLE`, or `MISSING` before execution begins.

Minimum v1 capabilities:

| Capability | Purpose | Default risk |
|---|---|---|
| `filesystem.read` | inspect project files | LOW |
| `filesystem.write_scoped` | modify explicitly authorized files | MEDIUM |
| `git.inspect` | status, diff, log, HEAD | LOW |
| `git.commit` | create a commit | MEDIUM |
| `verification.run` | run configured project checks | MEDIUM |
| `github.inspect` | inspect repository/CI evidence | LOW |
| `github.mutate` | change remote GitHub state | HIGH |

A host may expose additional capabilities, but additional capabilities do not weaken the core runtime or security contracts.

## Operation lifecycle

```text
Discover capability
      ↓
Validate target + scope
      ↓
Check authorization
      ↓
Execute bounded operation
      ↓
Capture actual result
      ↓
Return normalized evidence
```

## Filesystem rules

`filesystem.write_scoped` must identify the target path and intended scope before mutation. It must not silently rewrite unrelated files. Sensitive files should be rejected or escalated according to the host's security policy.

## Git rules

Inspection is read-only. Mutating Git operations require an explicit authorized work unit. The adapter must report the resulting HEAD/status/diff evidence after mutation when available.

## Verification rules

Verification commands come from project configuration or an explicitly selected workflow. The adapter reports the real exit status and safe output. If the required runtime/toolchain is unavailable, return `UNAVAILABLE` or `BLOCKED`; never convert that condition into `VERIFIED`.

## External integration rules

Remote GitHub or CI mutations require an actual supported integration and applicable authorization. A textual instruction to perform an external action is not evidence that the action happened.

## Security

Adapters must avoid exposing secrets in output, logs, checkpoints, or `.ai` state. High-risk and production-affecting operations must remain behind the Security Gate and applicable approval requirements.
