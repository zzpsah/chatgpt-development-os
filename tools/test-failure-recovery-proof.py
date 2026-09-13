#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "tools" / "failure-recovery-proof.py"
spec = importlib.util.spec_from_file_location("failure_recovery_proof", MODULE)
assert spec and spec.loader
recovery = importlib.util.module_from_spec(spec)
spec.loader.exec_module(recovery)


def read_scenario(project: Path, head: str = "head-1") -> dict:
    return {
        "project_root": str(project),
        "human_request": "check repository",
        "context": {"project": "RECOVERY-FIXTURE"},
        "repository_head": head,
        "capabilities": {"S1": "AVAILABLE"},
        "authorization_by_step": {},
        "security_gate_by_step": {},
        "runtime_request": {
            "step_id": "S1",
            "operation": "filesystem.read",
            "target": "README.md",
            "scope": "repository-read",
        },
        "verification": {
            "id": "readme-ok",
            "command": [
                sys.executable,
                "-c",
                "from pathlib import Path; assert Path('README.md').read_text(encoding='utf-8') == 'hello\\n'",
            ],
            "expected_exit_codes": [0],
            "timeout_seconds": 30,
        },
        "persistence": {
            "path": ".ai/EVIDENCE/failure-recovery.json",
            "authorization": "ALREADY_GRANTED",
        },
    }


