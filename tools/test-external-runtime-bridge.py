#!/usr/bin/env python3
"""Integration checks for the runtime bridge's external GitHub path."""
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("runtime_bridge", ROOT / "tools" / "runtime-adapter-bridge.py")
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class FakeClient:
    def get_repo(self, repository):
        return {"full_name": repository, "private": False}

    def get_commit(self, repository, commit_sha):
        return {"repository": repository, "sha": commit_sha}

    def get_workflow_run(self, repository, run_id):
        return {"repository": repository, "id": run_id, "conclusion": "success"}

    def update_file(self, repository, path, content, message, expected_sha):
        return {"commit": {"sha": "new-commit"}, "content": {"path": path, "sha": "new-file-sha"}}


client = FakeClient()
root = ROOT

repo = module.execute(
    {"operation": "github.inspect.repository", "target": "zzpsah/chatgpt-development-os", "scope": "repository-read", "authorization": "NOT_REQUIRED"},
    root, client,
)
assert repo["status"] == "SUCCESS"
assert repo["evidence"][0]["response"]["full_name"] == "zzpsah/chatgpt-development-os"

commit = module.execute(
    {"operation": "github.inspect.commit", "target": "zzpsah/chatgpt-development-os", "scope": "abc123", "authorization": "NOT_REQUIRED"},
    root, client,
)
assert commit["status"] == "SUCCESS"

run = module.execute(
    {"operation": "github.inspect.workflow_run", "target": "zzpsah/chatgpt-development-os", "scope": "123", "authorization": "NOT_REQUIRED"},
    root, client,
)
assert run["status"] == "SUCCESS"

assert module.execute(
    {"operation": "github.inspect.repository", "target": "invalid", "scope": "repository-read"}, root, client
)["status"] == "BLOCKED"

assert module.execute(
    {"operation": "github.inspect.repository", "target": "zzpsah/chatgpt-development-os", "scope": "repository-read", "authorization": "ALREADY_GRANTED"},
    root, client,
)["status"] == "BLOCKED"

assert module.execute(
    {"operation": "github.mutate.file", "target": "zzpsah/chatgpt-development-os", "scope": "docs/example.md", "content": "x", "message": "test", "expected_sha": "sha", "authorization": "NOT_REQUIRED", "security_gate": "PASS"},
    root, client,
)["status"] == "BLOCKED"

assert module.execute(
    {"operation": "github.mutate.file", "target": "zzpsah/chatgpt-development-os", "scope": "docs/example.md", "content": "x", "message": "test", "expected_sha": "sha", "authorization": "ALREADY_GRANTED", "security_gate": "UNVERIFIED"},
    root, client,
)["status"] == "BLOCKED"

mutation = module.execute(
    {"operation": "github.mutate.file", "target": "zzpsah/chatgpt-development-os", "scope": "docs/example.md", "content": "x", "message": "test: controlled mutation", "expected_sha": "sha", "authorization": "ALREADY_GRANTED", "security_gate": "PASS"},
    root, client,
)
assert mutation["status"] == "SUCCESS"
assert mutation["evidence"]

assert module.execute(
    {"operation": "github.mutate.file", "target": "zzpsah/chatgpt-development-os", "scope": "README.md", "content": "x", "message": "test", "expected_sha": "sha", "authorization": "ALREADY_GRANTED", "security_gate": "PASS"},
    root, None,
)["status"] == "UNAVAILABLE"

print("External runtime bridge integration checks passed.")
