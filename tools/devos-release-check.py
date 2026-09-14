#!/usr/bin/env python3
"""Fail-closed engineering distribution release gate for DevOS.

This gate validates repository/version/documentation/security/release metadata and,
for normal CLI use, exact Git checkout state. It does not publish a release, create
a tag, deploy anything, grant authority, or change production readiness.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import subprocess
from typing import Any

PROTOCOL = "DEVOS-DISTRIBUTION-RELEASE-CHECK-v1"
MANIFEST_PROTOCOL = "DEVOS-DISTRIBUTION-RELEASE-MANIFEST-v1"
CANONICAL_REPOSITORY = "zzpsah/chatgpt-development-os"
VERSION_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
BOUNDARIES = {
    "authority": "UNCHANGED",
    "authorization": "UNCHANGED",
    "execution": "NONE",
    "mutation": "NONE",
    "production_ready": False,
}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _git(root: Path, *args: str) -> tuple[int, str, str]:
    try:
        proc = subprocess.run(
            ["git", *args], cwd=root, text=True, capture_output=True, check=False
        )
        return proc.returncode, proc.stdout.strip(), proc.stderr.strip()
    except OSError as exc:
        return 127, "", str(exc)


def check(root: Path, *, require_git: bool = True) -> dict[str, Any]:
    root = root.resolve()
    reasons: list[str] = []
    evidence: dict[str, Any] = {}

    version_path = root / "VERSION"
    manifest_path = root / "config" / "release-manifest.json"
    if not version_path.is_file():
        reasons.append("VERSION_MISSING")
        version = None
    else:
        version = _read(version_path).strip()
        if not VERSION_RE.fullmatch(version):
            reasons.append("VERSION_NOT_STABLE_SEMVER")
    evidence["version"] = version

    manifest: dict[str, Any] = {}
    if not manifest_path.is_file():
        reasons.append("RELEASE_MANIFEST_MISSING")
    else:
        try:
            loaded = json.loads(_read(manifest_path))
            if not isinstance(loaded, dict):
                reasons.append("RELEASE_MANIFEST_NOT_OBJECT")
            else:
                manifest = loaded
        except json.JSONDecodeError:
            reasons.append("RELEASE_MANIFEST_JSON_INVALID")

    expected_manifest = {
        "protocol": MANIFEST_PROTOCOL,
        "canonical_repository": CANONICAL_REPOSITORY,
        "channel": "stable",
        "minimum_python": "3.11",
        "entrypoint": "python tools/devos.py",
        "release_gate": "python tools/devos-release-check.py",
        "artifact_strategy": "git-archive-source-zip-with-sha256",
        **BOUNDARIES,
        "distribution_release_claim": "CI_REQUIRED",
    }
    for key, expected in expected_manifest.items():
        if manifest.get(key) != expected:
            reasons.append(f"RELEASE_MANIFEST_{key.upper()}_INVALID")
    if version is not None and manifest.get("version") != version:
        reasons.append("RELEASE_MANIFEST_VERSION_MISMATCH")

    publication = manifest.get("publication")
    if not isinstance(publication, dict) or publication != {
        "automatic_release": False,
        "automatic_tag": False,
        "automatic_deploy": False,
    }:
        reasons.append("RELEASE_MANIFEST_PUBLICATION_BOUNDARY_INVALID")

    required_paths = manifest.get("required_paths")
    if not isinstance(required_paths, list) or not required_paths or any(
        not isinstance(item, str) or not item.strip() for item in required_paths
    ):
        reasons.append("RELEASE_MANIFEST_REQUIRED_PATHS_INVALID")
    else:
        for rel in required_paths:
            candidate = (root / rel).resolve()
            try:
                inside = candidate.is_relative_to(root)
            except AttributeError:  # pragma: no cover - compatibility fallback
                inside = str(candidate).startswith(str(root) + os.sep)
            if not inside:
                reasons.append(f"REQUIRED_PATH_ESCAPES_ROOT={rel}")
            elif not candidate.is_file():
                reasons.append(f"REQUIRED_PATH_MISSING={rel}")

    boundaries = manifest.get("release_boundaries")
    if not isinstance(boundaries, list) or len(boundaries) < 4 or any(
        not isinstance(item, str) or not item.strip() for item in boundaries
    ):
        reasons.append("RELEASE_BOUNDARIES_INCOMPLETE")

    readme_path = root / "README.md"
    if readme_path.is_file():
        readme = _read(readme_path)
        required_readme_markers = [
            "## Quick start",
            "## Release status",
            "python tools/devos.py version",
            "python tools/devos.py release-check",
        ]
        for marker in required_readme_markers:
            if marker not in readme:
                reasons.append(f"README_MARKER_MISSING={marker}")
        if version and f"**{version}**" not in readme:
            reasons.append("README_VERSION_MISMATCH")
    else:
        reasons.append("README_MISSING")

    manifest_ai = root / ".ai" / "manifest.yaml"
    if not manifest_ai.is_file() or f"canonical_repository: {CANONICAL_REPOSITORY}" not in _read(manifest_ai):
        reasons.append("CANONICAL_REPOSITORY_IDENTITY_INVALID")

    for rel in (".ai/CURRENT-STATE.md", ".ai/TASKS.md"):
        path = root / rel
        if not path.is_file():
            reasons.append(f"DURABLE_STATE_MISSING={rel}")
            continue
        text = _read(path).lower()
        if re.search(r"production_ready\s*=\s*true", text):
            reasons.append(f"UNSUPPORTED_PRODUCTION_READY_TRUE={rel}")
        if "production_ready = false" not in text:
            reasons.append(f"PRODUCTION_BOUNDARY_MARKER_MISSING={rel}")

    security = root / ".github" / "SECURITY.md"
    if security.is_file():
        sec_text = _read(security)
        for marker in ("# Security Policy", "Do not include secrets", "production_ready = false"):
            if marker not in sec_text:
                reasons.append(f"SECURITY_MARKER_MISSING={marker}")

    release_doc = root / "docs" / "RELEASE.md"
    if release_doc.is_file():
        rel_text = _read(release_doc)
        for marker in (
            "Distribution release readiness is not production readiness",
            "git archive",
            "SHA-256",
            "production_ready = false",
        ):
            if marker not in rel_text:
                reasons.append(f"RELEASE_DOC_MARKER_MISSING={marker}")

    if require_git:
        rc, head, err = _git(root, "rev-parse", "HEAD")
        if rc != 0 or not re.fullmatch(r"[0-9a-f]{40}", head):
            reasons.append("GIT_HEAD_UNAVAILABLE")
            evidence["git_error"] = err
        else:
            evidence["git_head"] = head
            expected_head = os.environ.get("DEVOS_EXPECTED_HEAD") or os.environ.get("GITHUB_SHA")
            if expected_head and expected_head != head:
                reasons.append("GIT_HEAD_EXPECTATION_MISMATCH")
                evidence["expected_head"] = expected_head
        rc, status, err = _git(root, "status", "--porcelain")
        if rc != 0:
            reasons.append("GIT_STATUS_UNAVAILABLE")
            evidence["git_status_error"] = err
        elif status:
            reasons.append("GIT_WORKTREE_DIRTY")
            evidence["dirty_entries"] = status.splitlines()

    status = "READY" if not reasons else "BLOCKED"
    return {
        "protocol": PROTOCOL,
        "status": status,
        "version": version,
        "canonical_repository": CANONICAL_REPOSITORY,
        "reasons": sorted(set(reasons)),
        "evidence": evidence,
        "scope": "ENGINEERING_DISTRIBUTION_RELEASE_READINESS",
        "final_ci_required": True,
        **BOUNDARIES,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--no-git", action="store_true", help="Skip Git checkout checks (unit-test/support use only).")
    args = parser.parse_args()
    report = check(Path(args.root), require_git=not args.no_git)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"DEVOS RELEASE CHECK: {report['status']}")
        print(f"Version: {report.get('version')}")
        print(f"Scope: {report['scope']}")
        if report["reasons"]:
            for reason in report["reasons"]:
                print(f"- {reason}")
        else:
            print("- repository metadata, safety boundaries, documentation, and Git checkout are release-gate consistent")
        print("- production_ready=false; this gate does not authorize deployment or publication")
    return 0 if report["status"] == "READY" else 2


if __name__ == "__main__":
    raise SystemExit(main())
