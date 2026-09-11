#!/usr/bin/env python3
"""Provider-backed GitHub reference adapter using an injected API client.

The adapter intentionally accepts a small client interface instead of owning
credentials. This keeps credentials in the host integration boundary.
"""
from __future__ import annotations

from typing import Any, Protocol


class GitHubClient(Protocol):
    def get_repo(self, repository: str) -> Any: ...
    def get_commit(self, repository: str, commit_sha: str) -> Any: ...
    def get_workflow_run(self, repository: str, run_id: int) -> Any: ...


READ_CAPABILITIES = {
    "github.inspect.repository",
    "github.inspect.commit",
    "github.inspect.workflow_run",
}


def capability_status(name: str) -> str:
    return "AVAILABLE" if name in READ_CAPABILITIES else "MISSING"


def inspect_repository(client: GitHubClient, repository: str) -> dict[str, Any]:
    if not repository or "/" not in repository:
        return {"status": "BLOCKED", "reason": "repository must be owner/name"}
    try:
        response = client.get_repo(repository)
        return {"status": "SUCCESS", "provider": "github", "operation": "inspect_repository", "repository": repository, "response": response}
    except Exception as exc:
        return {"status": "FAILED", "provider": "github", "operation": "inspect_repository", "error": str(exc)}


def inspect_commit(client: GitHubClient, repository: str, commit_sha: str) -> dict[str, Any]:
    if not repository or not commit_sha:
        return {"status": "BLOCKED", "reason": "repository and commit are required"}
    try:
        response = client.get_commit(repository, commit_sha)
        return {"status": "SUCCESS", "provider": "github", "operation": "inspect_commit", "repository": repository, "commit": commit_sha, "response": response}
    except Exception as exc:
        return {"status": "FAILED", "provider": "github", "operation": "inspect_commit", "error": str(exc)}


def inspect_workflow_run(client: GitHubClient, repository: str, run_id: int) -> dict[str, Any]:
    if not repository or not isinstance(run_id, int) or run_id <= 0:
        return {"status": "BLOCKED", "reason": "repository and positive workflow run id are required"}
    try:
        response = client.get_workflow_run(repository, run_id)
        return {"status": "SUCCESS", "provider": "github", "operation": "inspect_workflow_run", "repository": repository, "run_id": run_id, "response": response}
    except Exception as exc:
        return {"status": "FAILED", "provider": "github", "operation": "inspect_workflow_run", "error": str(exc)}
