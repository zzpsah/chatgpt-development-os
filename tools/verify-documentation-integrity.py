#!/usr/bin/env python3
"""Enforce the DevOS rule: what is not written was never done."""
from __future__ import annotations

import subprocess

DOC_PREFIXES = (".ai/", "core/", "workflows/", "rules/", "docs/")
DOC_EXACT = {"AGENTS.md", "CHANGELOG.md", "README.md"}


def changed_files() -> list[str]:
    try:
        out = subprocess.check_output(["git", "diff", "--name-only", "HEAD^", "HEAD"], text=True)
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        print(f"FAIL: unable to inspect latest commit boundary: {exc}")
        raise SystemExit(1) from exc
    return [line.strip() for line in out.splitlines() if line.strip()]


def is_durable_record(path: str) -> bool:
    return path.startswith(DOC_PREFIXES) or path in DOC_EXACT


def is_material(path: str) -> bool:
    if path.startswith(".git/") or is_durable_record(path):
        return False
    return path.startswith(("tools/", "tests/", ".github/")) or path.endswith((".py", ".ps1", ".sh", ".yml", ".yaml", ".json", ".toml"))


def main() -> None:
    files = changed_files()
    material = [p for p in files if is_material(p)]
    durable = [p for p in files if is_durable_record(p)]
    if material and not durable:
        print("FAIL: material implementation change has no durable documentation in the same commit")
        for path in material:
            print(f"  - {path}")
        print("Required: update the affected .ai/core/workflows/rules/docs record in the same commit.")
        raise SystemExit(1)
    print("PASS: material changes have a durable documentation record in the same commit" if material else "PASS: latest commit has no material implementation change requiring a durable record")
    print("PASS: Documentation Integrity Contract v1")


if __name__ == "__main__":
    main()
