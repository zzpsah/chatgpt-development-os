#!/usr/bin/env python3
"""Bounded live GitHub integration test against the public DevOS repository.

No credential is required for these read-only public-resource checks. The
adapter still receives a real provider client, so SUCCESS means a real GitHub
response was obtained rather than a fake response.
"""
from __future__ import annotations

import importlib.util
import json
import os
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("github_reference", ROOT / "adapters" / "github-reference.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class GitHubRestClient:
    def __init__(self, token: str | None = None):
        self.token = token

    def _get(self, path: str):
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "devos-reference-adapter-test",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        request = urllib.request.Request(f"https://api.github.com{path}", headers=headers, method="GET")
        with urllib.request.urlopen(request, timeout=10) as response:
            return json.loads(response.read().decode("utf-8"))

    def get_repo(self, repository):
        return self._get(f"/repos/{repository}")

    def get_commit(self, repository, commit_sha):
        return self._get(f"/repos/{repository}/commits/{commit_sha}")

    def get_workflow_run(self, repository, run_id):
        return self._get(f"/repos/{repository}/actions/runs/{run_id}")


repository = os.environ.get("DEVOS_GITHUB_REPOSITORY", "zzpsah/chatgpt-development-os")
client = GitHubRestClient(os.environ.get("GITHUB_TOKEN"))

repo_result = module.inspect_repository(client, repository)
assert repo_result["status"] == "SUCCESS", repo_result
assert repo_result["response"].get("default_branch") == "main", repo_result

branch_response = client._get(f"/repos/{repository}/branches/main")
commit_sha = branch_response["commit"]["sha"]
commit_result = module.inspect_commit(client, repository, commit_sha)
assert commit_result["status"] == "SUCCESS", commit_result
assert commit_result["response"].get("sha") == commit_sha, commit_result

print(json.dumps({
    "status": "SUCCESS",
    "provider": "github",
    "repository": repository,
    "branch": "main",
    "commit": commit_sha,
    "evidence": "actual GitHub REST responses",
}, sort_keys=True))
