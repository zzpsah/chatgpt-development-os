#!/usr/bin/env python3
"""Integration checks for the provider-backed GitHub reference adapter."""
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("github_reference", ROOT / "adapters" / "github-reference.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class FakeClient:
    def __init__(self):
        self.repo_calls = 0

    def get_repo(self, repository):
        self.repo_calls += 1
        return {"full_name": repository}

    def get_commit(self, repository, commit_sha):
        return {"repository": repository, "sha": commit_sha}

    def get_workflow_run(self, repository, run_id):
        return {"repository": repository, "id": run_id, "conclusion": "success"}


class FlakyClient(FakeClient):
    def get_repo(self, repository):
        self.repo_calls += 1
        if self.repo_calls == 1:
            raise RuntimeError("temporary provider failure")
        return {"full_name": repository}


client = FakeClient()
assert module.capability_status("github.inspect.repository") == "AVAILABLE"
assert module.capability_status("github.mutate.repository") == "MISSING"
assert module.inspect_repository(client, "zzpsah/chatgpt-development-os")["status"] == "SUCCESS"
assert module.inspect_commit(client, "zzpsah/chatgpt-development-os", "abc123")["status"] == "SUCCESS"
assert module.inspect_workflow_run(client, "zzpsah/chatgpt-development-os", 123)["status"] == "SUCCESS"
assert module.inspect_repository(client, "invalid")["status"] == "BLOCKED"

flaky = FlakyClient()
retry_result = module.inspect_repository(flaky, "zzpsah/chatgpt-development-os")
assert retry_result["status"] == "SUCCESS"
assert retry_result["attempt"] == 2
assert flaky.repo_calls == 2

print("GitHub reference adapter integration checks passed.")
