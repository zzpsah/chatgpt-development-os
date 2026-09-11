#!/usr/bin/env python3
"""Deterministic repository-only DevOS bootstrap inspector.

This tool does not execute project work. It discovers the durable context a fresh
AI/tool must inspect and reports missing required context explicitly.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

REQUIRED = [
    "AGENTS.md",
    ".ai/manifest.yaml",
    ".ai/PROJECT.md",
    ".ai/CURRENT-STATE.md",
]
RECOMMENDED = [
    ".ai/STATE-INDEX.md",
    ".ai/ARCHITECTURE.md",
    ".ai/DECISIONS.md",
    ".ai/TASKS.md",
    ".ai/CHANGELOG.md",
]


def git_value(root: Path, *args: str) -> str | None:
    try:
        return subprocess.check_output(["git", *args], cwd=root, text=True).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def inspect(root: Path) -> dict[str, object]:
    required = {p: (root / p).is_file() for p in REQUIRED}
    recommended = {p: (root / p).is_file() for p in RECOMMENDED}
    missing_required = [p for p, present in required.items() if not present]
    return {
        "protocol": "DevOS Portable Project Memory Bootstrap v1",
        "repository": str(root),
        "git": {
            "branch": git_value(root, "branch", "--show-current"),
            "head": git_value(root, "rev-parse", "HEAD"),
        },
        "required_context": required,
        "recommended_context": recommended,
        "missing_required": missing_required,
        "status": "READY" if not missing_required else "INCOMPLETE",
        "authority": "repository_source_git_and_durable_ai_context",
        "execution": "NONE",
        "authorization": "UNCHANGED",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect DevOS portable project memory for a fresh AI/tool")
    parser.add_argument("path", nargs="?", default=".")
    args = parser.parse_args()
    root = Path(args.path).resolve()
    result = inspect(root)
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["status"] == "READY" else 2)


if __name__ == "__main__":
    main()
