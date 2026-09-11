#!/usr/bin/env python3
"""Checks the runtime-to-reference-adapter bridge safety boundary."""
from pathlib import Path
import tempfile
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("bridge", ROOT / "tools" / "runtime-adapter-bridge.py")
bridge = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bridge)

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)

    blocked = bridge.execute({
        "operation": "filesystem.write_scoped",
        "target": "a.txt",
        "scope": "write only a.txt",
        "authorization": "NOT_REQUIRED",
        "content": "x",
    }, root)
    assert blocked["status"] == "BLOCKED"

    written = bridge.execute({
        "operation": "filesystem.write_scoped",
        "target": "a.txt",
        "scope": "write only a.txt",
        "authorization": "ALREADY_GRANTED",
        "content": "x",
    }, root)
    assert written["status"] == "SUCCESS"

    read = bridge.execute({
        "operation": "filesystem.read",
        "target": "a.txt",
        "scope": "read only a.txt",
    }, root)
    assert read["status"] == "SUCCESS"
    assert read["content"] == "x"

    unsupported = bridge.execute({
        "operation": "production.deploy",
        "target": "production",
        "scope": "deploy",
    }, root)
    assert unsupported["status"] == "UNAVAILABLE"

print("Runtime-adapter bridge checks passed.")
