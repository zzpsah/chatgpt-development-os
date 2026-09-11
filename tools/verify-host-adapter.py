#!/usr/bin/env python3
"""Static contract checks for Host Adapter Contract v1."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read(path):
    return (ROOT / path).read_text(encoding="utf-8")

def require(text, needles, source):
    for needle in needles:
        assert needle in text, f"missing {needle!r} in {source}"

contract = read("core/host-adapter-contract.md")
adapter = read("adapters/host-adapter.md")
roadmap = read("docs/ROADMAP.md")
architecture = read("docs/ARCHITECTURE.md")

require(contract, [
    "Capability lookup", "Authorization / Security Gate", "Actual result", "Evidence normalization",
    "AVAILABLE | DELEGATABLE | MISSING",
    "filesystem", "Git", "Verification", "GitHub / CI",
    "explicit scope", "No authorization is created by the adapter",
    "must not be simulated", "never fabricate command output",
    "Production, destructive, irreversible, security-sensitive, and data-affecting",
    "BLOCKED", "FAILED", "UNAVAILABLE", "bounded",
], "core/host-adapter-contract.md")

require(adapter, [
    "Capability discovery", "filesystem.read", "filesystem.write_scoped", "git.inspect",
    "verification.run", "github.inspect", "github.mutate",
    "Validate target + scope", "Check authorization", "Capture actual result",
    "never simulated", "never convert that condition into `VERIFIED`",
], "adapters/host-adapter.md")

require(roadmap, [
    "P6 — Host Execution Adapters",
    "[x] Define host adapter contract",
    "[x] Define capability discovery and honest availability states",
    "[x] Define scoped filesystem, Git, verification, and GitHub/CI boundaries",
    "[x] Define normalized execution evidence and failure semantics",
], "docs/ROADMAP.md")

require(architecture, ["AI Adapter Contract", "Executable Development Runtime"], "docs/ARCHITECTURE.md")

print("Host Adapter Contract v1 checks passed.")
