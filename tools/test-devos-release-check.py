#!/usr/bin/env python3
"""Adversarial regression corpus for the DevOS distribution release gate."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import shutil
import tempfile

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools" / "devos-release-check.py"


def load_checker():
    spec = importlib.util.spec_from_file_location("devos_release_check_test", CHECKER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fixture() -> tuple[tempfile.TemporaryDirectory[str], Path]:
    td = tempfile.TemporaryDirectory()
    root = Path(td.name) / "repo"
    shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns(".git", "__pycache__", "dist"))
    return td, root


def assert_blocked(report: dict, reason_fragment: str) -> None:
    assert report["status"] == "BLOCKED", report
    assert any(reason_fragment in reason for reason in report["reasons"]), report
    assert report["production_ready"] is False
    assert report["authority"] == "UNCHANGED"
    assert report["authorization"] == "UNCHANGED"


def different_stable_semver(version: str) -> str:
    """Return a valid stable semver guaranteed to differ from the fixture baseline."""
    parts = version.split(".")
    assert len(parts) == 3 and all(part.isdigit() for part in parts), version
    major, minor, patch = (int(part) for part in parts)
    return f"{major}.{minor}.{patch + 1}"


def main() -> None:
    checker = load_checker()
    canonical_version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()

    td, root = fixture()
    try:
        report = checker.check(root, require_git=False)
        assert report["status"] == "READY", report
        assert report["version"] == canonical_version
        assert report["production_ready"] is False
        assert report["final_ci_required"] is True
    finally:
        td.cleanup()

    td, root = fixture()
    try:
        (root / "VERSION").write_text(different_stable_semver(canonical_version) + "\n", encoding="utf-8")
        assert_blocked(checker.check(root, require_git=False), "RELEASE_MANIFEST_VERSION_MISMATCH")
    finally:
        td.cleanup()

    td, root = fixture()
    try:
        current = root / ".ai" / "CURRENT-STATE.md"
        current.write_text(current.read_text(encoding="utf-8").replace("production_ready = false", "production_ready = true"), encoding="utf-8")
        assert_blocked(checker.check(root, require_git=False), "UNSUPPORTED_PRODUCTION_READY_TRUE")
    finally:
        td.cleanup()

    td, root = fixture()
    try:
        manifest_path = root / "config" / "release-manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["authority"] = "EXPANDED"
        manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        assert_blocked(checker.check(root, require_git=False), "RELEASE_MANIFEST_AUTHORITY_INVALID")
    finally:
        td.cleanup()

    td, root = fixture()
    try:
        (root / ".github" / "SECURITY.md").unlink()
        assert_blocked(checker.check(root, require_git=False), "REQUIRED_PATH_MISSING=.github/SECURITY.md")
    finally:
        td.cleanup()

    td, root = fixture()
    try:
        readme = root / "README.md"
        readme.write_text(readme.read_text(encoding="utf-8").replace("## Release status", "## Status"), encoding="utf-8")
        assert_blocked(checker.check(root, require_git=False), "README_MARKER_MISSING=## Release status")
    finally:
        td.cleanup()

    print("PASS: DevOS distribution release gate fails closed across adversarial drift cases")
    print(f"PASS: release-version regressions derive from canonical VERSION={canonical_version}")


if __name__ == "__main__":
    main()
