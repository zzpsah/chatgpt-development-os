#!/usr/bin/env python3
"""Managed Project Lifecycle v1 for Development OS.

Detect whether a local or provider-observed repository is durably managed by
DevOS. Development continuation is allowed only after management identity and
minimum portable context are verified. Local onboarding can be applied only
with an explicit authorization signal; remote snapshots are read-only evidence.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
from pathlib import Path
from typing import Any

PROTOCOL = "DEVOS-MANAGED-PROJECT-LIFECYCLE-v1"
SNAPSHOT_PROTOCOL = "DEVOS-REPOSITORY-DISCOVERY-SNAPSHOT-v1"
CANONICAL_DEVOS = "zzpsah/chatgpt-development-os"
SHA40 = re.compile(r"^[0-9a-f]{40}$")

ROOT = Path(__file__).resolve().parents[1]
ONBOARD_MODULE = ROOT / "tools" / "devos-onboard.py"
spec = importlib.util.spec_from_file_location("devos_onboard", ONBOARD_MODULE)
assert spec and spec.loader
onboard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(onboard)

REQUIRED_PROJECT_FILES = frozenset({".ai/manifest.yaml", *onboard.MINIMUM_FILES.keys()})

BOUNDARIES = {
    "authority": "UNCHANGED",
    "authorization": "UNCHANGED",
    "production_ready": False,
}


def _base(status: str, repository: str | None, *, reason: str | None = None) -> dict[str, Any]:
    report: dict[str, Any] = {
        "protocol": PROTOCOL,
        "status": status,
        "repository": repository,
        "managed": status == "MANAGED",
        "onboarding_required": status == "ONBOARDING_REQUIRED",
        "development_continuation_allowed": status == "MANAGED",
        "next_action": "CONTINUE" if status == "MANAGED" else "HOLD",
        "mutation": "NONE",
        **BOUNDARIES,
    }
    if reason:
        report["reason"] = reason
    return report


def _validate_manifest(manifest: Any, repository: str | None) -> tuple[str | None, list[str]]:
    reasons: list[str] = []
    if not isinstance(manifest, dict):
        return "MANIFEST_INVALID", ["manifest must be an object"]
    if manifest.get("managed_by") != "development-os":
        reasons.append("managed_by is not development-os")
    devos_repo = manifest.get("devos_repository")
    if devos_repo not in (None, CANONICAL_DEVOS):
        reasons.append("devos_repository identifies a different DevOS authority")
    canonical = manifest.get("canonical_repository")
    if repository and canonical not in (None, "null", "None", repository):
        reasons.append("canonical_repository conflicts with observed repository")
    if not manifest.get("project_id"):
        reasons.append("project_id is missing")
    return ("MANIFEST_CONFLICT" if reasons else None), reasons


def classify_observation(
    *, repository: str | None, files: set[str], manifest: dict[str, Any] | None,
    observed_head: str | None = None,
) -> dict[str, Any]:
    if not repository:
        return _base("BLOCKED", repository, reason="repository identity is required")
    if observed_head is not None and not SHA40.fullmatch(observed_head):
        return _base("BLOCKED", repository, reason="observed_head must be a 40-character lowercase Git SHA or null")

    if manifest is None:
        report = _base("ONBOARDING_REQUIRED", repository, reason="DevOS manifest is absent")
        report["management_state"] = "UNMANAGED"
        report["missing_files"] = sorted(REQUIRED_PROJECT_FILES - files)
        report["next_action"] = "ONBOARD_PROJECT"
        report["observed_head"] = observed_head
        return report

    code, reasons = _validate_manifest(manifest, repository)
    if code:
        report = _base("HOLD", repository, reason="; ".join(reasons))
        report["management_state"] = "CONFLICT"
        report["next_action"] = "RESOLVE_MANAGEMENT_IDENTITY"
        report["observed_head"] = observed_head
        return report

    missing = sorted(REQUIRED_PROJECT_FILES - files)
    if missing:
        report = _base("ONBOARDING_REQUIRED", repository, reason="DevOS context is incomplete")
        report["management_state"] = "PARTIAL"
        report["missing_files"] = missing
        report["next_action"] = "COMPLETE_ONBOARDING"
        report["observed_head"] = observed_head
        return report

    report = _base("MANAGED", repository)
    report["management_state"] = "MANAGED"
    report["missing_files"] = []
    report["observed_head"] = observed_head
    report["next_action"] = "RECOVER_STATE_THEN_CONTINUE"
    return report


def classify_local(root: Path) -> dict[str, Any]:
    root = root.expanduser().resolve()
    if not root.exists() or not root.is_dir():
        return _base("BLOCKED", None, reason="project path does not exist or is not a directory")

    remote = onboard.git_remote(root)
    repository = onboard.canonical_repo_from_remote(remote)
    if repository is None:
        repository = f"local:{root.name}"
    files = {
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file() and ".git" not in path.relative_to(root).parts
    }
    manifest = onboard.load_manifest(root) if (root / ".ai/manifest.yaml").exists() else None
    report = classify_observation(repository=repository, files=files, manifest=manifest)
    report["path"] = str(root)
    report["repository_kind"] = "git" if (root / ".git").exists() else "directory"
    report["observed_remote"] = remote
    return report


def apply_local(root: Path, *, authorization: str | None) -> dict[str, Any]:
    before = classify_local(root)
    if before["status"] == "MANAGED":
        before["created"] = []
        before["mutation"] = "NONE"
        return before
    if before["status"] in {"HOLD", "BLOCKED"}:
        return before
    if authorization != "EXPLICIT":
        report = dict(before)
        report["status"] = "NEEDS_APPROVAL"
        report["managed"] = False
        report["development_continuation_allowed"] = False
        report["next_action"] = "OBTAIN_ONBOARDING_APPROVAL"
        report["reason"] = "explicit onboarding authorization is required"
        return report

    plan = onboard.inventory(root.expanduser().resolve(), None, None)
    if plan.get("status") != "READY":
        report = _base("HOLD", before.get("repository"), reason=plan.get("reason", "onboarding plan is not ready"))
        report["management_state"] = before.get("management_state")
        return report
    code, created = onboard.apply(root.expanduser().resolve(), plan)
    if code != 0:
        report = _base("HOLD", before.get("repository"), reason="onboarding apply failed")
        report["created"] = created
        return report

    after = classify_local(root)
    after["created"] = created
    after["mutation"] = "MISSING_DEVOS_INFRASTRUCTURE_ONLY"
    if after["status"] != "MANAGED":
        after["status"] = "HOLD"
        after["managed"] = False
        after["development_continuation_allowed"] = False
        after["next_action"] = "ONBOARDING_READBACK_REQUIRED"
        after["reason"] = "onboarding mutation completed but managed-state readback did not verify"
    return after


def load_snapshot(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("snapshot must be a JSON object")
    return payload


def classify_snapshot(payload: dict[str, Any]) -> dict[str, Any]:
    if payload.get("protocol") != SNAPSHOT_PROTOCOL:
        return _base("BLOCKED", payload.get("repository"), reason="snapshot protocol is invalid")
    allowed = {"protocol", "repository", "default_branch", "observed_head", "files", "manifest"}
    if set(payload) != allowed:
        return _base("BLOCKED", payload.get("repository"), reason="snapshot fields are invalid")
    files = payload.get("files")
    if not isinstance(files, list) or any(not isinstance(item, str) or not item.strip() for item in files):
        return _base("BLOCKED", payload.get("repository"), reason="snapshot files must be a list of non-empty paths")
    if len(set(files)) != len(files):
        return _base("BLOCKED", payload.get("repository"), reason="snapshot files contain duplicates")
    manifest = payload.get("manifest")
    if manifest is not None and not isinstance(manifest, dict):
        return _base("BLOCKED", payload.get("repository"), reason="snapshot manifest must be an object or null")
    report = classify_observation(
        repository=payload.get("repository"),
        files=set(files),
        manifest=manifest,
        observed_head=payload.get("observed_head"),
    )
    report["default_branch"] = payload.get("default_branch")
    report["evidence_source"] = "PROVIDER_READBACK_SNAPSHOT"
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="DevOS Managed Project Lifecycle v1")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--path", help="local project directory")
    source.add_argument("--snapshot", help="provider-readback JSON snapshot")
    parser.add_argument("--apply", action="store_true", help="apply local onboarding when required")
    parser.add_argument("--authorization", choices=["EXPLICIT"], help="explicit authorization for local onboarding mutation")
    parser.add_argument("--require-managed", action="store_true", help="exit non-zero unless the final state is MANAGED")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if args.snapshot:
        if args.apply:
            report = _base("BLOCKED", None, reason="remote snapshot apply is unsupported; use a governed provider onboarding path")
        else:
            try:
                report = classify_snapshot(load_snapshot(Path(args.snapshot)))
            except (OSError, json.JSONDecodeError, ValueError) as exc:
                report = _base("BLOCKED", None, reason=f"snapshot load failed: {exc}")
    else:
        root = Path(args.path)
        report = apply_local(root, authorization=args.authorization) if args.apply else classify_local(root)

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print("DEVOS MANAGED PROJECT LIFECYCLE v1")
        print(f"Repository: {report.get('repository') or 'unknown'}")
        print(f"Status: {report.get('status')}")
        print(f"Managed: {str(report.get('managed', False)).lower()}")
        print(f"Development continuation: {'ALLOWED' if report.get('development_continuation_allowed') else 'HOLD'}")
        print(f"Next action: {report.get('next_action', 'HOLD')}")
        if report.get("reason"):
            print(f"Reason: {report['reason']}")
        print("Authority: UNCHANGED")
        print("production_ready=false")

    if args.require_managed and report.get("status") != "MANAGED":
        return 2
    return 0 if report.get("status") not in {"BLOCKED", "HOLD", "NEEDS_APPROVAL"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
