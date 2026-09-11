#!/usr/bin/env python3
"""Bounded reference verification adapter.

Commands must be supplied explicitly. No shell is used: argv execution avoids
implicit shell interpretation and keeps the reference adapter deliberately small.
"""
from __future__ import annotations

import subprocess
import time
from pathlib import Path
from typing import Any


def run_verification(project_root: Path, verification: dict[str, Any]) -> dict[str, Any]:
    command = verification.get("command")
    if not isinstance(command, list) or not command or not all(isinstance(x, str) for x in command):
        return {"status": "BLOCKED", "reason": "verification command must be an explicit argv list"}

    timeout = verification.get("timeout_seconds", 300)
    if not isinstance(timeout, int) or timeout <= 0 or timeout > 1800:
        return {"status": "BLOCKED", "reason": "timeout outside reference adapter bounds"}

    expected = verification.get("expected_exit_codes", [0])
    if not isinstance(expected, list) or not all(isinstance(x, int) for x in expected):
        return {"status": "BLOCKED", "reason": "invalid expected exit codes"}

    started = time.monotonic()
    try:
        result = subprocess.run(
            command,
            cwd=project_root,
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
    except FileNotFoundError as exc:
        return {"status": "UNAVAILABLE", "reason": str(exc)}
    except subprocess.TimeoutExpired:
        return {"status": "FAILED", "reason": "verification timed out", "duration_seconds": time.monotonic() - started}

    status = "VERIFIED" if result.returncode in expected else "FAILED"
    return {
        "status": status,
        "verification_id": verification.get("id", "unnamed"),
        "command": command,
        "exit_status": result.returncode,
        "duration_seconds": time.monotonic() - started,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }
