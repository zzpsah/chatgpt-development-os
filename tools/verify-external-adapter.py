#!/usr/bin/env python3
"""Static and reference-integration checks for External Integration Adapter v1."""
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]

def read(path):
    return (ROOT / path).read_text(encoding="utf-8")

def require(text, needles, source):
    for needle in needles:
        assert needle in text, f"missing {needle!r} in {source}"

contract = read("core/external-integration-adapter.md")
github = read("adapters/github-integration.md")
reference = read("adapters/github-reference.py")
roadmap = read("docs/ROADMAP.md")
architecture = read("docs/ARCHITECTURE.md")

require(contract, ["provider capability discovery", "target + scope validation", "authorization / Security Gate", "actual provider response", "AVAILABLE | DELEGATABLE | MISSING", "Read-only", "Mutating", "Remote mutations require an authorized work unit", "Only an actual provider response is execution evidence", "bounded", "idempotency", "credentials remain in the host/provider credential system"], "core/external-integration-adapter.md")
require(github, ["Read-only capabilities", "Mutating capabilities", "github.inspect.repository", "github.inspect.workflow_run", "github.mutate.file", "github.mutate.pull_request", "authorized work unit", "Security Gate", "UNAVAILABLE", "Credentials are supplied by the host"], "adapters/github-integration.md")
require(reference, ["GitHubClient", "READ_CAPABILITIES", "github.inspect.repository", "inspect_repository", "inspect_commit", "inspect_workflow_run"], "adapters/github-reference.py")
require(roadmap, ["P7 — External Integration Adapters", "provider-backed reference operations", "external integration end-to-end tests"], "docs/ROADMAP.md")
require(architecture, ["Host Execution Adapters", "GitHub / CI integrations"], "docs/ARCHITECTURE.md")

spec = importlib.util.spec_from_file_location("github_reference", ROOT / "adapters" / "github-reference.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class FakeClient:
    def get_repo(self, repository): return {"full_name": repository}
    def get_commit(self, repository, commit_sha): return {"repository": repository, "sha": commit_sha}
    def get_workflow_run(self, repository, run_id): return {"repository": repository, "id": run_id, "conclusion": "success"}

client = FakeClient()
assert module.capability_status("github.inspect.repository") == "AVAILABLE"
assert module.capability_status("github.mutate.repository") == "MISSING"
assert module.inspect_repository(client, "zzpsah/chatgpt-development-os")["status"] == "SUCCESS"
assert module.inspect_commit(client, "zzpsah/chatgpt-development-os", "abc123")["status"] == "SUCCESS"
assert module.inspect_workflow_run(client, "zzpsah/chatgpt-development-os", 123)["status"] == "SUCCESS"
assert module.inspect_repository(client, "invalid")["status"] == "BLOCKED"

print("External Integration Adapter v1 checks passed.")
