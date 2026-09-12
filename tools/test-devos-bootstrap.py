#!/usr/bin/env python3
"""Executable proof that DevOS portable memory is discoverable from a fresh repo path."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "devos-bootstrap.py"


def run() -> dict[str, object]:
    completed = subprocess.run(
        [sys.executable, str(TOOL), str(ROOT)],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


first = run()
second = run()
assert first == second, "bootstrap output is not deterministic"
assert first["status"] == "READY", first
assert not first["missing_required"], first
assert first["execution"] == "NONE", first
assert first["authorization"] == "UNCHANGED", first
assert first["authority"] == "repository_source_git_and_durable_ai_context", first
assert all(first["required_context"].values()), first
print("DevOS portable-memory bootstrap proof: PASS")
