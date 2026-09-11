#!/usr/bin/env python3
"""Static and reference-integration checks for External Integration Adapter v1."""
from pathlib import Path
import importlib.util
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

def read(path):
    return (ROOT / path).read_text(encoding="utf-8")

def require(text, needles, source):
    for needle in needles:
        assert needle in text, f"missing {needle!r} in {source}"

contract = read("core/external-integration-adapter.md")
github = read("adapters/github-integration.md")
reference = read("adapters/github-reference.py")
bridge_contract = read("core/runtime-adapter-bridge.md")
bridge = read("tools/runtime-adapter-bridge.py")
roadmap = read("docs/ROADMAP.md")
architecture = read("docs/ARCHITECTURE.md")

require(contract, ["provider capability discovery", "target + scope validation", "authorization / Security Gate", "actual provider response", "AVAILABLE | DELEGATABLE | MISSING", "Read-only", "Mutating", "Remote mutations require an authorized work unit", "Only an actual provider response is execution evidence", "bounded", "idempotency", "credentials remain in the host/provider credential system"], "core/external-integration-adapter.md")
require(github, ["Read-only capabilities", "Mutating capabilities", "github.inspect.repository", "github.inspect.workflow_run", "github.mutate.file", "github.mutate.pull_request", "authorized work unit", "Security Gate", "UNAVAILABLE", "Credentials are supplied by the host"], "adapters/github-integration.md")
require(reference, ["GitHubClient", "READ_CAPABILITIES", "MUTATION_CAPABILITIES", "github.inspect.repository", "github.mutate.file", "inspect_repository", "inspect_commit", "inspect_workflow_run", "mutate_file"], "adapters/github-reference.py")
require(bridge_contract, ["github.inspect.repository", "github.inspect.commit", "github.inspect.workflow_run", "github.mutate.file", "actual provider response", "security_gate: PASS", "expected current file SHA"], "core/runtime-adapter-bridge.md")
require(bridge, ["github.inspect.repository", "github.inspect.commit", "github.inspect.workflow_run", "github.mutate.file", "github_client", "NOT_REQUIRED", "ALREADY_GRANTED", "security_gate", "UNAVAILABLE"], "tools/runtime-adapter-bridge.py")
require(roadmap, ["P7 — External Integration Adapters", "provider-backed reference operations", "external integration end-to-end tests", "P8 — Remote Mutation Controls v1"], "docs/ROADMAP.md")
require(architecture, ["Host Execution Adapters", "GitHub / CI integrations", "External services"], "docs/ARCHITECTURE.md")

spec = importlib.util.spec_from_file_location("github_reference", ROOT / "adapters" / "github-reference.py")
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class FakeClient:
    def get_repo(self, repository): return {"full_name": repository}
    def get_commit(self, repository, commit_sha): return {"repository": repository, "sha": commit_sha}
    def get_workflow_run(self, repository, run_id): return {"repository": repository, "id": run_id, "conclusion": "success"}
    def update_file(self, repository, path, content, message, expected_sha): return {"commit": {"sha": "new-commit"}}

client = FakeClient()
assert module.capability_status("github.inspect.repository") == "AVAILABLE"
assert module.capability_status("github.mutate.file") == "AVAILABLE"
assert module.capability_status("github.mutate.repository") == "MISSING"
assert module.inspect_repository(client, "zzpsah/chatgpt-development-os")["status"] == "SUCCESS"
assert module.inspect_commit(client, "zzpsah/chatgpt-development-os", "abc123")["status"] == "SUCCESS"
assert module.inspect_workflow_run(client, "zzpsah/chatgpt-development-os", 123)["status"] == "SUCCESS"
assert module.inspect_repository(client, "invalid")["status"] == "BLOCKED"
assert module.mutate_file(client, "zzpsah/chatgpt-development-os", "docs/example.md", "x", "test", "old-sha", "ALREADY_GRANTED")["status"] == "SUCCESS"

result = subprocess.run(
    [sys.executable, str(ROOT / "tools" / "test-external-runtime-bridge.py")],
    text=True,
    capture_output=True,
    check=False,
)
assert result.returncode == 0, result.stdout + result.stderr

print("External Integration Adapter v1 checks passed.")
