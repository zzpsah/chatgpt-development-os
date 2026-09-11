#!/usr/bin/env python3
"""Integration-style tests for the portable reference host adapter."""
from pathlib import Path
import importlib.util
import tempfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("reference_host", ROOT / "adapters" / "reference-host.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    assert module.capability_status("filesystem.read") == "AVAILABLE"
    assert module.capability_status("unknown.capability") == "MISSING"

    result = module.write_text(root, "nested/example.txt", "hello")
    assert result["status"] == "SUCCESS"
    assert module.read_text(root, "nested/example.txt")["content"] == "hello"

    escaped = module.read_text(root, "../outside.txt")
    assert escaped["status"] == "BLOCKED"

print("Reference host adapter integration checks passed.")
