#!/usr/bin/env python3
"""Integration checks for the bounded verification adapter."""
from pathlib import Path
import importlib.util
import tempfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("verification", ROOT / "adapters" / "reference-verification.py")
verification = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verification)

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)

    good = verification.run_verification(root, {
        "id": "python-check",
        "command": ["python", "-c", "print('ok')"],
        "timeout_seconds": 30,
        "expected_exit_codes": [0],
    })
    assert good["status"] == "VERIFIED"
    assert good["exit_status"] == 0

    bad = verification.run_verification(root, {
        "id": "expected-failure",
        "command": ["python", "-c", "raise SystemExit(2)"],
        "timeout_seconds": 30,
        "expected_exit_codes": [0],
    })
    assert bad["status"] == "FAILED"

    invalid = verification.run_verification(root, {
        "id": "invalid",
        "command": "python -c pass",
        "timeout_seconds": 30,
    })
    assert invalid["status"] == "BLOCKED"

print("Verification adapter integration checks passed.")
