#!/usr/bin/env python3
"""Static contract checks for External Integration Adapter v1."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read(path):
    return (ROOT / path).read_text(encoding="utf-8")

def require(text, needles, source):
    for needle in needles:
        assert needle in text, f"missing {needle!r} in {source}"

contract = read("core/external-integration-adapter.md")
github = read("adapters/github-integration.md")
roadmap = read("docs/ROADMAP.md")
architecture = read("docs/ARCHITECTURE.md")

require(contract, [
    "provider capability discovery", "target + scope validation", "authorization / Security Gate",
    "actual provider response", "AVAILABLE | DELEGATABLE | MISSING",
    "Read-only", "Mutating", "Remote mutations require an authorized work unit",
    "Only an actual provider response is execution evidence", "bounded", "idempotency",
    "credentials remain in the host/provider credential system",
], "core/external-integration-adapter.md")
require(github, [
    "Read-only capabilities", "Mutating capabilities", "github.inspect.repository",
    "github.inspect.workflow_run", "github.mutate.file", "github.mutate.pull_request",
    "authorized work unit", "Security Gate", "UNAVAILABLE", "Credentials are supplied by the host",
], "adapters/github-integration.md")
require(roadmap, ["P7 — External Integration Adapters"], "docs/ROADMAP.md")
require(architecture, ["Host Execution Adapters", "GitHub / CI integrations"], "docs/ARCHITECTURE.md")

print("External Integration Adapter v1 checks passed.")
