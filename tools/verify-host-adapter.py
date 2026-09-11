#!/usr/bin/env python3
"""Static and reference-implementation checks for Host Adapter v1."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

def read(path):
    return (ROOT / path).read_text(encoding="utf-8")

def require(text, needles, source):
    for needle in needles:
        assert needle in text, f"missing {needle!r} in {source}"

contract = read("core/host-adapter-contract.md")
adapter = read("adapters/host-adapter.md")
reference = read("adapters/reference-host.py")
bridge = read("tools/runtime-adapter-bridge.py")
roadmap = read("docs/ROADMAP.md")
architecture = read("docs/ARCHITECTURE.md")

require(contract, ["Capability lookup", "Authorization / Security Gate", "Actual result", "Evidence normalization", "AVAILABLE | DELEGATABLE | MISSING", "filesystem", "Git", "Verification", "GitHub / CI", "explicit scope", "No authorization is created by the adapter", "must not be simulated", "never fabricate command output", "Production, destructive, irreversible, security-sensitive, and data-affecting", "BLOCKED", "FAILED", "UNAVAILABLE", "bounded"], "core/host-adapter-contract.md")
require(adapter, ["Capability discovery", "filesystem.read", "filesystem.write_scoped", "git.inspect", "verification.run", "github.inspect", "github.mutate", "Validate target + scope", "Check authorization", "Capture actual result", "never simulated", "never convert that condition into `VERIFIED`"], "adapters/host-adapter.md")
require(reference, ["SAFE_CAPABILITIES", "filesystem.read", "filesystem.write_scoped", "git.inspect", "capability_status", "target outside project root", "subprocess.run"], "adapters/reference-host.py")
require(bridge, ["filesystem.read", "filesystem.write_scoped", "git.inspect", "explicit authorization required for mutation", "UNAVAILABLE"], "tools/runtime-adapter-bridge.py")
require(roadmap, ["P6 — Host Execution Adapters", "[x] Define host adapter contract", "[x] Define capability discovery and honest availability states", "[x] Define scoped filesystem, Git, verification, and GitHub/CI boundaries", "[x] Define normalized execution evidence and failure semantics"], "docs/ROADMAP.md")
require(architecture, ["Host Execution Adapters", "Executable Development Runtime"], "docs/ARCHITECTURE.md")

for test in ("test-reference-host-adapter.py", "test-runtime-adapter-bridge.py"):
    result = subprocess.run([sys.executable, str(ROOT / "tools" / test)], text=True, capture_output=True, check=False)
    assert result.returncode == 0, result.stdout + result.stderr

print("Host Adapter v1 contract and reference integration checks passed.")
