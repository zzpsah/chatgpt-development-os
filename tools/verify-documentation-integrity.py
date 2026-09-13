#!/usr/bin/env python3
"""Enforce DevOS documentation integrity at the latest Git change boundary."""
from __future__ import annotations

import subprocess
from typing import Iterable

DURABLE_PREFIXES = (".ai/", "docs/")
DURABLE_EXACT = {"AGENTS.md", "CHANGELOG.md", "README.md"}
MATERIAL_PREFIXES = ("tools/", "tests/", "core/", "workflows/", "rules/", ".github/")
MATERIAL_SUFFIXES = (".py", ".ps1", ".sh", ".yml", ".yaml", ".json", ".toml")


def changed_files() -> list[str]:
    try:
        out = subprocess.check_output(
            ["git", "diff", "--name-only", "HEAD^", "HEAD"],
            text=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        print(f"FAIL: unable to inspect latest commit boundary: {exc}")
        raise SystemExit(1) from exc
    return [line.strip() for line in out.splitlines() if line.strip()]


def is_durable_record(path: str) -> bool:
    return path.startswith(DURABLE_PREFIXES) or path in DURABLE_EXACT


def is_material(path: str) -> bool:
    if path.startswith(".git/") or is_durable_record(path):
        return False
    return path.startswith(MATERIAL_PREFIXES) or path.endswith(MATERIAL_SUFFIXES)


def evaluate_paths(paths: Iterable[str]) -> dict[str, object]:
    files = [str(path).strip() for path in paths if str(path).strip()]
    material = [path for path in files if is_material(path)]
    durable = [path for path in files if is_durable_record(path)]
    ok = not material or bool(durable)
    return {
        "ok": ok,
        "files": files,
        "material": material,
        "durable": durable,
    }


def main() -> None:
    result = evaluate_paths(changed_files())
    material = result["material"]
    durable = result["durable"]

    if not result["ok"]:
        print("FAIL: material implementation change has no durable documentation in the same change boundary")
        for path in material:
            print(f"  - {path}")
        print("Required: update an affected .ai/docs/AGENTS.md/CHANGELOG.md/README.md record in the same bounded change.")
        raise SystemExit(1)

    if material:
        print("PASS: material changes have a durable documentation record in the same change boundary")
        for path in durable:
            print(f"  documented-by: {path}")
    else:
        print("PASS: latest change boundary has no material implementation change requiring a durable record")
    print("PASS: Documentation Integrity Contract v1")


if __name__ == "__main__":
    main()
