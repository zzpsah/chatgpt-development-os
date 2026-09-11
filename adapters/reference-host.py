#!/usr/bin/env python3
"""Portable reference host adapter for bounded DevOS operations."""
from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

SAFE_CAPABILITIES = {
    "filesystem.read",
    "filesystem.write_scoped",
    "git.inspect",
    "verification.run",
}


def capability_status(name: str) -> str:
    return "AVAILABLE" if name in SAFE_CAPABILITIES else "MISSING"


def _inside(root: Path, target: Path) -> bool:
    root = root.resolve()
    target = target.resolve()
    return target == root or root in target.parents


def read_text(root: Path, relative_path: str) -> dict[str, Any]:
    target = (root / relative_path).resolve()
    if not _inside(root, target):
        return {"status": "BLOCKED", "reason": "target outside project root"}
    if not target.is_file():
        return {"status": "FAILED", "reason": "file not found"}
    return {"status": "SUCCESS", "path": relative_path, "content": target.read_text(encoding="utf-8")}


def write_text(root: Path, relative_path: str, content: str, authorization: str) -> dict[str, Any]:
    if authorization != "ALREADY_GRANTED":
        return {"status": "BLOCKED", "reason": "explicit authorization required"}
    target = (root / relative_path).resolve()
    if not _inside(root, target):
        return {"status": "BLOCKED", "reason": "target outside project root"}
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return {"status": "SUCCESS", "path": relative_path, "bytes": len(content.encode("utf-8"))}


def git_inspect(root: Path, operation: str = "status") -> dict[str, Any]:
    allowed = {"status", "diff", "log", "rev-parse"}
    if operation not in allowed:
        return {"status": "BLOCKED", "reason": "git operation not allowed by reference adapter"}
    args = {
        "status": ["status", "--short"],
        "diff": ["diff", "--no-ext-diff"],
        "log": ["log", "-5", "--oneline"],
        "rev-parse": ["rev-parse", "HEAD"],
    }[operation]
    result = subprocess.run(["git", *args], cwd=root, text=True, capture_output=True, check=False)
    return {
        "status": "SUCCESS" if result.returncode == 0 else "FAILED",
        "operation": operation,
        "exit_status": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="DevOS reference host adapter")
    parser.add_argument("root", type=Path)
    args = parser.parse_args()
    print({name: capability_status(name) for name in sorted(SAFE_CAPABILITIES)})
    print(git_inspect(args.root))
