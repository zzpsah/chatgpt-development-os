#!/usr/bin/env python3
"""Minimal runtime-to-reference-adapter bridge.

The bridge deliberately accepts only declared, bounded operations. It is a
reference implementation, not a general-purpose shell executor.
"""
from __future__ import annotations

from pathlib import Path
import importlib.util
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


adapter = _load_module("reference_host", ROOT / "adapters" / "reference-host.py")
github_adapter = _load_module("github_reference", ROOT / "adapters" / "github-reference.py")


def _github_execute(request: dict[str, Any], client: Any) -> dict[str, Any]:
    operation = request["operation"]
    repository = request["target"]
    scope = request["scope"]
    authorization = request.get("authorization", "NOT_REQUIRED")

    if github_adapter.capability_status(operation) != "AVAILABLE":
        return {"status": "UNAVAILABLE", "reason": "GitHub capability is not available"}
    if not isinstance(repository, str) or not repository or repository.count("/") != 1:
        return {"status": "BLOCKED", "reason": "GitHub target must be owner/name"}

    if operation in github_adapter.READ_CAPABILITIES:
        if authorization != "NOT_REQUIRED":
            return {"status": "BLOCKED", "reason": "read-only GitHub inspection requires NOT_REQUIRED authorization"}
        if operation == "github.inspect.repository":
            if scope != "repository-read":
                return {"status": "BLOCKED", "reason": "repository inspection requires scope repository-read"}
            result = github_adapter.inspect_repository(client, repository)
        elif operation == "github.inspect.commit":
            if not isinstance(scope, str) or not scope or "/" in scope:
                return {"status": "BLOCKED", "reason": "commit scope must be a commit identifier"}
            result = github_adapter.inspect_commit(client, repository, scope)
        elif operation == "github.inspect.workflow_run":
            try:
                run_id = int(scope)
            except (TypeError, ValueError):
                return {"status": "BLOCKED", "reason": "workflow-run scope must be a positive numeric run id"}
            result = github_adapter.inspect_workflow_run(client, repository, run_id)
        else:
            return {"status": "UNAVAILABLE", "reason": "operation not supported by external bridge"}
    elif operation in github_adapter.MUTATION_CAPABILITIES:
        if authorization != "ALREADY_GRANTED":
            return {"status": "BLOCKED", "reason": "explicit authorization required for remote mutation"}
        if request.get("security_gate") != "PASS":
            return {"status": "BLOCKED", "reason": "Security Gate PASS is required for remote mutation"}
        if not isinstance(request.get("content"), str):
            return {"status": "BLOCKED", "reason": "file content is required"}
        if not isinstance(request.get("message"), str) or not request["message"]:
            return {"status": "BLOCKED", "reason": "commit message is required"}
        expected_sha = request.get("expected_sha")
        if not isinstance(expected_sha, str) or not expected_sha:
            return {"status": "BLOCKED", "reason": "expected current file SHA is required"}
        result = github_adapter.mutate_file(
            client,
            repository,
            scope,
            request["content"],
            request["message"],
            expected_sha,
            authorization,
        )
    else:
        return {"status": "UNAVAILABLE", "reason": "operation not supported by external bridge"}

    return {
        "status": result.get("status", "FAILED"),
        "provider": "github",
        "operation": operation,
        "target": repository,
        "scope": scope,
        "evidence": [result] if result.get("status") == "SUCCESS" else [],
        "provider_result": result,
    }


def execute(request: dict[str, Any], project_root: Path, github_client: Any = None) -> dict[str, Any]:
    operation = request.get("operation")
    target = request.get("target")
    scope = request.get("scope")
    authorization = request.get("authorization", "NOT_REQUIRED")

    if not operation or target is None or not scope:
        return {"status": "BLOCKED", "reason": "operation, target, and scope are required"}

    if operation.startswith("github."):
        if github_client is None:
            return {"status": "UNAVAILABLE", "reason": "GitHub provider client is not supplied by the host"}
        return _github_execute(request, github_client)

    if operation == "filesystem.read":
        return adapter.read_text(project_root, target)

    if operation == "filesystem.write_scoped":
        if authorization != "ALREADY_GRANTED":
            return {"status": "BLOCKED", "reason": "explicit authorization required for mutation"}
        content = request.get("content")
        if not isinstance(content, str):
            return {"status": "BLOCKED", "reason": "write content is required"}
        return adapter.write_text(project_root, target, content, authorization)

    if operation == "git.inspect":
        return adapter.git_inspect(project_root, target or "status")

    return {"status": "UNAVAILABLE", "reason": "operation not supported by reference bridge"}
