#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "tools" / "devos-project-lifecycle.py"
spec = importlib.util.spec_from_file_location("devos_project_lifecycle", MODULE)
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def managed_manifest(repository: str) -> dict:
    return {
        "context_version": "1",
        "specification": "portable-project-context",
        "project_id": repository.split("/")[-1].lower(),
        "name": repository.split("/")[-1],
        "managed_by": "development-os",
        "canonical_repository": repository,
        "canonical_url": f"https://github.com/{repository}",
        "devos_repository": "zzpsah/chatgpt-development-os",
    }


def main() -> None:
    required = set(mod.REQUIRED_PROJECT_FILES)

    remote_unmanaged = mod.classify_snapshot({
        "protocol": mod.SNAPSHOT_PROTOCOL,
        "repository": "zzpsah/new-project",
        "default_branch": "main",
        "observed_head": "a" * 40,
        "files": ["README.md"],
        "manifest": None,
    })
    assert remote_unmanaged["status"] == "ONBOARDING_REQUIRED", remote_unmanaged
    assert remote_unmanaged["management_state"] == "UNMANAGED"
    assert remote_unmanaged["development_continuation_allowed"] is False
    assert remote_unmanaged["next_action"] == "ONBOARD_PROJECT"

    remote_partial = mod.classify_snapshot({
        "protocol": mod.SNAPSHOT_PROTOCOL,
        "repository": "zzpsah/partial-project",
        "default_branch": "main",
        "observed_head": "b" * 40,
        "files": ["README.md", ".ai/manifest.yaml", "AGENTS.md"],
        "manifest": managed_manifest("zzpsah/partial-project"),
    })
    assert remote_partial["status"] == "ONBOARDING_REQUIRED", remote_partial
    assert remote_partial["management_state"] == "PARTIAL"
    assert remote_partial["missing_files"]

    remote_managed = mod.classify_snapshot({
        "protocol": mod.SNAPSHOT_PROTOCOL,
        "repository": "zzpsah/managed-project",
        "default_branch": "main",
        "observed_head": "c" * 40,
        "files": sorted(required | {"README.md"}),
        "manifest": managed_manifest("zzpsah/managed-project"),
    })
    assert remote_managed["status"] == "MANAGED", remote_managed
    assert remote_managed["managed"] is True
    assert remote_managed["development_continuation_allowed"] is True

    conflict_manifest = managed_manifest("zzpsah/other-project")
    conflict = mod.classify_snapshot({
        "protocol": mod.SNAPSHOT_PROTOCOL,
        "repository": "zzpsah/conflict-project",
        "default_branch": "main",
        "observed_head": "d" * 40,
        "files": sorted(required),
        "manifest": conflict_manifest,
    })
    assert conflict["status"] == "HOLD", conflict
    assert conflict["development_continuation_allowed"] is False
    assert conflict["next_action"] == "RESOLVE_MANAGEMENT_IDENTITY"

    invalid_head = mod.classify_snapshot({
        "protocol": mod.SNAPSHOT_PROTOCOL,
        "repository": "zzpsah/bad-head",
        "default_branch": "main",
        "observed_head": "not-a-sha",
        "files": [],
        "manifest": None,
    })
    assert invalid_head["status"] == "BLOCKED", invalid_head

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory) / "new-local-project"
        root.mkdir()
        (root / ".git").mkdir()
        before = mod.classify_local(root)
        assert before["status"] == "ONBOARDING_REQUIRED", before
        assert before["development_continuation_allowed"] is False

        needs_approval = mod.apply_local(root, authorization=None)
        assert needs_approval["status"] == "NEEDS_APPROVAL", needs_approval
        assert not (root / ".ai/manifest.yaml").exists()

        after = mod.apply_local(root, authorization="EXPLICIT")
        assert after["status"] == "MANAGED", after
        assert after["development_continuation_allowed"] is True
        assert ".ai/manifest.yaml" in after["created"]
        assert (root / "AGENTS.md").exists()
        assert (root / ".ai/CURRENT-STATE.md").exists()

        again = mod.apply_local(root, authorization="EXPLICIT")
        assert again["status"] == "MANAGED", again
        assert again["created"] == []
        assert again["mutation"] == "NONE"

    with tempfile.TemporaryDirectory() as directory:
        snapshot = Path(directory) / "snapshot.json"
        snapshot.write_text(json.dumps({
            "protocol": mod.SNAPSHOT_PROTOCOL,
            "repository": "zzpsah/cli-unmanaged",
            "default_branch": "main",
            "observed_head": "e" * 40,
            "files": ["README.md"],
            "manifest": None,
        }), encoding="utf-8")
        import subprocess, sys
        result = subprocess.run(
            [sys.executable, str(MODULE), "--snapshot", str(snapshot), "--require-managed", "--json"],
            cwd=ROOT, text=True, capture_output=True, check=False,
        )
        assert result.returncode == 2, result.stdout + result.stderr
        payload = json.loads(result.stdout)
        assert payload["status"] == "ONBOARDING_REQUIRED"

    print("PASS: managed project lifecycle detects unmanaged/partial/conflicting repositories")
    print("PASS: local onboarding requires explicit authorization and verifies managed readback")
    print("PASS: development continuation is allowed only for MANAGED state")


if __name__ == "__main__":
    main()
