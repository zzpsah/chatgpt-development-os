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
        self.update_calls = 0

    def get_repo(self, repository):
        self.repo_calls += 1
        return {"full_name": repository}

    def get_commit(self, repository, commit_sha):
        return {"repository": repository, "sha": commit_sha}

    def get_workflow_run(self, repository, run_id):
        return {"repository": repository, "id": run_id, "conclusion": "success"}

    def update_file(self, repository, path, content, message, expected_sha):
        self.update_calls += 1
        return {"commit": {"sha": "new-commit"}, "content": {"path": path, "sha": "new-file-sha"}}


class FlakyClient(FakeClient):
    def get_repo(self, repository):
        self.repo_calls += 1
        if self.repo_calls == 1:
            raise RuntimeError("temporary provider failure")
        return {"full_name": repository}


class ConflictClient(FakeClient):
    def update_file(self, repository, path, content, message, expected_sha):
        self.update_calls += 1
        raise RuntimeError("409 conflict: sha does not match")


class UncertainClient(FakeClient):
    def update_file(self, repository, path, content, message, expected_sha):
        self.update_calls += 1
        raise RuntimeError("connection reset after request")


client = FakeClient()
assert module.capability_status("github.inspect.repository") == "AVAILABLE"
assert module.capability_status("github.mutate.file") == "AVAILABLE"
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

mutation = module.mutate_file(
    client,
    "zzpsah/chatgpt-development-os",
    "docs/example.md",
    "hello",
    "test: controlled remote update",
    "current-file-sha",
    "ALREADY_GRANTED",
)
assert mutation["status"] == "SUCCESS"
assert mutation["attempt"] == 1
assert client.update_calls == 1

assert module.mutate_file(
    client,
    "zzpsah/chatgpt-development-os",
    "docs/example.md",
    "hello",
    "test: blocked update",
    "current-file-sha",
    "NOT_REQUIRED",
)["status"] == "BLOCKED"

assert module.mutate_file(
    client,
    "zzpsah/chatgpt-development-os",
    "../outside.md",
    "hello",
    "test: blocked path",
    "current-file-sha",
    "ALREADY_GRANTED",
)["status"] == "BLOCKED"

conflict = ConflictClient()
conflict_result = module.mutate_file(
    conflict,
    "zzpsah/chatgpt-development-os",
    "docs/example.md",
    "hello",
    "test: conflict",
    "stale-sha",
    "ALREADY_GRANTED",
)
assert conflict_result["status"] == "BLOCKED"
assert conflict.update_calls == 1

uncertain = UncertainClient()
uncertain_result = module.mutate_file(
    uncertain,
    "zzpsah/chatgpt-development-os",
    "docs/example.md",
    "hello",
    "test: uncertain",
    "current-file-sha",
    "ALREADY_GRANTED",
)
assert uncertain_result["status"] == "UNVERIFIED"
assert uncertain.update_calls == 1

print("GitHub reference adapter integration checks passed.")
