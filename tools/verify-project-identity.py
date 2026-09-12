#!/usr/bin/env python3
"""Verify the automatic DevOS project identity discovery contract and mismatch guard."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "discover-project-identity.py"
MANIFEST = ROOT / ".ai" / "manifest.yaml"
REGISTRY = ROOT / "projects" / "registry.md"
EXPECTED_REPOSITORY = "zzpsah/chatgpt-development-os"
EXPECTED_URL = "https://github.com/zzpsah/chatgpt-development-os"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def run_identity(observed_repository: str) -> dict[str, object]:
    env = os.environ.copy()
    env.pop("DEVOS_WRITE_IDENTITY", None)
    env["GITHUB_REPOSITORY"] = observed_repository
    result = subprocess.run(
        [sys.executable, str(TOOL)],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(result.stdout)


def main() -> None:
    require(TOOL.is_file(), "project identity discovery tool is missing")
    text = TOOL.read_text(encoding="utf-8")
    for needle in (
        "remote.origin.url",
        "GITHUB_REPOSITORY",
        ".ai/manifest.yaml",
        "project_id",
        "canonical_repository",
        "canonical_url",
        "canonical_alias",
        "observed_repository",
        "repository_match",
        "identity_status",
        "CONFLICT",
        "identity_source",
        "confidence",
        '"UNKNOWN"',
        "DEVOS_WRITE_IDENTITY",
        "non-destructive",
        "application source",
    ):
        require(needle in text, f"identity discovery contract missing {needle!r}")
    require("manifest" in text and "github-ci" in text and "git-remote" in text, "identity source precedence must be explicit")

    manifest = MANIFEST.read_text(encoding="utf-8")
    require(f"canonical_repository: {EXPECTED_REPOSITORY}" in manifest, "canonical repository missing from manifest")
    require(f"canonical_url: {EXPECTED_URL}" in manifest, "canonical URL missing from manifest")
    require("canonical_alias: DEVOS" in manifest, "canonical DEVOS alias missing from manifest")

    registry = REGISTRY.read_text(encoding="utf-8")
    require("DevOS / Development OS" in registry, "DevOS alias is missing from project registry")
    require(EXPECTED_REPOSITORY in registry, "canonical DevOS repository is missing from project registry")

    verified = run_identity(EXPECTED_REPOSITORY)
    require(verified["repository"] == EXPECTED_REPOSITORY, "canonical repository must be returned when observed repository matches")
    require(verified["canonical_url"] == EXPECTED_URL, "canonical URL must be recoverable")
    require(verified["canonical_alias"] == "DEVOS", "canonical alias must be recoverable")
    require(verified["identity_status"] == "VERIFIED", "matching observed repository must verify identity")
    require(verified["repository_match"] is True, "matching observed repository must report repository_match=true")

    conflict = run_identity("SamyPesse/devos")
    require(conflict["repository"] == EXPECTED_REPOSITORY, "canonical repository must not be replaced by a name-similar observed repository")
    require(conflict["observed_repository"] == "SamyPesse/devos", "conflicting observed repository must remain visible as evidence")
    require(conflict["identity_status"] == "CONFLICT", "repository mismatch must be surfaced as CONFLICT")
    require(conflict["repository_match"] is False, "repository mismatch must report repository_match=false")
    require(conflict["confidence"] == "low", "repository mismatch must lower identity confidence")

    print("PASS: automatic DevOS project identity discovery contract is structurally valid")
    print("PASS: DEVOS resolves to zzpsah/chatgpt-development-os from durable repository evidence")
    print("PASS: a name-similar wrong repository is surfaced as CONFLICT instead of silently accepted")
    print("NOTE: identity discovery remains non-destructive by default")


if __name__ == "__main__":
    main()
