#!/usr/bin/env python3
"""Provider-backed GitHub reference adapter using an injected API client.

The adapter owns no credentials. The client is the provider boundary, while
this module validates inputs, applies bounded read retries, and normalizes
actual provider responses into DevOS evidence.
"""
from __future__ import annotations

import time
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


def _read_operation(call: Any, operation: str, **metadata: Any) -> dict[str, Any]:
    try:
        response = call()
        return {
            "status": "SUCCESS",
            "provider": "github",
            "operation": operation,
            **metadata,
            "response": response,
        }
    except Exception as exc:
        return {
            "status": "FAILED",
            "provider": "github",
            "operation": operation,
            **metadata,
            "error": str(exc),
        }


def _read_with_retry(
    call: Any,
    operation: str,
    retries: int = 2,
    backoff_seconds: float = 0.1,
    **metadata: Any,
) -> dict[str, Any]:
    """Retry only read operations; never retries a mutation."""
    attempts = max(1, retries + 1)
    last: dict[str, Any] | None = None
    for attempt in range(1, attempts + 1):
        last = _read_operation(call, operation, **metadata)
        last["attempt"] = attempt
        if last["status"] == "SUCCESS":
            return last
        if attempt < attempts and backoff_seconds > 0:
            time.sleep(backoff_seconds * attempt)
    assert last is not None
    return last


def inspect_repository(client: GitHubClient, repository: str) -> dict[str, Any]:
    if not repository or "/" not in repository or repository.count("/") != 1:
        return {"status": "BLOCKED", "reason": "repository must be owner/name"}
    return _read_with_retry(
        lambda: client.get_repo(repository),
        "inspect_repository",
        repository=repository,
    )


def inspect_commit(client: GitHubClient, repository: str, commit_sha: str) -> dict[str, Any]:
    if not repository or "/" not in repository or not commit_sha:
        return {"status": "BLOCKED", "reason": "repository and commit are required"}
    return _read_with_retry(
        lambda: client.get_commit(repository, commit_sha),
        "inspect_commit",
        repository=repository,
        commit=commit_sha,
    )


def inspect_workflow_run(client: GitHubClient, repository: str, run_id: int) -> dict[str, Any]:
    if not repository or "/" not in repository or not isinstance(run_id, int) or run_id <= 0:
        return {"status": "BLOCKED", "reason": "repository and positive workflow run id are required"}
    return _read_with_retry(
        lambda: client.get_workflow_run(repository, run_id),
        "inspect_workflow_run",
        repository=repository,
        run_id=run_id,
    )
