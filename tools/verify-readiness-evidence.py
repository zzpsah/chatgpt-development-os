#!/usr/bin/env python3
"""Read-only validation of the versioned DevOS capability/evidence ledger."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = "DEVOS-READINESS-EVIDENCE-v1"
FAMILIES = {
    "bootstrap", "state", "interpretation", "planning", "readiness", "controller",
    "runtime", "verification", "security", "persistence_recovery", "continuation",
    "self_healing", "external_reads", "remote_mutation", "high_impact",
}
LEVELS = {"deterministic", "integrated", "real_read_only", "provider_simulated"}
# v1 cannot accept live/production claims: adding those requires a reviewed protocol change.
STATUSES = {"implemented", "partial", "planned", "unavailable"}


def read_json(path: Path):
    """Reject duplicate keys instead of silently taking a later contradictory value."""
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError(f"duplicate JSON key: {key}")
            result[key] = value
        return result
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=pairs)


def file_in_root(root: Path, value: str) -> Path:
    """Only allow existing, repository-relative files after resolving symlinks."""
    if not isinstance(value, str) or not value or "\\" in value:
        raise ValueError("invalid repository-relative path")
    if value.startswith("/") or ":" in value or ".." in value.split("/"):
        raise ValueError("path escapes repository")
    path = (root / value).resolve()
    if not path.is_relative_to(root.resolve()) or not path.is_file():
        raise ValueError(f"missing or escaping evidence file: {value}")
    return path


def validate(data, root: Path = ROOT) -> list[str]:
    """Validate claims and archived provenance; do not execute tests or contact providers."""
    errors = []
    if not isinstance(data, dict):
        return ["ledger must be an object"]
    top_keys = {"protocol", "repository", "authority", "authorization", "execution",
                "production_ready", "snapshot_head", "archive", "archive_sha256", "capabilities"}
    if set(data) - top_keys:
        errors.append("unknown ledger fields")
    if data.get("protocol") != PROTOCOL:
        errors.append("unsupported ledger protocol")
    for name, expected in {"repository": "zzpsah/chatgpt-development-os",
                           "authority": "UNCHANGED", "authorization": "UNCHANGED",
                           "execution": "NONE", "production_ready": False}.items():
        if type(data.get(name)) is not type(expected) or data.get(name) != expected:
            errors.append(f"invalid invariant: {name}")
    try:
        archive_path = file_in_root(root, data.get("archive"))
        digest = hashlib.sha256(archive_path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()
        if digest != data.get("archive_sha256"):
            raise ValueError("archive hash mismatch; review evidence before updating")
        archive = read_json(archive_path)
        if archive.get("repository") != "https://github.com/zzpsah/chatgpt-development-os":
            raise ValueError("archive repository mismatch")
        if archive.get("head") != data.get("snapshot_head"):
            raise ValueError("archive snapshot head mismatch")
        if not re.fullmatch(r"[0-9a-f]{40}", str(data.get("snapshot_head", ""))):
            raise ValueError("invalid snapshot head")
    except (OSError, ValueError, TypeError, AttributeError) as exc:
        return errors + [str(exc)]
    try:
        inventory = {item["path"]: item["sha256"] for item in archive["tracked_inventory"]}
        assert isinstance(archive["latest_main_runs"], list)
        assert isinstance(archive["final_source_runs"], dict)
        assert isinstance(archive["local_checks"], list)
    except (KeyError, TypeError, AssertionError):
        return errors + ["malformed archive collections"]
    runs = list(archive["latest_main_runs"])
    for group in archive["final_source_runs"].values():
        runs.extend(group)
    run_by_id = {item["id"]: item for item in runs}
    local = {item["script"]: item for item in archive["local_checks"]}
    rows = data.get("capabilities")
    if not isinstance(rows, list) or not rows:
        return errors + ["capabilities must be a nonempty list"]
    seen = set()
    for row in rows:
        if not isinstance(row, dict):
            errors.append("capability must be an object")
            continue
        name = row.get("id")
        if not isinstance(name, str) or name not in FAMILIES or name in seen:
            errors.append(f"unknown or duplicate capability: {name}")
            continue
        seen.add(name)
        prefix = name + ": "
        row_keys = {"id", "summary", "implementation", "implementation_refs", "verification_levels",
                    "evidence", "authorization_boundary", "security_boundary", "recovery_policy",
                    "allowed_claim", "limitations", "production_proven", "live_mutation_proven"}
        if set(row) - row_keys:
            errors.append(prefix + "unknown capability fields")
        status = row.get("implementation")
        if not isinstance(status, str) or status not in STATUSES:
            errors.append(prefix + "invalid implementation status")
            continue
        if row.get("production_proven") is not False or row.get("live_mutation_proven") is not False:
            errors.append(prefix + "v1 forbids live-mutation/production promotion")
        for field in ["summary", "authorization_boundary", "security_boundary", "recovery_policy", "allowed_claim"]:
            if not isinstance(row.get(field), str) or not row[field].strip():
                errors.append(prefix + "missing " + field)
        limitations = row.get("limitations")
        if not isinstance(limitations, list) or not limitations or not all(isinstance(x,str) and x.strip() for x in limitations):
            errors.append(prefix + "explicit limitations required")
        refs = row.get("implementation_refs")
        if not isinstance(refs, list):
            errors.append(prefix + "implementation_refs must be a list")
        else:
            if row.get("implementation") in {"implemented", "partial"} and not refs:
                errors.append(prefix + "implemented capability needs source references")
            for ref in refs:
                try:
                    file_in_root(root, ref)
                except (OSError, ValueError, TypeError) as exc:
                    errors.append(prefix + str(exc))
        evidence = row.get("evidence")
        if not isinstance(evidence, list):
            errors.append(prefix + "evidence must be a list")
            continue
        if row.get("implementation") in {"planned", "unavailable"} and evidence:
            errors.append(prefix + "planned/unavailable capability cannot claim proof")
        observed_levels = set()
        for item in evidence:
            try:
                if not isinstance(item, dict) or not isinstance(item.get("level"), str) or item.get("level") not in LEVELS:
                    raise ValueError("unsupported evidence level")
                allowed_keys = {"kind", "level", "test", "source_head", "freshness"}
                if item.get("kind") == "ci_run":
                    allowed_keys.update({"run_id", "workflow"})
                if set(item) - allowed_keys:
                    raise ValueError("unknown evidence fields")
                level = item["level"]
                if level in observed_levels:
                    raise ValueError("duplicate evidence level")
                observed_levels.add(level)
                if item.get("freshness") != "historical":
                    raise ValueError("archived evidence must remain historical")
                path = file_in_root(root, item.get("test"))
                # Normalize checkout line endings so GitHub LF and Windows CRLF agree.
                blob = path.read_bytes().replace(b"\r\n", b"\n")
                # The published snapshot hashed a Windows checkout; accept its CRLF
                # form or canonical LF form, without ignoring any other content drift.
                digests = {hashlib.sha256(blob).hexdigest(),
                           hashlib.sha256(blob.replace(b"\n", b"\r\n")).hexdigest()}
                if inventory.get(item["test"]) not in digests:
                    raise ValueError("test differs from archived source; refresh evidence")
                if item.get("kind") == "local_check":
                    record = local.get(path.name)
                    if not record or record.get("exit_code") != 0:
                        raise ValueError("missing successful archived local check")
                    if level == "real_read_only":
                        raise ValueError("local corpus cannot establish external read-only proof")
                    if item.get("source_head") != archive["head"]:
                        raise ValueError("local check source head mismatch")
                elif item.get("kind") == "ci_run":
                    run = run_by_id.get(item.get("run_id"))
                    if not run or run.get("conclusion") != "success" or run.get("head_sha") != item.get("source_head"):
                        raise ValueError("CI run success/head mismatch")
                    workflow_path = file_in_root(root, item.get("workflow"))
                    workflow = workflow_path.read_text(encoding="utf-8")
                    if item["test"] not in workflow or run["name"] not in workflow:
                        raise ValueError("test/run not covered by declared workflow")
                    if level == "real_read_only" and path.name not in {
                        "test-github-live.py", "verify-production-e2e-managed-project.py",
                        "verify-failure-recovery-managed-project.py", "verify-multi-session-managed-project.py",
                        "verify-managed-project-orchestration.py"}:
                        raise ValueError("test is not a v1 external read-only proof")
                else:
                    raise ValueError("unknown evidence kind")
                # Prevent relabeling the simulated provider corpus as integrated/live proof.
                if name == "remote_mutation" and level != "provider_simulated":
                    raise ValueError("remote mutation is provider-simulated only")
                if level == "provider_simulated" and item["test"] != "tools/test-controlled-remote-mutation-proof.py":
                    raise ValueError("simulated mutation needs controlled-mutation corpus")
            except (OSError, ValueError, TypeError, KeyError) as exc:
                errors.append(prefix + str(exc))
        declared = row.get("verification_levels")
        if not isinstance(declared, list) or len(declared) != len(set(str(x) for x in declared)) or set(str(x) for x in declared) != observed_levels:
            errors.append(prefix + "declared levels must exactly match evidence")
    if seen != FAMILIES:
        errors.append("missing capability families: " + ", ".join(sorted(FAMILIES - seen)))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--matrix", default="config/readiness-evidence.json")
    args = parser.parse_args()
    try:
        data = read_json(file_in_root(ROOT, args.matrix))
        errors = validate(data)
    except (OSError, ValueError, TypeError, KeyError) as exc:
        errors = [str(exc)]
    print(json.dumps({"protocol": PROTOCOL, "status": "HOLD" if errors else "VALID",
                      "production_ready": False, "authority": "UNCHANGED",
                      "authorization": "UNCHANGED", "execution": "NONE",
                      "errors": errors}, indent=2))
    return 2 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
