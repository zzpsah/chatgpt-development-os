#!/usr/bin/env python3
"""Minimal runtime-to-reference-adapter bridge.

The bridge deliberately accepts only declared, bounded operations. It is a
reference implementation, not a general-purpose shell executor.
"""
from __future__ import annotations

from pathlib import Path
import importlib.util
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("reference_host", ROOT / "adapters" / "reference-host.py")
adapter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adapter)


def execute(request: dict[str, Any], project_root: Path) -> dict[str, Any]:
    operation = request.get("operation")
    target = request.get("target")
    scope = request.get("scope")
    authorization = request.get("authorization", "NOT_REQUIRED")

    if not operation or target is None or not scope:
        return {"status": "BLOCKED", "reason": "operation, target, and scope are required"}

    if operation == "filesystem.read":
        return adapter.read_text(project_root, target)

    if operation == "filesystem.write_scoped":
        if authorization != "ALREADY_GRANTED":
            return {"status": "BLOCKED", "reason": "explicit authorization required for mutation"}
        content = request.get("content")
        if not isinstance(content, str):
            return {"status": "BLOCKED", "reason": "write content is required"}
        return adapter.write_text(project_root, target, content)

    if operation == "git.inspect":
        return adapter.git_inspect(project_root, target or "status")

    return {"status": "UNAVAILABLE", "reason": "operation not supported by reference bridge"}