def run_failed(payload: dict) -> tuple[dict, dict]:
    result = recovery.harness.run(payload)
    assert result["status"] == "BLOCKED", json.dumps(result, indent=2)
    checkpoint = recovery.build_checkpoint(payload, result)
    assert checkpoint["protocol"] == "DEVOS-FAILURE-RECOVERY-v1"
    assert checkpoint["status"] == "FAILED_CHECKPOINT"
    assert checkpoint["authority"] == "UNCHANGED"
    assert checkpoint["authorization"] == "UNCHANGED"
    assert checkpoint["execution"] == "NONE"
    return result, checkpoint


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project = Path(tmp)
        (project / "README.md").write_text("hello\n", encoding="utf-8")

        # 1. Repository drift/stale plan must stop, then recover only after a
        # repaired compilation/current head pair is supplied.
        stale_payload = read_scenario(project, "head-2")
        stale_payload["compiled_repository_head"] = "head-1"
        stale_result, stale_checkpoint = run_failed(stale_payload)
        assert stale_result["stage"] == "READINESS"
        assert stale_checkpoint["failure_class"] == "REPOSITORY_DRIFT"
        assert stale_checkpoint["replay_policy"] == "RECOMPILE_AND_REVALIDATE_REQUIRED"
        repaired_stale = read_scenario(project, "head-2")
        repaired_stale["compiled_repository_head"] = "head-2"
        recovered_stale = recovery.resume(stale_checkpoint, repaired_stale)
        assert recovered_stale["status"] == "RECOVERED_VERIFIED", recovered_stale

        # 2. Repository head changes after a different failure require explicit
        # recompilation acknowledgement before any replay-safe retry.
        cap_payload = read_scenario(project, "head-1")
        cap_payload["capabilities"] = {"S1": "MISSING"}
        _, cap_checkpoint = run_failed(cap_payload)
        assert cap_checkpoint["failure_class"] == "CAPABILITY_MISSING"
        changed_head = read_scenario(project, "head-2")
        blocked_head_change = recovery.resume(cap_checkpoint, changed_head)
        assert blocked_head_change["status"] == "HOLD"
        assert blocked_head_change["reason"] == "RECOMPILE_REQUIRED_AFTER_REPOSITORY_CHANGE"
        changed_head["recompiled_after_repository_change"] = True
        recovered_capability = recovery.resume(cap_checkpoint, changed_head)
        assert recovered_capability["status"] == "RECOVERED_VERIFIED"

        # 3. Authorization and Security Gate failures remain distinct and are
        # recoverable only after exact step-bound evidence is supplied.
        auth_payload = read_scenario(project)
        auth_payload["human_request"] = "check security"
        auth_payload["authorization_by_step"] = {}
        auth_payload["security_gate_by_step"] = {"S1": "PASS"}
        _, auth_checkpoint = run_failed(auth_payload)
        assert auth_checkpoint["failure_class"] == "AUTHORIZATION_REQUIRED"
        auth_fixed = read_scenario(project)
        auth_fixed["human_request"] = "check security"
        auth_fixed["authorization_by_step"] = {"S1": "ALREADY_GRANTED"}
        auth_fixed["security_gate_by_step"] = {"S1": "PASS"}
        assert recovery.resume(auth_checkpoint, auth_fixed)["status"] == "RECOVERED_VERIFIED"

        sec_payload = read_scenario(project)
        sec_payload["human_request"] = "check security"
        sec_payload["authorization_by_step"] = {"S1": "ALREADY_GRANTED"}
        sec_payload["security_gate_by_step"] = {}
        _, sec_checkpoint = run_failed(sec_payload)
        assert sec_checkpoint["failure_class"] == "SECURITY_BLOCKED"
        sec_fixed = read_scenario(project)
        sec_fixed["human_request"] = "check security"
        sec_fixed["authorization_by_step"] = {"S1": "ALREADY_GRANTED"}
        sec_fixed["security_gate_by_step"] = {"S1": "PASS"}
        assert recovery.resume(sec_checkpoint, sec_fixed)["status"] == "RECOVERED_VERIFIED"

        # 4. Runtime/provider failure on a read-only operation is replay-safe only
        # after revalidation and repair of the runtime request.
        runtime_payload = read_scenario(project)
        runtime_payload["runtime_request"]["target"] = "MISSING.md"
        runtime_result, runtime_checkpoint = run_failed(runtime_payload)
        assert runtime_result["stage"] == "RUNTIME"
        assert runtime_checkpoint["failure_class"] == "PROVIDER_OR_RUNTIME_UNAVAILABLE"
        assert runtime_checkpoint["mutation_attempted"] is False
        assert recovery.resume(runtime_checkpoint, read_scenario(project))["status"] == "RECOVERED_VERIFIED"

        # 5. Verification failure on a read-only operation can be retried after
        # repair and full revalidation.
        verification_payload = read_scenario(project)
        verification_payload["verification"] = {
            "id": "forced-fail",
            "command": [sys.executable, "-c", "raise SystemExit(3)"],
            "expected_exit_codes": [0],
            "timeout_seconds": 30,
        }
        verification_result, verification_checkpoint = run_failed(verification_payload)
        assert verification_result["stage"] == "VERIFICATION"
        assert verification_checkpoint["failure_class"] == "VERIFICATION_FAILED"
        assert recovery.resume(verification_checkpoint, read_scenario(project))["status"] == "RECOVERED_VERIFIED"

        # 6. Persistence authorization failure can recover on a read-only path.
        persistence_payload = read_scenario(project)
        persistence_payload["persistence"]["authorization"] = "NOT_REQUIRED"
        persistence_result, persistence_checkpoint = run_failed(persistence_payload)
        assert persistence_result["stage"] == "PERSISTENCE"
        assert persistence_checkpoint["failure_class"] == "PERSISTENCE_AUTHORIZATION_REQUIRED"
        assert recovery.resume(persistence_checkpoint, read_scenario(project))["status"] == "RECOVERED_VERIFIED"

        # 7. A mutation rejected during runtime preflight has NOT been attempted;
        # after exact-step authorization is repaired it may proceed once.
        preflight_mutation = {
            "project_root": str(project),
            "human_request": "update docs",
            "context": {"project": "RECOVERY-FIXTURE"},
            "repository_head": "head-1",
            "step_id": "S2",
            "completed_steps": ["S1"],
            "capabilities": {"S1": "AVAILABLE", "S2": "AVAILABLE"},
            "authorization_by_step": {},
            "security_gate_by_step": {},
            "runtime_request": {
                "step_id": "S2",
                "operation": "filesystem.write_scoped",
                "target": "notes.txt",
                "scope": "repository-write",
                "content": "changed once\n",
            },
            "verification": {
                "id": "notes-ok",
                "command": [
                    sys.executable,
                    "-c",
                    "from pathlib import Path; assert Path('notes.txt').read_text(encoding='utf-8') == 'changed once\\n'",
                ],
                "expected_exit_codes": [0],
                "timeout_seconds": 30,
            },
            "persistence": {
                "path": ".ai/EVIDENCE/mutation-recovery.json",
                "authorization": "ALREADY_GRANTED",
            },
        }
        preflight_result, preflight_checkpoint = run_failed(preflight_mutation)
        assert preflight_result["stage"] == "RUNTIME"
        assert preflight_checkpoint["failure_class"] == "AUTHORIZATION_REQUIRED"
        assert preflight_checkpoint["mutation_operation"] is True
        assert preflight_checkpoint["mutation_attempted"] is False
        assert not (project / "notes.txt").exists()
        fixed_mutation = json.loads(json.dumps(preflight_mutation))
        fixed_mutation["authorization_by_step"] = {"S2": "ALREADY_GRANTED"}
        recovered_mutation = recovery.resume(preflight_checkpoint, fixed_mutation)
        assert recovered_mutation["status"] == "RECOVERED_VERIFIED", recovered_mutation
        assert (project / "notes.txt").read_text(encoding="utf-8") == "changed once\n"

        # 8. Once a mutation DID execute, a downstream verification failure must
        # HOLD forever at this supervisor boundary rather than replay the mutation.
        mutation_verify_fail = json.loads(json.dumps(fixed_mutation))
        mutation_verify_fail["runtime_request"]["content"] = "mutated-before-failure\n"
        mutation_verify_fail["verification"] = {
            "id": "forced-post-mutation-failure",
            "command": [sys.executable, "-c", "raise SystemExit(9)"],
            "expected_exit_codes": [0],
            "timeout_seconds": 30,
        }
        mutation_result, mutation_checkpoint = run_failed(mutation_verify_fail)
        assert mutation_result["stage"] == "VERIFICATION"
        assert mutation_checkpoint["mutation_attempted"] is True
        assert mutation_checkpoint["replay_policy"] == "NO_REPLAY_HOLD"
        observed_after_failure = (project / "notes.txt").read_text(encoding="utf-8")
        attempted_resume = recovery.resume(mutation_checkpoint, fixed_mutation)
        assert attempted_resume["status"] == "HOLD"
        assert attempted_resume["reason"] == "MUTATION_REPLAY_FORBIDDEN"
        assert (project / "notes.txt").read_text(encoding="utf-8") == observed_after_failure

        # 9. Persisted evidence corruption is detected and held rather than used
        # as recovery authority.
        clean = recovery.harness.run(read_scenario(project))
        assert clean["status"] == "COMPLETE"
        evidence = project / ".ai" / "EVIDENCE" / "failure-recovery.json"
        assert recovery.inspect_persisted_evidence(project, ".ai/EVIDENCE/failure-recovery.json")["status"] == "RECOVERABLE"
        evidence.write_text("{broken-json", encoding="utf-8")
        corrupt = recovery.inspect_persisted_evidence(project, ".ai/EVIDENCE/failure-recovery.json")
        assert corrupt["status"] == "HOLD"
        assert corrupt["reason"] == "PERSISTED_EVIDENCE_CORRUPT"

        # 10. Tampered checkpoint authority is never accepted for resume.
        tampered = dict(cap_checkpoint)
        tampered["authority"] = "GRANTED"
        rejected = recovery.resume(tampered, read_scenario(project))
        assert rejected["status"] == "HOLD"
        assert rejected["reason"] == "CHECKPOINT_AUTHORITY_BOUNDARY_CHANGED"

    print("PASS: Failure + Recovery Proof deterministic injection corpus")


if __name__ == "__main__":
    main()
