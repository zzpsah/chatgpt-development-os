#!/usr/bin/env python3
"""Safely reconcile deterministic derived context files.

Semantic project files are never overwritten by this tool.
"""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

ROOT = Path.cwd()
CONTEXT = ROOT / os.environ.get("DEVOS_CONTEXT_DIRECTORY", ".ai")
DERIVED = {"STATE-INDEX.md", "CHANGELOG.md", "PROJECT-IDENTITY.json"}


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=False)


def main() -> None:
    requested = [p.strip() for p in os.environ.get("DEVOS_RECONCILE_FILES", "STATE-INDEX.md,CHANGELOG.md").split(",") if p.strip()]
    unsafe = sorted(set(requested) - DERIVED)
    if unsafe:
        raise SystemExit(f"BLOCKED: semantic/non-derived files cannot be auto-reconciled: {', '.join(unsafe)}")

    missing = [name for name in requested if not (CONTEXT / name).exists()]
    if missing:
        # This tool intentionally delegates regeneration to the canonical sync implementation.
        print("REPAIR_REQUIRED:", ", ".join(missing))
        print("ACTION: run tools/context-sync.py with the normal project evidence inputs")
        return

    print("SAFE: requested derived context files exist and are eligible for deterministic reconciliation")
    print("NOOP: this tool does not modify semantic project state")


if __name__ == "__main__":
    main()
