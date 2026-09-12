#!/usr/bin/env python3
"""Discover a project's durable DevOS identity from repository evidence.

The tool is intentionally non-destructive by default. It can emit a stable
identity document without changing application source. An existing
`.ai/manifest.yaml` is authoritative for declared identity; Git/CI metadata is
observed evidence. Conflicts are reported rather than guessed or silently
accepted.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
from pathlib import Path

ROOT = Path.cwd()
MANIFEST = ROOT / ".ai" / "manifest.yaml"
IDENTITY = ROOT / ".ai" / "PROJECT-IDENTITY.json"


def run(*args: str) -> str:
    result = subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=False)
    return result.stdout.strip()


def repo_from_remote() -> str | None:
    remote = run("git", "config", "--get", "remote.origin.url")
    if not remote:
        return None
    remote = remote.removesuffix("/")
    match = re.search(r"github\.com[/:]([^/]+)/([^/]+?)(?:\.git)?$", remote)
    if match:
        return f"{match.group(1)}/{match.group(2)}"
    return None


def yaml_value(text: str, key: str) -> str | None:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith(key + ":"):
            return stripped.split(":", 1)[1].strip().strip('"').strip("'")
    return None


def discover() -> dict[str, object]:
    manifest: dict[str, str] = {}
    if MANIFEST.exists():
        text = MANIFEST.read_text(encoding="utf-8")
        for key in (
            "context_version",
            "specification",
            "project_id",
            "name",
            "managed_by",
            "canonical_repository",
            "canonical_url",
            "canonical_alias",
        ):
            value = yaml_value(text, key)
            if value:
                manifest[key] = value

    github_repository = os.environ.get("GITHUB_REPOSITORY")
    observed_repository = github_repository or repo_from_remote()
    observed_source = "github-ci" if github_repository else "git-remote" if observed_repository else "none"
    canonical_repository = manifest.get("canonical_repository")
    repository = canonical_repository or observed_repository or "UNKNOWN"

    if canonical_repository and observed_repository:
        repository_match: bool | None = canonical_repository.lower() == observed_repository.lower()
        identity_status = "VERIFIED" if repository_match else "CONFLICT"
    elif canonical_repository:
        repository_match = None
        identity_status = "DECLARED"
    elif observed_repository:
        repository_match = None
        identity_status = "OBSERVED"
    else:
        repository_match = None
        identity_status = "UNKNOWN"

    project_id = manifest.get("project_id")
    if not project_id and repository != "UNKNOWN":
        project_id = repository
    if not project_id:
        project_id = "UNKNOWN"

    name = manifest.get("name")
    if not name:
        package = ROOT / "package.json"
        pyproject = ROOT / "pyproject.toml"
        if package.exists():
            try:
                name = json.loads(package.read_text(encoding="utf-8")).get("name")
            except (json.JSONDecodeError, OSError):
                name = None
        if not name and pyproject.exists():
            text = pyproject.read_text(encoding="utf-8")
            match = re.search(r"^name\s*=\s*[\"']([^\"']+)[\"']", text, re.MULTILINE)
            name = match.group(1) if match else None
    if not name:
        name = Path(repository.split("/", 1)[-1]).name if repository != "UNKNOWN" else ROOT.name

    managed_by = manifest.get("managed_by", "unknown")
    managed = managed_by == "development-os" or MANIFEST.exists() or (ROOT / "AGENTS.md").exists()

    if identity_status == "VERIFIED":
        confidence = "high"
    elif identity_status in {"DECLARED", "OBSERVED"}:
        confidence = "medium"
    else:
        confidence = "low"

    canonical_url = manifest.get("canonical_url")
    if not canonical_url and canonical_repository:
        canonical_url = f"https://github.com/{canonical_repository}"

    return {
        "identity_version": 2,
        "project_id": project_id,
        "name": name,
        "repository": repository,
        "canonical_repository": canonical_repository or "UNKNOWN",
        "canonical_url": canonical_url or "UNKNOWN",
        "canonical_alias": manifest.get("canonical_alias", "UNKNOWN"),
        "observed_repository": observed_repository or "UNKNOWN",
        "observed_repository_source": observed_source,
        "repository_match": repository_match,
        "identity_status": identity_status,
        "managed_by": managed_by,
        "devos_managed": managed,
        "identity_source": "manifest" if MANIFEST.exists() else observed_source if observed_source != "none" else "filesystem",
        "manifest_context_version": manifest.get("context_version", "UNKNOWN"),
        "manifest_specification": manifest.get("specification", "UNKNOWN"),
        "confidence": confidence,
    }


def main() -> None:
    result = discover()
    print(json.dumps(result, indent=2, sort_keys=True))
    if os.environ.get("DEVOS_WRITE_IDENTITY", "false").lower() == "true":
        IDENTITY.parent.mkdir(parents=True, exist_ok=True)
        IDENTITY.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"WROTE: {IDENTITY}")


if __name__ == "__main__":
    main()
