#!/usr/bin/env python3
"""Enforce the DevOS rule: what is not written was never done.

This verifier checks the latest commit boundary. Material implementation changes
must land with a durable documentation/contract record in the same commit.
It is intentionally deterministic and does not attempt to infer semantic
completeness from filenames or AI/session claims.
"""

from __future__ import annotations

import subprocess
import sys

MATERIAL_EXTENSIONS = {
    ".py", ".ps1", ".sh", ".yml", ".yaml", ".json", ".toml",
}
DOC_PREFIXES = (".ai/", "core/", "workflows/", "rules/", "docs/")
DOC_EXACT = {
    "AGENTS.md",
    "CHANGELOG.md",
    "README.md",
}
IGNORED_PREFIXES = (".git/",)


def changed_files() -> list[str]:
    try:
        out = subprocess.check_output(
            ["git", "diff", "--name-only", "HEAD^", "HEAD"],
            text=True,
            stderr=subprocess.STDOUT,
        )
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        print(f"FAIL: unable to inspect latest commit boundary: {exc}")
        raise SystemExit(1)
    return [line.strip() for line in out.splitlines() if line.strip()]


def is_material(path: str) -> bool:
    if path.startswith(IGNORED_PREFIXES):
        return False
    if path.startswith(DOC_PREFIXES) or path in DOC_EXACT:
        return False
    if path.startswith(".github/"):
        # Workflow changes are material and need a durable record.
        return True
    if path.startswith("tests/") or path.startswith("tools/"):
        return True
    return any(path.endswith(ext) for ext in MATERIAL_EXTENSIONS)


def is_durable_record(path: str) -> bool:
    return path.startswith(DOC_PREFIXES) or path in DOC_EXACT


def main() -> None:
    files = changed_files()
    material = [p for p in files if is_material(p)]
    durable = [p for p in files if is_durable_record(p)]

    assert "core/documentation-integrity.md" in files or "core/documentation-integrity.md" in durable, (
        "documentation integrity contract must be present"
    )

    if material and not durable:
        print("FAIL: material implementation change has no durable documentation in the same commit")
        print("Material changes:")
        for path in material:
            print(f"  - {path}")
        print("Required: update the affected .ai/core/workflows/rules/docs record in the same commit.")
        raise SystemExit(1)

    if material:
        print("PASS: material changes have a durable documentation record in the same commit")
    else:
        print("PASS: latest commit contains no material implementation change requiring a durable record")

    print("PASS: Documentation Integrity Contract v1")


if __name__ == "__main__":
    main()
