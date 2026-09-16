#!/usr/bin/env python3
"""Regression corpus for DevOS Project Fleet Watch v1."""
from __future__ import annotations

import base64
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "tools" / "devos-project-fleet.py"
spec = importlib.util.spec_from_file_location("devos_project_fleet", MODULE)
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def managed_manifest(repository: str) -> dict[str, str]:
    return {
        "managed_by": "development-os",
        "devos_repository": "zzpsah/chatgpt-development-os",
        "canonical_repository": repository,
        "project_id": repository.split("/", 1)[1].lower(),
    }


def entry(repository: str, *, managed: bool = True, archived: bool = False, manifest=None):
    files = sorted(mod.lifecycle.REQUIRED_PROJECT_FILES) if managed else ["README.md"]
    if manifest is None and managed:
        manifest = managed_manifest(repository)
    return {
        "repository": repository,
        "default_branch": "main",
        "observed_head": "a" * 40,
        "archived": archived,
        "files": files,
        "manifest": manifest,
    }


def snapshot(*entries):
    return {
        "protocol": mod.SNAPSHOT_PROTOCOL,
        "provider": "fixture",
        "observed_at": "2026-09-17T00:00:00+05:30",
        "repositories": list(entries),
    }


def main() -> None:
    healthy = mod.assess_snapshot(snapshot(entry("zzpsah/managed-one")))
    assert healthy["fleet_status"] == "HEALTHY", healthy
    assert healthy["fleet_clean"] is True
    assert healthy["summary"]["managed"] == 1
    assert healthy["repositories"][0]["development_continuation_allowed"] is True
    assert healthy["external_mutation"] == "NONE"
    assert healthy["production_ready"] is False

    unmanaged = mod.assess_snapshot(snapshot(entry("zzpsah/new-repo", managed=False, manifest=None)))
    assert unmanaged["fleet_status"] == "ATTENTION", unmanaged
    assert unmanaged["summary"]["onboarding_required"] == 1
    assert unmanaged["repositories"][0]["next_action"] == "ONBOARD_PROJECT"
    assert unmanaged["repositories"][0]["development_continuation_allowed"] is False

    previous = snapshot(entry("zzpsah/managed-one"))
    current = snapshot(
        entry("zzpsah/managed-one"),
        entry("zzpsah/new-repo", managed=False, manifest=None),
    )
    drifted = mod.assess_snapshot(current, previous)
    assert drifted["fleet_status"] == "ATTENTION", drifted
    assert drifted["drift"]["new_repositories"] == ["zzpsah/new-repo"]
    assert drifted["drift"]["new_unmanaged"] == ["zzpsah/new-repo"]
    assert drifted["drift"]["management_regressions"] == []

    regressed = mod.assess_snapshot(
        snapshot(entry("zzpsah/managed-one", managed=False, manifest=None)),
        previous,
    )
    assert regressed["fleet_status"] == "HOLD", regressed
    assert regressed["drift"]["management_regressions"] == ["zzpsah/managed-one"]

    newly_managed = mod.assess_snapshot(
        snapshot(entry("zzpsah/new-repo")),
        snapshot(entry("zzpsah/new-repo", managed=False, manifest=None)),
    )
    assert newly_managed["drift"]["newly_managed"] == ["zzpsah/new-repo"]

    conflict_manifest = managed_manifest("zzpsah/conflict")
    conflict_manifest["devos_repository"] = "someone/else"
    conflict = mod.assess_snapshot(snapshot(entry("zzpsah/conflict", manifest=conflict_manifest)))
    assert conflict["fleet_status"] == "HOLD", conflict
    assert conflict["summary"]["hold"] == 1

    archived = mod.assess_snapshot(snapshot(entry("zzpsah/old", archived=True)))
    assert archived["fleet_status"] == "EMPTY", archived
    assert archived["summary"]["archived"] == 1

    duplicate_payload = snapshot(entry("zzpsah/dup"), entry("zzpsah/dup"))
    duplicate = mod.assess_snapshot(duplicate_payload)
    assert duplicate["fleet_status"] == "BLOCKED", duplicate
    assert "duplicate repository" in duplicate["reason"]

    wrong_protocol = snapshot(entry("zzpsah/x"))
    wrong_protocol["protocol"] = "wrong"
    blocked = mod.assess_snapshot(wrong_protocol)
    assert blocked["fleet_status"] == "BLOCKED"

    required_files = sorted(mod.lifecycle.REQUIRED_PROJECT_FILES)
    manifest_text = "\n".join(
        [
            "context_version: 1",
            "project_id: live-repo",
            'name: "live-repo"',
            "managed_by: development-os",
            "canonical_repository: zzpsah/live-repo",
            "devos_repository: zzpsah/chatgpt-development-os",
        ]
    ) + "\n"
    encoded_manifest = base64.b64encode(manifest_text.encode()).decode()
    calls: list[str] = []

    def fake_fetch(url: str, token: str | None, *, allow_404: bool = False):
        calls.append(url)
        if "/user/repos?" in url:
            return [{"full_name": "zzpsah/live-repo", "default_branch": "main", "archived": False}]
        if "/branches/main" in url:
            return {
                "commit": {
                    "sha": "b" * 40,
                    "commit": {"tree": {"sha": "c" * 40}},
                }
            }
        if "/git/trees/" in url:
            return {"tree": [{"path": path, "type": "blob"} for path in required_files]}
        if url.endswith("/contents/.ai/manifest.yaml"):
            return {"content": encoded_manifest}
        raise AssertionError(url)

    live_snapshot = mod.discover_github("@me", "SUPERSECRET", limit=10, fetch_json=fake_fetch)
    live = mod.assess_snapshot(live_snapshot)
    assert live["fleet_status"] == "HEALTHY", live
    assert live["repositories"][0]["repository"] == "zzpsah/live-repo"
    assert "SUPERSECRET" not in repr(live_snapshot)
    assert any("/user/repos?" in url for url in calls)

    try:
        mod.discover_github("@me", None)
    except ValueError as exc:
        assert "GITHUB_TOKEN" in str(exc)
    else:
        raise AssertionError("@me discovery without token must fail")

    print("PASS: Project Fleet Watch v1 detects unmanaged repos, drift, regressions, and read-only GitHub fleet state")


if __name__ == "__main__":
    main()
